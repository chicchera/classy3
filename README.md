# Program notes

- [Program notes](#program-notes)
  - [Handy tools](#handy-tools)
    - [grp](#grp)
  - [find \& replace](#find--replace)
    - [Executing Python Scripts With a Shebang – Real Python](#executing-python-scripts-with-a-shebang--real-python)
  - [Aho-Corasick - string searching algorithm that efficiently searches for multiple patterns in a text](#aho-corasick---string-searching-algorithm-that-efficiently-searches-for-multiple-patterns-in-a-text)
  - [GLOBS](#globs)
  - [Schema](#schema)
    - [Tips / tricks](#tips--tricks)
    - [Componentes](#componentes)
    - [Tools](#tools)
      - [json](#json)
      - [Vs Code](#vs-code)
        - [Used VS Code extensions](#used-vs-code-extensions)
    - [Reddit API](#reddit-api)
    - [Notes](#notes)
  - [Extensions](#extensions)
    - [Git Automator](#git-automator)
      - [Usage](#usage)
        - [Add all edited files to Git and commit them](#add-all-edited-files-to-git-and-commit-them)
        - [Add ONLY the current file to Git and commit it](#add-only-the-current-file-to-git-and-commit-it)
        - [Push local commits](#push-local-commits)
        - [Setup the auto-prefill for commit messages](#setup-the-auto-prefill-for-commit-messages)
    - [autoDocstring](#autodocstring)
      - [How to use](#how-to-use)
      - [Extension Settings](#extension-settings)
      - [Custom Docstring Templates](#custom-docstring-templates)
    - [Bookmarks](#bookmarks)
  - [globals](#globals)
  - [The table txt\_transforms](#the-table-txt_transforms)
    - [txt\_transforms explanation](#txt_transforms-explanation)
    - [The indices table](#the-indices-table)
  - [Índices de legibilidad](#índices-de-legibilidad)

## Handy tools

### grp

```bash
grep --include=\*.py  -rnw './' -e "search"
```

## find & replace

```bash
find /path/to/files -type f -exec sed -i 's/oldstring/new string/g' {} \;
```

### [Executing Python Scripts With a Shebang – Real Python](https://realpython.com/python-shebang/)

## Aho-Corasick - string searching algorithm that efficiently searches for multiple patterns in a text

-[WojciechMula/pyahocorasick: Python module (C extension and plain python) implementing Aho-Corasick algorithm](https://github.com/WojciechMula/pyahocorasick)

## [GLOBS](#globals)

## [Schema](https://github.com/chicchera/classy3/blob/main/config/db_schema.sql)

### Tips / tricks

- [~~To see how to import GLOBS only onece~~](https://stackoverflow.com/a/13034908/18511264)
- [GLOBS To see why it was changed](https://stackoverflow.com/a/15959638/18511264)
- [**Unravelling `global`**](https://snarky.ca/unravelling-global/)

### Componentes

- [Play sound in Python](https://pythonbasics.org/python-play-sound/#Play-sound-in-Python)
- [Click and Python: Build Extensible and Composable CLI Apps – **Real Python**](https://realpython.com/python-click/)
- [Welcome to Click — Click Documentation (8.1.x)](https://click.palletsprojects.com/en/8.1.x/)
  - [Nested commands — Click Documentation (8.0.x)](https://click.palletsprojects.com/en/8.0.x/quickstart/#nesting-commands)
  - [Click - Deferring subcommand registration – **Real Python**](https://realpython.com/python-click/#deferring-subcommand-registration)
  - [Must have arguments](https://pymbook.readthedocs.io/en/latest/click.html#must-have-arguments)
- [dateutil - powerful extensions to datetime — dateutil 2.8.2 documentation](https://dateutil.readthedocs.io/en/stable/)
  - Relative deltas, Generic parsing of dates, Timezone (tzinfo) implementations, etc.
- [Rich’s documentation](https://rich.readthedocs.io/en/stable/index.html)
  - [Standard Colors](https://rich.readthedocs.io/en/stable/appendix/colors.html)
  - [Styles](https://rich.readthedocs.io/en/stable/style.html)
  - INCOGNITO [Rich: Generate Rich and Beautiful Text in the Terminal with Python](https://towardsdatascience.com/rich-generate-rich-and-beautiful-text-in-the-terminal-with-python-541f39abf32e)
- [tqdm](https://pypi.org/project/tqdm/)
  - [Double Progress Bar in Python](https://stackoverflow.com/questions/23113494/double-progress-bar-in-python/38489852#38489852)
  - [Writing messages](https://pypi.org/project/tqdm/#writing-messages)
  - [Pandas Integration](https://pypi.org/project/tqdm/#pandas-integration)
  - valid colors **colour**: [hex (#00ff00), BLACK, RED,
    GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]

    ```python

    for recs in tqdm.tqdm(blocks, colour='cyan'):
        for i in tqdm.tqdm(range(recs), leave=False, colour='magenta'):
            sleep(0.0001)

    ```

### Tools

#### json

- [Convert INI to JSON Online - ConvertSimple.com](https://www.convertsimple.com/convert-ini-to-json/)
- [How do I add comments to JSON?](https://reqbin.com/json/5wzepqmt/json-comment-example)
- [SEE configparser — Configuration file parser — Python 3.11.3 documentation](https://docs.python.org/3/library/configparser.html)

#### Vs Code

- [Performance Issues · microsoft/vscode Wiki][def]
- [??? Reducing VSCode Memory Consumption](https://dev.to/claudiodavi/reducing-vscode-memory-consumption-527k)
- [11 Best VS Code extensions for Python (2022) | Towards the Cloud](https://towardsthecloud.com/best-vscode-extensions-python#2_Pylance)
- [Ignoring Errors with Flake8 — flake8 3.1.1 documentation](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html)
- [microsoft/pyright: Static Type Checker for Python](https://github.com/microsoft/pyright)

##### Used VS Code extensions

- [Bookmarks Extension for Visual Studio Code](#bookmarks)
- [GitAutomator](#git-automator)
- [autoDocstring](#autodocstring)
- [vscode-json-editor](https://github.com/sunmorgus/vscode-json-editor)
- [Copy Python Path](https://marketplace.visualstudio.com/items?itemName=mgesbert.python-path)
- [Python Type Hint](https://marketplace.visualstudio.com/items?itemName=njqdev.vscode-python-typehint)
- [Safurai - AI Assistant](https://marketplace.visualstudio.com/items?itemName=Safurai.Safurai)
- [Tabnine: AI assistant for software developers](https://github.com/codota/tabnine-vscode)
- [MagicPython - Formatter](https://marketplace.visualstudio.com/items?itemName=magicstack.MagicPython)
- [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
  - [**Todo Tree Configuration** | Highlighting Comments in VS Code](https://dev.to/koustav/how-a-vs-code-extension-todo-tree-can-make-your-coding-easier-todo-tree-configuration-and-use-cases-11kc)
  - BUG, COMMENT, FIXME, HACK, INCOMPLETE, LEARN, NOTE, POST, RECHECK, SEE NOTES, TODO, USEFUL, [ ], [x]

### Reddit API

Sure, here's an example code that uses the Pushshift API to extract submissions:

import requests

```# Set the API endpoint```
endpoint = '<https://api.pushshift.io/reddit/search/submission/>'

```# Set the parameters for the API request```
params = {
    'subreddit': 'example_subreddit', # Replace with the subreddit you want to search
    'size': 100, # Number of submissions to retrieve (max 1000)
    'after': '30d', # Retrieve submissions from the last 30 days
}

```# Make the API request```
response = requests.get(endpoint, params=params)

```# Get the submission data from the response```
submissions = response.json()['data']

```# Print the title of each submission```
for submission in submissions:
    print(submission['title'])

This code retrieves the 100 most recent submissions from the specified subreddit (change
example_subreddit
 to the subreddit you want to search), posted within the last 30 days. You can adjust the
size
 and
after
 parameters to retrieve more or fewer submissions, and to search for submissions posted within a different timeframe.

### Notes

- on runs

  - the first time is dealt with directly from PRAW and from there on with PSAW, just to get the ids to download as PRAW doesn't have the capability.
  - dates for extraction are read from the .ini file
  - if it is the first run and there is nothing to the contrary in the .ini file then the last 1.000 posts are downloaded
  - as there are defaults in the .ini file the would return false data, to check if it is a first run the values of **last_run** and **last_id** are checked

- on language

  - NLTK for the heavy lifting
  - spacy for the analisys
  - add a category for titles grams
  - grams are now:
        [T]itle
        [S]elfpost
        [C]omments
        [A]nalisys

- on ini files

  - to preserve the case in configparser see: <https://bit.ly/3MjUZhm>
  - to create it see: <https://bit.ly/3vz5BC9>

[def]: https://github.com/Microsoft/vscode/wiki/Performance-Issues

--------------------------

## Extensions

### [Git Automator](https://marketplace.visualstudio.com/items?itemName=ivangabriele.vscode-git-add-and-commit)

#### Usage

##### Add all edited files to Git and commit them

1. Hit Ctrl + Shift + A (PC) / Cmd + Shift + A (Mac).
2. Enter the commit message.
3. Press ENTER.

##### Add ONLY the current file to Git and commit it

1. Hit Ctrl + Shift + Z (PC) / Cmd + Shift + Z (Mac).
2. Enter the commit message.
3. Press ENTER.

##### Push local commits

- Hit Ctrl + Shift + X (PC) / Cmd + Shift + X (Mac).

##### Setup the auto-prefill for commit messages

1. Hit Ctrl + Shift + P (PC) / Cmd + Shift + P (Mac).
2. Look for Preferences: Open User Settings.
3. Look for gaac. settings to customize them.

:-------------------------;

### [autoDocstring](https://github.com/NilsJPWerner/autoDocstring/edit/master/README.md)

#### How to use

Cursor must be on the line directly below the definition to generate full auto-populated docstring

- Press enter after opening docstring with triple quotes (configurable `"""` or `'''`)
- Keyboard shortcut: `ctrl+shift+2` or `cmd+shift+2` for mac
  - Can be changed in Preferences -> Keyboard Shortcuts -> extension.generateDocstring
- Command: `Generate Docstring`
- Right click menu: `Generate Docstring`

#### Extension Settings

This extension contributes the following settings:

- `autoDocstring.docstringFormat`: Switch between different docstring formats
- `autoDocstring.customTemplatePath`: Path to a custom docstring template (absolute or relative to the project root)
- `autoDocstring.generateDocstringOnEnter`: Generate the docstring on pressing enter after opening docstring
- `autoDocstring.includeExtendedSummary`: Include extended summary section in docstring
- `autoDocstring.includeName`: Include function name at the start of docstring
- `autoDocstring.startOnNewLine`: New line before summary placeholder
- `autoDocstring.guessTypes`: Infer types from type hints, default values and variable names
- `autoDocstring.quoteStyle`: The style of quotes for docstrings

#### Custom Docstring Templates

[see ext. page](https://github.com/NilsJPWerner/autoDocstring/edit/master/README.md)
:----------------------------;

### Bookmarks

- `Bookmarks: Toggle` - **Ctl+Alt+K** Mark/unmark positions with bookmarks
- `Bookmarks: Toggle Labeled` Mark labeled bookmarks
- `Bookmarks: Jump to Next` - **Ctl+Alt+L** Move the cursor forward, to the bookmark below
- `Bookmarks: Jump to Previous` - **Ctl+Alt+J** Move the cursor backward, to the bookmark above
- `Bookmarks: List` List all bookmarks in the current file
- `Bookmarks: List from All Files` List all bookmarks from all files
- `Bookmarks: Clear` remove all bookmarks in the current file
- `Bookmarks: Clear from All Files` remove all bookmarks from all files
- `Bookmarks (Selection): Select Lines` Select all lines that contains bookmarks
- `Bookmarks (Selection): Expand Selection to Next` Expand the selected text to the next bookmark
- `Bookmarks (Selection): Expand Selection to Previous` Expand the selected text to the previous bookmark
- `Bookmarks (Selection): Shrink Selection` Shrink the select text to the Previous/Next bookmark

[see extension page](https://github.com/alefragnani/vscode-bookmarks)
:----------------------------;

## globals

The GLOBS dictionary is already creted at the end of th init function

```python
{
    'DB': {
        'local': '/home/silvio/data/test_classy3/classy4.db',
        'remote': '/home/silvio/data/redsdb/stats.db',
        'local_bak_path': '/home/silvio/classy3_bak',
        'remote_bak_path': '/home/silvio/classy3_bak',
        'dfr_db': '/home/silvio/.SomeGuySoftware/DownloaderForReddit/dfr.db',
        'dfr_alias': 'dfr'
    },
    'MISC': {
        'STOPWORDS': 'stopwords_es.txt',
        'DICTIONARY': {
            'use_alternate': False,
            'symspell': 'es-100l-dic.txt',
            'subtitle': 'subtl_es.txt'
        },
        'CLASSES': 'classy.json',
        '_CHUNK': 'CHUNK is used to define the number of records that form a
block to retrieve from the database',
        'CHUNK': 100000,
        '_POSTS_CHUNK': 'POSTS_CHUNK is used to define the number of retrieved
posts between saves in the database. As avg, each pots hase 10 comments and 5
new users',
        'POSTS_CHUNK': 10
    },
    'SUBREDS': [
        'askredditespanol',
        'cuentaleareddit',
        'espanol',
        'preguntaleareddit',
        'preguntareddit',
        'preguntasreddit',
        'preguntasreddit_extra',
        'redditpregunta',
        'vivimosenunasociedad',
        'historiasdeterror'
    ],
    'DOWNlOAD': {
        '_CUT_DATE': 'How many days before the actual date we want to stop
downloading to avoid having to go back later to add missing data',
        'CUT_DATE': 2
    },
    'REDDIT_PROFILE': 'SilvioWcloud',
    'PRG': {
        'PATHS': {
            'ROOT': '/home/silvio/miniconda3/envs/classy3/prg',
            'CONFIG_PATH': '/home/silvio/miniconda3/envs/classy3/prg/config',
            'LOGS_PATH': '/home/silvio/miniconda3/envs/classy3/prg/logs',
            'DATA_PATH': '/home/silvio/miniconda3/envs/classy3/prg/data',
            'PICKLES_PATH': '/home/silvio/miniconda3/envs/classy3/prg/pickles'
        }
    },
    'subreddits_data': None,
    'INITIALIZED': True
}

```

## The table txt_transforms

```python
CREATE TABLE IF NOT EXISTS "txt_transforms" (
    "id_submission" TEXT,
    "id_comment"    TEXT,
    "kind"  TEXT,
    "content"   TEXT,
    CONSTRAINT "category_FK" FOREIGN KEY("id_submission") REFERENCES "submissions"("id_submission") ON DELETE CASCADE,
    CONSTRAINT "category_FK2" FOREIGN KEY("id_comment") REFERENCES "comments"("id_comment") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_submission_comment" ON "txt_transforms" (
    "id_submission",
    "id_comment"
);
CREATE INDEX IF NOT EXISTS "idx_submission_comment_kind" ON "txt_transforms" (
    "id_submission",
    "id_comment",
    "kind"
);
CREATE INDEX IF NOT EXISTS "idx_submission_comment_kind_dups" ON "txt_transforms" (
    "id_submission",
    "id_comment",
    "kind",
    "dups"
);

```

### txt_transforms explanation

- txt_transforms
  - ~~the originals are kept in submissions and comments~~
  - originals are moved to this table as they are needed to calculate the legibility indexes
  - this table contains original as well as  normalized data
  - content of table contains sevral things, differentiated by the kind flag
- kind can be
  - OT title (original title)
  - OB body  (original self text / body)
  - TN title with original punctuation and no spelling mistakes
  - BN body with original punctuation and no spelling mistakes
  - PD poll data
  - TT title (normalized)
  - BB body  (self text / body normalized)
  - SP misspells (separated by spaces)
  - NS no stopwords
  - SS single stopwords (no repeated)

### The indices table

TODO: add kind and original to table?

```python
CREATE TABLE IF NOT EXISTS "indices" (
    "id_submission" TEXT,
    "id_comment"    TEXT,
    "kind"          TEXT,
    "paragraphs"    INTEGER,
    "sentences"     INTEGER,
    "syllables"     INTEGER,
    "num_words"     INTEGER,
    "distinct_words" INTEGER,
    "unique_words"  INTEGER,
    "misspells"     INTEGER,
    "enthropy"      NUMBER,
    "redundancy"    NUMBER,
    "densidad"      NUMBER,
    CONSTRAINT "category_FK" FOREIGN KEY("id_submission") REFERENCES "submissions"("id_submission") ON DELETE CASCADE,
    CONSTRAINT "category_FK2" FOREIGN KEY("id_comment") REFERENCES "comments"("id_comment") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS indices_id_submission_IDX ON indices (id_submission,id_comment,kind);




## From ChatGPT
- [UTC Date Functions](https://chat.openai.com/share/bfa9e861-a111-4667-9623-92597a62c82b)
- [Transfer data between databases](https://chat.openai.com/share/52a20488-5c6b-48a3-82e0-880dbb40dc13)
- [Eval](https://chat.openai.com/share/d16f743d-0ad3-45c6-b123-f4b2ffb2b5bb)
- [Check if sqlite table exists.](https://chat.openai.com/share/b9b79961-4d41-4c99-aae6-935a994c2325)
- PRAW
  - [Reddit PRAW Scraper.](https://chat.openai.com/share/1f9f508c-ac68-41e6-a67e-1352f9884313)
- [SQL Database Relationships](https://chat.openai.com/share/96027641-ef49-4b89-b62a-6df101dcd07e)
- [SQLite Batch Insert](https://chat.openai.com/share/52dc62b3-24c6-4864-8f6c-9177e34277b0)
- [Dicts for SQLite Insert](https://chat.openai.com/share/a0432bae-88a4-4cd6-a988-d51d55bcdd1c)
- [Get SQL column names (Python)](https://chat.openai.com/share/96448061-28a8-49ff-bbca-497afa138b50)

### Search for reverse index

According to the web search results, a reversed ordered query in SQLite can use a normal default ascending index, but it may not be very efficient. One way to do this is to use a subquery to select the desired rows in descending order, and then order them again in ascending order in the outer query¹². For example:

```sql
select * from
  (select * from raw_all_sensors order by timestamp desc limit 10) t
order by timestamp;
```

This query will return the last 10 records from the raw_all_sensors table in ascending order by timestamp. However, this method may require scanning the entire index or table to find the matching rows, which can be slow for large data sets³.

Another way to improve the performance of a reversed ordered query is to create a separate index with the opposite order of the default one. For example, if the default index is on timestamp ascending, you can create another index on timestamp descending³. Then, you can use the `INDEXED BY` clause to specify which index to use for your query⁴. For example:

```sql
create index idx_timestamp_desc on raw_all_sensors(timestamp desc);
select * from raw_all_sensors indexed by idx_timestamp_desc order by timestamp desc limit 10;
```

This query will use the idx_timestamp_desc index to quickly find the last 10 records from the raw_all_sensors table in descending order by timestamp. This method may require more storage space and maintenance for the additional index, but it can speed up the query execution³.

I hope this answer was helpful and informative. If you have any other questions, please feel free to ask me. 😊

Source: Conversation with Bing, 8/7/2023
(1) Reverse the order of the result set in SQLite - Stack Overflow. <https://stackoverflow.com/questions/10529764/reverse-the-order-of-the-result-set-in-sqlite>.
(2) SQLite3 output in reverse order latest 10 records - Stack Overflow. <https://stackoverflow.com/questions/71430445/sqlite3-output-in-reverse-order-latest-10-records>.
(3) SQLite - reverse string function - Stack Overflow. <https://stackoverflow.com/questions/7826876/sqlite-reverse-string-function>.
(4) java - Sort sqlite query in reverse order - Stack Overflow. <https://stackoverflow.com/questions/34027843/sort-sqlite-query-in-reverse-order>.

## Índices de legibilidad

- [Los índices de legibilidad: su importancia en SEO - IONOS](https://www.ionos.es/digitalguide/online-marketing/marketing-para-motores-de-busqueda/los-indices-de-legibilidad/)
- [Guía para usar la Calculadora de Índice de Legibilidad](https://jjdeharo.github.io/utilidades/legibilidad/instrucciones.html)
- [Herramienta para el Análisis de Legibilidad de Recursos de Texto: Aplicación en la Creación de Contenido Didáctico y su uso junto con ChatGPT – Bilateria](https://educacion.bilateria.org/analisis-de-legibilidad-de-recursos-escritos-importancia-y-aplicacion-en-la-creacion-de-contenido-didactico)
- [Fórmulas de legibilidad y comprensibilidad validadas y/o adaptadas para la lengua española.](https://www.siicsalud.com/imagenes/blancopet1.pdf)
- [Prueba de legibilidad de Flesch-Kincaid - Wikipedia, la enciclopedia libre](https://es.wikipedia.org/wiki/Prueba_de_legibilidad_de_Flesch-Kincaid)
- [Escala INFLESZ | Legible](https://legible.es/blog/escala-inflesz/)
- [Índice de perspicuidad de Szigriszt-Pazos | Legible](https://legible.es/blog/perspicuidad-szigriszt-pazos/)
- [Fórmula de Crawford | Legible - Años de escolaridad](https://legible.es/blog/formula-de-crawford/)
- [Fórmula de comprensibilidad de Gutiérrez de Polini | Legible](https://legible.es/blog/comprensibilidad-gutierrez-de-polini/)
- [Lecturabilidad de Fernández Huerta | Legible](https://legible.es/blog/lecturabilidad-fernandez-huerta/)
- [Error in the Fernandez Huerta Readability Formula - Linguist](https://linguistlist.org/issues/22/22-2332/)

- ### online

  - [Calculadora de Entropía, Redundancia y Densidad del Léxico](https://jjdeharo.github.io/utilidades/entropia/)
  - [Análisis de Legibilidad de recursos de texto](https://jjdeharo.github.io/utilidades/legibilidad/)
  - [Analizador de legibilidad de texto | Legible](https://legible.es/)
  - [Analizador de legibilidad de un texto (beta) | Legible](<https://legible.es/beta/>

- ### sources

  - [github - alejandromunozes/legibilidad: Spanish text readability calculation](https://github.com/alejandromunozes/legibilidad)
    - [legibilidad/README.rest at master · alejandromunozes/legibilidad](https://github.com/alejandromunozes/legibilidad/blob/master/README.rest)
    - [mabodo/sibilizador: Script python que intenta separar en silabas palabras en español](https://github.com/mabodo/sibilizador/tree/master)
    - [raw.githubusercontent.com/amunozf/separasilabas/master/separasilabas.py](https://raw.githubusercontent.com/amunozf/separasilabas/master/separasilabas.py)

- ### corrrectores autpmáticos

  - [Correctores automáticos de texto | Legible](https://legible.es/blog/correctores-automaticos/)
