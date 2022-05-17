from helper import remove_stopwords, remove_punctuations, model_file_path, output_file_path, remove_least_frequent_words
import glob, os, re, json, sys, math

def main():
    
    input_path = sys.argv[1]
    
    # read the model file and its parameters
    with open(model_file_path, 'r') as f:
        model_data = f.read()

    likelihood_dict, prior_proba, wd_cls_cnt = model_data.split("\n")
    # load them into dictionaries
    likelihood_dict     = json.loads(likelihood_dict)
    prior_proba         = json.loads(prior_proba)
    wd_cls_cnt          = json.loads(wd_cls_cnt)
        
    test_loc            = glob.glob(os.path.join(input_path, "*", "*", "*", "*"))
    
    # open output file for writing with every iteration
    out_file = open(output_file_path, mode = 'w+', encoding = 'UTF-8')

    for input_path in test_loc:
        prob_dict = {"positive": 1, "negative": 1, "truthful": 1, "deceptive": 1}
        with open(input_path, 'r') as f:
            clean_wds = remove_punctuations(f.read())
            clean_wds = remove_stopwords(clean_wds)
            """ least_frequent_words = remove_least_frequent_words(clean_wds)
            refined_wd_list = []
            for wd in clean_wds:
                if wd not in least_frequent_words:
                    refined_wd_list.append(wd) """
        for word in clean_wds:
            for k in prob_dict:
                if word in likelihood_dict: 
                    prob_dict[k] += likelihood_dict[word][k]

        for k in prob_dict:
            prob_dict[k] = prob_dict[k] + prior_proba[k]

        label2 = "negative" if prob_dict["negative"] > prob_dict["positive"] else "positive"
        label1 = "truthful" if prob_dict["truthful"] > prob_dict["deceptive"] else "deceptive"

        out_file.write(f"{label1} {label2} {input_path}")
        out_file.write("\n")
    
    out_file.close()

main()