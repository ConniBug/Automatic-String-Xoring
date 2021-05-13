#!/usr/bin/env python

xorFunctionName = str(input("Whats your xor/cryptstr function name: "))#"crypt_str"
filename = str(input("Whats your file name? "))

outputAlreadyXoredMessage = False

with open(filename) as f:
    content = f.readlines()

f = open("cleaned_" + filename, "w")

lineCount = 1

checkedStringCount = 0
hitsCount = 0

inLargeComment = False
lastChar = ""

print("starting.")
for line in content:

    #print("Checking line", lineCount, "line:", line)
    lineCount += 1

    if(line.replace(" ", "").startswith("//")):
        #print("Skipping line", lineCount + 1, "As we believe its a comment:", line)
        continue
    if(line.replace(" ", "").startswith("#include") or line.startswith("#pragma")):
        #print("Skipping Visual Studio #include.")
        f.write(line)
        continue
    
    lineToWrite = ""

    foundXorCall = False

    skipNext = False
    building = False
    
    built = ""

    current = ""
    for char_index in range(len(line)):
        char = line[char_index]
        #if(char == "*"):
            #print(lastChar + char)
        if(lastChar + char == "/*"):
            f.write( "/*")
            print("We are now in a large commanet - line:", lineCount - 1)
            inLargeComment = True
            lastChar = char
            continue

        #if(len(line) <= 3):
           # print("==================")
           # print("chk:", lastChar + char)
            #print("lastchar:", lastChar + char)
            #print("char:", lastChar + char)
            #print("==================")
        if(lastChar + char == "*/"):
            f.write( "*/")
            print("Left large comment - line:", lineCount - 1)
            inLargeComment = False
            lastChar = char
            continue

        if(inLargeComment):
            if(current != line):
                ##print("Skipping as we are in a large comment... line:", lineCount - 1, "line:", line)
                current = line
                lastChar = char
                continue
                                
        lastChar = char
        if(building == False and char == '"'):
            if(lineToWrite.replace(" ", "").endswith(xorFunctionName + "(")):
                if(outputAlreadyXoredMessage):
                    print("Already xored")
                skipNext = True
            else:
                if(skipNext == False):
                    built = built + char
                    building = True
                    skipNext = False
                    continue
               
        if(building == True and char == '"'):
            if(skipNext):
                skipNext = False
            else:
                built = built + char
                building = False
                continue
            

        if(building):
            #print(char)
            built = built + char
        else:
            if(built != ""):
                tmp = built[len(built) - 2] + built[len(built) - 1]
                if(tmp == '\"'):
                    print("Built ends with weird thing skipping the xor to avoid breaking things...", built)
                    print("built:", built[len(built) - 1])
                    print("built:", built[len(built) - 2])
                else:
                    lineToWrite += xorFunctionName + "(" + built + ")"
                    print("Found non xored string on line", lineCount - 1, "String was", built)
                    hitsCount = hitsCount + 1
                    built = ""
            checkedStringCount = checkedStringCount + 1
            lineToWrite = lineToWrite + char

        #print("lineToWrite", lineToWrite)
        #print("Built", 
    f.write(lineToWrite)
    
f.write("\n\n // ReXored By https://github.com/ConniBug/Automatic-String-Xoring")
f.write  ("\n // Creator: Conni!~#0920")

f.close()

print("")
print("Checked", checkedStringCount, "strings got", hitsCount, "hits.")
