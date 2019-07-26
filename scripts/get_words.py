import nltk
import requests
from pathlib import Path
import re


def get_words(src: str, target: str):
    r = requests.get("https://github.com/first20hours/google-10000-english/blob/master/20k.txt?raw=true")
    common = set(r.text.strip().split("\n"))

    r = requests.get("https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt?raw=true")
    common.update(r.text.strip().split("\n"))

    target_path = Path(target)
    pre_existing = set(target_path.read_text().strip().split("\n")) if target_path.exists() else set()

    corpus = getattr(nltk.corpus, src)
    for file_id in corpus.fileids():
        for word in corpus.words(file_id):
            word = re.sub(r"[^A-Za-z0-9]", "", word)

            if len(word) > 3 and any(c.isalpha() for c in word):
                word = word.lower()

                if word not in common:
                    pre_existing.add(word)

    target_path.write_text("\n".join(sorted(pre_existing)))


if __name__ == "__main__":
    get_words("gutenberg", "../rare.txt")
