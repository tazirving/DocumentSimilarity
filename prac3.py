from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import prac2
#Librerias para la interfaz
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MesBox
from tkinter import filedialog
import pandas as pd

#Cargando el corpus
with open("noticias_nuevo_corpus_2.txt", "r", encoding='utf-8') as txt_file:
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

    
# Función de comparación utilizando coseno
def cal_similarity(a, b):
    similarity_scores = cosine_similarity(a, b)
    # Se invierte el vector [::-1] ya que el ordenamiento argsort lo hace de menor a mayor (en este caso similitud)
    most_similar_id = np.argsort(similarity_scores[:,-1])[::-1][:10]
    most_similar_values = similarity_scores[:, -1][most_similar_id]
    return most_similar_id, most_similar_values

def show_results(a_list, b_list):
    idx_list, val_list = a_list, b_list
    
    # Limpia el resultado anterior si lo hubiera
    if hasattr(show_results, "result_label"):
        show_results.result_label.destroy()
    
    # Crea una etiqueta de texto para mostrar los resultados
    result_text = "Posición\tValor Función Coseno\n"
    for idx, value in zip(idx_list, val_list):
        formatted_value = "{:.10f}".format(value)  # Formatea a 2 decimales
        result_text += f"{idx}\t{formatted_value}\n"
    
    show_results.result_label = Label(root, text=result_text)
    show_results.result_label.place(x=20, y=170)
    show_results.result_label.config(font=("Arial", 12))

#Función de la interfaz
def clkPick():
    global X_binario, X_frecuencia, X_tf
    global vectorizador_binario, vectorizador_frecuencia, vectorizador_tf
    #Se busca el archivo 
    file = filedialog.askopenfilename(filetypes=[("Text file", "*.txt"), ("All the files", "*.*")])
    fileNor=prac2.corpusNormalizado(file)
    with open(fileNor, 'r', encoding='utf-8') as txt_testfile:
            test_corpus = txt_testfile.readlines()
    print(test_corpus)
    rep = com_rep.current() #Obtiene el tipo de representación elegida por el usuario

    if rep < 0:
            MesBox.showerror(title='Error!', message='You must select a representation mode.') #Mensaje de error
    elif rep == 0: #Representación binaria
            print("Se escogio la representación 'Binaria'")
            #Agrega aquí el código para la representación binaria 
            Y_binario = vectorizador_binario.transform(test_corpus)
            vector_bi = vectorizador_binario.get_feature_names_out()# NO SE UTILIZA
            """
            # Solo para verificar que está tomando las matrices
            print("Corpus(Train)", X_binario.shape[0], X_binario.shape[1])
            print("Doc(Test)", Y_binario.shape[0], Y_binario.shape[1])
            """
            # Casting a Dense Arrays
            da1 = X_binario.toarray()
            da2 = Y_binario.toarray()
            # Ejecutando la función para calcular similaridad
            idx_list, val_list = cal_similarity(da1, da2)
    elif rep == 1: #Representación de frecuencia
            print("Se escogio la representación 'Frecuencia'")
            #Agrega aquí el código para la representación Frecuencia 
            Y_frecuencia = vectorizador_frecuencia.transform(test_corpus)
            vector_frec = vectorizador_frecuencia.get_feature_names_out() # NO SE UTILIZA
            # Casting a Dense Arrays
            da1 = X_frecuencia.toarray()
            da2 = Y_frecuencia.toarray()
            # Ejecutando la función para calcular similaridad
            idx_list, val_list = cal_similarity(da1, da2)
            
    else:
            print("Se escogio la representación 'Tf-idf'")#Esta linea se puede borrar solo es demostrativa
            #Agrega aquí el código para la representación Tf-idf 
            Y_tf = vectorizador_tf.transform(test_corpus)
            vector_td = vectorizador_tf.get_feature_names_out() # NO SE UTILIZA
            idx_list = cal_similarity(X_tf, Y_tf)
            # Casting a Dense Arrays
            da1 = X_tf.toarray()
            da2 = Y_tf.toarray()
            # Ejecutando la función para calcular similaridad
            idx_list, val_list = cal_similarity(da1, da2)
    
    #Resultados en Consola
    print("")
    print("Posición\tValor de la Función Coseno") # Títulos de las columnas
    # Imprime la lista de los 10 más similares (posición, valor)
    for idx, value in zip(idx_list, val_list):
        print(f"{idx}\t\t\t{value}")
   # Imprime el contenido de los 10 documentos en ese orden
    print("")
    for idx in idx_list:
        print(corpus[idx])
        
    show_results(idx_list, val_list)
    
#Interfaz
root = tk.Tk()
root.title("P3: Document Similarity") #Titulo de la ventana
main_Frame = Frame(root)
main_Frame.grid()
main_Frame.config(width=300, height=420) #Dimesiones de la ventana

welcomeLabel = Label(root, text='Welcome!') #Mensaje de bienvenida
welcomeLabel.place(x=105, y=30, width=90, height=20) #Dimensiones del Label de bienvenida
welcomeLabel.config(font=('Arial',14))

keyLabel = Label(root, text='Representation:')#Leyenda
keyLabel.place(x=20, y=90) 
rep = ['Binary', 'Frequency', 'Tf-idf'] #Tipo de representación
com_rep = ttk.Combobox(root, values=rep, width=15) #Lista despegable
com_rep.place(x=120, y=90)
com_rep['values']=rep

btnAccept = tk.Button(text='Pick a Document', command=clkPick, bg='#79D0F0') #Botón de busqueda
btnAccept.place(x=80, y=130, width=120, height=25)#Dimesiones y posición del botón

root.mainloop() #Mantiene la ventana abierta para interactuar con ella