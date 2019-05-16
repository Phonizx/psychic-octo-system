import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf 
import numpy as np 
import json 

pre_embed =[]


def string_to_num_list(l):
    ln=[]
    for c in l:
        ln.append(float(c))
    return ln

with open("dict.json") as diz:
    dictz = json.load(diz)

    for k, v in dictz.items():
        tmp=string_to_num_list(list(str(v).replace('.','').replace('-','')))
        pre_embed.append(tmp)

print(pre_embed)

vocab_size = 10 
vocab_embed_dim = 7


embed_shape = [vocab_size, vocab_embed_dim]
embed_placeholder = tf.placeholder(tf.float32, embed_shape)
word_embed = tf.get_variable('word_embeddings', embed_shape, trainable=False)

embed_init_op = word_embed.assign(embed_placeholder)


with tf.Session() as sess:
    sess.run(embed_init_op, feed_dict={embed_placeholder: pre_embed})
