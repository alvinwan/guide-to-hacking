"""
Save Wordle from its impending doom. Find more 5-letter words.
"""

import nltk
import urllib.request
nltk.download('averaged_perceptron_tagger')


def read(fname):
    with open(fname) as f:
        return f.read().splitlines()


def report(name, words, dst):
    step2 = [word for word in words if len(word) == 5]
    step3 = [word for word, tag in nltk.tag.pos_tag(words)
             if tag not in ('NNP', 'NNPS')]
    print(f"[{name}] {len(words)} => {len(step2)} => {len(step3)}")
    with open(dst, 'w') as f:
        for word in step2:
            f.write(f"{word}\n")
    return set(step2)


urllib.request.urlretrieve('https://www.mit.edu/~ecprice/wordlist.10000', 'raw-mit.txt')
mit = report('mit', read('raw-mit.txt'), 'out-mit.txt')
MIT = report('MIT', [w.title() for w in read('raw-mit.txt')], 'out-MIT.txt')

unix = report('Unix', read('/usr/share/dict/words'), 'out-unix.txt')
