# HS2DDS - A Secure And Fast Way To Store Data
##### PROGRESS: PRE-ALPHA 40%
## Up Next: Establish 'write', 'read', and 'maintain' threads | Create node sectors for HADOOP processing
### IDEA: Educational purposes. 
Presenting data visually has its obvious benefits when it comes to communicating ideas such as sorting or manipulating data. with this program, it could easily be modified to produce a string of images, each representing a step in the data maniputlation process. These imagese could then be used to create an animation of what is happening to any data set in real time using moving pixels rather than log outputs. 
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
