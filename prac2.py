import re
import spacy
import sys
from spacy.tokenizer import Tokenizer
from spacy.util import compile_suffix_regex


def custom_tokenizer(nlp):
    prefix_re = re.compile(r'^[\–\—\.\$\,\?\:\;\‘\’\`\“\”\"\'\[~\¡«()¿\_\…\*-]|^\d{1,}$|^@\w+$]')
    infix_re = re.compile(r'[~\,\”\“\]\;\…|\?$|^\¿\/\(\.]|\&{1}[a-z\u00C0-\u017F]+|\-|\—')
    # infix_re = re.compile(r'[~\,\”\“\]\;\…|\?$|^\¿\/\(\.]|[A-Z]{1}[a-z\u00C0-\u017F]+\d?$|\&{1}[a-z\u00C0-\u017F]+|\-|\—')
    # infix_re = re.compile(r'[-~\,\_\”\“\]\;…|\?$|^\¿\/\(\—\.]|[^*][A-Z]{1}[a-z\u00C0-\u017F]+\d?$|\&{1}[a-z\u00C0-\u017F]+|\–|\´')
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    simple_url_re = re.compile(r'''^https?://|pic.twitter.com/\w|\w+\.com/?|www\.?\w+\.?\w+\.?\w+|twitter.com/\w''')
    usuario_underscore = re.compile(r'@\w+_$|^@\w+$|(\.{3}$)|\d{1,}\,{0,}\d{0,}\.{1}\d+\%?$|\#\w+$|[A-Z]{1}\.{1}[A-Z]{1}\.?$|\w+\*\w+|\w+\-\w+')

    

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=usuario_underscore.match,
                                url_match=simple_url_re.match)


def corpusNormalizado(nombre_corpus):        
    #Leyendo el archivo de texto
    with open(nombre_corpus, "r") as txt_file:
        corpus = txt_file.readlines()

    #Obteniendo solo las noticias
    lista_noticias = []
    for linea in corpus:
        #Corta la línea del txt cada que encuentra más de dos espacio en blanco o un tabulador
        # partes = re.split(patron, linea)#cada que encuentra uno de estos hace un corte y cuando encuentra otro hace el otro corte para incluir es nueva cadena entre los dos corte en la lista
        # partes = re.split('\&\&\&\&\&\&\&\&', linea)#cada que encuentra uno de estos hace un corte y cuando encuentra otro hace el otro corte para incluir es nueva cadena entre los dos corte en la lista
        lista_noticias.append(linea)

    # print(lista_noticias)

    #definir listas
    palabras_tokenizadas_espacios = []
    palabras_retokenizadas = []
    tokens_minimos = []
    noticias_tokenizadas = []
    noticias_lemmas = []
    lista_stop_words = ["DET","ADP","CCONJ", "SCONJ","PRON","SPACE"]
    prueba = []


    #Se carga el corpus para el tagger en español
    nlp = spacy.load("es_core_news_sm")
    nlp.tokenizer = custom_tokenizer(nlp)


    #Agregando el sufijo -
    suffixes = nlp.Defaults.suffixes + [r'''-+$''',]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search
    suffixes = nlp.Defaults.suffixes + [r'''\d+$''',]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search
    suffixes = nlp.Defaults.suffixes + [r'''-''',]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search
    suffixes = nlp.Defaults.suffixes + [r'''@\w+''',]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search
    nlp.tokenizer.suffix_search = suffix_regex.search
    # suffixes = nlp.Defaults.suffixes + [r'''[A-Z]{1}[a-z\u00C0-\u017F]+\d?$''',]
    # suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    # nlp.tokenizer.suffix_search = suffix_regex.search
    # nlp.tokenizer.suffix_search = suffix_regex.search
    suffixes = nlp.Defaults.suffixes + [r'''\.{3}''',]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search
    nlp.tokenizer.suffix_search = suffix_regex.search

    # lista_provicional = [lista_noticias[0],lista_noticias[1],lista_noticias[2],'twitter.com/S10zFIQA81', '@RealDonaldTrump']

    partes_de_la_ruta_del_archivo = nombre_corpus.split("/")
    nombre_archivo = partes_de_la_ruta_del_archivo[len(partes_de_la_ruta_del_archivo)-1]

    for noticia in lista_noticias:

        doc = nlp(noticia)

        for token in doc:
            
            if(token.pos_ not in lista_stop_words):
                noticias_lemmas.append(str(token.lemma_))

        cadena_lematizada = " ".join(noticias_lemmas)

        with open('pruebas 1/pruebas_normalizadas/'+nombre_archivo, 'w') as archivo:
            archivo.write(cadena_lematizada + '\n')

        cadena_lematizada=""
        noticias_lemmas=[]
    
    return 'pruebas 1/pruebas_normalizadas/'+nombre_archivo






        
    

