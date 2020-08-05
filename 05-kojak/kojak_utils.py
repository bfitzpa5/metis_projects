# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:10:05 2020

@author: Brendan Non-Admin
"""

import os
import datetime as dt
import codecs
import unicodedata
from keras.models import Sequential
from keras.layers import Dense,LSTM,Embedding
from keras.preprocessing.sequence import pad_sequences

def read_book_texts():
    datapath = os.path.join('Data', 'BookTXTs')

    os.listdir(datapath)
    
    book_filenames = [
        'philosophers_stone.txt',
        # 'chamber_of_secrets.txt',
        #'prisoner_of_azkaban.txt',
        # 'goblet_of_fire.txt',
        # 'order_of_the_phoenix.txt',
        # 'half_blood_prince.txt',
        #'deathly_hallows.txt',
    ]
    
    books = list()
    for book_filename in book_filenames:
        filepath = os.path.join(datapath, book_filename)
            
        with codecs.open(filepath, 'r', encoding='utf-8', errors="ignore") as f:
            book_text = unicodedata.normalize("NFKD", f.read())
        books.append(book_text)
    
    book_text = ''.join(books)
    
    #if len(book_text) != 6244250:
    #    raise ValueError("Book Texts Not Properly Read In")
    
    return book_text

def separate_punc(tokens):
    punc_tokens = '\n\n \n\n\n!"-#$%&()--.*+,-/:;<=>?@[\\]^_`{|}~\t\n '
    return [token.text.lower() for token in tokens if token.text not in punc_tokens]

def create_text_sequences(tokens, train_len):
    # Empty list of sequences
    text_sequences = []
    
    for i in range(train_len, len(tokens)):
        
        # Grab train_len# amount of characters
        seq = tokens[i-train_len:i]
        
        # Add to list of sequences
        text_sequences.append(seq)
    return text_sequences

def initalize_model(vocabulary_size, seq_len):
    model = Sequential()
    model.add(Embedding(vocabulary_size, 25, input_length=seq_len))
    model.add(LSTM(150, return_sequences=True))
    model.add(LSTM(150))
    model.add(Dense(150, activation='relu'))
    model.add(Dense(vocabulary_size, activation='softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
   
    model.summary()
    
    return model

def seconds_factorization(duration):
    days, remainder = divmod(duration, (24 * 60**2))
    hours, remainder = divmod(remainder , (60**2))
    minutes, seconds = divmod(remainder, (60**1))
    return days, hours, minutes, seconds

def time_to_iso(t):
    return dt.datetime.fromtimestamp(t).isoformat(timespec='minutes')

def generate_text(model, tokenizer, seq_len, seed_text, num_gen_words):
    '''
    INPUTS:
    model : model that was trained on text data
    tokenizer : tokenizer that was fit on text data
    seq_len : length of training sequence
    seed_text : raw string text to serve as the seed
    num_gen_words : number of words to be generated by model
    '''
    
    # Final Output
    output_text = []
    
    # Intial Seed Sequence
    input_text = seed_text
    
    # Create num_gen_words
    for i in range(num_gen_words):
        
        # Take the input text string and encode it to a sequence
        encoded_text = tokenizer.texts_to_sequences([input_text])[0]
        
        # Pad sequences to our trained rate (50 words in the video)
        pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
        
        # Predict Class Probabilities for each word
        pred_word_ind = model.predict_classes(pad_encoded, verbose=0)[0]
        
        # Grab word
        pred_word = tokenizer.index_word[pred_word_ind] 
        
        # Update the sequence of input text (shifting one over with the new word)
        input_text += ' ' + pred_word
        
        output_text.append(pred_word)
        
    # Make it look like a sentence.
    return ' '.join(output_text)


# epoch_25 ended at 12:34
hours = 300 * 3 / 60
25*3
# started at about 11:15