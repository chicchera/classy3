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

# # Classification labels RAW

# **Substitutions**
#
# $ -> s
# @ -> o,a,os,as
# & -> es
#

# # Imports

import json
import os
import pathlib
import datetime
import shutil
import pprint
import pickle
from collections import Counter

# # Logger

# [**details of logger:**](https://stackoverflow.com/a/68930736/18511264)

# +
# see https://stackoverflow.com/a/68930736/18511264
# for details of logger

import logging
from IPython.display import display, HTML

class DisplayHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        display(message)

class HTMLFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: 'lightblue',
        logging.INFO: 'dodgerblue',
        logging.WARNING: 'goldenrod',
        logging.ERROR: 'crimson',
        logging.CRITICAL: 'firebrick'
    }

    def __init__(self):
        super().__init__(
            '<span style="font-weight: bold; color: green">{asctime}</span> '
            '[<span style="font-weight: bold; color: {levelcolor}">{levelname}</span>] '
            '{message}',
            style='{'
        )

    def format(self, record):read
        record.levelcolor = self.level_colors.get(record.levelno, 'black')
        return HTML(super().format(record))


# -

log = logging.getLogger()
handler = DisplayHandler()
handler.setFormatter(HTMLFormatter())
log.addHandler(handler)
log.setLevel(logging.DEBUG)


# [Python Get File Creation and Modification DateTime [3 Ways]– PYnative](https://pynative.com/python-file-creation-modification-datetime/)

# # Functions

# ## file_mod_dt(fname: str):
#
# File modification time

def file_mod_dt(fname: str):

    # if the file doesn't exists
    if not os.path.isfile(fname):
        return 0
    # create a file path
    f = pathlib.Path(fname)
    # get and return the modification time
    return f.stat().st_mtime


# ## create_expanded_dictionary(d_in: -> dict) -> dict:
#
# Expand the shortcuts in the labels lists and return a new dictionary

test = {}
test["amistades"] = [
        'amig@', 'amigable$', 'amiguero$', 'amistad&',
        'camarada$', 'amistos@', 'socializa$', 'socializo', 'socializó',
        'socializar', 'socializan'
    ]
test["lgtbq"] = [
        'andrógino$', 'bisexual&', 'gay$', 'homosexual&', 'invertido$', 'lesbi@',
        'lesbian@', 'pansexual&', 'transgender$'
    ]


def create_expanded_dictionary(din: dict) -> dict:
    dout = {}
    for key, value in din.items():
        lst = []
        for item in value:
            if '@' in item:
                lst.append(item.replace('@', 'o'))
                lst.append(item.replace('@', 'a'))
                lst.append(item.replace('@', 'os'))
                lst.append(item.replace('@', 'as'))
            elif '&' in item:
                lst.append(item.replace('&', ''))
                lst.append(item.replace('&', 'es'))
            elif '$' in item:
                lst.append(item.replace('$', ''))
                lst.append(item.replace('$', 's'))
            else:
                lst.append(item)
        dout[key] = Counter(lst)
    return dout



print(create_expanded_dictionary(test))

pp = pprint.PrettyPrinter(indent=1, width=80, sort_dicts=True)


# # Classy lists (Dictionary)

classy = {}
classy["sexo"] = [
        'afeminado$', 'afrodisíac@', 'anal&', 'amanerado', 'amaricado',
        'amiguit@', 'asexuad@',
        'asexual&', 'andropausia', 'anticonceptivo$', 'ardor&', 'ardoros@',
        'capar', 'carnal&', 'carnalmente', 'castidad', 'castrar', 'climaterio',
        'clímax', 'coito', 'concupiscente', 'concupiscible', 'concupiscencia',
        'concupiscentes', 'concupiscibles', 'concupiscencias', 'consolador',
        'continencia', 'copular', 'copulado', 'copulé', 'copuló', 'corneador&',
        'dad', 'daddy', 'delicioso', 'demichic@', 'demihombre',
        'demimasculino$', 'depravad@', 'escort$', 'erección', 'erecciones',
        'defloración', 'deflorar',
        'erotic@', 'erotiza', 'erotice', 'erotizo', 'erotizó', 'erotismo',
        'erógen@', 'erótic@', 'esperma', 'espermatozoo', 'gameto', 'semen',
        'testículos', 'próstata', 'fecundación', 'impotente', 'impotentes',
        'impotencia$', 'esterilidad', 'esterilizar', 'estupro$', 'ets',
        'eunuco', 'excitación', 'eyaculación', 'faldero', 'falo', 'fantasía$',
        'fap', 'fetiche$', 'fetichismo', 'fimosis', 'fornicar', 'frigidez',
        'frotador', 'genital&', 'hermafrodita$', 'heterosexual&', 'hiv',
        'impúdic@', 'incesto$', 'incestuos@', 'invertido$', 'lasciv@',
        'lascivia$', 'lésbic@', 'libertin@', 'libertinaje$', 'lujuros@',
        'marica$', 'maricón', 'maricones', 'masoquismo$', 'masoquista$', 'menopausia',
        'menstruación', 'mil', 'mirón&', 'mom', 'mommy$', 'mujeriego$',
        'necrofilia', 'nepe', 'ninfomanía$', 'ninfómana$', 'no fap', 'nofap',
        'nopor', 'obscen@', 'obscenidad&', 'ninfomaníac@', 'onanismo',
        'orgasmo', 'paja$', 'pajer@', 'parafilia', 'pederasta',
        'pedófilo', 'pene', 'penetrar', 'pecho$', 'penetración&', 'pervers@',
        'pervertir', 'pervertid@', 'pilín', 'poliamor', 'poliamoros@',
        'polución', 'porno', 'pornografía$', 'pornográfic@', 'prepucio',
        'priapismo', 'promíscu@', 'promiscuidad&', 'pronografía', 'prostitut@',
        'prostituirse', 'pubis', 'puñeta', 'píldora', 'testosterona',
        'sadomaso', 'sexo', 'sexual', 'sexuad@', 'sexualizar', 'sodomía',
        'sodomizar', 'sodomizó', 'sodomita$', 'sodomizad@', 'sugar', 'sáfic@',
        'swinger', 'trío', 'travesti', 'vagina', 'vasectomía', 'venére@',
        'verga', 'violación', 'virgen', 'virginidad', 'voluptuos@',
        'voluptuosidad&', 'voluptuosamente', 'voyeur', 'voyeurismo', 'vulva',
        'zoofilia', 'masturbarse', 'masturbé', 'masturbar', 'masturbo',
        'masturba$', 'masturbe$', 'masturban'
    ]
classy["parejas"] = [
        'adulterio$', 'adulterin@', 'adulter@', 'afecto', 'aman', 'amante',
        'amar', 'amor', 'amoros@', 'amorosamente', 'atracción', 'atracciones',
        'atraer', 'atraes', 'besar', 'beso', 'boda', 'cariño$', 'cariños@', 'casad@',
        'casamiento', 'casarme', 'casarnos', 'casarse', 'casaría', 'casé',
        'celo$', 'celosos@', 'chic@', 'cita', 'compañer@', 'con derechos', 'concubin@',
        'concubinato$', 'conquistar', 'conquista$', 'consorte',
        'coquet@', 'coquetear', 'cortejar', 'crush', 'cumpleaño$', 'cumplido$',
        'declarar', 'declaré', 'enamorad@', 'enamorar', 'enamorard@',
        'engañad@', 'engañó', 'engañé', 'engañara$', 'engañaría', 'enlace',
        'espos@', 'ex', 'exnovi@', 'friendzone', 'infidelidad', 'infiel&',
        'infielmente', 'ligar', 'ligue', 'matrimonio$', 'niñ@', 'novi@',
        'noviazgo$', 'nupcias', 'olvidar', 'pareja', 'pretendiente$',
        'prometid@', 'relación', 'relaciones', 'relacionar',
        'seduce', 'seducir', 'seducid@', 'seducirl@',
        'seducción', 'seducciones', 'seducidor&', 'seducidora',
        'sensual&', 'sensualidad', 'sensualmente', 'tinder', 'tóxic@'
    ]
classy["oculto"] = [
        'adivin@', 'adivinador', 'adivinar', 'alquimista', 'amarre', 'amuleto',
        'arcano', 'arpía', 'bruj@', 'cabalista', 'chamán', 'clarividente',
        'conjurar', 'embrujad@', 'embrujar', 'encantador', 'evocar', 'filtro',
        'fórmula', 'hechicer@', 'hechizad@', 'invocar', 'licántropo', 'magia',
        'mag@', 'maleficiar', 'malojo', 'milagrero', 'mágic@',
        'nigromante', 'ocultismo', 'ocultista', 'orácul@', 'pentagrama',
        'pentáculo', 'piropo$', 'pitonisa', 'poseer', 'poseid@', 'predecir',
        'predicción', 'presagiar', 'premonitor&', 'premonitora$',
        'premonitori@', 'presagio$', 'presagiad@', 'presagió',
        'profecía$', 'profeta$', 'profetizar', 'profetizó', 'profetisa$',
        'profetiza', 'profétic@', 'pronostica', 'pronostico', 'pronosticó',
        'pronosticad@', 'pronóstico', 'quiromante', 'quiromántico', 'runa',
        'runas', 'sibila', 'sortilegio$', 'supersticios@', 'superstición',
        'talismán', 'tarot$', 'vampiro$', 'vaticinio$', 'vaticin@', 'vaticinar',
        'vidente$', 'videncia$', 'vudú', 'zahorí', 'zombi$', 'zombies'
    ]
classy["medidas"] = [
        'altura', 'ancho', 'bajo', 'estatura', 'gord@', 'largo', 'medida',
        'mide', 'mido', 'peso', 'sobrepeso', 'talla'
    ]
classy["belleza"] = ['acne', 'arreglad@',
                     'atractiv@','belleza', 'bell@', 'beldad&', 'cabello$', 'cuidad@',
                     'emperejilar', 'emperejilad@', 'grano$', 'hemos@','pelo$']
classy["fantasy"] = [
        'backroom$', 'deepweb', 'hada$', 'duende$', 'elfo$',
        'genio$', 'hobbit$', 'dragón&', 'dragon$', 'superpoder&', 'darkweb',
    ]
classy["cyber"] = [
        'aplicación', 'app', 'deep', 'hacker', 'laptop$', 'lenguaje$', 'pc$',
        'progama$', 'programador&', 'programación', 'programar', 'programé',
        'software', 'web'
    ]
classy["miedos"] = [
        'amedrantar', 'amedrantad@', 'amedrentador', 'angusti@', 'angustié',
        'angustió', 'asqueros@', 'asquerosidad', 'atemoriza$', 'atemorizo,',
        'atemorizó', 'atemorizad@', 'aterrad@', 'aterrador', 'aterradora$',
        'aterradores', 'aterrar', 'aterrorizar', 'aterrorizad@', 'aterrorizan',
        'aterrorizó', 'atroz', 'atrozmente', 'bizarr@', 'enorme$',
        'escalofrío', 'escalofriante', 'espanto$', 'espantos@', 'espantas',
        'espeluznante$', 'estremecedor', 'estremecedores', 'estremecedoras',
        'horrend@', 'horrible$', 'horriblemente', 'horripilan',
        'horripilante$', 'horror&', 'horroros@', 'horrorizó', 'horroricé',
        'impresionante$', 'malign@', 'miedo', 'pavor', 'pavoros@',
        'perturbador&', 'perturbadora$', 'petrificante', 'petrificar',
        'petrificarse', 'repugnan', 'repugnante', 'terrible$', 'terror&',
        'terrífic@', 'traumátic@', 'traumatizar', 'traumatizad@', 'traumad@',
        'tremend@', 'turbi@', 'vergonzos@'
    ]
classy["sf"] = [
        'alienígen@', 'espacial&', 'extraterrestre$', 'marcian@',
        'matrix', 'ovni$', 'reptilian@', 'ufo$'
    ]
classy["psicología"] = [
        'abatid@', 'abatir', 'abatirse', 'angustia$', 'angustiar',
        'angustiad@', 'anonadad@', 'anonadar', 'ansia', 'ansiedad&',
        'arrebat@', 'autodestructiv@', 'catatónic@', 'demencia&', 'demente&',
        'depresiv@', 'depresión&', 'desalentad@', 'desalentador&',
        'desalentadoras', 'desalentar', 'desanimad@', 'desanimar',
        'despersonalización', 'desequilibrad@', 'esquizofrénic@',
        'esquizofrenia$', 'estrés', 'fobía$', 'loc@', 'lucura$', 'manicomio$'
        'matarme', 'matarse', 'obsesiv@', 'obsesión&', 'obsesiona$', 'manía$',
        'paranoia', 'paranoic@', 'paranoide', 'psicosis', 'psicólog@',
        'psicótic@', 'psiquiatra', 'psíquic@', 'pánico', 'salud mental',
        'senil&', 'senilidad&', 'sicólog@', 'sicótic@', 'siquiatra$',
        'suicida$', 'suicidio', 'suicidarse', 'suicidó', 'síquico', 'tdha',
        'tourette', 'sociopátic@', 'psicopatía$', 'psicopátic@',
        'psicopatológic@'
    ]
classy["religión"] = [
        'adventista$', 'agnóstic@', 'altar&', 'anabaptista$', 'anglican@', 'ate@',
        'baptista$', 'biblia', 'calvinista$', 'cielo', 'confesionista$', 'confesor&',
        'confesión', 'confesiones', 'congregacionalista$', 'convicción', 'convicciones',
        'credo$', 'creencia$', 'cristian@', 'cristo', 'culto$', 'cuáquer@',
        'descreíd@', 'dios&', 'dogma$', 'episcopal&', 'episcopalian@',
        'espiritual', 'evangelio$', 'evangélico$', 'exorcista$', 'hereje$',
        'heterodox@', 'iglesia$', 'impí@', 'infiel&', 'infierno', 'infernal&',
        'jehová', 'luteran@', 'metodista$', 'monje$', 'mormón', 'mormones',
        'muerte', 'orden&', 'pagan@', 'paraíso', 'pastor&', 'pietista$',
        'poseid@', 'presbiterian@', 'protestante$', 'protestantismo$',
        'prédica$', 'puritan@', 'puritanismo$', 'religión', 'religiones',
        'religios@', 'religiosidad', 'satán', 'satánic@', 'satanás',
        'satanismo', 'secta$', 'sectari@', 'templo$', 'teología$',
        'universalista$'
    ]
classy["paranormal"] = [
        'aparecid@', 'aparición', 'apariciones', 'djinn', 'espectro$',
        'espectral&', 'espiritista$', 'espiritu$', 'fantasma$', 'fantasmal&',
        'fantasmagóric@', 'médium$', 'ouija$', 'paranormal&', 'presencia$',
        'secreto$', 'sobrentaural&', 'visión', 'visiones'
    ]
classy["estudiantes"] = [
        'academia', 'académic@', 'aprendo', 'aprende', 'aprender', 'aprendí',
        'asignatura$', 'ateneo$', 'carrera', 'clase$', 'colegio$', 'colegial&',
        'colegialas', 'cursillo', 'curso$', 'deber$', 'educadora$',
        'educador&', 'escolar', 'estudio', 'estudiantes', 'estudié', 'estudió',
        'exámen&', 'examinar', 'examinador&', 'facultad', 'grado$',
        'instituto$', 'liceo$', 'maestr@', 'preparatori@', 'primaria',
        'profesor&', 'profesora$', 'recreo', 'reprobé', 'reprobó', 'reprobar',
        'reprobados', 'salón', 'school', 'secundaria', 'tesis', 'título',
        'uni', 'universidad&', 'universitari@'
    ]
classy["sueños"] = [
        'adormece$', 'adormecí', 'adormecer', 'adormecid@', 'adormecerme',
        'adormilé', 'adormilarse', 'adormilado', 'desperté', 'despertó',
        'despertarse', 'despiert@', 'desvelé', 'desvele', 'desvela', 'desvelo',
        'desveló', 'dormir', 'dormiré', 'dormirá', 'dormirse', 'duermo',
        'ensueño$', 'húmedo$', 'insomnio', 'melatonina', 'parálisis sueño',
        'sueño$', 'pesadilla$', 'parálisis'
    ]
classy["drogas"] = [
        'alcaloide$', 'aluciné', 'alucino', 'alucinar', 'alucinan',
        'barbitúrico$', 'cannabis', 'coca', 'cocainóman@', 'cocaína', 'dopé',
        'doparse', 'dope', 'dopen', 'dopad@', 'droga$', 'drogadict@',
        'drogarse', 'drogad@', 'drogan', 'drogarme', 'drogarte',
        'estupefaciente$', 'heroinóman@', 'heroína', 'hongos', 'lsd',
        'marihuana', 'narco$', 'narcotraficante$', 'toxicóman@', 'weed',
        'high'
    ]
classy["amistades"] = [
        'amig@', 'amigable', 'amiguero$', 'amistad&',
        'camarada', 'amistos@', 'socializa', 'socializo', 'socializó',
        'socializar', 'socializas', 'socializan'
    ]
classy["lgtbq"] = [
        'andrógino', 'bisexual', 'gay$', 'homosexual&', 'invertido', 'lesbi@',
        'lesbian@', 'pansexual&', 'transgender$'
    ]
classy["odios"] = [
        'aborre$', 'aborrezca', 'aborrezco', 'aborto', 'antipatía',
        'antisemita$', 'antisemitismo', 'aversión', 'cruel&', 'despecho',
        'desprecio', 'enemistad', 'execrable', 'execración', 'execrear',
        'fanátic@', 'feminismo$', 'feminista$', 'hastio', 'hostilidad',
        'judí@', 'machismp$', 'machista$', 'misoginía', 'misógino$', 'odio$',
        'rencor&', 'rencoros@', 'odios@', 'resentimiento$', 'vengativ@',
        'venganza$', 'enoj@', 'enojé', 'enojó', 'enojen'
    ]
classy["dinero"] = [
        'bitcoin$', 'capital&', 'capitalismo', 'capitalizar', 'capitalizado$',
        'comerciar', 'comercio$', 'comercié', 'criptomoneda$', 'cryptomoneda$',
        'defraudar', 'defraudé', 'defraudó', 'defraudaron', 'defraude',
        'dinero', 'emprendimiento$', 'engañ@', 'estafa$', 'evasión&', 'evadir',
        'finanza$', 'financia', 'financiar', 'financiari@', 'financias',
        'fondo$', 'fortuna$', 'fraude$', 'ganar', 'gasta$', 'gastar', 'gastan',
        'gastos', 'gastado', 'gastando', 'gastarás', 'gastamos',
        'gastarse', 'gastarías', 'gastabas', 'inversión', 'inversor&',
        'inversora$', 'inversionista', 'invertir', 'impuesto$', 'moneda$',
        'negocio$', 'negociar', 'negocia', 'negociador', 'negociante',
        'negocié', 'negocien', 'negocias', 'oficina$', 'pecuniari@', 'plata',
        'riqueza$', 'trabajé', 'trabajó', 'trabajo', 'trabajador', 'trabajan',
        'trabajar', 'trabajaría$', 'trampa$', 'vender', 'venta$'
    ]
classy["salud"] = [
        'doctor&', 'doctora$', 'saludable$', 'salubre$',
        'salubridad', 'higiene$', 'higienice', 'higienizo', 'higienicé',
        'higieniza', 'higienizó', 'higienizar', 'higienista$', 'benéfic@',
        'bienestar', 'sanidad', 'desinfectante$', 'desinfecte', 'desinfecto',
        'desinfecté', 'desinfecta', 'desinfectó', 'dentista$', 'catarro&',
        'resfrío$', 'resfrió', 'resfrié', 'resfría$', 'resfrían', 'resfríar',
        'constipad@', 'enfriamiento$', 'gripe$', 'influenza', 'dolencia$',
        'enfermedad&', 'indisposición&', 'achaque$'
    ]
classy["juegos"] = [
        'deporte$', 'deportiv@', 'deportista$', 'futbol', 'fútbol',
        'juego$', 'jugar', 'videojuego$', 'gamer$', 'jugad@', 'jugador&',
        'jugadora$', 'nintendo', 'ps5', 'ps4', 'ps3', 'xbox', 'console$',
        'consola$', 'consol', 'playstation', 'minecraft', 'gamer@', 'gaming',
        'warzone', 'wii', 'gta', 'sega', 'naipe$', 'carta$', 'baraja$'
    ]
classy["familia"] = [
        'abuel@', 'comadre$', 'compadre$', 'consanguíne@', 'familia$',
        'familiar', 'herman@', 'hij@', 'madrastra$', 'madre$', 'madrina$',
        'mamá$', 'padrastro$', 'padre$', 'padrino$', 'papá$', 'pariente$',
        'suegr@', 'tí@'
    ]
classy2 = create_expanded_dictionary(classy)
# pclassy = pp.pformat(classy)
# print(pclassy)
# pp.pprint(classy)

# DON'T DELETE THIS BIT AS IT CAN BE HANDY TO REGENERATE THE DICTIONARY
filename = "classy2.json"
with open(filename, 'w') as file:
    json.dump(classy2, file)

# +
# pp.pprint(classy)

# formatted_dic = pprint.pformat(classy)
# print(formatted_dic)
# -

# # WIP

# - if in the cwd there is a classy_raw.json file
#     - move it to the data directory
#       (there should be one only on the first run)
# - if the classy_raw.json file is newer then the pickled file
#     - regenerate the dictionary
#     - regenerate the pickle file
# - load the pickled fille

# +
CLASSY_JSON = 'classy.json'
CLASSY_PKL = 'classy.pkl'

cwd = os.getcwd()
data_dir = cwd + '/data/'

classy_json = data_dir + CLASSY_JSON
classy_pkl = cwd + "/" + CLASSY_PKL
file2move = cwd + "/" + CLASSY_JSON

# check (or create) the the data dir exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# if there is a classy file in the local dir move it to the data dir
if file_mod_dt(file2move) > file_mod_dt(classy_json):
    shutil.move(file2move, classy_json) # file2move will be the the work file
    print(F'''FOUND {file2move}
              moved to {classy_json}''' )

# compare the dates of the json and pkl files
# if the json is newer regenerate the pickle
if file_mod_dt(classy_json) > file_mod_dt(classy_pkl):
    with open(classy_json, 'r') as f:
        classy_raw = json.load(f)

    # regenerate the internal json variable
    classy = create_expanded_dictionary(classy_raw)

    # create a new pickle file
    with open(classy_pkl, 'wb') as fl:
        pickle.dump(classy, f)

# and at last reload the piccle file into the classy variable
with open(classy_pkl, 'rb') as f:
    classy = pickle.load(f)


# +
# print(json.dumps(classy))
# print(s)
# with open(file2move, 'w') as f:
#     f.write(formatted_dic)
# -

io = open(in_file,"r")
xx = json.load(io)
print(xx)

# +
classify_raw = {}
classify_raw['xx'] = Counter(['22','xx','aa'])
classify_raw['yy'] = Counter(['afeminado&', 'afrodisíac@', 'anal&', 'amanerado'])
print(classify_raw)
print('amanerado' in classify_raw['yy'])

print(json.dumps(classify_raw))


# -

formatted_dic = pprint.pformat(classify_raw)
print(formatted_dic)

print(classy3)
