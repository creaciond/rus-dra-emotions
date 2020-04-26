import os

import numpy as np
import pandas as pd

from pymystem3 import Mystem
from tqdm import tqdm

import warnings
warnings.simplefilter("ignore")


def prepare_lexicons():
    """Loads lexicons for the experiment.
    
    :returns lexicons_dict (dict) - dictionary with all lexicons used
    """
    path_to_lexicons = "./data/sentiment_datasets"
    lexicons = [lex[:-4] for lex in os.listdir(path_to_lexicons) if lex.endswith(".csv")]
    lexicons_dict = {}
    for lexicon in lexicons:
        lex_df = pd.read_csv("./data/sentiment_datasets/{}.csv".format(lexicon), sep=";", encoding="utf-8")
        lexicons_dict[lexicon] = lex_df
    return lexicons_dict


def load_plays():
    """Loads play list for the experiment.
    
    :returns play_list (str) - list of RusDraCor plays for the experiment
    """
    with open("./data/rusdracor_list.txt", "r", encoding="utf-8") as f:
        play_list = [play.strip("\n") for play in f.readlines()]
    return play_list


def evaluate_phrase_polarity(phrase, lexicon, mystem):
    """Calculates polarity for the whole phrase.
    
    :arg phrase (str) - phrase to evaluate
    :arg lexicon (pandas.DataFrame) - lexicon to check the lemmas
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer
    
    :returns sign(phrase_sum) (int) - calculated polarity
    """
    sign = lambda x: x and (1, -1)[x < 0]
    phrase_sum = 0
    lemmas = [parse["analysis"][0]["lex"] for parse in mystem.analyze(phrase) if parse.get("analysis")]
    for lemma in lemmas:
        if lemma in lexicon["lemma"].values:
            lemma_polarity = lexicon[lexicon["lemma"] == lemma].iloc[0]["sentiment"]
            phrase_sum += lemma_polarity
    return sign(phrase_sum)


def analyse_line_all_lexicons(dict_by_line, play_name, line_type, phrases, lexicons_dict, mystem):
    """Analyses one line against all lexicons, saves changes to a dataframe.
    
    :arg dict_by_line (dict) - storage for all results
    :arg play_name (str)
    :arg line_type (str) - spoken/stage
    :arg phrases (list of str) - lines to analyse
    :arg lexicons_dict (dict) - storage of all lexicons
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer
    
    :returns dict_by_line (dict) - parsed lines
    """
    for phrase in phrases:
        dict_by_line["play"].append(play_name)
        dict_by_line["line type"].append(line_type)
        dict_by_line["line"].append(phrase)
        phrase_lemmas = " ".join([parse["analysis"][0]["lex"] for parse in mystem.analyze(phrase) if parse.get("analysis")])
        dict_by_line["line, lemmas"].append(phrase_lemmas)
        for lexicon_name in lexicons_dict.keys():
            lexicon = lexicons_dict[lexicon_name]
            polarity = evaluate_phrase_polarity(phrase_lemmas, lexicon, mystem)
            dict_by_line[lexicon_name].append(polarity)
    return dict_by_line


def pipeline_analysis_by_line(lexicons_dict, play_list, mystem):
    """Pipeline for analysing plays line-by-line.

    :arg lexicons_dict (dict) - lexicons to use
    :arg play_list (list of str)
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns None
    """
    dict_by_line = {
        "play": [],
        "line": [],
        "line, lemmas": [],
        "line type": [],
        "RuSentiLex": [],
        "EmoLex": [], 
        "LinisCrowd": [],
        "ChenSkiena": [], 
        "ProductSentiRus": []
    }
    for play_name in tqdm(play_list):
        # load drama lines
        with open("./data/rusdracor/spoken_raw/{}.txt".format(play_name), "r", encoding="utf-8") as spoken_src:
            play_spoken = [l.strip("\n") for l in spoken_src.readlines() if l != "\n"]
            dict_by_line = analyse_line_all_lexicons(dict_by_line, play_name, "spoken", play_spoken, lexicons_dict, mystem)
        with open("./data/rusdracor/stage_raw/{}.txt".format(play_name), "r", encoding="utf-8") as stage_src:
            play_stage = [l.strip("\n") for l in stage_src.readlines() if l != "\n"]
            dict_by_line = analyse_line_all_lexicons(dict_by_line, play_name, "stage", play_stage, lexicons_dict, mystem)
    df_by_line = pd.DataFrame.from_dict(dict_by_line)
    df_by_line.to_csv("./data/lexicons_by_line.csv", sep=";", encoding="utf-8", index=False)


def analyse_type(phrases, lexicon, mystem):
    """Pipeline for sentiment analysis of all phrases of a given type in a play.
    
    :arg phrases (list of str) - drama lines
    :arg lexicon (pandas.DataFrame) - lexicon to check the lemmas
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer
    
    :returns type_total (int) - line count
    :returns type_positive (int) - count of positively evaluated lines
    :returns type_negative (int) - count of negatively evaluated lines
    """
    type_total = len(phrases)
    type_positive = 0
    type_negative = 0
    for phrase in phrases:
        sent = evaluate_phrase_polarity(phrase, lexicon, mystem)
        if sent > 0:
            type_positive += 1
        elif sent < 0:
            type_negative += 1
    return type_total, type_positive, type_negative


def analyse_play(overall_dict, play_name, lexicon_name, lexicon, mystem):
    """Analyses play in general.
    
    :arg overall_dict (dict) - storage for all results
    :arg play_name (str) - play name to access TXT files
    :arg lexicon_name (str) - lexicon name
    :arg lexicon (pandas.DataFrame) - lexicon and polarity values
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer
    
    :returns overall_dict (dict) - updated dict
    """
    # load drama lines
    with open("./data/rusdracor/spoken_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as spoken_src:
        play_spoken = [l.strip("\n") for l in spoken_src.readlines() if l != "\n"]
    with open("./data/rusdracor/stage_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as stage_src:
        play_stage = [l.strip("\n") for l in stage_src.readlines() if l != "\n"]
    # analyse lines
    spoken_total, spoken_positive, spoken_negative = analyse_type(play_spoken, lexicon, mystem)
    stage_total, stage_positive, stage_negative = analyse_type(play_stage, lexicon, mystem)
    # save information
    overall_dict["play"].append(play_name)
    overall_dict["lexicon"].append(lexicon_name)
    overall_dict["spoken, total"].append(spoken_total)
    overall_dict["spoken positive"].append(spoken_positive)
    overall_dict["spoken positive, %"].append(spoken_positive/spoken_total*100)
    overall_dict["spoken negative"].append(spoken_negative)
    overall_dict["spoken negative, %"].append(spoken_negative/spoken_total*100)
    overall_dict["stage, total"].append(stage_total)
    overall_dict["stage positive"].append(stage_positive)
    overall_dict["stage positive, %"].append(stage_positive/stage_total*100)
    overall_dict["stage negative"].append(stage_negative)
    overall_dict["stage negative, %"].append(stage_negative/stage_total*100)
    return overall_dict


def pipeline_analysis_by_play(lexicons_dict, play_list, mystem):
    """Pipeline for analysis by play.

    :arg lexicons_dict (dict) - lexicons to use
    :arg play_list (list of str)
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns None
    """
    overall_dict = {
        "play": [],
        "lexicon": [],
        "spoken, total": [],
        "spoken positive": [],
        "spoken positive, %": [],
        "spoken negative": [],
        "spoken negative, %": [],
        "stage, total": [],
        "stage positive": [],
        "stage positive, %": [],
        "stage negative": [],
        "stage negative, %": []
    }
    for play_name in tqdm(play_list):
        for lexicon_name in lexicons_dict:
            lexicon_df = lexicons_dict[lexicon_name]
            overall_dict = analyse_play(overall_dict, play_name, lexicon_name, lexicon_df, mystem)
    df = pd.DataFrame.from_dict(overall_dict)
    df.to_csv("./data/lexicons_experiment.csv", sep=";", encoding="utf-8", index=False)


def main():
    lexicons_dict = prepare_lexicons()
    play_list = load_plays()
    mystem = Mystem()
    pipeline_analysis_by_line(lexicons_dict, play_list, mystem)
    pipeline_analysis_by_play(lexicons_dict, play_list, mystem)


if __name__ == "__main__":
    main()
