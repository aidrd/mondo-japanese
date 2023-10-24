
from nltk.tokenize import word_tokenize
import sys
import re
import csv
from pronto import Ontology

def load_mondo_obo(filename):
    dict_mondo_label = {}
    dict_mondo_synonym = {}
    ont = Ontology(filename)
    for term in ont.terms():
        # exclude obsolete classes
        if term.obsolete:
            continue

        id_mondo = term.id
        label = term.name

        if id_mondo in dict_mondo_label:
            (dict_mondo_label[id_mondo]).append(label)
        else:
            dict_mondo_label[id_mondo] = []
            (dict_mondo_label[id_mondo]).append(label)

        # exclude the synonyms those SynonymType is "ABBREVIATION" or "EXCLUDE" or "DEPRECATED" or "AMBIGUOUS" or "DUBIOUS" or "MISSPELLING"
        for synonym in term.synonyms:
            if re.search(r"ABBREVIATION", str(synonym.type)) or re.search(r"EXCLUDE", str(synonym.type)) or re.search(r"DEPRECATED", str(synonym.type)) or re.search(r"AMBIGUOUS", str(synonym.type)) or re.search(r"DUBIOUS", str(synonym.type)) or re.search(r"MISSPELLING", str(synonym.type)):
                continue

            if id_mondo in dict_mondo_synonym:
                (dict_mondo_synonym[id_mondo]).append(synonym.description)
            else:
                dict_mondo_synonym[id_mondo] = []
                (dict_mondo_synonym[id_mondo]).append(synonym.description)

    return dict_mondo_label, dict_mondo_synonym


def main():

    dict_mondo_label, dict_mondo_synonym = load_mondo_obo(sys.argv[1])

    for id_mondo in sorted(dict_mondo_label.keys()):
        for label in list(set(dict_mondo_label[id_mondo])):
            tokens = word_tokenize(label.replace(',', ''))
            tokens_sorted = sorted(tokens)
            print(id_mondo + "\tlabel\t" + label + "\t" + " ".join(tokens_sorted))

        if id_mondo in dict_mondo_synonym:
            for synonym in list(set(dict_mondo_synonym[id_mondo])):
                tokens = word_tokenize(synonym.replace(',', ''))
                tokens_sorted = sorted(tokens)
                #print(id_mondo + "\tlabel\t" + synonym + "\t" + " ".join(tokens_sorted))
                print(id_mondo + "\tsynonym\t" + synonym + "\t" + " ".join(tokens_sorted))


if __name__ == '__main__':
    main()
