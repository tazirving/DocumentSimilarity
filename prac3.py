from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re

#Cargando el corpus
with open("noticias_nuevo_corpus_2.txt", "r") as txt_file:
        corpus = txt_file.readlines()

#Generar las tres representaciones vectoriales

#Binaria
vectorizador_binario = CountVectorizer(binary=True,token_pattern=r'(?u)\w\w+|\.')
X_binario = vectorizador_binario.fit_transform(corpus)
vector_bi = vectorizador_binario.get_feature_names_out()
#Frecuencia
vectorizador_frecuencia = CountVectorizer(token_pattern=r'(?u)\w\w+|\.')
X_frecuencia = vectorizador_frecuencia.fit_transform(corpus)
vector_frec = vectorizador_frecuencia.get_feature_names_out()
#Tf-idf
vectorizador_tf = TfidfVectorizer(token_pattern=r'(?u)\w\w+|\.')
X_tf = vectorizador_tf.fit_transform(corpus)
vector_td = vectorizador_tf.get_feature_names_out()