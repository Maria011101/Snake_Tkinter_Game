import os,time
def spell_check_sentence():
    sentence=input("Please enter your sentence: \n")
    wordList=sentence.split()
    file=open("EnglishWords.txt")
    dictionaryList=[]
    for x in file:
        dictionaryList.append(x.strip())


    for word in wordList:
        if (word in dictionaryList):
            print(word + " ")
        else:
            print("OOpsie! The word you have written (" + word + ") seems to not appear in the dictionary. You have three options:")


print("Loading...")
time.sleep(2)
print("Welcome, "+ os.getlogin() +"!🥰 This is the Spell Check machine. What would you like to do?")
print("The options are:")
optionsList=["quit the program","spell check a sentence", "spell check a file"]
i=0
while i<len(optionsList):
    time.sleep(1)
    print("Press "+ str(i) + " to " + optionsList[i])
    i+=1
i=0
while i==0:
    choice=int(input("My choice is: "))
    if(choice==0):
        i=1
        os._exit(0)
    elif(choice==1):
        i=1
        spell_check_sentence()
    elif(choice==2):
        i=1
        speel_check_file()
    else:
        print("Invalid input.😤 Please enter a valid input.")
