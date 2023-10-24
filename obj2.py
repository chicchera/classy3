import nltk
from rich import print
import os

from utils.file_utils import diy_file_validate

class Stopwords:
    def __init__(self):
        self._lang = None
        self._use_nltk_stopwords = True
        self._stopwords = set()
        self._files = []
        self._disabled = False

    def load_stopwords(self, files, lang="spanish", nltk=True):
        if files:
            self._files = files
        self._lang = lang
        self._use_nltk_stopwords= nltk

        def validate_files_argument(files):
            if files is None:
                return False  # Argument is None, not valid

            if isinstance(files, str):
                # If it's a single string, convert it to a list
                self._files = [files]
                return True

            if isinstance(files, list):
                # Check if the list is empty
                if not files:
                    return False

                # Check that all elements are of type string
                if all(isinstance(item, str) for item in files):
                    self._files = files
                    return True  # Valid list of strings

            return False  # Invalid

        def validate_language(val: any) -> bool:
            """
            Validates the input language value and sets the appropriate language for the instance.

            Args:
                val (any): The input language value to be validated.
                if non is passed nltk will inferr the language from the text

            Returns:
                bool: True if the language value is valid and set successfully or none was passed.
                It returns False only if a wrong string was passed
            """
            if isinstance(val, str):
                val = val.strip().lower()
            if not val:
                return True

            if val in ["es", "es_ES", "español", "spanish"]:
                self._lang = "spanish"
            elif val in ["en", "en_US", "english"]:
                self._lang = "english"
            elif val in ["it", "italiano", "it_IT", "italian"]:
                self._lang = "italian"
            else:
                return False

        if not validate_files_argument(files):
            self._disabled = True


        if not self._disabled:
            new_stopwords = []
            for filename in self._files:

                success, message = diy_file_validate(filename)
                if not success:
                    print(message)
                    continue

                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if word := line.strip():
                            new_stopwords.append(word)

            self._stopwords = set(new_stopwords)
            # TODO: reenable ntlk dictionary
            # if self._use_nltk:
            #     self._stopwords = self._stopwords | set(stopwords.words(self._lang))

    @property
    def language(self):
        return self._lang

    @property
    def files(self) -> list:
        return self._files

    @property
    def stopwords(self):
        return self._stopwords


    def count_stopwords(self, text: str) -> tuple[int, int]:
        """
        Count the number of words and stopwords in the given text.

        Parameters:
            self (object): The instance of the class.
            text (str): The text to be analyzed.

        Returns:
            tuple: A tuple containing the total number of words in the original text and the total number of stopwords.
            ((tot_words - tot_stopwords) / tot_words) * 100 = percentage density
        """
        if not text:
            return 0, 0

        sentences = nltk.sent_tokenize(text)
        tot_words = 0
        tot_stops = 0
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            no_stops = set(words) - self._stopwords
            tot_words += len(words)
            tot_stops += len(words) - len(no_stops)
        return tot_words, tot_stops

CONFIG_DIR = '/home/silvio/miniconda3/envs/classy3/prg/config/'
STOPWORD_ES = 'stopwords_es.txt'
STOPWORD_RED = 'stopwords_reddit.txt'
DICTIONARY = 'new_dic.txt'

dictionary = os.path.join(CONFIG_DIR, DICTIONARY)
stopwords_files = [os.path.join(CONFIG_DIR, STOPWORD_ES),
                  os.path.join(CONFIG_DIR,STOPWORD_RED)]
lang = "es"
# print(stopwords_files)
# print(dictionary)



txt = """
Yo el Supremo Dictador de la Repubca.
Ordeno qe al acaecer mi muerte, mi cadáver sea decapitado; la cabeza puesta en una pica por tres días en la Plaza de la República donde se convocará al pueblo al son de las campanas echadas al vuelo.
Todos mis servidores civiles y militares sufrirán pena de horca. Sus cadáveres serán enterrados en potreros de extramuros sin cruz ni marca qe memore sus nombres.
Al término del dicho plazo, mando qe mis restos sean quemados y las cenizas arrojadas al río…
¿Dónde encontraron eso? Clavado en la puerta de la catedral, Excelencia. Una partida de granaderos lo descubrió esta madrugada y lo retiró llevándolo a la comandancia. Felizmente nadie alcanzó a leerlo. No te he preguntado eso ni es cosa que importe. Tiene razón Usía, la tinta de los pasquines se vuelve agria más pronto que la leche. Tampoco es hoja de Gaceta porteña ni arrancada de libros, señor. ¡Qué libros va a haber aquí fuera de los míos! Hace mucho tiempo que los aristócratas de las veinte familias han convertido los suyos en naipes. Allanar las casas de los antipatriotas. Los calabozos, ahí en los calabozos, vichea en los calabozos. Entre esas ratas uñudas greñudas puede hallarse el culpable. Apriétales los refalsos a esos falsarios. Sobre todo a Peña y a Molas. Tráeme las cartas en las que Molas me rinde pleitesía durante el Primer Consulado, luego durante la Primera Dictadura. Quiero releer el discurso que pronunció en la Asamblea del año 14 reclamando mi elección de Dictador. Muy distinta es su letra en la minuta del discurso, en las instrucciones a los diputados, en la denuncia en que años más tarde acusará a un hermano por robarle ganado de su estancia de Altos. Puedo repetir lo que dicen esos papeles, Excelencia. No te he pedido que me vengas a recitar los millares de expedientes, autos, providencias del archivo. Te he ordenado simplemente que me traigas el legajo de Mariano Antonio Molas. Tráeme también los panfletos de Manuel Pedro de Peña. ¡Sicofantes rencillosos! Se jactan de haber sido el verbo de la Independencia. ¡Ratas! Nunca la entendieron. Se creen dueños de sus palabras en los calabozos. No saben más que chillar. No han enmudecido todavía. Siempre encuentran nuevas formas de secretar su maldito veneno. Sacan panfletos, pasquines, libelos, caricaturas. Soy una figura indispensable para la maledicencia. Por mí, pueden fabricar su papel con trapos consagrados. Escribirlo, imprimirlo con letras consagradas sobre una prensa consagrada. ¡Impriman sus pasquines en el Monte Sinaí, si se les frunce la realísima gana, folicularios letrinarios!
Hum. Ah. Oraciones fúnebres, panfletos condenándome a la hoguera. Bah. Ahora se atreven a parodiar mis Decretos Supremos. Remedan mi lenguaje, mi letra, buscando infiltrarse a través de él; llegar hasta mí desde sus madrigueras. Taparme la boca con la voz que los fulminó. Recubrirme en palabra, en figura. Viejo truco de los hechiceros de las tribus. Refuerza la vigilancia de los que se alucinan con poder suplantarme después de muerto. ¿Dónde está el legajo de los anónimos? Ahí lo tiene, Excelencia, bajo su mano.
No es del todo improbable que los dos tunantes escri-vanos Molas y De la Peña hayan podido dictar esta mofa. La burla muestra el estilo de los dos infames faccionarios porteñistas. Si son ellos, inmolo a Molas, despeño a Peña. Pudo uno de sus infames secuaces aprenderla de memoria. Escribirla un segundo. Un tercero va y pega el escarnio con cuatro chinches en la puerta de la catedral. Los propios guardianes, los peores infieles. Razón que le sobra a Usía. Frente a lo que Vuecencia dice, hasta la verdad parece mentira. No te pido que me adules, Patiño. Te ordeno que busques y descubras al autor del pasquín. Debes ser capaz, la ley es un agujero sin fondo, de encontrar un pelo en ese agujero. Escúlcales el alma a Peña y a Molas. Señor, no pueden. Están encerrados en la más total obscuridad desde hace años. ¿Y eso qué? Después del último Clamor que se le interceptó a Molas, Excelencia, mandé tapiar a cal y canto las claraboyas, las rendijas de las puertas, las fallas de tapias y techos. Sabes que continuamente los presos amaestran ratones para sus comunicaciones clandestinas. Hasta para conseguir comida. Acuérdate que así estuvieron robando los santafesinos las raciones de mis cuervos durante meses. También mandé taponar todos los agujeros y corredores de las hormigas, las alcantarillas de los grillos, los suspiros de las grietas. Obscuridad más obscura imposible, Señor. No tienen con qué escribir. ¿Olvidas la memoria, tú, memorioso patán? Puede que no dispongan de un cabo de lápiz, de un trozo de carbonilla. Pueden no tener luz ni aire. Tienen memoria. Memoria igual a la tuya. Memoria de cucaracha de archivo, trescientos millones de años más vieja que el homo sapiens. Memoria del pez, de la rana, del loro limpiándose siempre el pico del mismo lado. Lo cual no quiere decir que sean inteligentes. Todo lo contrario. ¿Puedes certificar de memorioso al gato escaldado que huye hasta del agua fría? No, sino que es un gato miedoso. La escaldadura le ha entrado en la memoria. La memoria no recuerda el miedo. Se ha transformado en miedo ella misma.
¿Sabes tú qué es la memoria? Estómago del alma, dijo erróneamente alguien. Aunque en el nombrar las cosas nunca hay un primero. No hay más que infinidad de repetidores. Sólo se inventan nuevos errores. Memoria de uno solo no sirve para nada.
Estómago del alma. ¡Vaya fineza! ¿Qué alma han de tener estos desalmados calumniadores? Estómagos cuádruples de bestias cuatropeas. Estómagos rumiantes. Es ahí donde fermenta la perfidia de esos sucesivos e incurables pícaros. Es ahí donde cocinan sus calderadas de infamia. ¿De qué memoria no han de necesitar para acordarse de tantas patrañas como han forjado con el único fin de difamarme, de calumniar al Gobierno? Memoria de masca-masca. Memoria de ingiero-digiero. Repetitiva. Desfigurativa. Mancillativa. Profetizaron convertir a este país en la nueva Atenas. Areópago de las ciencias, las letras, las artes de este Continente. Lo que buscaban en realidad bajo tales quimeras era entregar el Paraguay al mejor impostor. A punto de conseguirlo estuvieron los aeropagitas. Los fui sacando de en medio. Los derroqué uno a uno. Los puse donde debían estar. ¡Areópagos a mí! ¡A la cárcel, collones!
"""

sw = Stopwords()
sw.load_stopwords(stopwords_files, lang=(lang), nltk=True)
print(sw.count_stopwords(txt))