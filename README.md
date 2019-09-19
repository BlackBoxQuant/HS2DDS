# HS2DDS
High Speed 2 Dimensional Data Strucutre is a long lived idea of mine that is finally, slowly being brought to life. 
Currently HS2DDS is in its infancy. 
## How Will HS2DDS Work When It Is Done?
HS2DDS will be able to be given a classical data structure, and convert the data in each node into a sequence of RGB values.
Before writing the data to the image file, HS2DDS will perform a "RGB Spectrum Distribution Sort". This will create a 
distribution function that, given the color data of a node, will determine where on the image the new node should be inserted.
Thus, the image will be sorted based on the RGB spectrum. This will allow for very quick queries; given a node to query,
it will use the distribution function to determine a range of coordinates on the image that the data would exist. This
will narrow down the search to O(n) where n is a very small fraction of N. 
Essentially, given a node, we determine if it is mostly R,B,or G, then we determine how R,B,G it is relative 
to nodes in the data structure.
Furthermore, due to the 2D nature of images, multithreading the search function will be very easy. 
New data will sit in a prestorage section
of the image file until someone queries the data structure.  
##HS2DDS Isn't So High Speed - YET
HS2DDS gets faster with each iteration.
