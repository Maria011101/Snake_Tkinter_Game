import os,time,string
from difflib import SequenceMatcher
from datetime import datetime

# Stats variables
wrong_words = 0
correct_words = 0
words_changed = 0
added_words = 0
total_words = 0
start = time.time()

#Word filter is a function that filters out uppercase characters and non-alpha characters.
def word_filter(word1):
    newWord = word1.lower()
    alphabet = list(string.ascii_lowercase)
    a = range(len(newWord))
    temp = ''
    for i in newWord:
        if i in alphabet:
            temp += i
    return temp

#Match is a function that finds the closest match(suggestion) to a given word and asks the user if they accept the suggestion. If the user accepts it, the function returns the match, otherwise it returns the initial word.
def match(word1):
    global correct_words
    global words_changed
    global wrong_words

    best_score = 0
    best_word = ""
    score =  0

    for word2 in dictionaryList:
        score = SequenceMatcher(None, word1, word2).ratio()
        if(best_score <= score):
            best_word = word2
            best_score = score

    print("The best match found is: " + best_word + ". Do you accept this?")
    choice3 = input(" Type YES or NO: ")

    if choice3 in ["YES","yes", "y","Y","YEAH","yeah"]:
        correct_words += 1
        words_changed += 1
        print("\n Okay! Word updated!")
        return best_word
    else:
        wrong_words += 1
        print("\n Okay! Word was not updated!")
        return word1

def spell_check_sentence(wordList1):
    global wrong_words
    global correct_words
    global added_words
    global wordList_modified

    for word in wordList1:
        word = word_filter(word)


        if ( word in dictionaryList):
            correct_words += 1
        else:
            time.sleep(1)
            print("\n   ⟶ OOpsie! The following word seems to not be in the dictionary: " + word +  ". You have the following options: \n")
            time.sleep(1)
            print("     1.Ignore\n" + "     2.Mark\n" + "     3.Add to dictionary\n" + "     4.Suggest a likely correct spelling\n")

            i = 0
            while(i == 0):
                choice2=input("My choice is: ")
                i = 1
                if(choice2 == '1'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word ignored!😅 \n")
                    wrong_words += 1

                elif(choice2 == '2'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word marked!😅 \n")
                    word = word + "(?)"

                elif(choice2 == '3'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word added to dictionary!📖\n")
                    added_words += 1
                    correct_words += 1
                    dictionaryList.append(word)

                elif(choice2 == '4'):
                    print("\n")
                    word = match(word)

                else:
                    print("\nInvalid input! Please write a valid input: 1, 2, 3 or 4.\n")
                    i = 0
        wordList_modified.append(word)

def spell_check_file(fileList1):
    global wrong_words
    global correct_words
    global added_words
    global fileList_modified

    for file_word in fileList:
        file_word = word_filter(file_word)

        if ( file_word in dictionaryList):
            correct_words += 1
        else:
            time.sleep(1)
            print("\n   ⟶ OOpsie! The following word seems to not be in the dictionary: " + file_word + ". You have the following options: \n")
            print("     1.Ignore\n"+"     2.Mark\n"+"     3.Add to dictionary\n" + "     4.Suggest a likely correct spelling\n")

            i = 0
            while(i == 0):
                choice3 = input("My choice is: ")
                i = 1
                if(choice3 == '1'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word ignored!\n")
                    wrong_words += 1

                elif(choice3 == '2'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word marked!\n")
                    #marked_words.append(file_word)
                    file_word = file_word + "(?)"

                elif(choice3 == '3'):
                    time.sleep(1)
                    print("\n")
                    print("Okay! Word added to dictionary!\n")
                    added_words += 1
                    correct_words += 1
                    dictionaryList.append(file_word)

                elif(choice3 == '4'):
                    time.sleep(1)
                    print("\n")
                    file_word = match(file_word)

                else:
                    print("\nInvalid input! Please write a valid input: 1, 2, 3 or 4.\n")
                    i = 0
        fileList_modified.append(file_word)


def createFile(the_list):
    global start
    global end

    newFile_name = input("Please tell me the name of your new file:")
    newFile=open(newFile_name,"a")

    newFile.write("\nOK! Time for statistics:\n")
    newFile.write("     ✓ In total, you wrote " + str(total_words) + " words. \n")
    newFile.write("     ✓ You spelled corectly " + str(correct_words) + " words. \n")
    newFile.write("     ✓ You spelled incorectly " + str(wrong_words) + " words. \n")
    newFile.write("     ✓ You changed " + str(words_changed) + " words with my suggestions. \n")
    newFile.write("     ✓ You added " + str(added_words) + " words to the dictionary \n")
    newFile.write("     ✓ The date and time that the program executed: " + str(datetime.now()) + "\n")
    newFile.write("     ✓ The amount of time elapsed to spellcheck the input: " + str(end-start))
    newFile.write("\n")
    for z in the_list:
        newFile.write(z + " ")

enter_menu = '1'
while(enter_menu == '1'):
    enter_menu = '1'

    #Reassigning the stats variables the values of 0 for when the user wants to do a second spell check
    wrong_words = 0
    correct_words = 0
    words_changed = 0
    added_words = 0
    total_words = 0

    print("\n")
    load="Loading...\n"
    print(load.center(80))

    time.sleep(1)

    #Reading the dictionary and storing it into a list
    file = open("EnglishWords.txt")
    dictionaryList = []
    for x in file:
        dictionaryList.append(x.strip())
    file.close()



    #Menu
    print("   Welcome, " + os.getlogin() + "!🥰 This is the Spell Check machine. What would you like to do?💕\n")
    print("   The options are:\n")
    optionsList = ["quit the program", "spell check a sentence", "spell check a file"]

    #Printing the options
    i = 0
    while i < len(optionsList):
        time.sleep(1)
        print("     •Press " + str(i) + " to " + optionsList[i])
        i += 1
    print("\n")

    i = 0
    while i == 0:
        choice = input("My choice is: ")

        if(choice == '0'):
            i = 1
            os._exit(0)
        elif(choice=='1'):
            i = 1
            time.sleep(1)
            sentence = input("\nPlease enter your sentence: \n")
            wordList = sentence.split()
            total_words = len(wordList)
            wordList_modified=[]
            spell_check_sentence(wordList)
            end=time.time()
            createFile(wordList_modified)

        elif(choice == '2'):
            i = 1
            time.sleep(1)
            file_name = input("\nPlease write the name of your file:")

            if(os.path.exists(file_name) == True):
                file_checked = open(file_name)
            else:
                while(os.path.exists(file_name) == False):
                    file_name= input("It seems your file doesn't exist. Please enter the correct name of your file ")


                file_checked = open(file_name)

            fileList_modified=[]
            fileList = file_checked.read().split()
            file_checked.close()
            total_words = len(fileList)
            spell_check_file(fileList)
            end=time.time()
            createFile(fileList_modified)

        else:
            print("Invalid input.😤 Please enter a valid input.")


    time.sleep(1)
    print("\nOK! Time for statistics:\n")
    print("\n")
    time.sleep(1)
    print("    ✓ In total, you wrote " + str(total_words) + " word(s). \n")
    time.sleep(1)
    print("    ✓ You spelled corectly " + str(correct_words) + " word(s). \n")
    time.sleep(1)
    print("    ✓ You spelled incorectly " + str(wrong_words) + " word(s). \n")
    time.sleep(1)
    print("    ✓ You changed " + str(words_changed) + " words(s) with my suggestions. \n")
    time.sleep(1)
    print("    ✓ You added " + str(added_words) + " word(s) to the dictionary \n")
    time.sleep(1)
    print("    ✓ The date and time that the program executed: " + str(datetime.now()) + "\n")
    time.sleep(1)
    print("    ✓ The amount of time elapsed to spellcheck the input: " + str(end-start))
    time.sleep(1)
    print("\n")
    enter_menu=input("\nWould you like to return to the menu? If so, press 1: ")
