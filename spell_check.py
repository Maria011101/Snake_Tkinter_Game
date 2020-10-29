import os,time,string
from difflib import SequenceMatcher
def word_filter(word1):
    newWord=word1.lower()
    alphabet=list(string.ascii_lowercase)
    a=range(len(newWord))
    temp=''
    for i in newWord:
        if i in alphabet:
            temp += i
    return temp

def match(word1):
    best_score=0
    best_word=""
    for word2 in dictionaryList:
        score = SequenceMatcher(None, word1, word2).ratio()
        if(best_score < score):
        best_score = best_score
        best_word = word2

def spell_check_sentence():
    sentence=input("Please enter your sentence: \n")
    wordList=sentence.split()
    total_words=len(wordList)
    wrong_words=0
    correct_words=0
    marked_words=[]
    print("\n")
    file=open("EnglishWords.txt")
    dictionaryList=[]
    for x in file:
        dictionaryList.append(x.strip())
    for word in wordList:
        word=word_filter(word)
        if (not word in dictionaryList):
            print("OOpsie! The following word seems to not be in the dictionary: " + word +". You have the following options: \n")
            print("1.Ignore\n"+"2.Mark\n"+"3.Add to dictionary\n" + "4.Suggest a likely correct spelling\n")
            i=0
            while(i==0):
                choice2=input("My choice is: ")
                i=1
                if(choice2=='1'):
                    print("\n")
                    print("Okay! Word ignored!\n")
                elif(choice2=='2'):
                    print("\n")
                    print("Okay! Word marked!\n")
                    marked_words.append(word)
                    print(marked_words)
                elif(choice2=='3'):
                    print("\n")
                    print("Okay! Word added to dictionary!\n")
                    dictionaryList.append(word)
                elif(choice2=='4'):
                    print("\n")
                    match(word)
                else:
                    print("\nInvalid input! Please write a valid input: 1, 2, 3 or 4. It's not hard.\n")
                    i=0







print("Loading...")
time.sleep(2)
print("Welcome, "+ os.getlogin() +"!🥰 This is the Spell Check machine. What would you like to do?\n")
print("The options are:\n")
optionsList=["quit the program","spell check a sentence", "spell check a file"]
i=0
while i<len(optionsList):
    time.sleep(1)
    print("Press "+ str(i) + " to " + optionsList[i])
    i+=1
print("\n")
i=0
while i==0:
    choice=input("My choice is: ")
    if(choice=='0'):
        i=1
        os._exit(0)
    elif(choice=='1'):
        i=1
        spell_check_sentence()
    elif(choice=='2'):
        i=1
        speel_check_file()
    else:
        print("Invalid input.😤 Please enter a valid input.")
