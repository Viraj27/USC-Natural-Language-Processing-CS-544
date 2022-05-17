# Separator is always the last slash in the word/tag sequecne. Use rsplit instead of just split.
from collections import defaultdict
import math
import sys

_MODEL_FILE = 'hmmmodel.txt'
_START_TAG  = 'start_tag_99999'
_END_TAG    = 'end_tag_99999'

def hmmlearn():

    transition_dict = defaultdict(dict)
    emission_dict   = defaultdict(dict)
    unique_vocabulary_set_per_tag = defaultdict(set)

    #input_path = sys.argv[1]
    input_path = 'train_dummy.txt'
    with open(input_path) as f:
        input_data = f.readlines()

    for sentence in input_data:
        words_tags_list = sentence.split()
        previous_tag        = _START_TAG

        for word_tag in words_tags_list:
            # Split word and tag on the last slash as indicated in assignment.
            word, tag = word_tag.rsplit('/', 1)
            # transition frequency update
            transition_dict[previous_tag][tag] = 1 if tag not in transition_dict[previous_tag] else transition_dict[previous_tag][tag] + 1
            # emission frequency update
            emission_dict[tag][word] = 1 if word not in emission_dict[tag] else emission_dict[tag][word] + 1
            # moving forward in the transition
            previous_tag = tag

        # End state where last tag of sentence is now prev_tag
        transition_dict[previous_tag][_END_TAG] = 1 if _END_TAG not in transition_dict[previous_tag] else transition_dict[previous_tag][_END_TAG] + 1

        # Calculate probabilities for transition and emission
    all_tags_list = list(transition_dict.keys()) + [_END_TAG]

    # Add 1 smoothing for transition states and calculate transition probabilities
    # tag_e - existing tag in dict. tag_a - tag in all tags list.
    for tag_e in transition_dict:
        total_transition_events = 0
        # Also takes into account self-loop transitions. Start -> Start.
        for tag_a in all_tags_list:
            transition_dict[tag_e][tag_a] = 1 if tag_a not in transition_dict[tag_e] else transition_dict[tag_e][tag_a] + 1
            total_transition_events += transition_dict[tag_e][tag_a]

        for new_tag in transition_dict[tag_e]:
            transition_dict[tag_e][new_tag] = math.log(transition_dict[tag_e][new_tag] / total_transition_events)
        
    # Calculate emission probabilities
    for tag in emission_dict:
        total_emission_events = sum([emission_dict[tag][emitted_word] for emitted_word in emission_dict[tag]])
        
        for emitted_word in emission_dict[tag]:
            emission_dict[tag][emitted_word] = math.log(emission_dict[tag][emitted_word]/total_emission_events)
    
    # write to hmmmodel.txt file
    output = ""
    output += 'Transition Probabilities\n'
    
    for tag in transition_dict:
        output += '{0}'.format(tag)
        for new_tag in transition_dict[tag]:
            output += ' {0}/{1}'.format(new_tag, transition_dict[tag][new_tag])
        output += '\n'

    output += 'Emission Probabilities\n'

    for tag in emission_dict:
        output += '{0}'.format(tag)
        for emitted_word in emission_dict[tag]:
            # create a set of words for each tag in a dictionary
            unique_vocabulary_set_per_tag[tag].add(emitted_word)
            output += ' {0}/{1}'.format(emitted_word, emission_dict[tag][emitted_word])
        output += '\n'


    with open(_MODEL_FILE, 'w') as f:
        f.write(output[:-1])
        f.write('\n')
        f.write('Unique Vocabulary Set Per Tag \n')
        print(dict(unique_vocabulary_set_per_tag), file=f)
    

if __name__ == '__main__':
    hmmlearn()