Ms. Manners was a joint project with my classmate Joe Hakanson, Saint Mary's University of MN, 2025

MS. MANNERS – AI TABLE MANNERS CHATBOT
A Python-based etiquette assistant with learning, typo correction, and a graphical interface.

OVERVIEW

Ms. Manners is a Python chatbot that answers questions about table manners and dining etiquette.
It uses a structured knowledge base, typo correction, memory, and automatic learning to provide natural responses.
A Tkinter + ttkbootstrap GUI is used for chatting with the bot.

HOW THE KNOWLEDGE SYSTEM WORKS

The chatbot uses the data file:

cleanedInfo.txt — structured knowledge the bot uses internally

This is created from the following file:

info.txt — raw etiquette information

The script dataFormater.py converts info.txt into cleanedInfo.txt, but only needs to run if cleanedInfo.txt is missing or outdated.

Each entry in cleanedInfo.txt follows this format:

sentence | [keywords] | [question_words]

INSTALLATION

Required packages:

pip install pyspellchecker
pip install ttkbootstrap


Make sure cleanedInfo.txt is present or run dataFormater.py to generate it.

RUNNING THE CHATBOT

Start Ms. Manners by running:

python "chatbot_main.py"


This opens the GUI and displays an initial greeting.

KEY FEATURES

Typo Detection
Detects likely spelling errors in the user’s message and asks for confirmation before answering.

Message Classification
Determines whether the input is a greeting, gesture-question, real question, or new information.

Follow-Up Memory
If the user asks a vague follow-up question (using pronouns or too few keywords), the bot reuses keywords from the previous question.

Repeated Question Handling
If the same question is asked again, the bot recognizes it and adds a varied reminder phrase before answering again.

Politeness Recognition
Detects polite phrases (such as “please” or “excuse me”) and adds an appropriate polite introduction to the response.

Automatic Learning
When the user provides new etiquette information, the bot extracts keywords, predicts question types, and stores it in cleanedInfo.txt.

Clean, Capitalized Output

Automatically fixes capitalization and proper-noun formatting to keep answers polished.


