import sys 

#Elmer:
def clean_text(text):
    result = []  #empty list to hold finished words
    words = text.split() #split function as suggested to devide the words 
   
    for word in words: #looping each word in the list 
        cleaned_word = "" #empty string, will be filled later on
        for char in word: #looping every char in word
            if char.isalpha(): #returns true for letters A-Ö
                cleaned_word = cleaned_word + char #puts togehter the letters
        cleaned_word = cleaned_word.lower() #method for converting to lowercase 
        if cleaned_word != "": #skipping words without letters 
            result.append(cleaned_word) #adding element to list 
    return result

#Alex 
# parts of the code taken from https://www.w3schools.com/python/python_file_open.asp and https://www.geeksforgeeks.org/python/how-to-read-from-a-file-in-python/ and https://stackoverflow.com/questions/4796764/read-file-from-line-2-or-skip-header-row
def load_dictionary(filename): #loads CSV file
    # Open file in readmode
    with open(filename, "r") as f:
        sentiment_weights = {} #Create empty dictionary
        next(f) #Skips first line
        for line in f: #loops the file
            word, score = line.strip().split(",") # Removes whitespace ande split at ,
            sentiment_weights[word] = int(score) # Store as key-value, word key and score value
        return sentiment_weights # Return the dict


#Elmer: 
def calculate_score(text, sentiment_weights):
    words = clean_text(text) #making a list for the cleaned words 
    score = 0 #sets inital value to 0 

    for word in words: #looping all words in the list 
        if word in sentiment_weights: #if the word exists in the list
            score = score + sentiment_weights[word] #add the score assaigned to the word 
        else:
            score = score + 0 #not adding score if word is not in the list 
    return (text, score) 

#Lukas:
def analyze_sentiment(document, sentiment_weights):
    # make an empty array where we collect the results
    resultat_lista = []

    # go through the document one row at a time
    for rad in document:

        # use the function calculate_score to - surprise!!! - calculate the score
        text_och_poang = calculate_score(rad, sentiment_weights)

        # make the points and text separately
        texten = text_och_poang[0]
        poangen = text_och_poang[1]

        # use if here to make points over 0 positive and below 0 negative
        if poangen > 0:
            kansla = "Positive"
        elif poangen < 0:
            kansla = "Negative"
        else:
            kansla = "Neutral"

        fardig_trio = (texten, poangen, kansla)

        # append to our list of results
        resultat_lista.append(fardig_trio)

    # send it baackkkk after the entire list has gone through our little processing
    return resultat_lista

#Lukas: 
def print_report(results, n=None):
    # print out
    # make it look nice with ljust and rjust
    print("Post Content".ljust(60) + "| " + "Score".rjust(5) + " | Sentiment")

    # make it look nice here too
    print("-" * 80)

    if n == None:
        n = len(results)

    # range in loop here to just loop n amount of times
    for i in range(n):
        # safety check because im paranoid
        if i < len(results):
            # text, points and feelings
            trio = results[i]
            texten = trio[0]
            poangen = trio[1]
            kanslan = trio[2]

            # ljust and rjust only works on text so we make the points a string
            poang_text = str(poangen)

            # print
            print(texten.ljust(60) + "| " + poang_text.rjust(5) + " | " + kanslan)


#
if len(sys.argv) < 3:
    print("Not supported")
else:
    ord_fil = sys.argv[1]
    text_fil = sys.argv[2]

    # load the words.csv
    sentiment_weights = load_dictionary(ord_fil)

    # read the reviews.txt
    dokument = []
    recensioner_fil = open(text_fil, 'r')
    rader = recensioner_fil.readlines()

    for rad in rader:
        ren_rad = rad.strip()
        if ren_rad != "":
            dokument.append(ren_rad)
    recensioner_fil.close()

    # analyze the document with this little function here
    alla_resultat = analyze_sentiment(dokument, sentiment_weights)


    if len(sys.argv) == 4:
        kommando = sys.argv[3]

        if kommando == "POS":
            # here for positive pick it out
            pos_lista = []
            for res in alla_resultat:
                if res[2] == "Positive":
                    pos_lista.append(res)
            print_report(pos_lista)

        elif kommando == "NEG":
            # pick out the negative
            neg_lista = []
            for res in alla_resultat:
                if res[2] == "Negative":
                    neg_lista.append(res)
            print_report(neg_lista)

        elif kommando == "NEUT":
            # pick out the neutral
            neut_lista = []
            for res in alla_resultat:
                if res[2] == "Neutral":
                    neut_lista.append(res)
            print_report(neut_lista)

        elif kommando.isdigit():
            # if you want to print like the first 10 or something we can use this
            antal = int(kommando)
            print_report(alla_resultat, antal)

        else:
            print("Not supported")

    elif len(sys.argv) == 3:
        # if number is not specified print out the entire thing
        print_report(alla_resultat)

    else:
        print("Not supported")