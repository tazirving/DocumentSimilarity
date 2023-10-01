from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import Prac2
#Librerias para la interfaz
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MesBox
from tkinter import filedialog
import pandas as pd


    #Generar las tres representaciones vectoriales

def repVectFrecuencia(corpus):
     #Frecuencia
    vectorizador_frecuencia = CountVectorizer(token_pattern=r'(?u)\w\w+|\.')
    X_frecuencia = vectorizador_frecuencia.fit_transform(corpus)
    vector_frec = vectorizador_frecuencia.get_feature_names_out()
    return vectorizador_frecuencia,vector_frec,X_frecuencia

def repVectTf(corpus):
     #Tf-idf
    vectorizador_tf = TfidfVectorizer(token_pattern=r'(?u)\w\w+|\.')
    X_tf = vectorizador_tf.fit_transform(corpus)
    vector_td = vectorizador_tf.get_feature_names_out()
    return vectorizador_tf,X_tf,vector_td

def repVectBi(corpus):
    #Binaria
    vectorizador_binario = CountVectorizer(binary=True,token_pattern=r'(?u)\w\w+|\.')
    X_binario = vectorizador_binario.fit_transform(corpus)
    vector_bi = vectorizador_binario.get_feature_names_out()
    return vectorizador_binario,vector_bi,X_binario

#Función de la interfaz
def clkAccept():
        #Se busca el archivo a cifrar
        file = filedialog.askopenfilename(filetypes=[("Text file", "*.txt"), ("All the files", "*.*")])
        fileNor=Prac2.corpusNormalizado(file)
        with open(fileNor, 'r', encoding='utf-8') as txt_testfile:
                test_corpus = txt_testfile.readlines()
        print(test_corpus)
        rep = com_rep.current() #Obtiene el tipo de representación elegida por el usuario

        if rep < 0:
                 MesBox.showerror(title='Error!', message='You must select a representation mode.') #Mensaje de error
        elif rep == 0: #Representación binaria
                print("Se escogio la representación 'Binaria'")#Esta linea se puede borrar solo es demostrativa
                #Agrega aquí el código para la representación binaria 
                vectorizador_biTC,vector_biTC,X_binarioTC=repVectBi(test_corpus) #Representacion Binaria del texto de prueba


                
        elif rep == 1: #Representación de frecuencia
                print("Se escogio la representación 'Frecuencia'")#Esta linea se puede borrar solo es demostrativa
                #Agrega aquí el código para la representación Frecuencia 
                vectorizador_frecTC,vector_frecTC,X_frecuenciaTC=repVectFrecuencia(corpus) #Representacion frecuencia del texto de prueba

        else:
                print("Se escogio la representación 'Tf-idf'")#Esta linea se puede borrar solo es demostrativa
                #Agrega aquí el código para la representación Tf-idf 
                
                vectorizador_tfTC,X_tfTC,vector_tdTC=repVectTf(corpus) #Representacion tf-idf del texto de prueba

#Cargando el corpus
with open("noticias_nuevo_corpus_2.txt", "r", encoding='utf-8') as txt_file:
        corpus = txt_file.readlines()

#Generar las tres representaciones vectoriales de noticias_nuevo_corpus
vectorizador_biC,vector_biC,X_binarioC=repVectBi(corpus)
vectorizador_frecC,vector_frecC,X_frecuenciaC=repVectFrecuencia(corpus)
vectorizador_tfC,X_tfC,vector_tdC=repVectTf(corpus)

#Interfaz
root = tk.Tk()
root.title("P3: Document Similarity") #Titulo de la ventana
main_Frame = Frame(root)
main_Frame.grid()
main_Frame.config(width=300, height=200) #Dimesiones de la ventana

welcomeLabel = Label(root, text='Welcome!') #Mensaje de bienvenida
welcomeLabel.place(x=105, y=30, width=90, height=20) #Dimensiones del Label de bienvenida
welcomeLabel.config(font=('Arial',14))

keyLabel = Label(root, text='Representation:')#Leyenda
keyLabel.place(x=20, y=90) 
rep = ['Binary', 'Frequency', 'Tf-idf'] #Tipo de representación
com_rep = ttk.Combobox(root, values=rep, width=15) #Lista despegable
com_rep.place(x=120, y=90)
com_rep['values']=rep

btnAccept = tk.Button(text='Accept', command=clkAccept) #Botón de busqueda
btnAccept.place(x=120, y=130, width=60, height=25)#Dimesiones y posición del botón

root.mainloop() #Mantiene la ventana abierta para interactuar con ella