import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json

with open("chats.json") as file:
    data = json.load(file)
    
words = []
labels = []
docs_x = []
docs_y = []

for chat in data["chats"]:
    for pattern in chat["prompt"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(chat["tag"])
        
    if chat["tag"] not in labels:
        labels.append(chat["tag"])
        
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    
    wrds = [stemmer.stem(w) for w in doc]
    
    for w in words:
        if w in wrds:
            if w in words:
                bag.append(1)
            else:
                bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    
    training.append(bag)
    output.append(output_row)
    
training = np.array(training)
output = np.array(output)

tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn. regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")