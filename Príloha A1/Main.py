# from the tkinter library
from tkinter import *
  
# import filedialog module
from tkinter import filedialog
import re
import nltk
import heapq
import deepl
from google.cloud import translate_v2 as translate
import os
# importing required modules
import httpx 

translate_client = translate.Client()
DeepLtranslator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

def browseFilesDeepL():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Pdf files",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*")))
    
    files = {'pdf': open(filename, 'rb')}

    headers={'access_token': "1234567asdfgh"}

    url='http://localhost:81/v2/pdf_file'

    response = httpx.post(url=url, files=files, headers=headers,timeout=10000)

    label_file_explorer.configure(text="File Opened: "+filename)        
    
    raw_text = re.sub(r'\[[0-9]*\]', ' ',response.text)  
    raw_text = re.sub(r'\s+', ' ', raw_text)

    formatted_article_text = re.sub('[^\.\,a-zA-Z\\u0080-\\u017F]', ' ', raw_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    ENG_text = DeepLtranslator.translate_text([formatted_article_text], target_lang="EN-GB") #DeepL translate

    sentence_list = nltk.sent_tokenize(ENG_text[0].text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(ENG_text[0].text):
        if word not in stopwords and word != '.' and word != ',':
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30 and len(sent.split(' ')) > 4:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    summary=DeepLtranslator.translate_text([summary], target_lang="SK")
    Output.delete("1.0", END)
    Output.insert(END,summary)


def browseFilesGT1():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Pdf files",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*")))

        # creating a pdf file object
    files = {'pdf': open(filename, 'rb')}

    headers={'access_token': "1234567asdfgh"}

    url='http://localhost:81/v2/pdf_file'

    response = httpx.post(url=url, files=files, headers=headers,timeout=10000)
    
    # Change label contents  
    label_file_explorer.configure(text="File Opened: "+filename)        
    
    raw_text = re.sub(r'\[[0-9]*\]', ' ',response.text)  
    raw_text = re.sub(r'\s+', ' ', raw_text)

    formatted_article_text = re.sub('[^\.\,a-zA-Z\\u0080-\\u017F]', ' ', raw_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

      
    
    ENG_text = translate_client.translate(formatted_article_text, target_language='en',source_language='sk') 

    sentence_list = nltk.sent_tokenize(ENG_text["translatedText"])

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(ENG_text["translatedText"]):
        if word not in stopwords and word != '.' and word != ',':
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30 and len(sent.split(' ')) > 4:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    summary=translate_client.translate(summary, target_language='sk',source_language='en')
    Output.delete("1.0", END)
    Output.insert(END,summary["translatedText"])


root = Tk()
root.geometry("1920x1080")
root.title(" Text Sumarization ")

# Create a File Explorer label
label_file_explorer = Label(root,
                            text = "File Explorer",
                            width = 100, height = 4,
                            fg = "blue")
      
Output = Text(root, height = 50,
			width = 200,
			bg = "light cyan")

button_explore_deepl = Button(root,
                        text = "Sumarization using DeepL",
                        command = browseFilesDeepL)

button_explore_GT1 = Button(root,
                        text = "Sumarization using Google translate",
                        command = browseFilesGT1)

button_exit = Button(root,
                     text = "Exit",
                     command = exit)

Output = Text(wrap=WORD)
Output.pack()
label_file_explorer.pack()
button_explore_deepl.pack()
button_explore_GT1.pack()
button_exit.pack()

root.mainloop()
