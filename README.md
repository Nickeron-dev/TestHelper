# TestHelper
This project helps to divide test questions between other people for faster test completion.

# Motivation
We sometimes have tests on Classtime.com. There was a feature to check whether an answer 
was correct or not. But some time ago they have fixed it. 

I complete my tests with two my friends. That's why I came up with an idea to create a test helper. Firstly this project will
parse a question page and take the question. Then the program sends it to the Google Drive API(each user has his own
file with questions). From there the project takes all of them and writes to the Telegram API(Name, questions ...). Also, 
it checks if any of questions was repeated, it outputs a warning, so you can ask you friend who faced it for the answer.
In addition, this project copies the question in buffer and opens a blank google page for maximum speed.

# Technologies
* Python
* Google Drive API
* Telegram Bot API
* Pyperclip
* Python Requests

# How to use
Install all used libraries/technologies from the 'Technologies' list.
Create an appliction with Google Drive API console.cloud.google.com/apis (Google Cloud Platform). Add a user for each user 
and one more for Questions Manager. Generate a token.json file for each of the of them. 
(Find info on topic: How to create applications with Google Drive API).
Firstly you run allQuestionsManager/main.py program on one of the computers. It checks all files 
with questions and manages the messages in Telegram.
After that, each user(3 max) runs one of 3 TakeQuestion.../main.py   (1 program for 1 user).
