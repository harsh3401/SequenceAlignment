
import sys
import time
import psutil

strings=[]
insertion_points=[]
penalty_grid =          [[0, 110, 48, 94],
                      [110, 0, 118, 48],
                      [48, 118, 0, 110],
                      [94, 48, 110, 0]]
gap =30
data_to_op = []   

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

def penalty_grid_value(character1,character2):
    mainString='ACGT'
    idx1=mainString.find(character1)
    idx2=mainString.find(character2)
    return penalty_grid[idx1][idx2]

def alignment(str1,str2):
    str1_length = len(str1)
    str2_length = len(str2)
    OPT = [[0 for _ in range(str2_length+1)] for _ in range(str1_length+1)]
    #Base Case
    for i in range(str1_length+1):
        OPT[i][0]=gap*i

    for j in range(str2_length+1):
        OPT[0][j]=gap*j

    for i in range(1,str1_length+1):
        for j in range(1,str2_length+1):
                min_value= min(OPT[i - 1][j - 1]+ penalty_grid_value(str1[i-1], str2[j-1]),
                                OPT[i - 1][j] + gap,
                                OPT[i][j - 1] + gap)
                OPT[i][j]=min_value
    return OPT

def get_path_simple(OPT, s1, s2):
  s1_length = len(s1)
  s2_length = len(s2)
  # Initialize aligned strings
  s1_final = ""
  s2_final = ""
  # Start from the bottom right corner
  i = s1_length
  j = s2_length

  while i > 0 or j > 0:
   
    # Move up if the previous row cell had the minimum cost (gap in s1)
    if OPT[i][j] == OPT[i - 1][j] + gap:
      s1_final = s1[i - 1] + s1_final
      s2_final = "_" + s2_final
      i -= 1
      
    # Move left if the previous column cell had the minimum cost (gap in s2)
    elif OPT[i][j] == OPT[i][j-1]+gap:
      s1_final = "_" + s1_final
      s2_final = s2[j - 1] + s2_final
      j -= 1

    else:
      s1_final = s1[i - 1] + s1_final
      s2_final = s2[j - 1] + s2_final
      i -= 1
      j -= 1
  # Print and return aligned strings
  return [s1_final, s2_final]

def process_memory():
    process = psutil.Process() 
    memory_info =process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

def driver():
  processInput()
  inputStrings = generateString()
  OPT = alignment(inputStrings[0],inputStrings[1])
  data_to_op.append(OPT[len(inputStrings[0])][len(inputStrings[1])])
  finalstr=get_path_simple(OPT,inputStrings[0],inputStrings[1])
  data_to_op.append(finalstr[0])
  data_to_op.append(finalstr[1])
  
if __name__ == "__main__":
    start_time=time.time()
    driver()
    end_time = time.time()
    mem_usage=process_memory()
    time_taken = (end_time - start_time)*1000 
    data_to_op.append(time_taken)
    data_to_op.append(mem_usage)
    OUTPUT_FILE = sys.argv[2]
    with open(OUTPUT_FILE, "w") as f:
         for item in data_to_op:
            f.write(f"{item}\n")