# Evaluating Sentiment in Russian Drama
Course paper for the 2019/20 academic year at DH Masters, HSE.

## About
The ultimate goal of this paper is to analyse whether any sentiment analysis is applicable to Russian Drama Corpus. Apart from problems of sentiment analysis as a task itself, there also are several issues when trying to apply it to dramatic text. With this research, I want to find out whether it would make any sense at all to use some of the popular instruments with Russian drama.

I'm going to test several approaches and answer the following questions:

1) how different lexicons will perform on our material?

2) if we ask people to perform manual annotation, how different would it be?

3) how difficult will it be to design a machine learning model to get what we need?

## Contents

|**Content**|**File(s)**|**Additional**|
|:---------:|:---------:|:------------:|
|downloading data for the experiments|[get_data.py](./get_data.py), [preprocessing.py](./preprocessing.py)|thanks DraCor API!|
|experiment 1: Russian WordNet package for Python|[wiki_ru_wordnet.ipynb](./wiki_ru_wordnet.ipynb)||
|experiment 2: out-of-the-box solution, dostoyevsky|[dostoyevsky.ipynb](./dostoyevsky.ipynb)||
|preparing experiment 3: using sentiment lexicons for Russian to parse plays|[extract_sentiment_from_plays.py](./extract_sentiment_from_plays.py)||
|experiment 3: analyzing performance of various Russian lexicons of different origins|[lexicons.ipynb](./lexicons.ipynb)||
|diving into emotional lines: most frequest items and word clouds|[emotional_lines.ipynb](./emotional_lines.ipynb)||

## Literature

Available as a .bib file: [emotions_drama_literature.bib](./emotions_drama_literature.bib).

## Lexicons used in the experiment

|**Lexicon name**|**Year developed**|**Article description**|**Dataset link**|
|:--------------:|:----------------:|:---------------------:|:--------------:|
|ProductSentiRus |2012              |[Extraction of Russian Sentiment Lexicon for Product Meta-Domain](https://pdfs.semanticscholar.org/e23b/1430b3c4c4850db1336c5ba9c51c2084f29b.pdf)||
|EmoLex          |2013              |[Crowdsourcing a Word-Emotion Association](https://arxiv.org/abs/1308.6297)|[link](http://sentiment.nrc.ca/lexicons-for-research/)|
|Chen-Skiena's Lexicon|2014         |[Building Sentiment Lexicons for All Major Languages](https://www.aclweb.org/anthology/P14-2063.pdf)|[link](https://sites.google.com/site/datascienceslab/projects/multilingualsentiment)|
|LinisCrowd      |2016              |[An Opinion Word Lexicon and a Training Dataset for Russian Sentiment Analysis of Social Media](http://www.dialog-21.ru/media/3400/koltsovaoyuetal.pdf)|[link](http://www.linis-crowd.org/)|
|RuSentiLex      |2017              |[Creating a General Russian Sentiment Lexicon](http://www.lrec-conf.org/proceedings/lrec2016/pdf/285_Paper.pdf)|[.txt file](http://www.labinform.ru/pub/rusentilex/rusentilex_2017.txt)|
