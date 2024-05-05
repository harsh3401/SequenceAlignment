import sys
strings=[]
insertion_points=[]
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
        print(indices)
        for insertionPoint in indices:
                inputString=inputStrings[index][:insertionPoint+1]+inputStrings[index]+inputStrings[index][insertionPoint+1:]
                inputStrings[index]=inputString
                print(inputStrings[index])
    print("final",inputStrings)      
        
        
processInput()
generateString()
    
    

# def getScore():
    
    

        
        
