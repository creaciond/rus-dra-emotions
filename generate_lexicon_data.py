import numpy as np
import os
import pandas as pd
import warnings

from pymystem3 import Mystem
from tqdm import tqdm

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


def evaluate_phrase_polarity(phrase, lexicon):
    """Calculates polarity for the whole phrase.
    
    :arg phrase (str) - phrase to evaluate
    :arg lexicon (pandas.DataFrame) - lexicon to check the lemmas
    
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


def analyse_play(overall_dict, play_name, lexicon_name, lexicon):
    """Analyses play in general.
    
    :arg overall_dict (dict) - storage for all results
    :arg play_name (str) - play name to access TXT files
    :arg lexicon_name (str) - lexicon name
    :arg lexicon (pandas.DataFrame) - lexicon and polarity values
    
    :returns overall_dict (dict) - updated dict
    """
    # load drama lines
    with open("./data/rusdracor/spoken_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as spoken_src:
        play_spoken = [l.strip("\n") for l in spoken_src.readlines() if l != "\n"]
    with open("./data/rusdracor/stage_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as stage_src:
        play_stage = [l.strip("\n") for l in stage_src.readlines() if l != "\n"]
    # analyse lines
    spoken_total, spoken_positive, spoken_negative = analyse_type(play_spoken, lexicon)
    stage_total, stage_positive, stage_negative = analyse_type(play_stage, lexicon)
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

    
def analyse_line_all_lexicons(dict_by_line, play_name, line_type, phrases, lexicons_dict):
    """Analyses one line against all lexicons, saves changes to a dataframe.
    
    :arg dict_by_line (dict) - storage for all results
    :arg play_name (str)
    :arg line_type (str) - spoken/stage
    :arg phrases (list of str) - lines to analyse
    :arg lexicons_dict (dict) - storage of all lexicons
    
    :returns dict_by_line (dict) - parsed lines
    """
    for phrase in phrases:
        dict_by_line["play"].append(play_name)
        dict_by_line["line type"].append(line_type)
        dict_by_line["line"].append(phrase)
        for lexicon_name in lexicons_dict.keys():
            lexicon = lexicons_dict[lexicon_name]
            polarity = evaluate_phrase_polarity(phrase, lexicon)
            dict_by_line[lexicon_name].append(polarity)
    return dict_by_line


def main():
    path_to_lexicons = "./data/sentiment_datasets"
    lexicons = [lex[:-4] for lex in os.listdir(path_to_lexicons) if lex.endswith(".csv")]
    lexicons_dict = {}
    for lexicon in lexicons:
        lex_df = pd.read_csv("./data/sentiment_datasets/{}.csv".format(lexicon), sep=";", encoding="utf-8")
        lexicons_dict[lexicon] = lex_df
    with open("./data/rusdracor_list.txt", "r", encoding="utf-8") as f:
        play_list = [play.strip("\n") for play in f.readlines()]
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
    dict_by_line = {
        "play": [],
        "line": [],
        "line type": [],
        "RuSentiLex": [],
        "EmoLex": [], 
        "LinisCrowd": [],
        "ChenSkiena": [], 
        "ProductSentiRus": []
    }
    mystem = Mystem()
    # analysis by play
    for play_name in tqdm(play_list):
        for lexicon_name in lexicons:
            lexicon_df = lexicons_dict[lexicon_name]
            overall_dict = analyse_play(overall_dict, play_name, lexicon_name, lexicon_df)
    df = pd.DataFrame.from_dict(overall_dict)
    df.to_csv("./data/lexicons_experiment.csv", sep=";", encoding="utf-8", index=False)
    # analysis by line
    for play_name in tqdm(play_list):
        # load drama lines
        with open("./data/rusdracor/spoken_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as spoken_src:
            play_spoken = [l.strip("\n") for l in spoken_src.readlines() if l != "\n"]
            dict_by_line = analyse_line_all_lexicons(dict_by_line, play_name, "spoken", play_spoken, lexicons_dict)
        with open("./data/rusdracor/stage_lemmas/{}.txt".format(play_name), "r", encoding="utf-8") as stage_src:
            play_stage = [l.strip("\n") for l in stage_src.readlines() if l != "\n"]
            dict_by_line = analyse_line_all_lexicons(dict_by_line, play_name, "spoken", play_stage, lexicons_dict)
    df_by_line = pd.DataFrame.from_dict(dict_by_line)
    df_by_line.to_csv("./data/lexicons_by_line.csv", sep=";", encoding="utf-8", index=False)

    
if __name__ == "__main__":
    main()
