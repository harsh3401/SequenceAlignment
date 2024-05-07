import sys
import numpy as np
import sys
from resource import * 
import time 
import psutil

def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed


strings=[]
insertion_points=[]
penalty_grid = [[0, 110, 48, 94],[110, 0, 118, 48],[48, 118, 0, 110],[94, 48, 110, 0]]
GAP_PENALTY=30
path=[]



def processInput():
    
    INPUT_FILE_NAME = sys.argv[1]
    fileContent= open(INPUT_FILE_NAME,"r")
  
    
    for index,line in enumerate(fileContent.readlines()):  
        line = line.strip() #removing whitespace  
        if line.isnumeric() and index == 0:
            raise ValueError("First line should be a string, followed by insertion points as Integers")
        if not line.isnumeric():
            strings.append(line)
        else:
            if len(insertion_points)==len(strings):
                insertion_points[len(strings)-1].append(int(line))
            else:
                insertion_points.append([int(line)])


def generateString():

    inputStrings=strings.copy()
    
    for index,_ in enumerate(inputStrings):
        indices=insertion_points[index]
        for insertionPoint in indices:
                inputString=inputStrings[index][:insertionPoint+1]+inputStrings[index]+inputStrings[index][insertionPoint+1:]
                inputStrings[index]=inputString
    return inputStrings
   

    
def divideAndConquerAlign(stringx,stringy,x_offset,y_offset):
    
    # Base Case
 
    strxlen=len(stringx)
    strylen=len(stringy)
    if strxlen<=2 or  strylen<=2:

        solveTrivialAlignment(stringx,stringy,x_offset,y_offset)  
     # Recursion steps
    else:
      
        forwardAlignment=runMemEfficientPass(stringx[0:strxlen//2],stringy)[1]
        backwardAlignment=runMemEfficientPass(stringx[strxlen//2:][::-1],stringy[::-1])[1][::-1]
        sum_data=np.add(forwardAlignment, backwardAlignment)
        minimum_data=[0,sum_data[0]]
        for idx,sum in enumerate(sum_data):
            if sum <minimum_data[1]:
                minimum_data=[idx,sum]

        path.append([strxlen//2+x_offset,minimum_data[0]+y_offset])
       
        divideAndConquerAlign(stringx[:strxlen//2],stringy[:minimum_data[0]],x_offset,y_offset)
        divideAndConquerAlign(stringx[strxlen//2:],stringy[minimum_data[0]:],x_offset +strxlen//2,minimum_data[0]+y_offset)
        return path
   

    
def solveTrivialAlignment(stringx,stringy,x_offset,y_offset):
    opt = [[0 for _ in range(len(stringy)+1)] for __ in range(len(stringx)+1)]
    for i in range(len(opt[0])):
        opt[0][i]=i*GAP_PENALTY
    for j in range(1,len(stringx)+1):
        opt[j][0]=j*GAP_PENALTY
        for k in range(1,len(opt[0])):
            opt[j][k]=min(opt[j][k-1]+GAP_PENALTY,opt[j-1][k]+GAP_PENALTY,opt[j-1][k-1]+penaltyGridValue(stringx[j-1],stringy[k-1]))
    getPath(opt,stringx,stringy,x_offset,y_offset)
    

def runMemEfficientPass(stringx,stringy):
    opt = [[0 for _ in range(len(stringy)+1)] for __ in range(2)]
    for i in range(len(opt[0])):
        opt[0][i]=i*GAP_PENALTY
    for j in range(1,len(stringx)+1):
        opt[1][0]=j*GAP_PENALTY
        for k in range(1,len(opt[0])):
            opt[1][k]=min(opt[1][k-1]+GAP_PENALTY,opt[0][k]+GAP_PENALTY,opt[0][k-1]+penaltyGridValue(stringx[j-1],stringy[k-1]))
        for t in range(0,len(opt[0])):
            opt[0][t]=opt[1][t]
       
    return opt

# def outputDump():
    
def getMismatchStrings(path,stringx,stringy):
    strx=""
    stry=""
    strxid=0
    stryid=0
    for idx in range(0,len(path)-1):
        if path[idx][1]==path[idx+1][1] and path[idx][0]<path[idx+1][0]:
            strx=strx+stringx[strxid]
            stry=stry+'-'
            strxid=strxid+1
        elif path[idx][0]==path[idx+1][0] and path[idx][1]<path[idx+1][1]:
            strx=strx+'-'
            stry=stry+stringy[stryid]
            stryid=stryid+1
        # Skipping overlapping cells in the path
        elif path[idx][1]==path[idx+1][1] and path[idx][0]==path[idx+1][0]:
            pass
        else :
            strx=strx+stringx[strxid]
            stry=stry+stringy[stryid]
            strxid=strxid+1
            stryid=stryid+1

    return strx,stry
        
    
    
    
def getPath(opt,stringx,stringy,x_offset,y_offset):
    i=len(stringx)
    j=len(stringy)
    path_new=[[0 for _ in range(len(stringy)+1)] for __ in range(len(stringx)+1)]
    path_new[i][j]=1
    path_new[0][0]=1

    while i!=0 or j!=0:

        if opt[i][j]==opt[i-1][j]+GAP_PENALTY :
            path_new[i-1][j]=1
            i=i-1
        elif opt[i][j]==opt[i][j-1]+GAP_PENALTY:
            path_new[i][j-1]=1
            j=j-1
        else :
            path_new[i-1][j-1]=1
            i=i-1
            j=j-1
        
    
    for idx,x in enumerate(path_new):
        for idy in range(len(path_new[0])):
            if x[idy] == 1:
                path.append([idx+x_offset , idy+y_offset])
    
    

        
    
        
def penaltyGridValue(character1,character2):
    mainString='ACGT'
    idx1=mainString.find(character1)
    idx2=mainString.find(character2)
    return penalty_grid[idx1][idx2]
    
def testRunner():
    processInput()
    strings=generateString()
    divideAndConquerAlign(strings[0],strings[1],0,0)
    path.sort(key = lambda x:(x[0],x[1]))
    res1,res2=getMismatchStrings(path,strings[0],strings[1])
    print(getStringDiff(res1,res2))
 

def getStringDiff(str1,str2):
    score=0
    for idx in range(len(str1)):
        if str1[idx].isalpha() and str2[idx].isalpha():
            score+=penaltyGridValue(str1[idx],str2[idx])
        else:
            if str1[idx].isalpha() and str2[idx]=='-':
                score+=30
            if str2[idx].isalpha() and str1[idx]=='-':
                score+=30
    return score
    
if __name__ == "__main__":
    start_time=time.time() 
    testRunner()
    end_time = time.time()
    print("memory",process_memory())
    time_taken = (end_time - start_time)*1000 
    data_to_op.append(time_taken)
    OUTPUT_FILE = sys.argv[2]
    with open(OUTPUT_FILE, "w") as f:
         for item in data_to_op:
            f.write(f"{item}\n")
    


    

        
        
