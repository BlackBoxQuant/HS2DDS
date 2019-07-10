#randomized creation of linked lists, conversion to BRG, writing onto surface.
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import base64
import requests
import string
print(random.randrange(0,14,1))
#GLOBAL VARS==============================================================================================
imageRow = 1
data1Column = 1
data2Column = 1
data3Column = 1
listSize = 100000
surface = 2000
softBoundary = surface*0.8
counter = 0
table  = {}
i = 0;
for x in range(48,58):
    B = x%11
    G = x%13
    R = x%17
    table[chr(x)] = [B*17,G*13,R*11]
for x in range(65,91):
    B = x%11
    G = x%13
    R = x%17
    table[chr(x)] = [B*17,G*13,R*11]
for x in range(97,123):
    B = x%11
    G = x%13
    R = x%17
    table[chr(x)] = [B*17,G*13,R*11]
for key,val in table.items():
    print(key, " | ", val)
 

#NODE CLASS===============================================================================================
class Node:
    def __init__(self, firstName = str, lastName = str, idNumber = str): #All the stuff the node needs to be created. Next is not included because a node doesn't NEED to have a "next" node imidiately upon creation
        self.firstName = firstName
        self.lastName = lastName
        self.idNumber = idNumber
        self.next = None
#LINKED LIST CLASS========================================================================================
class LinkedList:
    def __init__(self): #We want to be able to create the linked list without needing to give a node right away, thus we dont require one for initialization.
        self.headval = None
        self.last = None
    def append(self, F,L,I):
        newNode = Node(F,L,I)
        if self.headval is None: 
            self.headval = newNode 
            return
        newNode.next = self.headval
        self.headval = newNode
    def printList(self): 
        temp = self.headval 
        while (temp): 
            print (temp.firstName) 
            temp = temp.next
#RANDOM DATA GENERATORS=======================================================================================
def FIRST_NAME_GENERATOR():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randrange(5,11,1)))
def LAST_NAME_GENERATOR():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randrange(5,11,1)))
def ID_NUMBER_GENERATOR():
    return ''.join(random.choices(string.digits, k=random.randrange(5,11,1)))
#CREATES A RANDOM NODE========================================================================================= 
def RANDOM_LIST(x = int):
    list = LinkedList()
    global counter
    for i in range(x):
        list.append(FIRST_NAME_GENERATOR(),LAST_NAME_GENERATOR(),ID_NUMBER_GENERATOR())
        counter += 1
        if counter%100000 == 0:
            print(counter)
    return(list)
#DAPS SURFACE DEFINITION=======================================================================================
def DAPS_SURFACE(width = int, height = int, colorspace = int):
    img = np.ones((width, height, colorspace), np.uint8)*255    #create a numpy array of WxHxD of unsigned integers and make the image white
    return img
#CONVERTS NODE TO BGR FORMAT=================================================================================== 
def BGR_CONVERT(data):
    bgrOut = []
    for x in range(len(data)):
        B = ord(data[x])%11
        G = ord(data[x])%13
        R = ord(data[x])%17
        bgrOut.append([B*17,G*13,R*11]) #*5 max
    return(bgrOut)
#WRITE THE RAW NODE TO SURFACE IN BGR FORMAT===================================================================
def WRITE_NODE_TO_SURFACE (img = np.ndarray, inputNode = Node):
    global imageRow
    global data1Column 
    global data2Column
    global data3Column
    global softBoundary
    writeToSurface = BGR_CONVERT(inputNode.firstName)
    for x in range(len(writeToSurface)):
        img.itemset((imageRow+0,data1Column,0),writeToSurface[x][0]) #set blue
        img.itemset((imageRow+0,data1Column,1),writeToSurface[x][1]) #set green
        img.itemset((imageRow+0,data1Column,2),writeToSurface[x][2]) #set red
        data1Column += 1
    writeToSurface = BGR_CONVERT(inputNode.lastName)
    for x in range(len(writeToSurface)):
        img.itemset((imageRow+1,data2Column,0),writeToSurface[x][0]) #set blue
        img.itemset((imageRow+1,data2Column,1),writeToSurface[x][1]) #set green
        img.itemset((imageRow+1,data2Column,2),writeToSurface[x][2]) #set red
        data2Column += 1
    writeToSurface = BGR_CONVERT(inputNode.idNumber)
    for x in range(len(writeToSurface)):
        img.itemset((imageRow+2,data3Column,0),writeToSurface[x][0]) #set blue
        img.itemset((imageRow+2,data3Column,1),writeToSurface[x][1]) #set green
        img.itemset((imageRow+2,data3Column,2),writeToSurface[x][2]) #set red
        data3Column += 1

    if data1Column >= data2Column:
        if data1Column >= data3Column:
            data2Column,data3Column = data1Column,data1Column
        else:
           data1Column,data2Column = data3Column,data3Column
    elif data2Column >= data3Column:
        data1Column,data3Column = data2Column,data2Column
    else:
        data1Column,data2Column  = data3Column,data3Column

    if data1Column >= softBoundary:
        data1Column = 1
        data2Column = 1
        data3Column = 1
        imageRow += 3
    return (img)
#CREATE A LINKED LIST OF BGR NODES
def BGR_LINKED_LIST (list = LinkedList):
    tNode = list.headval
    while (tNode.next):
        tNode.firstName = BGR_CONVERT(tNode.firstName)
        tNode.lastName = BGR_CONVERT(tNode.lastName)
        tNode.idNumber = BGR_CONVERT(tNode.idNumber)
        tNode = tNode.next
    return(list)
#FIND THE DISTROBUTION OF BGR VALUES & INTENSITIES
def BGR_CLASSIFY (bgr_list = LinkedList):
    blue_count = 0
    green_count = 0
    red_count = 0
    bgrNode = bgr_list.headval
    while bgrNode.next:
        blue_vals = []
        green_vals = []
        red_vals = []
        for x in range(len(bgrNode.firstName)):
            blue_vals.append(bgrNode.firstName[x][0])
            green_vals.append(bgrNode.firstName[x][1])
            red_vals.append(bgrNode.firstName[x][2])
        bmean = np.mean(blue_vals)
        rmean = np.mean(red_vals)
        gmean = np.mean(green_vals)
        if (bmean >= rmean) & (bmean >= gmean):
            blue_count += 1
        elif (rmean >= bmean) & (rmean >=gmean):
            red_count += 1
        else:
            green_count += 1
        bgrNode = bgrNode.next
    print("RED: ", red_count)
    print("BLUE: ", blue_count)
    print("GREEN: ", green_count)

def QUERY_SURFACE(img = np.ndarray, qNode = Node, xStart = int, yStart = int):
    global table
    bgrArray = []
    bgrArray.append(BGR_CONVERT(qNode.firstName))
    bgrArray.append(BGR_CONVERT(qNode.lastName))
    bgrArray.append(BGR_CONVERT(qNode.idNumber))
    results = [False,False,False]
    print("looking for:\n", bgrArray[0],"\n",bgrArray[1],"\n",bgrArray[2])
    #EVENTUALLY WILL BE multithreaded search
    for x in range(xStart,surface-2):
        if x%10 == 0: print(x)
        for y in range(yStart,surface):
            for i in range(3):
                if np.array_equal(img[x+i][y], bgrArray[i][0]): #if we get a first name, first letter, hit
                    for j in range(1,len(bgrArray[i])):
                        if np.array_equal(img[x+i][y+j], bgrArray[i][j]):
                            if j == len(bgrArray[i])-1:
                                results[i]=True
                                if(i==2):
                                    if all(results):
                                        return(x,y)
                        else:                                   #a miss has occured, reset found table
                            for k in results: results[k] = False
        x+=3
    return(None,None)

def test ():
    dSurface = DAPS_SURFACE(surface,surface,3)
    list = RANDOM_LIST(listSize)
    test = Node('abcde','fgh','12345')
    tNode = list.headval
    #for x in range(1000):
        #WRITE_NODE_TO_SURFACE(dSurface, test)
    while (tNode.next):
        WRITE_NODE_TO_SURFACE(dSurface, tNode)
        tNode = tNode.next
    WRITE_NODE_TO_SURFACE(dSurface,test)
    x,y = QUERY_SURFACE(dSurface,test,0,0)
    print("x: ",x,"\ny: ",y)
    cv2.imshow('DAPS',dSurface)
    BGR_CLASSIFY(BGR_LINKED_LIST(list))
    cv2.waitKey(0)
    return
test()





def stats():
    red_values = []
    green_values = []
    blue_values = []
    dSurface = DAPS_SURFACE(surface,surface,3)
    list = RANDOM_LIST(listSize)
    dNode = list.headval
    while(dNode.next):
        first_name = BGR_CONVERT(dNode.firstName)
        for x in range(len(first_name)):
            red_values.append(first_name[x][2])
            green_values.append(first_name[x][1])
            blue_values.append(first_name[x][0])
        dNode = dNode.next
    return






#RED WEIGHTED, within red, blue weigth on last name, green weight 




#plt.hist(red_values,50,facecolor='r')
#plt.hist(green_values,50,facecolor='g')
#plt.hist(blue_values,50,facecolor='b',alpha = 0.5)
#plt.show()    
#NEXT GET DISTROBUTION WORD COLOR
