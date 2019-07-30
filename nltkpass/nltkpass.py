import nltk
from pathlib import Path
import string
import dataclasses as dc
from secrets import SystemRandom


@dc.dataclass
class PassObject:
    password: str
    sentence: str


class NltkPass:
    tagged_sents: set
    rare: dict
    common: set
    rand = SystemRandom()

    def __init__(self):
        self.tagged_sents = set()
        self.rare = dict()

        self.common = set(Path("common/20k.txt").read_text().strip().split("\n"))
        self.common.update(Path("common/100k.txt").read_text().strip().split("\n"))

    def add_source(self, tagged_source: str):
        corpus = getattr(nltk.corpus, tagged_source)
        for tagged_sent in corpus.tagged_sents():
            for word, pos in tagged_sent:
                # clean = re.sub(r"[^A-Za-z]", "", word)
                clean = word

                if len(word) > 3 and any(c.isalpha() for c in clean):
                    clean = clean.lower()

                    if clean not in self.common:
                        if pos not in self.rare.keys():
                            self.rare[pos] = set()

                        self.rare[pos].add(word)

            self.tagged_sents.add(tuple(tagged_sent))

    def generate_sentence(self, rare_count: int = 5, specificity: int = None) -> str:
        tss = list(self.tagged_sents)

        self.rand.shuffle(tss)

        tss_i = 0
        rare_i = 0
        output = list()

        while rare_i < rare_count:
            ts = list(tss[tss_i])
            ts_map = dict()

            for i, (word, pos) in enumerate(ts):
                pos = pos[:specificity]
                ts_map.setdefault(pos, dict())
                ts_map[pos][i] = word

            for ts_pos, ts_value in ts_map.items():
                for pos, word_set in self.rare.items():
                    if pos[:specificity] == ts_pos:
                        ts_i, _ = self.rand.choice(tuple(ts_value.items()))
                        ts[ts_i] = (self.rand.choice(tuple(word_set)), f"{pos}_RAND")
                        rare_i += 1

                        break

            output.append(ts)
            tss_i += 1

        return " ".join(" ".join(tp[0] for tp in sent) for sent in output)

    def generate_password(self, s: str = None, punctuation_count: int = 2, digit_count: int = 2) -> PassObject:
        if s is None:
            s = self.generate_sentence()

        words = [w for w in s.split(" ") if any(c.isalpha() for c in w)]

        for c in "".join(words):
            if c in string.punctuation:
                punctuation_count -= 1
            elif c in string.digits:
                digit_count -= 1

        n = 0
        while n < punctuation_count:
            position = self.rand.randrange(len(words) + 1)
            words.insert(position, self.rand.choice(string.punctuation))

            n += 1

        n = 0
        while n < digit_count:
            position = self.rand.randrange(len(words) + 1)
            words.insert(position, self.rand.choice(string.digits))

            n += 1

        for i, w in enumerate(words):
            if not self.is_rare(w):
                w = w[0]

            if i > 0:
                if words[i-1][-1].islower() and w[0].islower():
                    words[i] = w[0].upper() + w[1:]
                elif words[i-1][-1].isupper() and w[0].isupper():
                    words[i] = w[0].lower() + w[1:]
                else:
                    words[i] = w

        return PassObject(
            password="".join(words),
            sentence=s
        )

    def is_rare(self, w: str) -> bool:
        for k, v in self.rare.items():
            if w in v:
                return True

        return False
