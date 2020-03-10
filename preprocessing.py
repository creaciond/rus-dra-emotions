from pymystem3 import Mystem
from tqdm import tqdm
import os
import warnings


warnings.simplefilter("ignore")


def extract_lemmas(lines_raw, mystem):
    """Performs lemmatization. Each word is converted to its 'normal form' (nouns -> Nom.sg, etc.)

    :arg lines - (list of str) list of particular play's directions the
    way they were extracted from the text
    :arg mystem - an instance of Mystem, morphological analyzer, part of
    pymoystem3 module (a Python wrapper for the original programme)

    :returns lines_lemmatized - (list of str) same lines yet converted to
    their lemmas"""
    lines_lemmatized = []
    for line_raw in lines_raw:
        words_analyses = mystem.analyze(line_raw)
        line_lemmas = " ".join([parse["analysis"][0]["lex"] for parse in words_analyses if parse.get("analysis")])
        lines_lemmatized.append(line_lemmas)
    return lines_lemmatized


def main():
    mystem = Mystem()
    spoken_folder = "./data/rusdracor/spoken"
    spoken_lemmas_folder = spoken_folder + "_lemmas"
    for file in tqdm([f for f in os.listdir(spoken_folder) if f.endswith(".txt")]):
        with open(os.path.join(spoken_folder, file), "r", encoding="utf-8") as f_raw:
            lines_raw = f_raw.readlines()
        lines_lemmas = extract_lemmas(lines_raw, mystem)
        with open(os.path.join(spoken_lemmas_folder, file), "w", encoding="utf-8") as f_lemmas:
            f_lemmas.write("\n".join(lines_lemmas))

    stage_folder = "./data/rusdracor/stage"
    stage_lemmas_folder = stage_folder + "_lemmas"
    for file in tqdm([f for f in os.listdir(stage_folder) if f.endswith(".txt")]):
        with open(os.path.join(stage_folder, file), "r", encoding="utf-8") as f_raw:
            lines_raw = f_raw.readlines()
        lines_lemmas = extract_lemmas(lines_raw, mystem)
        with open(os.path.join(stage_lemmas_folder, file), "w", encoding="utf-8") as f_lemmas:
            f_lemmas.write("\n".join(lines_lemmas))


if __name__ == "__main__":
    main()
