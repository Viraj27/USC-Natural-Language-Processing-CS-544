
from collections import defaultdict
import sys
import ast

_MODEL_FILE             = 'hmmmodel.txt'
_EMISSION_PROBABILITIES = 'Emission Probabilities'
_UNIQUE_VOCAB_DICT      = 'Unique Vocabulary Set Per Tag'
_START_TAG              = 'start_tag_99999'
_OUTPUT_FILE            = 'hmmoutput.txt'
_END_TAG                = 'end_tag_99999'




def get_maximum_probability(cur_tag, probability, transition_dict):
	backwards_pointer   = ""
	maximum_probability = -(sys.maxsize)

	for tag in probability:

		if maximum_probability < probability[tag]+transition_dict[tag][cur_tag]:
			maximum_probability =  probability[tag]+transition_dict[tag][cur_tag]
			backwards_pointer   = tag

	return maximum_probability, backwards_pointer

def pos_tagger(data, tag_set, transition_dict, emission_dict, word_set, open_class_tags):
    
    words = data.split()

    maximum_probability = defaultdict(dict)
    backwards_pointer   = defaultdict(dict)

    for tag in tag_set:

        # initialization of the probability and backwards pointer for each tag in the tag set wrt 1st word of each line.

        # If word present in the trained corpus, then add transition and emission *log* probabilities. (adding because log).
        if words[0] in word_set and words[0] in emission_dict[tag]:
            maximum_probability[0][tag] = transition_dict[_START_TAG][tag] + emission_dict[tag][words[0]]
        # For 1st word, backward pointer always points to starting dummy tag.
        backwards_pointer[0][tag]   = _START_TAG 
    
    for tag in open_class_tags:
        # If word not present in the trained corpus, then only apply smoothed transition probability.
        # tag shou;d come from open class tag set for elif
        if words[0] not in word_set:
            maximum_probability[0][tag] = transition_dict[_START_TAG][tag]

    
    for i in range(1, len(words)):
        for tag in tag_set:
            if words[i] in word_set and words[i] in emission_dict[tag]:
                maximum_probability[i][tag], backwards_pointer[i][tag] = get_maximum_probability(tag, maximum_probability[i-1], transition_dict)
                maximum_probability[i][tag] += emission_dict[tag][words[i]]

        for tag in open_class_tags:
            if words[i] not in word_set:
                maximum_probability[i][tag], backwards_pointer[i][tag] = get_maximum_probability(tag, maximum_probability[i-1], transition_dict)

            
    end_probability = -(sys.maxsize)
    end_tag         = str()

    for tag in maximum_probability[len(words) - 1]:
        if maximum_probability[len(words)-1][tag] + transition_dict[tag][_END_TAG] > end_probability:
            end_tag         = tag
            end_probability = maximum_probability[len(words)-1][tag] + transition_dict[tag][_END_TAG]
    

    output = []
    predicted_tag = end_tag
    for i in range(len(words)-1, -1, -1):
        output.append('{0}/{1}'.format(words[i], predicted_tag))
        predicted_tag = backwards_pointer[i][predicted_tag]
    
    return ' '.join(output[::-1])

def hmmdecode():
    
    # read the test data to be tagged
    #test_input_path = sys.argv[1]
    test_input_path  = 'test_dummy.txt'
    #data_to_tag = open(input_path).readlines()

    # read the trained transition and emission probabilities from the hmmmodel.txt
    with open(_MODEL_FILE) as f:
        trained_model = f.readlines()

    # open class - calculate length for each key, average them out and open class create.

    transition_dict = defaultdict(dict)
    emission_dict   = defaultdict(dict)
    open_class_tags = []
    emission_idx    = 0
    vocab_set_idx   = 0
    # Find index on which transition probabilities end and post which emission probabilities start
    for i, line in enumerate(trained_model):
        if _EMISSION_PROBABILITIES in line:
            emission_idx = i
        if _UNIQUE_VOCAB_DICT in line:
            vocab_set_idx = i
    
    # extract all transition probabilities to transition_dict
    for line in trained_model[1:emission_idx]:
        line = line.split()
        tag  = line[0]
        
        for new_tag_probability in line[1:]:
            new_tag, probability = new_tag_probability.rsplit('/', 1)
            transition_dict[tag][new_tag] = float(probability)
    
    #extract all emission probabilities to emission_dict
    for line in trained_model[emission_idx+1:vocab_set_idx]:
        line = line.split()
        tag = line[0]
        
        for new_word_probability in line[1:]:
            new_word, probability = new_word_probability.rsplit('/', 1)
            emission_dict[tag][new_word] = float(probability)

    
    unique_vocab_dict = ast.literal_eval(trained_model[vocab_set_idx+1])

    sum_words = 0
    for k,v in unique_vocab_dict.items():
        sum_words += len(v)
    
    avg_vocab_size = sum_words // len(unique_vocab_dict)

    for k in unique_vocab_dict:
        if len(unique_vocab_dict[k]) > avg_vocab_size:
            open_class_tags.append(k)
    
    print(open_class_tags)

    # Create a set of all the tags seen in training
    tag_set  = set(list(transition_dict.keys()))
    tag_set.remove(_START_TAG)

    # Create a set of all the words seen in training
    word_set = set()
    for tag in list(emission_dict.keys()):
        for word in emission_dict[tag].keys():
            word_set.add(word)

    with open(test_input_path) as f:
        test_data = f.readlines()

    output = ''
    for data in test_data:
        output += pos_tagger(data, tag_set, transition_dict, emission_dict, word_set, open_class_tags) + '\n'
    
    with open(_OUTPUT_FILE, 'w') as f:
        f.write(output[:-1])


if __name__ == '__main__':
    hmmdecode()