import re
import unidecode
'''
regex       ==> r"\bchic[o|a]s?\b"  @  amoros@ o/a Includes s
accents     ==> \bmir[ó|á]\b       !@  like above with accents
starts with ==> \bsex?\w+?\b        *  begins with
two words   ==> \bprimer?\w+?\b\s\bvez?\w+?\b
'''
'''
FINE TUNE LISTS
see title / self_text toghether
    select title || COALESCE(' - ' || self_text, '')
    from posts;

    SELECT posts.title || COALESCE(' - ' || posts.self_text, '') AS question,
        category.cat
    FROM posts,  category
    WHERE posts.id_red = category.rid_post;
'''

from nltk.corpus import stopwords

std_stopwords = stopwords.words('spanish')
'''
How can I create a Set of Sets in Python?
https://stackoverflow.com/questions/5931291/how-can-i-create-a-set-of-sets-in-python
'''

classify_lbls_raw = {
    "sexo": {
        'afeminado', 'afrodisíac@', 'anal', 'amanerado', 'amaricado',
        'amiguit@', 'asex*', 'andropausia', 'anticonceptivo&', 'ardor*',
        'capar', 'carnal*', 'castidad', 'castrar', 'climaterio', 'clímax',
        'coito', 'concupisc*', 'consolador', 'continencia', 'copul*',
        'corneador', 'dad', 'daddy', 'delicioso', 'demichic@', 'demihombre',
        'demimasculino', 'depravad@', 'escort'
        'erección', 'defloración', 'eroti*', 'erógen@', 'erótic@', 'esperma',
        'espermatozoo', 'gameto', 'semen', 'testículos', 'próstata',
        'fecundación', 'impot*', 'esterilidad', 'esterilizar', 'estupro&',
        'ets', 'eunuco', 'excitación', 'eyaculación', 'faldero', 'falo',
        'fantasía&', 'fap', 'fetiche&', 'fetichismo', 'fimosis', 'fornic*',
        'frigidez', 'frotador', 'genital*', 'hermafrodita&', 'heterosexual*',
        'hiv', 'impúdic@', 'incest*', 'invertido', 'lasciv@*', 'lésbic@',
        'libertin*', 'lujur*', 'marica', 'maricón', 'masoq*', 'menopausia',
        'menstruación', 'milf', 'mirón', 'mom', 'mommy', 'mujeriego',
        'necrofilia', 'nepe', 'ninfoma*', 'ninfómana&', 'no fap', 'nofap',
        'nopor', 'obscen*', 'onanismo', 'orgasmo', 'clímax', 'paja&', 'pajer@',
        'parafilia', 'pederasta', 'pedófilo', 'pene', 'penetrar', 'pecho&',
        'penetración', 'perver*', 'pilín', 'poliamor*', 'polución', 'porno*',
        'prepucio', 'priapismo', 'promíscu*', 'pronografía', 'prostit*',
        'pubis', 'puñeta', 'píldora', 'testosterona', 'sadomaso', 'sexo',
        'sexu*', 'sodom*', 'sugar', 'sáfic*', 'swinger', 'trío', 'travesti',
        'vagina', 'vasectomía', 'venére@', 'verga', 'violación', 'virgen',
        'virginidad', 'volupt*', 'voyeur', 'voyeurismo', 'vulva', 'zoofilia',
        'mastur*'
    },
    "parejas": {
        'adulteri*', 'adulter@', 'afecto', 'aman', 'amante', 'amar', 'amor',
        'amoros*', 'atracc*', 'atraer', 'atraes', 'besar', 'beso', 'boda',
        'cariño&', 'casad@', 'casamiento', 'casarme', 'casarnos', 'casarse',
        'casaría', 'casé', 'celo&', 'chic@', 'cita', 'compañer@',
        'con derechos', 'concubin*', 'conquist*', 'consorte', 'coquet*',
        'cortejar', 'crush', 'cumpleaño&', 'cumplido&', 'declarar*',
        'enamorad@', 'enamorar*', 'engañad*', 'enlace', 'espos@', 'ex',
        'exnovi@', 'friendzone', 'infidel*', 'infiel*', 'ligar', 'ligue',
        'matrimonio&', 'niñ@', 'novi@', 'noviazgo&', 'nupcias', 'olvidar',
        'pareja', 'pretendiente', 'prometid@', 'relación', 'relacion*',
        'relación distancia', 'seduc*', 'sensu*', 'tinder', 'tóxic@'
    },
    "oculto": {
        'adivin@', 'adivinador', 'adivinar', 'alquimista', 'amarre', 'amuleto',
        'arcano', 'arpía', 'bruj@', 'cabalista', 'chamán', 'clarividente',
        'conjurar', 'embrujad@', 'embrujar', 'encantador', 'evocar', 'filtro',
        'fórmula', 'hechicer@', 'hechizad@', 'invocar', 'licántropo', 'magia',
        'mag@', 'maleficiar', 'malojo', 'milagrero', 'mágic@', 'mágic*',
        'nigromante', 'ocultismo', 'ocultista', 'orácul@', 'pentagrama',
        'pentáculo', 'piropo&', 'pitonisa', 'poseer', 'poseid@', 'predecir',
        'predicción', 'presagiar', 'premoni*', 'presag*', 'profecía&',
        'profet*', 'profétic@', 'pronostic*', 'pronóstico', 'quiromante',
        'quiromántico', 'runa', 'runas', 'sibila', 'sortilegio&', 'superstic*',
        'talismán', 'tarot&', 'vampiro', 'vatici*', 'viden*', 'vudú', 'zahorí',
        'zombi', 'zombie'
    },
    "medidas": {
        'altura', 'ancho', 'bajo', 'estatura', 'gord@', 'largo', 'medida',
        'mide', 'mido', 'peso', 'sobrepeso', 'talla'
    },
    "belleza": {'acne', 'belleza', 'cabello&', 'grano&', 'pelo&'},
    "fantasy": {
        'backroom&', 'deep web', 'deepweb', 'hada&', 'duende&', 'elfo&',
        'genio&', 'hobbit&', 'dragón&', 'dragones', 'superpoder*'
    },
    "cyber": {
        'aplicación', 'app', 'deep', 'hacker', 'laptop&', 'lenguaje', 'pc&',
        'progam*', 'software', 'web'
    },
    "miedos": {
        'amedrant*', 'amedrent*', 'angust*', 'asquero*', 'atemoriz*',
        'aterrad*', 'aterrar', 'aterroriz*', 'atroz*', 'bizarr@', 'enorme&',
        'escalofri*', 'espanto*', 'espeluznante&', 'estremeced*', 'horrend@',
        'horrible*', 'horripilan*', 'horro*', 'impresionante&', 'malign@',
        'miedo', 'pavor*', 'perturbador*', 'petrificante', 'petrificar',
        'petrificarse', 'repugnan*', 'terrib*', 'terror*', 'terrífic@',
        'traumátic@', 'traumat*', 'tremend@', 'turbi@', 'vergonzos@'
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
        'clase&', 'coleg*', 'cursillo', 'curso&', 'deberes', 'educador*',
        'escolar', 'estud*', 'exámen*', 'examin*', 'facultad', 'grado&',
        'instituto&', 'liceo&', 'maestr@', 'preparatori@', 'primaria',
        'profesor*', 'recreo', 'reprob*', 'salón', 'school', 'secundaria',
        'tesis', 'título', 'uni', 'universidad*'
    },
    "sueños": {
        'adormec*', 'adormil*', 'adormit*', 'despert*', 'despiert@', 'desvel*',
        'dormir*', 'duermo', 'ensueño&', 'húmedo&', 'insomnio', 'melatonina',
        'parálisis sueño', 'sueño&', 'pesadilla&', 'parálisis'
    },
    "drogas": {
        'alcaloide&', 'alucin*', 'barbitúrico&', 'cannabis', 'coca*', 'dop*',
        'droga*', 'estupefaciente&', 'heroinóman@', 'heroína', 'hongos', 'lsd',
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
        'doctor', 'doctora&', 'doctores', 'saludable&', 'salubr*', 'higie*',
        'benéfic@', 'bienestar', 'sanidad', 'desinfec*', 'dentist*'
        'catarro&', 'resfr*', 'constipad@', 'enfriamiento&', 'gripe&',
        'influenza', 'dolencia&', 'enfermeda*', 'indisposición*', 'achaque&'
    },
    "juegos": {
        'deporte&', 'deporti*', 'futbol*', 'fútbol', 'juego&', 'jugar',
        'videojuego&', 'gamer&', 'jugad*', 'nintendo', 'ps5'
        'ps4', 'ps3', 'xbox', 'console&', 'consola&', 'consol', 'playstation',
        'minecraft', 'gamer@', 'gaming', 'warzone', 'wii', 'gta', 'sega',
        'naipe&', 'carta&', 'baraja&'
    },
    "familia": {
        'abuel@', 'comadre&', 'compadre&', 'consanguíneo&', 'familia&',
        'familiar', 'herman@', 'hij@', 'madrastra&', 'madre&', 'madrina&',
        'mamá&', 'padrastro&', 'padre&', 'padrino&', 'papá&', 'pariente&',
        'suegr@', 'tí@'
    }
}


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


def classification_labels() -> dict:
    # tdic = {}
    # for lbl, lst in classify_lbls_raw.items():
    # terms = labels_list_(lst)
    # tdic[lbl] = sorted(set(terms))
    tdic = set(frozenset(i) for i in classify_lbls_raw)
    return tdic


def re_patterns() -> dict:
    master_patterns = {}
    # for lbl, lst in classify_lbls_raw:
    # master_patterns[lbl] = make_re_pattern(lst)

    for lbl, lst in classify_lbls_raw.items():
        #master_patterns[lbl] = make_re_pattern(classify_lbls_row[lbl])
        master_patterns[lbl] = make_re_pattern(lst)

    return master_patterns


def lbls_patterns_(dictnry) -> dict:
    '''Returns the patterns for finding the terms using regex'''
    # dictnry = lbls_data()
    master_patterns = {}
    for lbl, lst in dictnry:
        master_patterns[lbl] = map('\b({dictnry[key]})\b')

    print(master_patterns)
    quit()
    return master_patterns


def ama_wrds() -> set:
    return {
        'libres de preguntar', 'hagan sus preguntas',
        'pregunte lo que quieran', 'pregunten lo que quieran', 'pregúntenme',
        'preguntad', 'pregúntame', 'preguntame', 'alguna pregunta', 'pregunten'
    }


def re_ama_wrds() -> list:
    return ['ama', 'amaa']


def no_ama_wrds() -> set:
    return {
        'una pregunta', 'yo pregunto', 'quiero saber', 'pregunta para',
        'pregunta seria'
    }


def reddit_es_words() -> set:
    return {
        'ama', 'amaa', 'aqui', 'aquí', 'banda', 'banear', 'banead@',
        'banearon', 'edit', 'eli5eta', 'fap', 'fixed', 'flair', 'fta', 'ftfy',
        'gw', 'hivemind', 'iama', 'iirc', 'imho', 'imo', 'itt', 'karma',
        'karmawhore', 'mic', 'mod', 'mods', 'mra', 'neckbeard', 'ninjaedit',
        'nsfl', 'nsfw', 'op', 'orangered', 'post', 'pregunta', 'preguntarles',
        'preguntas', 'pregunten', 'pregunto', 'reddiquette', 'reddit',
        'relevant', 'repost', 'shitpost', 'sjw', 'sockpuppet', 'spam',
        'spamfilter', 'srd', 'srs', 'sub', 'subreddit', 'switcharoo', 'thread',
        'til', 'tip', 'tips', 'trees', 'whoooosh', 'wip'
    }


def wc_stopwords_es() -> set:
    return {
        'alguien', 'algun', 'alguna', 'algún', 'aquí', 'aqui', 'así', 'año',
        'bienvenido', 'bienvenidos', 'como', 'cual', 'cuales', 'cuál',
        'cuáles', 'cómo', 'gente', 'hace', 'hagan', 'hola', 'misma', 'persona',
        'personas', 'quien', 'quién', 'si', 'sí', 'usted', 'ustedes'
    }


def saludos_words() -> set:
    '''A list of common salutations to be replaced
       by the ones contained in rep_saludos_words
    '''
    return {
        'amigas de reddit', 'amigos de reddit', 'banda de reddit', 'banda',
        'buenas noches', 'buenas tardes', 'buenos días', 'chicas de reddit',
        'chicos de reddit', 'como están', 'comunidad de reddit', 'comunidad',
        'cómo estás', 'gente de reddit', 'hola a todos', 'holi',
        'hola amigos de reddit', 'hola amigas', 'hola amigos', 'hola chicas',
        'hola chicos', 'hola comunidad de reddit', 'hola comunidad', 'holis',
        'humanos de reddit', 'qué tal'
    }


def replace_saludos_words() -> list:
    return ['chicos', 'chicas', 'amigos', 'amigas']


def es_stopwords() -> set:
    sw = stopwords.words("spanish")
    # add the stopwords that have an accent but without it (ignorants)
    # create an empy list
    # new_sw = list()
    new_sw = ['cómo', 'cuál', 'cuándo', 'dónde', 'quién', 'quiénes']
    # check if a word has an accent
    for w in sw:
        # convert the word from unicode to plain text
        x = str(w)
        plain = unidecode.unidecode(x)
        if x != plain:
            new_sw.append(plain)
    return set(new_sw).union(stopwords.words("spanish"))


def unwanted_words_es() -> set:
    sw = stopwords.words("spanish")
    # add the stopwords that have an accent but without it (ignorants)
    # create an empy list
    new_sw = list()
    # check if a word has an accent
    for w in sw:
        # convert the word from unicode to plain text
        x = str(w)
        plain = unidecode.unidecode(x)
        if x != plain:
            new_sw.append(plain)
    useless_words = set(sw).union(es_stopwords())
    return useless_words


def spanish_punctuation():
    return "¿¡"
