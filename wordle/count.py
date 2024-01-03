"""
Save Wordle from its impending doom. Find more 5-letter words.
"""

import csv
import nltk
import string
import urllib.request
nltk.download('averaged_perceptron_tagger')


def read(fname):
    with open(fname) as f:
        return f.read().splitlines()


def fiveletters(words):
    return [word for word in words if len(word) == 5]


def propernouns(words):
    return [word for word, tag in nltk.tag.pos_tag(words)
            if tag not in ('NNP', 'NNPS')]


def report(name, words, dst, use_nltk=False):
    filtered = fiveletters(words)
    print(f"[{name}] {len(words)} => {len(filtered)}" + (
        f" => {len(propernouns(filtered))}" if use_nltk else ""))
    with open(dst, 'w') as f:
        for word in filtered:
            f.write(f"{word}\n")
    return set(filtered)


urllib.request.urlretrieve('https://www.mit.edu/~ecprice/wordlist.10000', 'raw-mit.txt')
mit = report('mit', read('raw-mit.txt'), 'out-mit.txt', use_nltk=True)
MIT = report('MIT', [w.title() for w in read('raw-mit.txt')], 'out-MIT.txt', use_nltk=True)

unix = report('Unix', read('/usr/share/dict/words'), 'out-unix.txt', use_nltk=True)


def read_websters(fname):
    words = set()

    pos_line = False
    for line in read(fname):
        if pos_line:
            line = remove_etymology(line)
            words.update(extract_plural(line))
            words.update(extract_conjugations(line))
            pos_line = False
        if is_valid_entry(line):
            pos_line = True
            words.add(line)

    return words


def is_valid_entry(line):
    return line and line.upper() == line and all(c in string.ascii_letters for c in line)


def remove_etymology(line):
    return line.split('Etym:')[0] if 'Etym:' in line else line


def extract_plural(line):
    if 'pl.' in line and not line.strip().endswith('pl.'):
        parts = line.split('pl.', 1)[1]
        word = parts.split('.', 1)[0].strip()
        cleaned = word.split(';')[0].split(' ')[0]
        return {cleaned}
    return set()


def extract_conjugations(line):
    words = set()
    if '[' in line and ']' in line:
        word = None
        insides = line.split('[')[1].split(']')[0]
        if any(pos in insides for pos in ('imp.', 'p.p.', 'p.pr.', 'vb.', 'superl.', 'Comp.')):
            sections = insides.split(';') if ';' in insides else insides.split(',')
            for section in sections:
                word = section.split(' ')[-1].replace('.', '')
                words.add(word)
    return words


urllib.request.urlretrieve('https://www.gutenberg.org/cache/epub/29765/pg29765.txt', 'raw-websters.txt')
websters = report('websters', read_websters('raw-websters.txt'), 'out-websters.txt')
websters = {w.lower() for w in websters}


def read_norvig(path):
    words = []
    with open(path) as f:
        for line in csv.reader(f, delimiter='\t'):
            word, count = line
            word = word.lower()
            if len(word) == 5 and word in websters:
                words.append(word)
                if int(count) < 1000000 or len(words) > 1400:
                    break
    return words


urllib.request.urlretrieve('https://norvig.com/ngrams/count_1w.txt', 'raw-norvig.txt')
norvig = report('norvig', read_norvig('raw-norvig.txt'), 'out-norvig.txt')


def read_knuth(path):
    with open(path) as f:
        words = []
        for line in csv.reader(f):
            word = line[0].lower()
            if len(words) > 2300:
                break
            if len(word) == 5 and word in websters:
                words.append(word)
    return words


urllib.request.urlretrieve('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt', 'raw-knuth.txt')
knuth = report('knuth', read_knuth('raw-knuth.txt'), 'out-knuth.txt')


urllib.request.urlretrieve('https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/45c977427419a1e0edee8fd395af1e0a4966273b/wordle-answers-alphabetical.txt', 'wordle-answers.txt')
answers = set(read('wordle-answers.txt'))

print(f"[Wordle] original: {len(answers)}")

v2 = answers | knuth | norvig
print(f"[Wordle] with ours: {len(v2)}")