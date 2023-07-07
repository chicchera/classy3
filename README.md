# Program notes
### hany tools
#### grp
-  ```grep --include=\*.py  -rnw './' -e "search"```
### [GLOBS](#globals)

### [Executing Python Scripts With a Shebang – Real Python](https://realpython.com/python-shebang/)

## Used extensions

- [Bookmarks Extension for Visual Studio Code](#bookmarks)
- [GitAutomator](#git-automator)
- [autoDocstring](#autodocstring)
- [vscode-json-editor](https://github.com/sunmorgus/vscode-json-editor)
- [Copy Python Path](https://marketplace.visualstudio.com/items?itemName=mgesbert.python-path)
- [Python Type Hint ](https://marketplace.visualstudio.com/items?itemName=njqdev.vscode-python-typehint)
- [Safurai - AI Assistant](https://marketplace.visualstudio.com/items?itemName=Safurai.Safurai)
- [Tabnine: AI assistant for software developers](https://github.com/codota/tabnine-vscode)
- [MagicPython - Formatter](https://marketplace.visualstudio.com/items?itemName=magicstack.MagicPython)
- [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
  - [**Todo Tree Configuration** | Highlighting Comments in VS Code](https://dev.to/koustav/how-a-vs-code-extension-todo-tree-can-make-your-coding-easier-todo-tree-configuration-and-use-cases-11kc)
  -  BUG, COMMENT, FIXME, HACK, INCOMPLETE, LEARN, NOTE, POST, RECHECK, SEE NOTES, TODO, USEFUL, [ ], [x]
### Tips / tricks
- [~~To see how to import GLOBS only onece~~](https://stackoverflow.com/a/13034908/18511264)
- [GLOBS To see why it was changed](https://stackoverflow.com/a/15959638/18511264)
- [**Unravelling `global`**](https://snarky.ca/unravelling-global/)

### Componentes
- [Welcome to Click — Click Documentation (8.1.x)](https://click.palletsprojects.com/en/8.1.x/)
  - [Building command line applications with Click — Python for you and me 0.5.beta1 documentation](https://pymbook.readthedocs.io/en/latest/click.html#must-have-arguments)
- [dateutil - powerful extensions to datetime — dateutil 2.8.2 documentation](https://dateutil.readthedocs.io/en/stable/)
    + Relative deltas, Generic parsing of dates, Timezone (tzinfo) implementations, etc.
- [Rich’s documentation](https://rich.readthedocs.io/en/stable/index.html)
  - [Standard Colors](https://rich.readthedocs.io/en/stable/appendix/colors.html)
  - [Styles](https://rich.readthedocs.io/en/stable/style.html)
  - INCOGNITO [Rich: Generate Rich and Beautiful Text in the Terminal with Python](https://towardsdatascience.com/rich-generate-rich-and-beautiful-text-in-the-terminal-with-python-541f39abf32e)
- [tqdm · PyPI](https://pypi.org/project/tqdm/)
  - [Double Progress Bar in Python](https://stackoverflow.com/questions/23113494/double-progress-bar-in-python/38489852#38489852)
  - [Writing messages](https://pypi.org/project/tqdm/#writing-messages)
  - [Pandas Integration](https://pypi.org/project/tqdm/#pandas-integration)
  - valid colors **colour**: [hex (#00ff00), BLACK, RED,
    GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]

    ```

    for recs in tqdm.tqdm(blocks, colour='cyan'):
        for i in tqdm.tqdm(range(recs), leave=False, colour='magenta'):
            sleep(0.0001)

    ```
### Tools
- json
    - [Convert INI to JSON Online - ConvertSimple.com](https://www.convertsimple.com/convert-ini-to-json/)
    - [How do I add comments to JSON?](https://reqbin.com/json/5wzepqmt/json-comment-example)
    - [SEE configparser — Configuration file parser — Python 3.11.3 documentation](https://docs.python.org/3/library/configparser.html)
- Vs Code
    - [Performance Issues · microsoft/vscode Wiki][def]
    - [??? Reducing VSCode Memory Consumption](https://dev.to/claudiodavi/reducing-vscode-memory-consumption-527k)
    - [11 Best VS Code extensions for Python (2022) | Towards the Cloud](https://towardsthecloud.com/best-vscode-extensions-python#2_Pylance)
    - [Ignoring Errors with Flake8 — flake8 3.1.1 documentation](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html)
    - [microsoft/pyright: Static Type Checker for Python](https://github.com/microsoft/pyright)

### Reddit API
Sure, here's an example code that uses the Pushshift API to extract submissions:

import requests

```# Set the API endpoint```
endpoint = 'https://api.pushshift.io/reddit/search/submission/'

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
### <u>Notes</u>


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

    - to preserve the case in configparser see: https://bit.ly/3MjUZhm
    - to create it see: https://bit.ly/3vz5BC9


[def]: https://github.com/Microsoft/vscode/wiki/Performance-Issues

--------------------------
# Extensions

## [Git Automator](https://marketplace.visualstudio.com/items?itemName=ivangabriele.vscode-git-add-and-commit)

### Usage
#### Add all edited files to Git and commit them
1. Hit Ctrl + Shift + A (PC) / Cmd + Shift + A (Mac).
2. Enter the commit message.
3. Press ENTER.
#### Add ONLY the current file to Git and commit it
1. Hit Ctrl + Shift + Z (PC) / Cmd + Shift + Z (Mac).
2. Enter the commit message.
3. Press ENTER.
#### Push local commits
- Hit Ctrl + Shift + X (PC) / Cmd + Shift + X (Mac).
#### Setup the auto-prefill for commit messages
1. Hit Ctrl + Shift + P (PC) / Cmd + Shift + P (Mac).
2. Look for Preferences: Open User Settings.
3. Look for gaac. settings to customize them.
-------------------------
## [autoDocstring](https://github.com/NilsJPWerner/autoDocstring/edit/master/README.md)
### Features

-   Quickly generate a docstring snippet that can be tabbed through.
-   Choose between several different types of docstring formats.
-   Infers parameter types through pep484 type hints, default values, and var names.
-   Support for args, kwargs, decorators, errors, and parameter types
### Usage

Cursor must be on the line directly below the definition to generate full auto-populated docstring

-   Press enter after opening docstring with triple quotes (configurable `"""` or `'''`)
-   Keyboard shortcut: `ctrl+shift+2` or `cmd+shift+2` for mac
    -   Can be changed in Preferences -> Keyboard Shortcuts -> extension.generateDocstring
-   Command: `Generate Docstring`
-   Right click menu: `Generate Docstring`

### Extension Settings

This extension contributes the following settings:

-   `autoDocstring.docstringFormat`: Switch between different docstring formats
-   `autoDocstring.customTemplatePath`: Path to a custom docstring template (absolute or relative to the project root)
-   `autoDocstring.generateDocstringOnEnter`: Generate the docstring on pressing enter after opening docstring
-   `autoDocstring.includeExtendedSummary`: Include extended summary section in docstring
-   `autoDocstring.includeName`: Include function name at the start of docstring
-   `autoDocstring.startOnNewLine`: New line before summary placeholder
-   `autoDocstring.guessTypes`: Infer types from type hints, default values and variable names
-   `autoDocstring.quoteStyle`: The style of quotes for docstrings
### Custom Docstring Templates

[see ext. page](https://github.com/NilsJPWerner/autoDocstring/edit/master/README.md)
----------------------------
### Bookmarks

* `Bookmarks: Toggle` - **Ctl+Alt+K** Mark/unmark positions with bookmarks
* `Bookmarks: Toggle Labeled` Mark labeled bookmarks
* `Bookmarks: Jump to Next` - **Ctl+Alt+L** Move the cursor forward, to the bookmark below
* `Bookmarks: Jump to Previous` - **Ctl+Alt+J** Move the cursor backward, to the bookmark above
* `Bookmarks: List` List all bookmarks in the current file
* `Bookmarks: List from All Files` List all bookmarks from all files
* `Bookmarks: Clear` remove all bookmarks in the current file
* `Bookmarks: Clear from All Files` remove all bookmarks from all files
* `Bookmarks (Selection): Select Lines` Select all lines that contains bookmarks
* `Bookmarks (Selection): Expand Selection to Next` Expand the selected text to the next bookmark
* `Bookmarks (Selection): Expand Selection to Previous` Expand the selected text to the previous bookmark
* `Bookmarks (Selection): Shrink Selection` Shrink the select text to the Previous/Next bookmark

[see extension page](https://github.com/alefragnani/vscode-bookmarks)
----------------------------
### globals

```
{   'DB': {   'CREATE_DB': True,
              'local': '/home/silvio/data/test_classyred/classyred.db',
              'local_bak_path': '~/classyred_bak',
              'remote': '/home/silvio/.SomeGuySoftware/DownloaderForReddit/dfr.db',
              'remote_bak_path': '~/classyred_bak'},
    'MISC': {'CLASSES': 'classy.json', 'STOPWORDS': 'stopwords_es.txt'},
    'PRG': {   'PATHS': {   'CONFIG_PATH': '/home/silvio/miniconda3/envs/classy3/prg/config',
                            'DATA_PATH': '/home/silvio/miniconda3/envs/classy3/prg/data',
                            'LOGS_PATH': '/home/silvio/miniconda3/envs/classy3/prg/logs',
                            'PICKLES_PATH': '/home/silvio/miniconda3/envs/classy3/prg/pickles',
                            'ROOT': '/home/silvio/miniconda3/envs/classy3/prg'}},
    'SUBREDS': [   'r/AskRedditEspanol',
                   'r/Espanol',
                   'r/PreguntaleAReddit',
                   'r/PreguntaReddit']}
```


