
#   MMM   MMM   SSSSS      MMM   MMM    AAA    NN   NN   NN   NN   EEEEE   RRRRR   SSSSS
#   MMMM MMMM   S          MMMM MMMM   A   A   NNN  NN   NNN  NN   E       R   RR  S
#   MM MMM MM   SSSSS      MM MMM MM   AAAAA   NN N NN   NN N NN   EEEE    RRRRR   SSSSS
#   MM     MM       S  ..  MM     MM   A   A   NN  NNN   NN  NNN   E       R  RR       S
#   MM     MM   SSSSS  ..  MM     MM   A   A   NN   NN   NN   NN   EEEEE   R   RR  SSSSS

#   Created through the grace of God by Joe Hakanson and Luke Rickert
#   CS328 - Saint Mary's University of Minnesota - 2025

import re
import random
import string
from spellchecker import SpellChecker #RUN THE COMMAND BELOW
#run in terminal --> pip install pyspellchecker
from tkinter import *
import ttkbootstrap as tb  # to install do: pip install ttkbootstrap
from ttkbootstrap.scrolled import ScrolledText

properNouns = [
    "american",
    "america",
    "pacific",
    "french",
    "france",
    "italian",
    "italy",
    "chinese",
    "china",
    "japanese",
    "japan",
    "european",
    "europe",
    "United States",
    "continental"
]

spell = SpellChecker()
def spellCheck(word): #used in the spellCheckQuestion functionality
    # Split leading punctuation
    i = 0
    while i < len(word) and word[i] in string.punctuation:
        i += 1
    prefix = word[:i]
    # Split trailing punctuation
    j = len(word)
    while j > i and word[j-1] in string.punctuation:
        j -= 1
    suffix = word[j:]
    core = word[i:j]
    if not core:
        return None
    corrected = spell.correction(core)

    if corrected.lower() == core.lower():
        return None

    return f"{prefix}{corrected}{suffix}"

def spellCheckQuestion(q): #Handles typos and returns correction
    corrected = False
    words = q.strip().split()
    outputWords = []

    for w in words:
        fixed = spellCheck(w)
        if fixed:
            corrected = True
            outputWords.append(fixed)
        else:
            outputWords.append(w)

    return corrected, " ".join(outputWords)
        
def capitalizes(text): #ensures proper capitalization
    text = text.strip()

    def cap_sentence(match):
        return match.group(1) + match.group(2).upper()

    text = re.sub(r'(^|[.!?]\s+)([a-zA-Z])', cap_sentence, text) #finds ends of sentences and capitalizes the next word

    for noun in properNouns:
        pattern = r'\b' + re.escape(noun) + r'\b'
        text = re.sub(pattern, noun.capitalize(), text, flags=re.IGNORECASE) 
        #finds matching proper nouns and capitalizes them as necessary

    return text

def findQWord(user_question: str): #finds which question word is used 
    question = user_question.lower().strip() 

    if question.startswith("what"):
        return "what"
    if question.startswith("which"):
        return "which"
    if question.startswith("where"):
        return "where"
    if question.startswith("when"):
        return "when"
    if question.startswith("how"):
        return "how"
    if question.startswith("who"):
        return "who"
    if question.startswith("why"):
        return "why"
    if question.startswith("should"):
        return "should"

    # fallback: look for first question word anywhere
    for word in ["what","which","where","when","how","who","why"]:
        if re.search(rf"\b{word}\b", question):
            return word

    return None

def findLikelyQWords(sentence): #Takes a sentence and finds question words that would likely go with this info
    testSentence = sentence.lower()
    categories = set()

    # WHEN
    timePhrases = ["before", "after", "when", "whenever", "while", "as", "since", "until",
    "once", "then", "now", "soon", "earlier", "later", "eventually",
    "finally", "immediately", "as soon as", "by the time", "the moment",
    "the minute", "the second", "just as", "right after", "right before",
    "in the meantime", "at the same time", "prior to", "from that point on",
    "during", "always", "never", "first", "last"]

    for f in timePhrases:    # Determines if statement has to do with time
        if f in testSentence:
            categories.add("when")
            break

    # WHAT: Almost all instructions answer "what"
    categories.add("what")

    # WHICH: choosing between items, positions, utensils, sides
    whichTriggers = ["left", "right", "outer", "inner", "smaller", "larger", "first", "second", "third",
    "best", "worst", "which", "big"]

    for t in whichTriggers:
        if t in testSentence:
            categories.add("which")

    # WHERE: placement, position, movement, location
    if re.search(r"\b(on|in|at|to|from|under|over|between|beside|across|around|inside|outside)\b", testSentence):
        categories.add("where")

    # WHEN: timing, sequencing
    if re.search(r"\b(before|after|during|when|while|as soon as|always|never|first|last)\b", testSentence):
        categories.add("when")

    # HOW: adverbs or manner
    if re.search(r"""\b(slowly|gently|politely|quietly|carefully|subtly|neatly|properly|correctly|firmly|softly|in a|with your
                 |gracefully|delicately|respectfully|courteously|mindfully|attentively|lightly|modestly|pleasantly|calmly|smoothly
                 |promptly|silently|steadily|deliberately|orderly|evenly|patiently|tastefully)\b""", testSentence):
        categories.add("how")

    # WHO: references to roles or people
    if re.search(r"\b(host|hostess|guest|person|waiter|server|lady|man|friend|boss)\b", testSentence):
        categories.add("who")

    # WHY: only when explanation exists
    if re.search(r"\b(because|so that|so you|in order to)\b", testSentence):
        categories.add("why")

    return list(categories)

def findKeyWords(user_question):    # Returns a list of the key words
    qKeyWords = []

    for word in user_question.split():
        word = word.lower()
        if word in stopWords:
            continue
        cleanedWord = ""
        for c in word:
            if c.isalnum():
                cleanedWord += c
        if cleanedWord: 
            qKeyWords.append(cleanedWord) #gets all the key words of the question
    return qKeyWords

def parse_list_string(s: str): #cleans up the data after receiving it from cleanedInfo (ironic)
    s = s.strip()[1:-1]
    items = [item.strip().lower().strip("'\"") for item in s.split(',') if item.strip()]
    return items

def entryType(entry): #determines the type of userEntry

    #AI Generated Dictionary
    gestureResponses = {
    # greetings (longer first)
    "good morning": [
        "Good morning! Ask me anything about table manners!",
        "Morning! What would you like to know about proper dining etiquette?",
    ],
    "good afternoon": [
        "Good afternoon! Ask me a question if you're curious about proper table manners!",
        "Afternoon! Ask me any questions about polite dining behavior.",
    ],
    "good evening": [
        "Good evening! Ask me something if you want to learn some table etiquette tips?",
        "Evening! Ask me about proper table manners!",
    ],
    "what's up": [
        "Not much! Are you curious about table manners today?",
        "Just here to help — ask me any questions about dining etiquette!",
    ],
    "whats up": [
        "Not much! Ask me any table manners questions!",
        "Here and ready to chat — what would you like to know about dining etiquette?",
    ],
    "how's it going": [
        "Going well! Ask me any questions about table manners!",
        "Doing great! Ask me a question if you're curious about dining etiquette!",
    ],
    "hows it going": [
        "Going well! Ask me something if you want to learn about table etiquette?",
        "All good here! Any dining etiquette questions?",
    ],
    "how are you": [
        "I'm doing well, thank you! What would you like to know about table manners?",
        "Pretty good! Ask me a question if you're curious about dining etiquette!",
    ],
    "how do you do": [
        "Doing well, thank you! Ask me anything about table!",
        "I’m doing fine! Any questions about proper dining etiquette?",
    ],
    "nice to meet you": [
        "Nice to meet you too! Would you like to talk about table manners?",
        "Pleasure meeting you! Ask me a question if you're curious about dining etiquette!",
    ],
    "pleasure to meet you": [
        "The pleasure’s mine! Ask me something if you want to learn about table manners?",
        "Likewise! Ask me any dining etiquette questions!",
    ],

    # short greetings
    "hello": [
        "Hello! What would you like to know about table manners?",
        "Hey there! Ask me a question if you're curious about dining etiquette!",
    ],
    "hi": [
        "Hi! Ask me anything about table manners!",
        "Hey! Ask me any questions about dining etiquette!",
    ],
    "hey": [
        "Hey! Ask me something if you want to talk about table manners!",
        "Hey there! Ask me a question if you're curious about dining etiquette!",
    ],
    "howdy": [
        "Howdy! Ask me something if you want table manners tips!",
        "Howdy partner! Ask me a question if you're curious about dining etiquette!",
    ],
    "greetings": [
        "Greetings! Ask me any table manners questions.",
        "Greetings! Ask me anything about dining etiquette!",
    ],
    "sup": [
        "Not much! Ask me something if you want to talk about table manners!",
        "Sup! Ask me a question if you're curious about dining etiquette!",
    ],
    "wassup": [
        "Wassup! What do you want to ask me about table etiquette?",
        "Wassup! Any questions about proper dining behavior?",
    ],
    "morning": [
        "Morning! Ask me about table manners!",
        "Morning! What would you like to know about dining etiquette?",
    ],
    "afternoon": [
        "Afternoon! Ask me a question if you're curious about proper table manners!",
        "Good afternoon! Any questions about dining etiquette?",
    ],
    "evening": [
        "Evening! What do you want to ask me about table manners?",
        "Good evening! Ask me about proper dining etiquette.",
    ],

    # thanks / appreciation
    "thank you": [
        "You're welcome! Ask me any questions about table manners!",
        "No problem at all! What would you like to ask me about dining etiquette?",
    ],
    "thanks": [
        "Anytime! What do you want to ask me about proper table manners?",
        "You got it! Ask me anything about table etiquette!",
    ],
    "thank u": [
        "You're welcome! Do you want some table manners tips?",
        "Happy to help! Any questions about proper dining etiquette?",
    ],
    "thx": [
        "No worries! Ask me about table etiquette.",
        "Anytime! What do you want to ask about proper dining manners?",
    ],
    "much appreciated": [
        "Of course! What do you want to learn about table manners tips?",
        "Glad I could help! Any questions about proper dining etiquette?",
    ],

    # farewells
    "good night": [
        "Good night! Remember your table manners for tomorrow!",
        "Night!",
    ],
    "goodbye": [
        "Goodbye! Hope you practice your table manners!",
        "Take care — and remember proper dining etiquette!",
    ],
    "bye": [
        "Bye! Keep those table manners in mind!",
        "See ya!",
    ],
    "see ya": [
        "See ya! Hope you remember proper table manners!",
        "Catch you later!",
    ],
    "see you": [
        "See you soon! Keep your table manners sharp!",
        "Until next time!",
    ],
    "take care": [
        "You too — and remember your table manners!",
        "Take care!",
    ],
    "later": [
        "Later! Keep those table manners in mind!",
        "Catch you later!",
    ],
    "catch you later": [
        "Catch you later!",
        "See you next time! Remember proper dining etiquette!",
    ],
    "farewell": [
        "Farewell! Keep your table manners sharp!",
        "Until we meet again!",
    ],
    "have a good day": [
        "You too — and remember proper table manners!",
        "Thanks!",
    ],
    "have a nice day": [
        "You too!",
        "Thanks!",
    ]
}

    # Gesture-questions (social questions that = greetings) - AI Generated Dictionary
    gestureQuestions = {
    "how are you": [
        "I am doing well, thank you! What would you like to know about table manners?",
        "Doing fine, thanks! Are you curious about any table etiquette tips?",
        "All good here! Ask me questions about proper table manners!"
    ],
    "how are you doing": [
        "I’m doing well, thank you! What can I tell you about table etiquette?",
        "Doing great! Would you like some tips on table manners?",
        "All good! Are there any table etiquette questions you have?"
    ],
    "how's it going": [
        "It’s going well, thanks! What would you like to know about dining etiquette?",
        "Pretty good! Ask me questions about table manners?",
        "All good! Ask me about some tips on proper table etiquette."
    ],
    "hows it going": [
        "It’s going well, thank you! What would you like to learn about table manners?",
        "Pretty good! Any table etiquette questions I can help with?",
        "All good here! Ask me a question if you're curious about dining etiquette!"
    ],
    "how have you been": [
        "I’ve been well, thank you! What would you like to know about table manners?",
        "Doing fine! Do you want some tips on dining etiquette?",
        "All good! Are there any table manners questions you have?"
    ],
    "what's up": [
        "Not much! Would you like to talk about table manners?",
        "Just here to help! Ask me any questions about dining etiquette.",
        "All good! Ask me a question if you're curious about proper table manners!"
    ],
    "whats up": [
        "Not much! What would you like to know about table manners?",
        "Just here to chat! Any questions about dining etiquette?",
        "All good! Ask me about proper table manners."
    ],
    "sup": [
        "Sup! What do you want to ask me about table manners?",
        "Hey! Ask me questions about proper dining etiquette!",
        "All good! Ask me a question if you're curious about proper table manners!"
    ],
    "howdy": [
        "Howdy! What would you like to know about table manners?",
        "Hey there! Ask me questions about dining etiquette!",
        "Howdy! Ask me about proper table manners."
    ],
    "you good": [
        "I’m good, thank you! Ask me questions about table etiquette.",
        "All good here! What would you like to know about table manners?",
        "Doing well! Ask me a question if you're curious about dining etiquette!"
    ],
    "everything alright": [
        "Everything’s fine, thank you! What would you like to know about table manners?",
        "All good! Ask me any questions about proper dining etiquette!",
        "Everything’s great! Ask me about learning table manners tips?"
    ],
    "everything okay": [
        "Yes, all okay! What would you like to know about table manners?",
        "All good! Curious about proper table etiquette?",
        "Everything’s fine! Ask me questions about table manners."
    ]}

    # clean up
    text = entry.lower().strip()

    # ---> special-case: gesture-questions --- When a gesture LOOKS like a question
    for gq in gestureQuestions.keys():
        if text.startswith(gq):
            if gestureQuestions[gq]:
                return 1, random.choice(gestureQuestions[gq])   # gesture and its response
            else:
                return 1, None


    # ---> question detection ---
    if isQuestion(text):
        return 2, None  # question


    # ---> gesture detection ---
    for g in sorted(gestureResponses.keys(), key=len, reverse=True):
        if g in text:
            if gestureResponses[g]:
                return 1, random.choice(gestureResponses[g])  # gesture
            else:
                return 1, None

    # ---> If it isn't a question or gesture blatantly, its new info!
    return 3, None  # statement / info

def isQuestion(text): #part of entryType functionality
    # ends with ?
    if text.endswith("?"):
        return True

    # WH question at start
    if re.match(r"^\s*(what|when|where|why|who|how)\b", text):
        return True

    # models like "can you", "should I", etc.
    model_patterns = [
        r"\bcan you\b", r"\bcould you\b", r"\bwould you\b",
        r"\bshould i\b", r"\bis it\b", r"\bare you\b",
        r"\bdo you\b", r"\bdoes it\b", r"\bdid you\b",
        r"\bwill you\b", r"\bwould it\b", r"\bshould it\b"
    ]

    for pat in model_patterns:
        if re.search(pat, text):
            return True

    return False

def answerQuestion(userQword, userQKeyW, isFollowUp):  #Takes the user's question and finds best answer.
    global previousKeyWords
    bestAnswer = None #this will store the best response
    bestScore = 0 #this is the way we will keep track of which response has the best score
    for i in infoBest:  #Format of i [answer, keywords, qwords]
        score = 0 #each response has a starting score of 0
        matches = 0
        
        if userQword in i[2]:
            score += 1 #bonus point for question-word being in there

        for q in userQKeyW:
            isMatch = any(q in kw or kw in q for kw in i[1]) #if there is a match at all
            if isMatch:
                if q not in wordLib:#if the key word isn't in known library of key words, will ignore and lower the score
                    score -= 0.3
                    continue 
                matches += 1 #counts it as another match
                weight = 1 + (total / wordLib[q]) ** 0.5
                score += weight
            else:
                score -= 0.3
        if userQKeyW: #added weight for multiple matches
                score += (matches / len(userQKeyW)) * 2

        if score > bestScore:
            bestScore = score #replace the best score with the new high score
            bestAnswer = i[0] #stores this response as the new best one
            if not isFollowUp:
                previousKeyWords = i[1]
            else:
                previousKeyWords = []
    if bestScore < 1:
        bestAnswer = "Sorry, I don't know the answer to that! \nTry asking me something about table manners or dining etiquette!"
    if bestAnswer:
        return bestAnswer
    
def answerInfo(userSentence, infoKeyWords, infoBest):
    sentence_to_add = ""
    qw = findLikelyQWords(userSentence)
    sentence_to_add = f"{userSentence}|{infoKeyWords}|{qw}\n"
    with open("cleanedInfo.txt", 'a') as ourData:
        ourData.write(sentence_to_add)
    infoBest.append([userSentence, infoKeyWords, qw])
    for w in infoKeyWords:
        if w in wordLib:
            wordLib[w] += 1
        else:
            wordLib[w] = 1
    return "I learned something new! I'll remember that."

def changeAnswer(reps): #Gets a prefix for the answer to give variety if user keeps asking same question.
    reps = (reps - 1) % 5
    prefixes = [
        "No worries if you missed it the first time, here it is again. ",
        "Alright, let’s revisit that question. ", 
        "Of course, happy to explain it again. ", 
        "No problem at all; let’s take another look. ", 
        "Sure thing! Here's the answer once more. "
    ]
    return prefixes[reps]

def makePolite(userSentence):   #Takes a sentence. Looks for courtesy words and adds it to the response.
    courtesies = {
        "please": "Certainly.",
        "excuse me": "Of course.",
        "pardon me": "No problem.",
        "would you mind": "I’d be happy to.",
        "could you please": "Sure.",
        "would you please": "Absolutely.",
        "may i ask": "Allow me to explain.",
        "i was wondering": "Let me see.",
        "do you think you could": "I’d be glad to help.",
        "if you don't mind": "Does this answer your question?",
        "if possible": "Happy to clarify further.",
        "thank you": "You're welcome.",
        "thanks": "My pleasure.",
        "much appreciated": "I appreciate your question."
    }
    userSentence = userSentence.lower().split() #Make list of words in the sentence 
    beginningEnd = " ".join(userSentence[:4]) + " ".join(userSentence[-4:]) # Get the first 5 and last 4
    for c in courtesies.keys():     #Checks to see if user used a courtesy word. If so, returns a response.
        if c in beginningEnd:
            return courtesies[c] + " "

def mainFunction(question):
    global previousQuestion
    global submitted
    global timesRepeated
    global errorFound
    global msg
    isFollowUp = False
   
    error, corrected = spellCheckQuestion(question)
    if error:
        errorFound = True
        bot_response(f"Pardon me, but did you mean '{corrected}'? [Y/N]")
        root.wait_variable(submitted)
        submitted.set(False)
        correctedResponse = msg.lower()
        if correctedResponse == 'y':
            bot_response("Glad I could catch that for you! I shall answer your question promptly.")
            question = corrected
        elif correctedResponse == 'n':
            bot_response("My apologies! I shall answer your question promptly.")
        else:
            bot_response("Well, you made a typo once. I take that as a yes.")
            question = corrected

    MsMannersAnswer = ""

    statementType, response = entryType(question) # ---> new implemented function with type and response returned
    qWord = findQWord(question) #gets the question-word
    qKeyWords = findKeyWords(question) #gets a list of key words

    pronouns = ["it", "them", "that", "those", "this", "these", "he", "she", "they"]

    if (any(p in qKeyWords for p in pronouns) or len(qKeyWords) < 2) and statementType == 2:
        qKeyWords += [w for w in previousKeyWords if w not in qKeyWords]
        isFollowUp = True
    #AI property 6: Handle user asking same question again
    if [qWord] + qKeyWords == previousQuestion and statementType != 1:  #Combines the qWord and Key words then compares
        timesRepeated += 1
        MsMannersAnswer += changeAnswer(timesRepeated)
    else:   #Reset data tracking variable
        timesRepeated = 0
    previousQuestion = [qWord] + qKeyWords #Records question

    if statementType == 1:  #If it thinks it is a gesture, gets an answer.
        if response: # ---> uses the response from entryType()
            MsMannersAnswer += response
        else:
            MsMannersAnswer += "Ask me anything about table manners! I'd love to help!" # ---> If it gets gesture but doesn't know how to answer, does this default.
    elif statementType == 2:    #If it thinks it's a question
        MsMannersAnswer += answerQuestion(qWord, qKeyWords, isFollowUp)
        #AI property 2: adds an additional response to sentences with thoughtful/polite phrases
        politeWord = makePolite(question)
        if politeWord:
            MsMannersAnswer = politeWord + MsMannersAnswer
    elif statementType == 3:    #If thinks new information
        MsMannersAnswer += answerInfo(question, qKeyWords, infoBest)

    if MsMannersAnswer: 
        bot_response(capitalizes(MsMannersAnswer))
    else:
        bot_response("I'm sorry, I don't know the answer.")

# ---> GUI Functions

def send_message(event=None):
    global submitted
    global errorFound
    global msg
    msg = my_message.get()
    submitted.set(True)
    if msg.strip() != "":
        chat_window.insert(END, "User>> " + msg + "\n\n")
        my_message.set("")
        if not errorFound:
            mainFunction(msg)
        else:
            errorFound = False
    else:
        bot_response("Oops! You didn't say anything to me!")


def bot_response(response):
    chat_window.insert(END, "Ms. Manners>> " + response + "\n\n")

############################################## SETUP ######################################################

#AI Generated List
stopWords = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
    "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
]
negative_words = ["no", "never", "not", "none", "nothing", "nowhere", "neither", "cannot", "under no circumstances", "without"]
wordLib = {} # Keeps track of word count 
with open("cleanedInfo.txt", 'r', encoding='utf-8') as file:
    info = file.read()

info = info[:-1] #removes the last \n that always shows up (it causes a weird error sometimes)
lines = info.split('\n')
infoBest = []
for l in lines:
    details = l.split('|')
    
    if len(details) < 3: #ensures all sentences have key words and question words stored
        continue
    
    answer = details[0]
    keywords = parse_list_string(details[1])
    qwords = parse_list_string(details[2])

    infoBest.append([answer, keywords, qwords])

for i in infoBest: #Does wordcount
    for word in i[1]:
        if word in wordLib:
            wordLib[word] += 1
        else:
            wordLib[word] = 1
total = 0
for k, v in wordLib.items():
    total += v

question = ""
previousQuestion = []    #Just stores the keywords and question word from the previous Q
previousKeyWords = []   # Just stores the keywords
timesRepeated = 0
errorFound = False
msg = ""

# --------------GUI-SETUP--------------------------------------
root = tb.Window(themename="darkly")
root.title("Ms. Manners")
root.geometry("690x635")

submitted = BooleanVar(value=False)

chat_window = ScrolledText(root, width=60, height=20, wrap=WORD, autohide=True, bootstyle="info", font=('Verdana', 15))
chat_window.grid(row=0, column=0, columnspan=2, padx=15, pady=15)

my_message = tb.StringVar()
entry_field = tb.Entry(root, textvariable=my_message, width= 48, bootstyle="info", font=('Verdana', 15))
entry_field.grid(row=1, column=0)
entry_field.bind("<Return>", send_message)

send_button = tb.Button(root, text="Send", command=send_message, width=6, bootstyle="outline")
send_button.grid(row=1, column=1)

initial_response = "Hi! I am Ms. Manners. Ask me anything about TABLE MANNERS and I hope to answer your question!"

root.after(500, bot_response(initial_response))

root.mainloop()
