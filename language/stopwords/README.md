# Stopwords handling

## Fastest (?) way to rremove stopwords

see: https://stackoverflow.com/a/55066343/18511264

- Create a dictionary of stopwords using collections library
- Use that dictionary for very fast search (time = O(1)) rather than doing it on list (time = O(stopwords))

```python
from collections import Counter
stop_words = stopwords.words('english')
stopwords_dict = Counter(stop_words)
text = ' '.join([word for word in text.split() if word not in stopwords_dict])
```

## Replace first letter of sentences with lowercase

You can use a regular expression to convert the first letter of each sentence or paragraph to lowercase. Here's an example using the `re` module in Python:

```python
import re

text = "This is a sample text. It has multiple sentences. Each sentence starts with an uppercase letter.\n\nThis is the second paragraph. It also starts with a capital letter."

# Define a pattern to match the first letter of a sentence or paragraph
pattern = re.compile(r"(?<=\. |^\s|^\n)\w")

# Use the pattern to convert the first letter to lowercase
modified_text = pattern.sub(lambda x: x.group().lower(), text)

print(modified_text)
```

In this code:

1. We define a regular expression pattern that matches the first letter of a sentence or paragraph. The pattern uses a positive lookbehind to match a period followed by a space, the start of a line with optional whitespace, or the start of a new line. This ensures that we target the first letter of each sentence or paragraph.

2. We use `pattern.sub()` to substitute the matched first letters with their lowercase counterparts.

The `modified_text` variable will contain the text with the first letter of each sentence or paragraph converted to lowercase. You can apply this to your longer texts with multiple paragraphs and sentences.


```
