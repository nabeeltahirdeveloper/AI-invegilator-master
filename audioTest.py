import os

import Levenshtein as lev


isMatched=False

def audioMatch(file1, file2):


    file=open(f'Dataset\my Data\{file1}','rb')
    a=str(file.read())


    file2=open(file2,'rb')
    b=str(file2.read())



    if a==b:
        print("same")
    else:
        print("not same")
    Ratio = lev.ratio(b.lower(), a.lower())
    print(Ratio)


    if Ratio>=0.8:
        print("almost same")
        isMatched=True
        return True
    else:
        print("not same")



for root, dirs, files in os.walk("Dataset\my Data"):
    for filename in files:
        print(filename)
        if audioMatch(filename,"demo.wav"):
            break
    if isMatched:
        break