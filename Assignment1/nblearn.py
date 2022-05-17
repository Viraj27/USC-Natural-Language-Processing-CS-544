from collections import defaultdict
from helper      import remove_stopwords, remove_punctuations, model_file_path #most_frequent_words
import os 
import sys 
import math
import re 
import json 
import glob
import pprint


def generate_word_list(dir, wd_list):
    ''' pre-process the files and return a word list '''
    for inp_path in dir:
        with open(inp_path, 'r') as f:
            clean_wds      = remove_punctuations(f.read())
            clean_wds      = remove_stopwords(clean_wds)
            wd_list.extend(clean_wds)
    #least_frequent_words = remove_least_frequent_words(wd_list)
    #m = most_frequent_words(wd_list)
    #print(m)
    """ refined_wd_list = []
    for wd in wd_list:
        if wd not in least_frequent_words:
            refined_wd_list.append(wd) """
    return wd_list

def write_model_file(likelihood_dict, prior_proba, wd_cls_cnt):
    ''' dump the important parameters for the classifier in the model file'''
    with open(model_file_path, mode = 'w+', encoding = 'UTF-8') as f:
        f.write(json.dumps(likelihood_dict))
        f.write("\n")
        f.write(json.dumps(prior_proba))
        f.write("\n")
        f.write(json.dumps(wd_cls_cnt))

def main():

    input_path  = sys.argv[1]
    # get all text files for each of the 4 classes.
    neg_dec_txt = glob.glob(os.path.join(input_path, "negative*", "deceptive*", "*", "*"))
    neg_tru_txt = glob.glob(os.path.join(input_path, "negative*", "truthful*", "*", "*"))
    pos_dec_txt = glob.glob(os.path.join(input_path, "positive*", "deceptive*", "*", "*"))
    pos_tru_txt = glob.glob(os.path.join(input_path, "positive*", "truthful*", "*", "*"))
    
    neg_dec_wd, neg_tru_wd, pos_dec_wd, pos_tru_wd = [], [], [], []
    likelihood_dict     = defaultdict(lambda : {"positive": 0, "negative": 0, "truthful": 0, "deceptive": 0})
    prior_proba         = {}

    # words list
    neg_dec_wd = generate_word_list(neg_dec_txt, neg_dec_wd)
    neg_tru_wd = generate_word_list(neg_tru_txt, neg_tru_wd)
    pos_dec_wd = generate_word_list(pos_dec_txt, pos_dec_wd)
    pos_tru_wd = generate_word_list(pos_tru_txt, pos_tru_wd)

    # word count per class
    pos_wd_cnt = len(pos_dec_wd) + len(pos_tru_wd)
    neg_wd_cnt = len(neg_dec_wd) + len(neg_tru_wd)
    tru_wd_cnt = len(pos_tru_wd) + len(neg_tru_wd)
    dec_wd_cnt = len(pos_dec_wd) + len(neg_dec_wd)

    # number of files per class
    pos_cnt    = len(pos_dec_txt) + len(pos_tru_txt)
    neg_cnt    = len(neg_dec_txt) + len(neg_tru_txt)
    tru_cnt    = len(pos_tru_txt) + len(neg_tru_txt)
    dec_cnt    = len(pos_dec_txt) + len(neg_dec_txt)

    wd_cls_cnt    = {"positive": pos_wd_cnt, "negative": neg_wd_cnt, "truthful": tru_wd_cnt, "deceptive": dec_wd_cnt}
    cls_cnt       = {"positive": pos_cnt,    "negative": neg_cnt   , "truthful": tru_cnt   , "deceptive": dec_cnt}
    total_reviews = cls_cnt["positive"] + cls_cnt["negative"]

    # calculate prior probability for each class  
    for cls, cnt in cls_cnt.items():
        prior_proba[cls] = math.log( cnt / total_reviews)

    wd_to_cls_map = {tuple(neg_dec_wd) : ["negative", "deceptive"], tuple(neg_tru_wd) : ["negative", "truthful"], tuple(pos_dec_wd) : ["positive", "deceptive"], tuple(pos_tru_wd) : ["positive", "truthful"]}

    # likelihood of a word belonging to one of the 4 classes.
    for k, v in wd_to_cls_map.items():
        for wd in k:
            for cls in v:
                likelihood_dict[wd][cls] += 1
    for wd, cnt_dict in likelihood_dict.items():
        for k, v in cnt_dict.items():
            likelihood_dict[wd][k] = math.log((v+1) / (wd_cls_cnt[k]+len(likelihood_dict)))
    
    write_model_file(likelihood_dict, prior_proba, wd_cls_cnt)  

main()