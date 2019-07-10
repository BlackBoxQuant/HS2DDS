#randomized creation of linked lists, conversion to BRG, writing onto surface.
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import base64
import requests
import string
import time
#GLOBAL VARS==============================================================================================
imageRow_B = 0
imageRow_G = 0
imageRow_R = 0
data1Column_B = 0
data2Column_B = 0
data3Column_B = 0
column_B_Bounds = [0,0]
data1Column_G = 0
data2Column_G = 0
data3Column_G = 0
column_G_Bounds = [0,0]
data1Column_R = 0
data2Column_R = 0
data3Column_R = 0
column_R_Bounds = [0,0]
listSize = 100000
surface = 2000
softBoundary = int(surface*0.90)
counter = 0
table  = {}
i = 0;
#BUILD TABLE=========================================================================================
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
    global imageRow_B
    global imageRow_G
    global imageRow_R

    global data1Column_B
    global data2Column_B
    global data3Column_B

    global data1Column_G
    global data2Column_G
    global data3Column_G

    global data1Column_R
    global data2Column_R
    global data3Column_R

    global softBoundary

    nodeBGR_values = BGR_CONVERT(inputNode.firstName)
    blue_vals = []
    green_vals = []
    red_vals = []
    for x in range(len(nodeBGR_values)):
        blue_vals.append(nodeBGR_values[x][0])
        green_vals.append(nodeBGR_values[x][1])
        red_vals.append(nodeBGR_values[x][2])
    bmean = np.mean(blue_vals)
    rmean = np.mean(red_vals)
    gmean = np.mean(green_vals)
#BLUE===============================================================================================
    if (bmean >= rmean) & (bmean >= gmean): 
        writeToSurface = BGR_CONVERT(inputNode.firstName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_B+0,data1Column_B,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_B+0,data1Column_B,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_B+0,data1Column_B,2),writeToSurface[x][2]) #set red
            data1Column_B += 1
        writeToSurface = BGR_CONVERT(inputNode.lastName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_B+1,data2Column_B,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_B+1,data2Column_B,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_B+1,data2Column_B,2),writeToSurface[x][2]) #set red
            data2Column_B += 1
        writeToSurface = BGR_CONVERT(inputNode.idNumber)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_B+2,data3Column_B,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_B+2,data3Column_B,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_B+2,data3Column_B,2),writeToSurface[x][2]) #set red
            data3Column_B += 1
        if data1Column_B >= column_B_Bounds[1]*0.98:          #soft boundary of column_B_Bounds (set this up in global
            data1Column_B = column_B_Bounds[0]
            data2Column_B = column_B_Bounds[0]
            data3Column_B = column_B_Bounds[0]
            imageRow_B += 3
        else:
            if (data1Column_B >= data2Column_B) & (data1Column_B >= data3Column_B):
                data2Column_B,data3Column_B = data1Column_B,data1Column_B
            elif (data2Column_B >= data1Column_B) & (data2Column_B >= data3Column_B):
                data1Column_B,data3Column_B = data2Column_B,data2Column_B
            else:
                data1Column_B,data2Column_B = data3Column_B,data3Column_B
#RED===============================================================================================================
    elif (rmean >= bmean) & (rmean >=gmean):
        writeToSurface = BGR_CONVERT(inputNode.firstName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_R+0,data1Column_R,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_R+0,data1Column_R,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_R+0,data1Column_R,2),writeToSurface[x][2]) #set red
            data1Column_R += 1
        writeToSurface = BGR_CONVERT(inputNode.lastName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_R+1,data2Column_R,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_R+1,data2Column_R,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_R+1,data2Column_R,2),writeToSurface[x][2]) #set red
            data2Column_R += 1
        writeToSurface = BGR_CONVERT(inputNode.idNumber)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_R+2,data3Column_R,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_R+2,data3Column_R,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_R+2,data3Column_R,2),writeToSurface[x][2]) #set red
            data3Column_R += 1
        if data1Column_R >= column_R_Bounds[1]*0.98:          #soft boundary of column_B_Bounds (set this up in global
            data1Column_R = column_R_Bounds[0]
            data2Column_R = column_R_Bounds[0]
            data3Column_R = column_R_Bounds[0]
            imageRow_R += 3
        else:
            if (data1Column_R >= data2Column_R) & (data1Column_R >= data3Column_R):
                data2Column_R,data3Column_R = data1Column_R,data1Column_R
            elif (data2Column_R >= data1Column_R) & (data2Column_R >= data3Column_R):
                data1Column_R,data3Column_R = data2Column_R,data2Column_R
            else:
                data1Column_R,data2Column_R = data3Column_R,data3Column_R
#GREEN=============================================================================================================
    else:
        writeToSurface = BGR_CONVERT(inputNode.firstName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_G+0,data1Column_G,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_G+0,data1Column_G,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_G+0,data1Column_G,2),writeToSurface[x][2]) #set red
            data1Column_G += 1
        writeToSurface = BGR_CONVERT(inputNode.lastName)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_G+1,data2Column_G,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_G+1,data2Column_G,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_G+1,data2Column_G,2),writeToSurface[x][2]) #set red
            data2Column_G += 1
        writeToSurface = BGR_CONVERT(inputNode.idNumber)
        for x in range(len(writeToSurface)):
            img.itemset((imageRow_G+2,data3Column_G,0),writeToSurface[x][0]) #set blue
            img.itemset((imageRow_G+2,data3Column_G,1),writeToSurface[x][1]) #set green
            img.itemset((imageRow_G+2,data3Column_G,2),writeToSurface[x][2]) #set red
            data3Column_G += 1
        if data1Column_G >= column_G_Bounds[1]*0.98:          #soft boundary of column_B_Bounds (set this up in global
            data1Column_G = column_G_Bounds[0]
            data2Column_G = column_G_Bounds[0]
            data3Column_G = column_G_Bounds[0]
            imageRow_G += 3
        else:
            if (data1Column_G >= data2Column_G) & (data1Column_G >= data3Column_G):
                data2Column_G,data3Column_G = data1Column_G,data1Column_G
            elif (data2Column_G >= data1Column_G) & (data2Column_G >= data3Column_G):
                data1Column_G,data3Column_G = data2Column_G,data2Column_G
            else:
                data1Column_G,data2Column_G = data3Column_G,data3Column_G
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

def QUERY_SURFACE(img = np.ndarray, qNode = Node):
    global imageRow
    bgrArray = []
    bgrArray.append(BGR_CONVERT(qNode.firstName))
    bgrArray.append(BGR_CONVERT(qNode.lastName))
    bgrArray.append(BGR_CONVERT(qNode.idNumber))
    results = [False,False,False]
    print("looking for:\n", bgrArray[0],"\n",bgrArray[1],"\n",bgrArray[2])

    nodeBGR_values = BGR_CONVERT(qNode.firstName)
    blue_vals = []
    green_vals = []
    red_vals = []
    for x in range(len(nodeBGR_values)):
        blue_vals.append(nodeBGR_values[x][0])
        green_vals.append(nodeBGR_values[x][1])
        red_vals.append(nodeBGR_values[x][2])
    bmean = np.mean(blue_vals)
    rmean = np.mean(red_vals)
    gmean = np.mean(green_vals)
    if (bmean >= rmean) & (bmean >= gmean):
        print("Item is in blue sector")
        for x in range(0,imageRow_B+1,3):
            for y in range(column_B_Bounds[0],column_B_Bounds[1]):
                for i in range(3):
                    if np.array_equal(img[x+i][y], bgrArray[i][0]): #if we get a first name, first letter, hit
                        for j in range(1,len(bgrArray[i])):
                            if np.array_equal(img[x+i][y+j], bgrArray[i][j]):
                                if j == len(bgrArray[i])-1:
                                    results[i]=True
                                    if all(results):
                                        return(x,y)
                            else:                                   #a miss has occured, reset found table
                                for k in results: results[k] = False
    elif (rmean >= bmean) & (rmean >=gmean):
        print("Item is in red sector")
        for x in range(0,imageRow_R+1,3):
            for y in range(column_R_Bounds[0],column_R_Bounds[1]):
                for i in range(3):
                    if np.array_equal(img[x+i][y], bgrArray[i][0]): #if we get a first name, first letter, hit
                        for j in range(1,len(bgrArray[i])):
                            if np.array_equal(img[x+i][y+j], bgrArray[i][j]):
                                if j == len(bgrArray[i])-1:
                                    results[i]=True
                                    if all(results):
                                        return(x,y)
                            else:                                   #a miss has occured, reset found table
                                for k in results: results[k] = False
    else:
        print("Item is in green sector")
        for x in range(0,imageRow_G+1,3):
            for y in range(column_G_Bounds[0],column_G_Bounds[1]):
                for i in range(3):
                    if np.array_equal(img[x+i][y], bgrArray[i][0]): #if we get a first name, first letter, hit
                        for j in range(1,len(bgrArray[i])):
                            if np.array_equal(img[x+i][y+j], bgrArray[i][j]):
                                if j == len(bgrArray[i])-1:
                                    results[i]=True
                                    if all(results):
                                        return(x,y)
                            else:                                   #a miss has occured, reset found table
                                for k in results: results[k] = False
        #x += 3
    return(None,None)

def init():
    global imageRow 
    global data1Column_B 
    global data2Column_B 
    global data3Column_B 
    global column_B_Bounds 
    global data1Column_G 
    global data2Column_G 
    global data3Column_G
    global column_G_Bounds 
    global data1Column_R 
    global data2Column_R 
    global data3Column_R 
    global column_R_Bounds 
    global listSize 
    global surface 
    softBoundary = int(surface*0.90)
    print("setting up global vars given a surface size of: ", surface)
    section = int(surface/3)
    column_B_Bounds = [0,section-1]
    column_G_Bounds = [section,(2*section)-1]
    column_R_Bounds = [2*section, surface-1]
    data1Column_B = int(column_B_Bounds[0])
    data2Column_B = int(column_B_Bounds[0])
    data3Column_B = int(column_B_Bounds[0])

    data1Column_G = int(column_G_Bounds[0])
    data2Column_G = int(column_G_Bounds[0])
    data3Column_G = int(column_G_Bounds[0])

    data1Column_R = int(column_R_Bounds[0])
    data2Column_R = int(column_R_Bounds[0])
    data3Column_R = int(column_R_Bounds[0])

    dSurface = DAPS_SURFACE(surface,surface,3)
    list = RANDOM_LIST(listSize)
    tNode = list.headval
    while (tNode.next):
        WRITE_NODE_TO_SURFACE(dSurface, tNode)
        tNode = tNode.next
    test = Node('abcde','fgh','12345')
    WRITE_NODE_TO_SURFACE(dSurface,test)

    start = time.time()
    x,y = QUERY_SURFACE(dSurface,test)
    print("node found at: ",x, ",", y)
    end = time.time()
    print(end-start)

    cv2.imshow('DAPS',dSurface)
    BGR_CLASSIFY(BGR_LINKED_LIST(list))
    cv2.waitKey(0)

    return()
init()
