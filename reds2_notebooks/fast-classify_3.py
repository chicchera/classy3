# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import warnings
# warnings.filterwarnings('ignore')

import ipywidgets as widgets
from IPython.display import display

# from txtlists
import re
import unidecode

#from txtutils
import os
import demoji
import unidecode
from prettyprinter import pprint

import json
import functools

import pandas as pd
import sqlite3

import time
import datetime

from time import perf_counter
import sys

from inscriptis import get_text
from tqdm.auto import tqdm

import nltk
from nltk.corpus import stopwords
nltk_stopwords = stopwords.words('spanish')
# -

# # Constants

# +
# CLEAN_DATA = False
# CLASSIFY_DATA = True

# REGEX_CLASSIFY = True
# SET_CLASSIFY = False

# MODE = REGEX_CLASSIFY

# TITLE_MULTIPLIER = 5
# SELF_MULTIPLIER = 3
# OP_MULTIPLIER = 2
# PLAIN_MULTIPLIER = 1

# QUERY_CHUNK = 50_000

DB = '/home/silvio/data/stats.db'
# DB = '/home/silvio/data/redsdb/stats.db'

WORD = re.compile(r'\w+')
ONLY_WORDS = re.compile(r'[^\w\s]')

re_nums_only = re.compile(r"^[0-9]*$")
re_nums_mix = re.compile(
    r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)")


# -

# ## Query support functions

# ### Clean query: removes all blank characters

def clean_sql(sql: str) -> str:
    return " ".join(sql.split())


def sel_to_cnt(qry) -> str:
    '''returns a count query from a select one'''
    return "SELECT COUNT (*) FROM " + qry.lower().partition("from")[2]


# ## Queries

# ### Count(?) imported data

# #### This queries works only if we are processing ALL the data

def qry_recs_to_clean(c) -> int:
    qry = clean_sql('''
        SELECT
          (select COUNT(*) from posts)
          +
          (select COUNT(*) from comments) AS totrecs;
    ''')
    return c.execute(qry).fetchone()[0]


# ### Clean posts

# #### Query sel posts from DFR

def qry_posts_from_remote():
    pass


# ### Classify posts / comments
#

def qry_sel_classify(limit, offset) -> str:
    return clean_sql(f'''
        SELECT
            title,
            body,
            rid_post,
            rid_comment,
            tbl,
            NULL AS cat,
            NULL AS num
        FROM
            vw_posts_comments
        WHERE
            rid_post + COALESCE(rid_comment, '') NOT IN
            (SELECT rid_post + COALESCE(rid_comment, '') FROM category)
            LIMIT {limit} OFFSET {offset};
        ''')


# + [markdown] jp-MarkdownHeadingCollapsed=true
# ## Classification dictionaries
# -

# ### Dictionary for classification by **RegEx**

classify_lbls_regex = {
    "parejas": {
        'adulteri*', 'adulter@', 'afecto', 'aman', 'amante', 'amar', 'amor',
        'amoros*', 'atracc*', 'atraer', 'atraes', 'besar', 'beso', 'boda',
        'cariño&', 'casad@', 'casamiento', 'casarme', 'casarnos', 'casarse',
        'casaría', 'casé', 'celo&', 'celos@' 'chic@', 'cita', 'compañer@',
        'con derechos', 'concubin*', 'conquist*', 'consorte', 'coquet*',
        'cortejar', 'crush', 'cumpleaño&','cumplido&',
        'declarar*', 'enamorad@', 'enamorar*', 'engañad*',
        'enlace', 'espos@', 'ex', 'exnovi@', 'friendzone', 'infidel*',
        'infiel*', 'ligar', 'ligue', 'matrimonio&', 'mujer', 'mujeres' 'niñ@', 'novi@',
        'noviazgo&', 'nupcias', 'olvidar', 'pareja', 'pretendiente',
        'prometid@', 'relación', 'relacion*', 'relación distancia', 'seduc*',
        'sensu*', 'tinder', 'tóxic@'
    },
    "sexo": {
        'afeminado', 'afrodisíac@', 'anal', 'amanerado', 'amaricado',
        'amiguit@', 'asex*', 'andropausia', 'anticonceptivo&', 'ardor*',
        'capar', 'carnal*', 'castidad', 'castrar', 'climaterio', 'clímax',
        'coito', 'concupisc*', 'consolador', 'continencia', 'copul*', 'dad',
        'daddy', 'delicioso',
        'demichic@', 'demihombre', 'demimasculino', 'depravad@', 'escort'
        'erección', 'defloración', 'eroti*', 'erógen@', 'erótic@', 'esperma',
        'espermatozoo', 'gameto', 'semen', 'testículos', 'próstata',
        'fecundación', 'impot*', 'esterilidad', 'esterilizar', 'estupro&',
        'ets', 'eunuco', 'excitación', 'eyaculación', 'faldero', 'falo',
        'fantasía&', 'fap', 'fetiche&', 'fetichismo', 'fimosis', 'fornic*',
        'frigidez', 'frotador', 'genital*', 'hermafrodita&', 'heterosexual*',
        'hiv', 'impúdic@', 'incest*', 'invertido', 'lasciv@*', 'lésbic@',
        'libertin*', 'lujur*', 'marica', 'maricón', 'masoq*', 'menopausia',
        'menstruación', 'milf', 'mirón', 'mirones', 'mom', 'mommy', 'mujeriego',
        'necrofilia', 'nepe', 'ninfoma*', 'ninfómana&', 'no fap', 'nofap',
        'nopor', 'obscen*', 'onanismo', 'orgasmo', 'clímax', 'paja&', 'pajer@',
        'parafilia', 'pederasta', 'pedófilo', 'pene', 'penetrar', 'pecho&',
        'penetración', 'perver*', 'pilín', 'poliamor*',
        'polución', 'porno*', 'prepucio',
        'priapismo', 'promíscu*', 'pronografía', 'prostit*', 'pubis', 'puñeta',
        'píldora', 'testosterona', 'sadomaso', 'sexo', 'sexu*', 'sodom*', 'sugar', 'sáfic*',
        'trío', 'travesti', 'vagina', 'vasectomía', 'venére@', 'verga',
        'violación', 'virgen', 'virginidad', 'volupt*', 'voyeur', 'voyeurismo',
        'zoofilia', 'mastur*'
    },
    "oculto": {
        'adivin@', 'adivinador', 'adivinar', 'alquimista', 'amarre', 'amuleto',
        'arcano', 'arpía', 'bruj@', 'cabalista', 'chamán', 'clarividente',
        'conjurar', 'embrujad@', 'embrujar', 'encantador', 'evocar', 'filtro',
        'fórmula', 'hechicer@', 'hechizad@', 'invocar', 'licántropo', 'magia',
        'mag@', 'maleficiar', 'malojo', 'milagrero', 'mágic@', 'mágic*',
        'nigromante', 'ocultismo', 'ocultista', 'orácul@', 'pentagrama',
        'pentáculo', 'piropo&', 'pitonisa', 'poseer', 'poseid@', 'predecir',
        'predicción', 'presagiar', 'premoni*', 'presag*', 'profecía&', 'profet*',
        'profétic@', 'pronostic*', 'pronóstico', 'quiromante', 'quiromántico',
        'runa', 'runas', 'sibila', 'sortilegio&', 'superstic*', 'talismán',
        'tarot&', 'vampiro', 'vatici*', 'viden*', 'vudú', 'zahorí', 'zombi',
        'zombie'
    },
    "medidas": {
        'altura', 'ancho', 'estatura', 'gord@','largo', 'medida', 'mide',
        'mido', 'peso', 'sobrepeso','talla'
    },
    "fantasy": {
        'backroom&', 'deep web', 'deepweb', 'hada&', 'duende&', 'elfo&',
        'genio&', 'hobbit&', 'dragón&', 'dragones', 'superpoder*'
    },
    "cyber":
    {'aplicación', 'app', 'hacker', 'laptop&','lenguaje', 'pc&','progam*', 'web', 'deep'},
    "miedos": {
        'amedrant*', 'amedrent*', 'angust*', 'asquero*', 'atemoriz*',
        'aterrad*', 'aterrar', 'aterroriz*', 'atroz*', 'bizarr@','enorme&', 'escalofri*',
        'espanto*', 'espeluznante&', 'estremeced*', 'horrend@', 'horrible*',
        'horripilan*', 'horro*', 'impresionante&', 'malign@', 'miedo',
        'pavor*', 'perturbador*', 'petrificante', 'petrificar', 'petrificarse',
        'repugnan*', 'terrib*', 'terror*', 'terrífic@', 'traumátic@',
        'traumat*', 'tremend@', 'turbi@', 'vergonzos@'
    },
    "sf": {
        'alienígen@', 'espacial', 'espaciales', 'extraterrestre&', 'marcian@&',
        'matrix', 'ovni&', 'reptilian@&', 'ufo&'
    },
    "psicología": {
        'abatid@', 'abatir', 'abatirse', 'angusti*', 'anonadad@', 'anonadar',
        'ansia', 'ansie*', 'arrebat*', 'autodestructiv@', 'catatónic@*',
        'demencia&', 'demente&', 'depresi*', 'desalentad*', 'desalentar',
        'desanimad@', 'desanimar', 'despersonalización', 'desequilibrad@',
        'esquizofr*', 'estrés', 'fobía&', 'loc@', 'lucura&', 'manicomio&'
        'matarme', 'matarse', 'obsesi*', 'manía&', 'paranoi*', 'psicosis',
        'psicólog@', 'psicótic@', 'psiquiatra', 'psíquic@', 'pánico',
        'salud mental', 'senil*', 'sicólog@', 'sicótic@', 'siquiatra&',
        'suicid*', 'síquico', 'tdha', 'tourette', 'sociopá*', 'psicop*'
    },
    "religión": {
        'adventista', 'agnóstic@', 'altar', 'anabaptista', 'anglican@', 'ate@',
        'baptista', 'biblia', 'calvinista', 'cielo', 'confesionista',
        'confesión', 'congregacionalista&', 'convicc*', 'credo', 'creenc*',
        'cristian@', 'cristo', 'culto', 'cuáquer@', 'descreíd@', 'dios',
        'dogma', 'episcopal', 'episcopalian@', 'espiritual', 'evangelio',
        'evangélico', 'exorcista', 'hereje', 'heterodox@', 'iglesia', 'impío&',
        'infiel*', 'infierno', 'infernal*', 'jehová', 'luteran@', 'metodista&',
        'monje&', 'mormón', 'mormon*', 'muerte', 'orden', 'pagan@', 'paraíso',
        'pastor', 'pietista', 'poseid@', 'presbiterian@', 'protestan*',
        'prédica', 'puritan*', 'religi*', 'satán*', 'satan*', 'secta*',
        'templo&', 'teología', 'universalista'
    },
    "paranormal": {
        'aparecid@', 'aparic*', 'djinn', 'espectro&', 'espectra*',
        'espiritista', 'espiritu', 'fantasm*', 'médium', 'ouija', 'paranorma*',
        'presencia&', 'secreto', 'sobrentaural*', 'visión', 'visiones'
    },
    "estudiantes": {
        'academ*', 'académ*', 'aprend*', 'asignatura&', 'ateneo&', 'carrera',
        'clase&', 'coleg*', 'cursillo', 'curso&', 'deberes','educador*', 'escolar',
        'estud*', 'exámen*', 'examin*', 'facultad', 'grado&', 'instituto&',
        'liceo&', 'maestr@', 'preparatori@', 'primaria', 'profesor*', 'recreo',
        'reprob*', 'salón', 'school', 'secundaria', 'tesis', 'título', 'uni',
        'universidad*'
    },
    "sueños": {
        'adormec*', 'adormil*', 'adormit*', 'despert*', 'despiert@', 'desvel*',
        'dormir*', 'duermo', 'ensueño&', 'húmedo&', 'insomnio', 'melatonina',
        'parálisis sueño', 'sueño&', 'pesadilla&', 'parálisis'
    },
    "drogas": {
        'alcaloide&', 'alucin*', 'barbitúrico&', 'cannabis', 'coca*', 'dop*', 'droga*',
        'estupefaciente&', 'heroinóman@', 'heroína', 'hongos', 'lsd',
        'marihuana', 'narco*', 'toxicómano&', 'weed', 'high'
    },
    "amistades": {
        'amig@', 'amigable', 'amiguero', 'amistad', 'amistades', 'amistos@',
        'camarada', 'amistos@', 'socializ*'
    },
    "lgtbq": {
        'andrógino', 'bisexual', 'gay&', 'homosex*', 'invertido', 'lesbi*',
        'pansexual*', 'transgender&'
    },
    "odios": {
        'aborre*', 'aborto', 'antipatía', 'antisemita&', 'antisemitismo',
        'aversión', 'cruel&', 'despecho', 'desprecio', 'enemistad',
        'execrable', 'execración', 'execrear', 'fanátic@', 'feminis*',
        'hastio', 'hostilidad', 'judí@', 'machis*', 'misoginía', 'misógino&',
        'odio*', 'rencor*', 'resentim*', 'vengativ@', 'venganza&'
    },
    "dinero": {
        'bitcoin&', 'capital*', 'comerc*', 'criptomoneda&', 'cryptomoneda&',
        'defraud*', 'dinero', 'enoj*'
        'emprendimiento&', 'engañ@', 'estafa&', 'evasión', 'evadir',
        'finanza&', 'financi*', 'fondo&', 'fortuna&', 'fraude&', 'ganar',
        'gasta*', 'inversión', 'invers*', 'invertir', 'impuesto&', 'moneda&',
        'negoci*', 'oficina&', 'pecuniari@', 'plata', 'riqueza&', 'trabaj*',
        'trampa&', 'vender', 'venta&'
    },
    "salud": {
        'doctor', 'doctora&', 'doctores', 'salud', 'saludable&', 'salubr*', 'higie*',
        'benéfic@', 'bienestar', 'sanidad', 'desinfec*', 'dentist*'
        'catarro&', 'resfr*', 'constipad@', 'enfriamiento&', 'gripe&',
        'influenza', 'dolencia&', 'enfermeda*', 'indisposición*', 'achaque&'
    },
    "juegos": {
        'deporte&','deporti*','futbol*', 'fútbol',
        'juego&', 'jugar', 'videojuego&', 'gamer&', 'jugad*', 'nintendo', 'ps5'
        'ps4', 'ps3', 'xbox', 'console&', 'consola&', 'consol', 'playstation',
        'minecraft', 'gamer@', 'gaming','warzone', 'wii', 'gta', 'sega', 'naipe&',
        'carta&', 'baraja&'
    },
    "familia": {
        'abuel@', 'comadre&', 'compadre&', 'consanguíneo&', 'familia&',
        'familiar', 'herman@', 'hij@', 'madrastra&', 'madre&', 'madrina&',
        'mamá&', 'padrastro&', 'padre&', 'padrino&', 'papá&', 'pariente&',
        'suegr@', 'tí@'
    }
}


# #### RegEx functions

def make_re_pattern(dict_list) -> list:
    newlist = []
    # bs = re.escape("\b")
    bs = r'\b'
    for w in dict_list:
        newlist.append(bs + w.replace('!@', '[ó|á]s?').replace(
            '@', '[o|a]s?').replace('*', '?\w+?').replace('&', 's?') + bs)

    pattrn = '|'.join(i for i in newlist)
    # print(x)
    # quit()
    return pattrn


def re_patterns(dic: dict) -> dict:
    retdic = {}

    for lbl, lst in dic.items():
         retdic[lbl] = make_re_pattern(lst)

    return retdic



# ### Dictionay for classification by **Sets**

# +
base_class_dic = {
    'parejas': [
        'adulterio&', 'adúlter@', 'afecto', 'aman', 'amante', 'amar', 'amor',
        'amoros@', 'atraccón', ' atracciones', 'atraer', 'atraes', 'besar',
        'beso', 'boda', 'cariño', 'cariños', 'casada', 'casadas', 'casado',
        'casados', 'casamiento', 'casarme', 'casarnos', 'casarse', 'casaría',
        'casé', 'celo', 'celos', 'chica', 'chicas', 'chico', 'chicos', 'cita',
        'citas', 'compañera', 'compañeras', 'compañero', 'compañeros',
        'concubin@', 'concubinato', 'conderechos', 'conquista&', 'conquistar',
        'consorte', 'coquet@', 'coquetón', 'coquetona', 'coquetear',
        'coqueteo', 'cortejar', 'crush', 'cumpleaño', 'cumpleaños', 'cumplido',
        'cumplidos', 'declarar', 'declaración', 'declaraciones', 'enamorad@',
        'enamorar', 'enamorarse', 'engañad@', 'enlace', 'espos@', 'ex',
        'exnovia', 'exnovias', 'exnovio', 'exnovios', 'friendzone',
        'infidelidad', 'infiel', 'infieles', 'ligar', 'ligue', 'matrimonio',
        'matrimonios', 'niña', 'niñas', 'niño', 'niños', 'novia', 'novias',
        'noviazgo', 'noviazgos', 'novio', 'novios', 'nupcias', 'olvidar',
        'pareja', 'parejas', 'piropo', 'piropos', 'pretendiente',
        'pretendientes', 'prometida', 'prometidas', 'prometido', 'prometidos',
        'relación', 'relaciones', 'seducción', 'seductor', 'seductora',
        'seductores', 'seductoras', 'sensul', 'sensuales', 'sensualidad',
        'sensualmeente', 'tinder', 'tóxic@'
    ],
    'sexo': [
        'afeminado', 'afrodisíaca', 'afrodisíacas', 'afrodisíaco',
        'afrodisíacos', 'amanerada', 'amaneradas', 'amanerado', 'amanerados',
        'amaricado', 'amiguita', 'amiguitas', 'amiguito', 'amiguitos', 'anal',
        'anales', 'andropausia', 'anticonceptiva', 'anticonceptivas',
        'anticonceptivo', 'anticonceptivos', 'ardor', 'ardores', 'arodoros@',
        'asexual', 'asexuado', 'asexuales', 'caliente&','capar', 'carnal', 'carnales',
        'carnalmente', 'castidad', 'castrar', 'climaterio', 'clímax', 'coito',
        'concupiscencia&', 'concupiscente&', 'consolador', 'continencia',
        'copular', 'corneador', 'dad', 'daddy', 'defloración', 'delicioso',
        'demichica', 'demichicas', 'demichico', 'demichicos', 'demihombre',
        'demimasculino', 'depravada', 'depravadas', 'depravado', 'depravados',
        'erotismo', 'erótic@', 'erógena', 'erógenas', 'erógeno', 'erógenos',
        'erótica', 'eróticas', 'erótico', 'eróticos', 'escort', 'erección',
        'esperma', 'espermatozoo', 'esterilidad', 'esterilizar', 'estupro',
        'estupros', 'ets', 'eunuco', 'excitación', 'eyaculación', 'faldero',
        'falo', 'fantasía', 'fantasías', 'fap', 'fecundación', 'fetiche',
        'fetiches', 'fetichismo', 'fimosis', 'fornicar', 'fornica', 'fornico',
        'fornicó', 'frigidez', 'frotador', 'gameto', 'genital', 'genitales',
        'hermafrodita', 'hermafroditas', 'heterosexual', 'heterosexuales',
        'hiv', 'hot&','impotente&', 'impotencia', 'impúdica', 'impúdicas', 'impúdico',
        'impúdicos', 'incesto&', 'incestuos@', 'invertido', 'lasciv@',
        'libertin@', 'libertinaje&', 'lujuria', 'lugurios@', 'lésbica',
        'lésbicas', 'lésbico', 'lésbicos', 'marica&', 'maricón', 'maricones',
        'masoquismo&', 'masoquista&', 'masturba&', 'masturbo', 'masturbar',
        'masturban', 'menopausia', 'menstruación', 'milf', 'mirón', 'mom',
        'mommy', 'mujeriego', 'necrofilia', 'nepe', 'ninfomaníac@',
        'ninfómana&', 'nofap', 'nopor', 'obscenidad', 'obscenidades',
        'obscen@', 'onanismo', 'orgasmo', 'paja', 'pajas', 'pajera', 'pajeras',
        'pajero', 'pajeros', 'parafilia', 'pecho', 'pechos', 'pederasta',
        'pedófilo', 'pene', 'penetración', 'penetrar', 'pervertid@',
        'perversión', 'perversiónes', 'pilín', 'poliamor', 'poliamoros@',
        'polución', 'pornográfic@', 'pornografía', 'porno', 'prepucio',
        'priapismo', 'promiscuidad', 'promiscu@', 'pronografía', 'prostitut@',
        'prostituir', 'prostituirse', 'prostituyen', 'próstata', 'pubis',
        'puñeta', 'píldora', 'sadomaso', 'semen', 'sexo', 'sexual', 'sexuales',
        'sodomía', 'sodomizar', 'sodomita', 'sugar', 'swinger', 'testosterona',
        'testículos', 'travesti', 'trío', 'vagina', 'vaginas', 'vasectomía',
        'venérea', 'venéreas', 'venéreo', 'venéreos', 'verga', 'violación',
        'virgen', 'virgenes','virginidad', 'voluptuos@', 'voluptuosamente',
        'voluptuosidad', 'voyeur', 'voyeurismo', 'vulva', 'zoofilia'
    ],
    'parejas': [
        'adulterio&', 'adúlter@', 'afecto', 'aman', 'amante', 'amar', 'amor',
        'amoros@', 'atraccón', ' atracciones', 'atraer', 'atraes', 'besar',
        'beso', 'boda', 'cariño', 'cariños', 'casada', 'casadas', 'casado',
        'casados', 'casamiento', 'casarme', 'casarnos', 'casarse', 'casaría',
        'casé', 'celo', 'celos', 'chica', 'chicas', 'chico', 'chicos', 'cita',
        'citas', 'compañera', 'compañeras', 'compañero', 'compañeros',
        'concubin@', 'concubinato', 'conderechos', 'conquista&', 'conquistar',
        'consorte', 'coquet@', 'coquetón', 'coquetona', 'coquetear',
        'coqueteo', 'cortejar', 'crush', 'cumpleaño', 'cumpleaños', 'cumplido',
        'cumplidos', 'declarar', 'declaración', 'declaraciones', 'enamorad@',
        'enamorar', 'enamorarse', 'engañad@', 'enlace', 'espos@', 'ex',
        'exnovia', 'exnovias', 'exnovio', 'exnovios', 'friendzone',
        'infidelidad', 'infiel', 'infieles', 'ligar', 'ligue', 'matrimonio',
        'matrimonios', 'niña', 'niñas', 'niño', 'niños', 'novia', 'novias',
        'noviazgo', 'noviazgos', 'novio', 'novios', 'nupcias', 'olvidar',
        'pareja', 'parejas', 'piropo', 'piropos', 'pretendiente',
        'pretendientes', 'prometida', 'prometidas', 'prometido', 'prometidos',
        'relación', 'relaciones', 'seducción', 'seductor', 'seductora',
        'seductores', 'seductoras', 'sensul', 'sensuales', 'sensualidad',
        'sensualmeente', 'tinder', 'tóxic@'
    ],
    'oculto': [
        'adivina', 'adivinador', 'adivinar', 'adivinas', 'adivino', 'adivinos',
        'alquimista&', 'amarre', 'amuleto&', 'arcano&', 'arpía&', 'bruja',
        'brujas', 'brujo', 'brujos', 'cabalista&', 'chamán', 'chamanes',
        'clarividente&', 'conjurar', 'embrujada', 'embrujadas', 'embrujado',
        'embrujados', 'embrujar', 'encantador', 'encantadora', 'evocar',
        'filtro', 'fórmula&', 'hechicera', 'hechiceras', 'hechicero',
        'hechiceros', 'hechizada', 'hechizadas', 'hechizado', 'hechizados',
        'invocar', 'invocación', 'licántropo&', 'maga', 'magas', 'magia',
        'mago', 'magos', 'maleficiar', 'maleficio', 'malojo', 'milagrero',
        'mágica', 'mágicas', 'mágico', 'mágicos', 'nigromante&', 'ocultismo',
        'ocultista&', 'orácula', 'oráculas', 'oráculo', 'oráculos',
        'pentagrama&', 'pentáculo', 'pitonisa&', 'poseer', 'poseida',
        'poseidas', 'poseido', 'poseidos', 'predecir', 'predicción',
        'predicciónes', 'premonitor', 'premonitora', 'premonición',
        'premoniciones', 'premonitori@', 'presagio', 'presagiar', 'profecía',
        'profecías', 'profeta', 'profética', 'proféticas', 'profético',
        'proféticos', 'profetizar', 'pronosticar', 'pronóstico&',
        'quiromante&', 'quiromántico&', 'runa', 'runas', 'sibila&',
        'sortilegio', 'sortilegios', 'superstición', 'supersticios@',
        'talismán', 'talismanes', 'tarot', 'tarots', 'vampiro&', 'vaticinar',
        'vaticino', 'vaticinios', 'vaticinad@', 'vidente&', 'videncia&',
        'vudú', 'zahorí', 'zombi&', 'zombie&'
    ],
    'medidas': [
        'altura', 'ancho', 'bajo', 'estatura', 'gorda', 'gordas', 'gordo',
        'gordos', 'largo', 'medida', 'mide', 'mido', 'peso', 'sobrepeso',
        'talla'
    ],
    'belleza': [
        'acne', 'belleza', 'cabello', 'cabellos', 'grano', 'granos', 'pelo',
        'pelos'
    ],
    'fantasy': [
        'backroom', 'backrooms', 'deepweb', 'deepweb', 'dragones', 'dragón',
        'dragóns', 'duende', 'duendes', 'elfo', 'elfos', 'genio', 'genios',
        'hada', 'hadas', 'hobbit', 'hobbits', 'superpoder', 'superpoderes',
        'superpoderos@'
    ],
    'miedos': [
        'amedrantar', 'amedrantador', 'amedrantadores', 'amedrantadora&',
        'angustia&', 'asqueros@', 'asquerosidad'
        'atemoriza', 'atemorizo', 'atemorizó', 'atemorizar', 'aterrad@',
        'aterrador', 'aterradoras', 'aterradores', 'aterrar', 'atroz',
        'atrozmente', 'bizarra', 'bizarras', 'bizarro', 'bizarros', 'enorme',
        'enormes', 'escalofriante&', 'espanto&', 'espantos@', 'espeluznante',
        'espeluznantes', 'estremecedor', 'estremecedora', 'estremecedores'
        'horrenda', 'horrendas', 'horrendo', 'horrendos', 'horrible&',
        'horripilan', 'horripilante&', 'horror', 'horrores', 'horroros@',
        'horrorizar', 'horrorizan', 'impresionante', 'impresionantes',
        'maligna', 'malignas', 'maligno', 'malignos', 'miedo', 'pavor',
        'pavores', 'pavoroso', 'perturbador', 'perturbadora&', 'perturbadores',
        'petrificante', 'petrificar', 'petrificarse', 'repugnan',
        'repugnante&', 'repugnancia', 'terrible&', 'terror', 'terrores',
        'terrífico', 'terríficos', 'traumática', 'traumáticas', 'traumático',
        'traumáticos', 'tremenda', 'tremendas', 'tremendo', 'tremendos',
        'turbia', 'turbias', 'turbio', 'turbios', 'vergonzosa', 'vergonzosas',
        'vergonzoso', 'vergonzosos'
    ],
    'psicología': [
        'abatida', 'abatidas', 'abatido', 'abatidos', 'abatir', 'abatirse',
        'angustia', 'angustiar', 'angustias', 'angustiad@', 'anonadada',
        'anonadadas', 'anonadado', 'anonadados', 'anonadar', 'ansia', 'ansie',
        'ansiedades', 'arrebato', 'autodestructiva', 'autodestructivas',
        'autodestructivo', 'autodestructivos', 'catatónic@', 'demencia',
        'demencias', 'demente', 'dementes', 'depresiv@', 'depresión',
        'depresiónes', 'desalentador', 'desalentadoras', 'desalentadores',
        'desalentar', 'desanimada', 'desanimadas', 'desanimado', 'desanimados',
        'desanimar', 'desequilibrada', 'desequilibradas', 'desequilibrado',
        'desequilibrados', 'despersonalización', 'esquizofrenia&',
        'esquizofrénic@', 'estrés', 'fobía', 'fobías', 'loca', 'locas', 'loco',
        'locos', 'lucura', 'lucuras', 'manicomio&','matarme',
        'manía', 'manías', 'matarse', 'obsesiv@', 'obsesión', 'obsesiones',
        'obsesionad@', 'paranoia&', 'paranoic@', 'paranoide&', 'psicopatía&',
        'psicopátic@', 'psicopatologías', 'psicopatológico', 'psicosis',
        'psicóloga', 'psicólogas', 'psicólogo', 'psicólogos', 'psicótica',
        'psicóticas', 'psicótico', 'psicóticos', 'psiquiatra', 'psíquica',
        'psíquicas', 'psíquico', 'psíquicos', 'pánico', 'saludmental', 'senil',
        'seniles', 'selinidad', 'sicóloga', 'sicólogas', 'sicólogo',
        'sicólogos', 'sicótica', 'sicóticas', 'sicótico', 'sicóticos',
        'siquiatra', 'siquiatras', 'suicidio&', 'síquico&', 'tdha', 'tourette'
    ],
    'religión': [
        'adventista', 'agnóstica', 'agnósticas', 'agnóstico', 'agnósticos',
        'altar', 'anabaptista', 'anglicana', 'anglicanas', 'anglicano',
        'anglicanos', 'atea', 'ateas', 'ateo', 'ateos', 'baptista', 'biblia',
        'calvinista', 'cielo', 'confesionista', 'confesión',
        'congregacionalista', 'congregacionalistas', 'convicción',
        'convicciones', 'credo', 'creenca&', 'cristiana', 'cristianas',
        'cristiano', 'cristianos', 'cristo', 'culto', 'cuáquera', 'cuáqueras',
        'cuáquero', 'cuáqueros', 'descreída', 'descreídas', 'descreído',
        'descreídos', 'dios', 'dogma', 'episcopal', 'episcopaliana',
        'episcopalianas', 'episcopaliano', 'episcopalianos', 'espiritual',
        'evangelio', 'evangélico', 'exorcista', 'hereje', 'heterodoxa',
        'heterodoxas', 'heterodoxo', 'heterodoxos', 'iglesia', 'impío',
        'impíos', 'infernal', 'infernales', 'infiel', 'infieles', 'infierno',
        'jehová', 'luterana', 'luteranas', 'luterano', 'luteranos',
        'metodista', 'metodistas', 'monje', 'monjes', 'mormon', 'mormones',
        'mormón', 'muerte', 'orden', 'pagana', 'paganas', 'pagano', 'paganos',
        'paraíso', 'pastor', 'pietista', 'poseida', 'poseidas', 'poseido',
        'poseidos', 'presbiteriana', 'presbiterianas', 'presbiteriano',
        'presbiterianos', 'protestante&', 'protestantismo&', 'prédica&',
        'predicador', 'puritan@', 'puritanismo&', 'religión', 'religios@',
        'religiones', 'religionari@', 'religiosidad', 'satán', 'satanás',
        'satanizar', 'satanismo', 'satánic@', 'secta&', 'sectari@',
        'sectarismo&', 'templo', 'templos', 'teología&', 'teológic@',
        'teológicamente', 'universalista'
    ],
    'paranormal': [
        'aparecida', 'aparecidas', 'aparecido', 'aparecidos', 'aparicón',
        'apariciones', 'djinn', 'espectral', 'espectrales', 'espectralmente',
        'espectro', 'espectros', 'espiritista', 'espiritu', 'fantasma&',
        'fantasmal', 'fantasmales', 'fantasmátic@', 'fantasmagóric@', 'médium',
        'ouija', 'paranormal', 'paranormales', 'presencia', 'presencias',
        'secreto', 'sobrenatural', 'sobrenaturales', 'visiones', 'visión'
    ],
    'estudiantes': [
        'academia&', 'académic@', 'académicamente', 'aprendo', 'aprendí',
        'aprende', 'aprender', 'asignatura', 'asignaturas', 'ateneo',
        'ateneos', 'carrera&', 'clase', 'clases', 'colegio', 'colegial',
        'cursillo', 'curso', 'cursos', 'deberes', 'educador', 'educadora',
        'educadores', 'educadoras', 'escolar', 'estudiar', 'estudian',
        'estudié', 'examinar', 'exámen', 'exámenes', 'facultad', 'grado',
        'grados', 'instituto', 'institutos', 'liceo', 'liceos', 'maestra',
        'maestras', 'maestro', 'maestros', 'preparatoria', 'preparatorias',
        'preparatorio', 'preparatorios', 'primaria', 'profesor', 'profesora',
        'profesores', 'profesoras', 'profesorado', 'recreo', 'reprobar',
        'reprobé', 'salón', 'school', 'secundaria', 'tesis', 'título', 'uni',
        'universidad', 'universidades', 'universitari@'
    ],
    'sueños': [
        'adormecid@', 'adormecer', 'adormecerse', 'adormilad@', 'desperté',
        'despertó', 'despertarse', 'despierta', 'despiertas', 'despierto',
        'despiertos', 'desvelad@', 'dormir', 'duermo', 'ensueño', 'ensueños',
        'húmedo', 'húmedos', 'insomnio', 'melatonina', 'parálisis',
        'pesadilla', 'pesadillas', 'sueño', 'sueños'
    ],
    'drogas': [
        'alcaloide', 'alcaloides', 'alucinar', 'aluciné', 'alucinógen@',
        'barbitúrico', 'barbitúricos', 'cannabis', 'coca', 'cocaína',
        'cocainóman@', 'dopar', 'dopado', 'droga&', 'drogad@', 'drogadict@',
        'adicción', 'adicciónes', 'estupefaciente', 'estupefacientes',
        'heroinómana', 'heroinómanas', 'heroinómano', 'heroinómanos',
        'heroína', 'high', 'hongos', 'lsd', 'marihuana', 'narco', 'narcótico&',
        'narcotizar', 'narcotizad@', 'narcotraficante&', 'toxicómano',
        'toxicómanos', 'weed'
    ],
    'amistades': [
        'amiga', 'amigable', 'amigas', 'amigo', 'amigos', 'amiguero',
        'amistad', 'amistades', 'amistos@',
        'camarada', 'socializar'
    ],
    'lgtbq': [
        'andrógino', 'bisexual', 'gay', 'gays', 'homosexual', 'homosexuales',
        'homosexualidad', 'invertido', 'lesbian@', 'pansexual',
        'pansexualismo', 'transgender', 'transgenders'
    ],
    'odios': [
        'aborrecer', 'aborrezco', 'aborrecen', 'aborecedor', 'aborecedora',
        'aborecedores', 'aborto', 'antipatía', 'antisemita', 'antisemitas',
        'antisemitismo', 'aversión', 'cruel', 'cruels', 'despecho',
        'desprecio', 'enemistad', 'execrable', 'execración', 'execrear',
        'fanática', 'fanáticas', 'fanático', 'fanáticos', 'feminismo&',
        'feminista&', 'hastio', 'hostilidad', 'judía', 'judías', 'judío',
        'judíos', 'machismo', "machista", 'misoginía', 'misógino', 'misóginos',
        'odio&', 'odioso&', 'odiosa&', 'rencor', 'reconres', 'rencoros@',
        'resentimiento&', 'venganza', 'venganzas', 'vengativa', 'vengativas',
        'vengativo', 'vengativos'
    ],
    'dinero': [
        'bitcoin', 'bitcoins', 'capital', 'capitales', 'capitalizar',
        'capitalización', 'comercio&', 'comercial', 'comerciales', 'comerciar',
        'comerciante', 'comercializar', 'criptomoneda', 'criptomonedas',
        'cryptomoneda', 'cryptomonedas', 'defraudar', 'defraudad@', 'dinero',
        'engaña', 'engañas', 'engaño', 'engaños', 'emprendimiento',
        'emprendimientos', 'estafa&', 'estafador', 'estafadora', 'estafadores',
        'estafadoras', 'evadir', 'evasión', 'financiar', 'financié',
        'financiro&', 'finanza', 'finanzas', 'fondo', 'fondos', 'fortuna',
        'fortunas', 'fraude', 'fraudes', 'ganar', 'gastar', 'gastan', 'gastas',
        'gasto&', 'gastado&', 'gastando', 'gastos', 'impuesto', 'impuestos',
        'inversiones', 'inversores', 'inversor', 'inversión', 'invertir',
        'moneda', 'monedas', 'negocio&', 'negociar', 'negociante&', 'negocié',
        'negoció', 'oficina', 'oficinas', 'pecuniaria', 'pecuniarias',
        'pecuniario', 'pecuniarios', 'plata', 'riqueza', 'riquezas',
        'trabajar', 'trampa', 'trampas', 'vender', 'venta', 'ventas'
    ],
    'salud': [
        'achaque', 'achaques', 'benéfica', 'benéficas', 'benéfico',
        'benéficos', 'bienestar', 'constipada', 'constipadas', 'constipado',
        'constipados', 'dentista&',
        'catarro&', 'desinfectar', 'desinfectante, '
        'doctor', 'doctora', 'doctoras', 'doctores', 'dolencia', 'dolencias',
        'enfermedad', 'enfermedades', 'enfriamiento', 'enfriamientos', 'gripe',
        'gripes', 'higiene', 'higienizar', 'indisposición', 'indisposiciónes',
        'indispuest@', 'influenza', 'resfrío', 'resfriado'
        'salubre', 'insalubre', 'saludable', 'saludables', 'sanidad'
    ],
    'juegos': [
        'baraja', 'barajas', 'carta', 'cartas', 'consol', 'consola',
        'consolas', 'console', 'consoles', 'deporte', 'deportes',
        'deportiv@',
        'futbol', 'futbolista', 'futbolero', 'hincha', 'hinchada',
        'futbolísticamente', 'fútbol', 'gamer', 'gamera', 'gameras', 'gamero',
        'gameros', 'gamers', 'gaming', 'gta', 'juego', 'juegos', 'jugador',
        'jugadora', 'jugad@',
        'jugar', 'minecraft', 'naipe', 'naipes', 'nintendo', 'playstation',
        'ps3', 'ps5ps4', 'sega', 'videojuego', 'videojuegos', 'warzone', 'wii',
        'xbox'
    ],
    'familia': [
        'abuela', 'abuelas', 'abuelo', 'abuelos', 'comadre', 'comadres',
        'compadre', 'compadres', 'consanguíneo', 'consanguíneos', 'familia',
        'familiar', 'familias', 'hermana', 'hermanas', 'hermano', 'hermanos',
        'hija', 'hijas', 'hijo', 'hijos', 'madrastra', 'madrastras', 'madre',
        'madres', 'madrina', 'madrinas', 'mamá', 'mamás', 'padrastro',
        'padrastros', 'padre', 'padres', 'padrino', 'padrinos', 'papá',
        'papás', 'pariente', 'parientes', 'suegra', 'suegras', 'suegro',
        'suegros', 'tía', 'tías', 'tío', 'tíos'
    ]

}


# -

# #### sets functions

def expand_word(w: str) -> str:
    newlist = []

    if '!@' in w:
        w = w.removesuffix('!@')
        newlist += [w + 'ó', w + 'á', w + 'ós', w + 'ás']
    elif '@' in w:
        w = w.removesuffix('@')
        newlist += [w + 'o', w + 'a', w + 'os', w + 'as']
    elif '&' in w:
        w = w.removesuffix('&')
        newlist += [w, w + 's']
    else:
        newlist += [w]

    return newlist


def expand_list(lst: list) -> set:
    newlist = []
    for w in lst:
        newlist += expand_word(w)

    return set(newlist)


def make_set_dict(dic: dict) -> dict:
    retdic = {}

    for lbl, lst in dic.items():
         retdic[lbl] = expand_list(lst)

    return retdic


set_class_dict = make_set_dict(base_class_dic)

# +
# pprint(set_class_dict)
# -

# # Spell Checker and stopwords from NLTK and a few others

# ## SymSpell

# +
# from inscriptis import get_text
from spellchecker import SpellChecker

# #####################
# SymSpell
import pkg_resources
from symspellpy import SymSpell, Verbosity

# ATTN: for portability put es-100l.txt in a dir easily accesible by the app
dictionary_path = os.getcwd() + '/reds_utils/' + "es-100l.txt"
ss = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
ss.load_dictionary(dictionary_path, term_index=0, count_index=1)
#
# #####################
# -

more_stopwords = [
    'acá', 'ahí', 'ajena', 'ajeno',  'ajenas', 'ajenos', 'algo', 'algún','alguna', 'alguno',
    'algunas','algunos', 'allá', 'allí', 'ambos', 'ante', 'aquel', 'aquella', 'aquello', 'aquellas', 'aquellos',
    'aquí', 'así', 'aun', 'aunque', 'bajo', 'bastante', 'contra', 'cual','cuál', 'cuales', 'cuáles', 'cualquier',
    'cualquiera',
    'cualquieras', 'cómo', 'cuan', 'cuán','cuando', 'cuándo','del', 'demás', 'demasiado', 'demasiada', 'demasiados',
    'demasiadas',
    'dentro', 'desde', 'donde', 'dónde','dos', 'ella', 'ello', 'ellas', 'ellos', 'encima', 'entonces', 'entre',
    'eras', 'eramos', 'eran', 'eres', 'estáis', 'estamos', 'están', 'estar', 'fin', 'fue', 'fueron',
    'fui', 'fuimos', 'gueno',  'hasta', 'incluso', 'jamás', 'modo', 'muchísima', 'muchísimo', 'si', 'sí'
    'muchísimas', 'muchísimos', 'nunca', 'por', 'porque', 'primero', 'que', 'qué',
    'quién', 'quiénes','según', 'ser', 'siempre',
    'siendo', 'sin', 'sino', 'sobre', 'sois', 'solamente', 'somos', 'soy',  'sra', 'sres', 'sta',
    'tal', 'tales', 'también', 'tampoco', 'tan', 'tanta', 'tanto','tantas', 'tantos', 'tenéis', 'tenemos',
    'tener', 'tengo',  'tiempo', 'tiene', 'tienen', 'toda', 'todo','todas', 'todos'
]
std_stopwords = set(nltk_stopwords + more_stopwords)


# ## Spelling functions

# ### spell_wrd(w: str) -> str:

def spell_wrd(w) -> str:
    if re_nums_only.match(w):
        return w
    if re_nums_mix.match(w):
        w = w.replace("1", "i").replace("3", "e").replace("4", "a").replace(
            "5", "s").replace("7", "t").replace("0", "o")
    suggestions = ss.lookup(w,
                            Verbosity.CLOSEST,
                            max_edit_distance=1,
                            include_unknown=True,
                            transfer_casing=False)
    return str(suggestions[0]).split(',')[0]



# ### fast_correct_spelling(s: str) -> str:

def fast_correct_spelling(s: str) -> str:
    if s is not None:
        return ' '.join(spell_wrd(w) for w in s.split())


# # Text functions

# ## Generic text functions

# ### regTokenize(s: str) -> list:

def regTokenize(text: str) -> list:
    words = WORD.findall(text)
    return words


# ### no_stops(s) -> str:

def no_stops(s) -> str:
    if s is None:
        return None
    s_tok = regTokenize(s)
    # return ' '.join([w for w  in s_tok if w not in std_stopwords])
    return ' '.join([w for w  in s_tok if len(w) > 2 and w not in std_stopwords])



s = '''
tengo que hacer un baile para el xv colegio en navidad pero todas las personas y
iban a salir renunciaron y estoy pensando en hacer algo yo solo donde hago papel
de hombre y mujer denme ideas fa
'''

print(no_stops(s))


# ### no_html(s: str) -> str:

def no_html(s: str) -> str:
    if s is None:
        return ''
    return get_text(s).strip()


# ### clean_text(s: str) -> str:

def clean_text(s) -> str:
    if s is None:
        return None

    s = s.strip().lower().replace('/', ' ').replace('@', 'o')

    if s.startswith('view poll'):
        return None

    # s = s.replace('/', ' ').replace('@', 'o')
    # replace the "at @" character with an o
    ## s = s.replace('@', 'o')

    # remove punctuation
    s = re.sub(r'[^\w\s]', ' ', s)
    # remove multiple white spaces
    s = ' '.join(s.split())
    # remove all the emojis, if any
    return demoji.replace(s, '')


# # Text functions

# ## Generic text functions

# ### regTokenize(s: str) -> list:

def regTokenize(text: str) -> list:
    words = WORD.findall(text)
    return words


# ### no_stops(s) -> str:

def no_stops(s) -> str:
    if s is None:
        return None
    s_tok = regTokenize(s)
    # return ' '.join([w for w  in s_tok if w not in std_stopwords])
    return ' '.join([w for w  in s_tok if len(w) > 2 and w not in std_stopwords])



s = '''
tengo que hacer un baile para el xv colegio en navidad pero todas las personas y
iban a salir renunciaron y estoy pensando en hacer algo yo solo donde hago papel
de hombre y mujer denme ideas fa
'''

print(no_stops(s))


# ### no_html(s: str) -> str:

def no_html(s: str) -> str:
    if s is None:
        return ''
    return get_text(s).strip()


# ### clean_text(s: str) -> str:

def clean_text(s) -> str:
    if s is None:
        return None

    s = s.strip().lower().replace('/', ' ').replace('@', 'o')

    if s.startswith('view poll'):
        return None

    # s = s.replace('/', ' ').replace('@', 'o')
    # replace the "at @" character with an o
    ## s = s.replace('@', 'o')

    # remove punctuation
    s = re.sub(r'[^\w\s]', ' ', s)
    # remove multiple white spaces
    s = ' '.join(s.split())
    # remove all the emojis, if any
    return demoji.replace(s, '')


# ### clean_title(s: str) -> str:

def clean_title(s: str)  -> str:
    return clean_text(s)


# ### clean_body(s: str) -> str:

def clean_body(s: str) -> str:
    return clean_text(no_html(s))


# ## For classification using RegEx

# ### make_re_pattern(dict_list) -> list:

# ### re_patterns() -> dict:

# The next two vars are here just to avoid triggering an error. They'll be set later
num_rows = 0
start_from_row = 0


## Test expand words
def expand_word(w: str) -> str:
    newlist = []
    if '@&' in w:
        w = w.removesuffix('@&')
        return [w + 'o', w + 'a', w + 'os', w + 'as']
    elif '!@' in w:
        w = w.removesuffix('!@')
        return [w + 'ó', w + 'á', w + 'ós', w + 'ás']
    elif '&' in w:
        w = w.removesuffix('&')
        return [w, w + 's']
    else:
        return []


# ### pre_clean

def pre_clean(row) -> list:
    nostops = fast_correct_spelling(no_stops(fast_correct_spelling(clean_text(row['no_stopwords']))))
    body = fast_correct_spelling(no_stops(fast_correct_spelling(clean_text(no_html(row['short_body'])))))

    return pd.Series([nostops, body])


# ### classify_12

def classify_12(row) -> list:
    totals = {}
    retval = list()

    if row['tbl'] == 'P':
        self = no_stops(row['self_text'])
    else:
        body = no_stops(row['body'])

    for lbl in regex_patterns:
        cnt = 0
        if row['tbl'] == 'P':
            cnt += (len(re.findall(regex_patterns[lbl],
                                   row['no_stopwords']))) * TITLE_MULTIPLIER
            if row['self_text'] is not None:
                cnt += len(re.findall(regex_patterns[lbl],
                                      self)) * SELF_MULTIPLIER
            # totals[lbl] = cnt
        else:
            if row['is_op'] == OP_MULTIPLIER:
                multiplier = 2
            else:
                multiplier = PLAIN_MULTIPLIER

            if row['body'] is not None:
                cnt += len(re.findall(regex_patterns[lbl],
                                      body)) * multiplier
        totals[lbl] = cnt

    # sort the total by values descending
    x = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    retval = pd.Series([None, None])

    # check if the top value is > 0, otherwise return None
    first_x = list(x.items())[0]

    if first_x[1] > 0:
        retval =  pd.Series([first_x[0], first_x[1]])

    return retval


# # RUN

# ## Run constants

# +
CLEAR_ALL_DATA = False # True deletes all data / False elabs only new data
CLASSIFY_DATA = True   # True classifies all data / False elabs only new data

REGEX_CLASSIFY = True  # Use regex functions
SET_CLASSIFY = False   # Use sets functions

MODE = REGEX_CLASSIFY  # To render more readable the two lines above

# Weights to assign
TITLE_MULTIPLIER = 5   # Terms contained in the title
SELF_MULTIPLIER = 3    # Terms contained in the tself_text
OP_MULTIPLIER = 2      # Comments by the OP
PLAIN_MULTIPLIER = 1   # Comments by other users

QUERY_CHUNK = 50_000   # How many recs to load into the df
# -

# ## Clear old data

t1_start = perf_counter()

# +
conn = sqlite3.connect(DB)
c = conn.cursor()

if CLASSIFY_ALL_DATA:
    c.execute("DELETE FROM category;")
    c.execute("DELETE FROM sqlite_sequence WHERE name = 'category';")
    recs_deleted = c.rowcount

if CLEAR_ALL_DATA:
    c.execute("DELETE FROM posts_nostops;")
    c.execute("DELETE FROM sqlite_sequence WHERE name = 'posts_nostops';")

conn.commit()
conn.close()
# -

# Create the dictionary of patterns
if MODE == REGEX_CLASSIFY:
    regex_patterns = re_patterns(classify_lbls_regex)

conn = sqlite3.connect(DB)

if CLEAN_DATA:
    recs_to_clean = qry_recs_to_clean(conn)
    chunksize = QUERY_CHUNK
    start_from_row = 0
    imported_rows = 0
    with tqdm(total=recs_to_clean, unit_scale=1) as pbar:
        while True:
            df_chunk = pd.read_sql(qry_sel_classify(chunksize,start_from_row), conn)
            if len(df_chunk.index) > 0:
                imported_rows += len(df_chunk.index)
                start_from_row += len(df_chunk.index)
                df_chunk[['title','body']] = df_chunk.apply(pre_clean, axis=1)
                df_chunk.to_sql('posts_more', conn, index=False, if_exists='append', method='multi')
                pbar.update(len(df_chunk))
            else:
                break
