###############################
# - Set the fileToReverse name:
fileToReverse = input("Enter file name: ")
###############################
'''
Reverses the prices, examle:

Input file contains:
1
2
3

Outut file will contain:
3
2
1
'''
outputFile = fileToReverse
current_list = open(fileToReverse, 'r').readlines()
output_list = [0]*len(current_list)
print()
print()
print()
print("Input file:", fileToReverse)
for i in range(len(current_list)):
    output_list[-i-1] = current_list[i]
print("Saving to file:", outputFile)
saveFile = open(outputFile, 'w')
i=0
while i < len(output_list):
    saveFile.write(output_list[i])
    i+=1
saveFile.close()
print("- Done!")
print()