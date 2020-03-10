import json
import requests
import os

from pymystem3 import Mystem
from tqdm import tqdm

import warnings
warnings.simplefilter("ignore")

def get_play_names(corpus):
    """Makes a request to RusDraCor API to get all play names (used as ids).
    
    :arg corpus - (str) an API corpus ID to send the request
    :returns play_names - (list of str) ids for all the plays currently present in the
    corpus"""
    play_names = []
    request_url = "https://dracor.org/api/corpora/{}".format(corpus)
    response = requests.get(request_url)
    if response:
        all_plays = response.json()["dramas"]
        for play in all_plays:
            play_names.append(play["name"])
    return play_names


def prepare_folders():
    """Makes folders for further work."""
    folder_list = ["./data", "./data/stage", "./data/spoken", "./data/stage_lemmas", "./data/spoken_lemmas"]
    for folder in folder_list:
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"Created folder {folder}")
        else:
            print(f"Folder {folder} already existed")


def get_play_text_by_type(play_name, text_type):
    """Uses an API request to get spoken/stage direction text.
    
    :arg play_name (str) - name of a play to work with
    :arg text_type (str) - "spoken" or "stage"
    
    :returns text_type_lines (list of str) - strings of texts of a given type
    to work with later
    """
    if text_type == "spoken":
        request_url = "https://dracor.org/api/corpora/rus/play/{}/spoken-text".format(play_name)
    elif text_type == "stage":
        request_url = "https://dracor.org/api/corpora/rus/play/{}/stage-directions".format(play_name)
    response = requests.get(request_url)
    if response:
        return response.text.split("\n")
    else:
        return []


def download_play(play_name, text_type, type_folder):
    """Dowloads a play by type of the text (spoken/stage direction) and saves it.

    :arg play_name (str) - name of a play to work with
    :arg text_type (str) - "spoken" or "stage"
    :arg type_folder (str) - folder to save the results to
    """
    play_text_type = get_play_text_by_type(play_name, text_type)
    play_type_path = type_folder + "/{}.txt".format(play_name)
    with open(play_type_path, "w", encoding="utf-8") as f:
        f.write("\n".join(play_text_type))


def extract_lemmas(lines_raw, mystem):
    """Performs lemmatization. Each word is converted to its 'normal form' (nouns -> Nom.sg, etc.)
    
    :arg lines (list of str) - list of particular play's directions the
    way they were extracted from the text
    :arg mystem (pymystem3.Mystem) - an instance of Mystem, morphological analyzer, part of
    pymoystem3 module (a Python wrapper for the original programme)
    
    :returns lines_lemmatized (list of str) - same lines yet converted to
    their lemmas"""
    lines_lemmatized = []
    for line_raw in lines_raw:
        words_analyses = mystem.analyze(line_raw)
        line_lemmas = " ".join([parse["analysis"][0]["lex"] for parse in words_analyses if parse.get("analysis")])
        lines_lemmatized.append(line_lemmas)
    return lines_lemmatized


if __name__ == "__main__":
    prepare_folders()
    play_names = get_play_names("rus")

    mystem = Mystem()
    
    stage_folder = "./data/rusdracor/stage_raw"
    spoken_folder = "./data/rusdracor/spoken_raw"

    for play in play_names:
        print("Dowloading play: {}".format(play))
        download_play(play, "stage", stage_folder)
        download_play(play, "spoken", spoken_folder)

        with open(os.path.join(spoken_folder, file), "r", encoding="utf-8") as f_raw:
            lines_raw = f_raw.readlines()
        lines_lemmas = extract_lemmas(lines_raw, mystem)
        with open(os.path.join(spoken_folder.replace("raw", "lemmas"), file), "w", encoding="utf-8") as f_lemmas:
            f_lemmas.write("\n".join(lines_lemmas))

        with open(os.path.join(stage_folder, file), "r", encoding="utf-8") as f_raw:
            lines_raw = f_raw.readlines()
        lines_lemmas = extract_lemmas(lines_raw, mystem)
        with open(os.path.join(stage_folder.replace("raw", "lemmas"), file), "w", encoding="utf-8") as f_lemmas:
            f_lemmas.write("\n".join(lines_lemmas))

