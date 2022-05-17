
import re
from collections import Counter, OrderedDict
from operator import itemgetter

model_file_path  = "nbmodel.txt"
output_file_path = "nboutput.txt"

stopwords = ["a", "able", "about", "above", "across", "again", "ain't", "all", "almost", "along", "also", "am", "among", "amongst", "an", "and", "anyhow", "anyone", "anyway", "anyways", "appear", "are", "around", "as", "a's", "aside", "ask", "asking", "at", "away", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "behind", "below", "beside", "besides", "between", "beyond", "both", "brief", "but", "by", "came", "can", "come", "comes", "consider", "considering", "corresponding", "could", "do", "does", "doing", "done", "down", "downwards", "during", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "etc", "even", "ever", "every", "ex", "few", "followed", "following", "follows", "for", "former", "formerly", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "happens", "has", "have", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "here's", "hereupon", "hers", "herself", "he's", "hi", "him", "himself", "his", "how", "hows", "i", "i'd", "ie", "if", "i'll", "i'm", "in", "inc", "indeed", "into", "inward", "is", "it", "it'd", "it'll", "its", "it's", "itself", "i've", "keep", "keeps", "kept", "know", "known", "knows", "lately", "later", "latter", "latterly", "lest", "let", "let's", "looking", "looks", "ltd", "may", "maybe", "me", "mean", "meanwhile", "might", "most", "my", "myself", "name", "namely", "nd", "near", "nearly", "need", "needs", "neither", "next", "nine", "no", "non", "now", "nowhere", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "ought", "our", "ours", "ourselves", "out", "over", "own", "per", "placed", "que", "quite", "re", "regarding", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "seven", "several", "she", "she'd", "she'll", "she's", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "take", "taken", "tell", "tends", "th", "than", "that", "thats", "that's", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "theres", "there's", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", "those", "though", "three", "through", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "t's", "twice", "two", "un", "under", "up", "upon", "us", "use", "used", "uses", "using", "usually", "value", "various", "very", "via", "viz", "vs", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "went", "were", "we're", "weren't", "we've", "what", "whatever", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "where's", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "who's", "whose", "why", "why's", "will", "willing", "wish", "with", "within", "without", "won't", "would", "wouldn't", "yes", "yet", "you", "you'd", "you'll", "your", "you're", "yours", "yourself", "yourselves", "you've"]
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def remove_stopwords(text):
    text = text.split(" ")
    return [w for w in text if w not in stopwords and not w.isdigit() and not any([c in digits for c in w])]

def remove_punctuations(text):
    return re.sub(r'[^\w\s]',' ',text.lower())

def remove_least_frequent_words(wdList):
    less_freq_words = set()
    freq_dict = Counter(wdList)
    for w, freq in freq_dict.items():
        if freq <= 1:
            less_freq_words.add(w)
    return list(less_freq_words)
"""
def most_frequent_words(wdList):
    most_freq_words = set()
    freq_dict = Counter(wdList)
    o_d = OrderedDict(sorted(freq_dict.items(), key = itemgetter(1), reverse = True))
    #a = 0
    #while a <= 15: 
        #print(l[a])
    #    a += 1
    return list(k for k, v in o_d.items() if v >= 90)"""