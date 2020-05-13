# HS2DDS - A Secure And Fast Way To Store Data
##### PROGRESS: PRE-ALPHA 40%
## Up Next: Establish 'write', 'read', and 'maintain' threads | Create node sectors for HADOOP processing
## Why?
### 1: Educational purposes. 
Presenting data visually has its obvious benefits when it comes to communicating ideas such as sorting or manipulating data. with this program, it could easily be modified to produce a string of images, each representing a step in the data maniputlation process. These imagese could then be used to create an animation of what is happening to any data set in real time using moving pixels rather than log outputs. 
 
### 2: As a platform for learning hadoop and machine vision.
After graduating, I plan to continue my education onward into the fields of big data and machine vision and this, for now, seems like a great platform for toying around with both. 
#### ALPHA ETA: Q3 2020 (After Graduation)
High Speed 2 Dimensional Data Strucutre is a long lived idea of mine that is finally, slowly being brought to life. 
Currently HS2DDS is in its infancy. 
## How Will HS2DDS Work When It Is Done?
HS2DDS will, given a classical data structure, convert the data in each node into a sequence of RGB values.
Before writing the data to the image file, HS2DDS will perform a "RGB Spectrum Distribution Sort". This will create a 
distribution function that, given the color data of a node and the current data image, will determine where on
the image the new node should be inserted. Thus, the image will be sorted based on the RGB spectrum. 
This will allow for very quick queries; given a node to query, it will use the distribution function to 
determine a range of coordinates on the image that the data would exist. This will narrow down the search to O(n) 
where n is a very small fraction of N. 

Essentially, given a node, we determine if it is mostly R,B,or G, then we determine how R,B,G it is relative 
to nodes in the data structure.

Furthermore, due to the 2D nature of images, multithreading the search function will be very easy. 
New data will sit in a prestorage section of the image file until someone queries the data structure.  
## Security
HS2DDS is, by design, inheirently secure with respect to data theft. The full release version will store the parameters used for conversion
on the image itself. They will of course be encoded using a secure password the user sets up. 
Since the attacker doesn't know what set of parameters were used (or their values), their only option 
is to use brute force. With 256 values for
each color, 3 colors per character, multiple characters per node, and no way to know if a guess is correct without checking 
to see if it produces data that makes sense - it's going to take a long time. 

Lets say HS2DDS has been set up in the **best possible way for the attacker** - using only lowercase letters (ie: a list of names).
Assuming our attacker somehow knows that this is a list of names with no capital letters:
let the parameters of the converter be complex enough that cracking the converter itself its not 
reasonable - this should always be the case. For **each character** there are 431,115,750 possible color settings. 
Infact, assuming our attacker is smart enough to pick the smallest node in the structure, if said node is just 4 characters
long, and none of them repeat, there are 1,597,524,182xN possible strings (where N is the number of *reasonable* 4 letter names).
Even then, they can't assume that the first 4 letter name they get is the right one - they would then have to check against another node
which happens to have at minimum the same 3 letters in it and then guess through that one until a reasonable result 
appears (if it does at all). Lets say they get super lucky and they find a 5 letter name that has these 4 characters (does such a name
exist?). Guessing + Verification = 1,597,524,182xN + 363,704,773. Again, this is the best possible scenario: No special characters,
no capital letters, no numbers.
**None of this takes into account the fact that encryption prior to conversion will be an option,
(key can safely stored in the structure behind a password) at that point, the attacker doesn't stand a chance**

Without encryption prior to conversion (which would make this number astronomically large), lets assume the list uses a capital letter
for the first letter of the name and the smallest name is 5 letters long (don't include names like DJ, which would be most securely
stored as d\&^...(\J or simply dJ since an attacker would never assume you would store a 2 letter name like that). Now lets assume they
can employ some sneaky tricks to throw out 90% of all possible (R,G,B) arrangements. They still have 1.9E13 possible choices...
and this doesn't include the verification step. 

To go even further, lets have the same situation as above, but now throw into the name random non character, non numerical, ascii
characters. Without preconversion encryption, we have 1.5E10 possibilities for the first character alone - and no way to know
that there are random nonimportant ascii values thrown in. The statistics of how many possible ways there are to guess if a node has
random ascii values and how many + verification against unknown amount of unknown random ascii characters is astronomical. 

##### note:
Parameters much more complex than 3 prime numbers will be available for use in BETA.

## HS2DDS Isn't So High Speed - YET
HS2DDS gets faster with each iteration and the next few iteration will result in vast improvements in speed.
## Eventual Experimental Branches
### Dynamic Multithread
Allow user to determine how many threads are used.
### Data Structure Stats Encoded Into Itself
This will allow us to keep all information about the data structure in the data structure itself. No text files, no recomputing
the distribution functions.
### f(x(R,G,B)) Sort
The RGB values of each node will be the input of a function which determines a unique position on the image. 
Quieries will be nearly instantaneous. Issue: This function must be injective and not waste too much space 
while also not overlaping nodes. 
