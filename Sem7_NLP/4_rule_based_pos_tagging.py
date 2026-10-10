import re


class POS:

    name: str
    short_name: str

    def __init__(self, name: str = "", short_name: str = ""):
        self.name = name
        self.short_name = short_name


class Rule:

    pos: POS
    re: list[str]

    def __init__(self, pos: POS = None, re: list[str] = None):
        self.pos = pos
        self.re = re if re is not None else []


def identify(rules: list[Rule], sentence: str) -> dict[str, POS]:

    dictionary = {}

    # extract words and punctuation as separate tokens.
    tokens = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[.,!?;:]", sentence)

    for token in tokens:

        # ignore punctuation for POS tagging.
        if re.fullmatch(r"[.,!?;:]", token):
            continue

        assigned_pos = None

        for rule in rules:
            for pattern in rule.re:

                # re.IGNORECASE makes morphological rules case-independent.
                if re.fullmatch(pattern, token, flags=re.IGNORECASE):
                    assigned_pos = rule.pos
                    break

            if assigned_pos is not None:
                break

        # if no rule matches, leave the word as unknown.
        if assigned_pos is None:
            assigned_pos = POS("Unknown", "UNK")

        dictionary[token] = assigned_pos

    return dictionary


if __name__ == "__main__":

    VERB = POS("Verb", "VB")
    NOUN = POS("Noun", "NN")
    ADJECTIVE = POS("Adjective", "JJ")
    ADVERB = POS("Adverb", "RB")
    PRONOUN = POS("Pronoun", "PRP")
    DETERMINER = POS("Determiner", "DT")
    PREPOSITION = POS("Preposition", "IN")
    CONJUNCTION = POS("Conjunction", "CC")
    AUXILIARY = POS("Auxiliary Verb", "AUX")
    UNKNOWN = POS("Unknown", "UNK")

    # rules
    rules = [
        Rule(
            DETERMINER,
            [
                r"the|an|a|"
            ]
        ),
        Rule(
            VERB,
            [
                r".+ing"
            ]
        ),
        Rule(
            VERB,
            [
                r".+ed"
            ]
        ),
        Rule(
            VERB,
            [
                r".+(?:s|es)$"
            ]
        ),
        Rule(
            ADVERB,
            [
                r".+ly"
            ]
        ),
        Rule(
            ADJECTIVE,
            [
                r".+(?:ful|less|ous)$"
            ]
        ),
        Rule(
            ADJECTIVE,
            [
                r".+(?:ive|able|ible)$"
            ]
        ),
        Rule(
            ADJECTIVE,
            [
                r".+(?:al|ic)$"
            ]
        ),
        Rule(
            NOUN,
            [
                r".+ness"
            ]
        ),
        Rule(
            NOUN,
            [
                r".+ment"
            ]
        ),
        Rule(
            NOUN,
            [
                r".+(?:er|or)$"
            ]
        ),
        Rule(
            NOUN,
            [
                r".+(?:ies|es|s)$"
            ]
        ),
        Rule(
            PRONOUN,
            [
                r".*(?:self|selves)$"
            ]
        ),
        Rule(
            NOUN,
            [
                r"[A-Z][a-z]+"
            ]
        ),
    ]


    sentence: str = "The boy liked the girl."

    dictionary = identify(
        rules=rules,
        sentence=sentence
    )

    # display result
    for key in dictionary.keys():
        pos = dictionary[key]
        print(f"{key}: {pos.name}")
