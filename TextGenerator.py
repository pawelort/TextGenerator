from nltk.tokenize import WhitespaceTokenizer
from nltk import bigrams, trigrams
import collections, random, re

def get_token(token_index, all_tokens):
    try:
        print(all_tokens[int(token_index)])
    except TypeError:
        print('Type Error. Please input an integer type.')
    except ValueError:
        print('Value Error. Please input an integer.')
    except IndexError:
        print('Index Error. Please input an integer that is in the range of the corpus.')

def get_bigram(bigram_index, all_bigrams):
    try:
        print(f"Head: {all_bigrams[int(bigram_index)][0]}\tTail: {all_bigrams[int(bigram_index)][1]}")
    except TypeError:
        print('Type Error. Please input an integer type.')
    except ValueError:
        print('Value Error. Please input an integer.')
    except IndexError:
        print('Index Error. Please input a value that is not greater than the number of all bigrams.')

def get_freq_bigram(key, bigram_dict):
    try:
        print(f"Head: {key}")
        for tail, amount in bigram_dict[key].most_common():
            print(f"Tail: {tail}\tCount: {amount}")

    except KeyError:
        print("Key Error. The requested word is not in the model. Please input another word.")

def find_word(bigrams, head):
    possible_next_words = bigrams.get(head).items()
    pos_next_words_keys, pos_next_words_values = zip(*possible_next_words)
    return random.choices(pos_next_words_keys, pos_next_words_values)[0]

def find_sentence_begin(word):
    pattern = r"[A-Z][^.!?]*$"
    # pattern = r"[A-Z]"
    return re.match(pattern, word)


def find_sentence_end(word):
    pattern = r".+[.!?]$"
    return re.match(pattern, word)

def head_update(current_head, new_word):
    temp_head = current_head.split()
    temp_head.append(new_word)
    return ' '.join(temp_head[1:])

tk = WhitespaceTokenizer()
with open(input(), 'r', encoding='utf-8') as corpus:
    tokens = tk.tokenize(corpus.read())
    list_of_trigrams = list(trigrams(tokens))


# r"[\w'=-]+[,.!?]?"

# print("Corpus statistics")
# print(f"All tokens: {len(tokens)}")
# print(f"Unique tokens: {len(set(tokens))}")
# print(f"Numbers of bigrams: {len(list_of_bigrams)}")

temp_trigrams = dict()
freq_trigrams = dict()

for single in list_of_trigrams:
    head = single[0] + ' ' + single[1]
    temp_trigrams.setdefault(head, []).append(single[2])

for key, value in temp_trigrams.items():
    counter_dict = collections.Counter(value)
    freq_trigrams[key] = counter_dict


# while True:
#     user_input = input()
#     if user_input == 'exit':
#         break
#     else:
#         get_freq_bigram(user_input, freq_bigrams)


while True:
    current_head = random.choice(list(freq_trigrams.keys()))
    if find_sentence_begin(current_head):
        actual_sentence = [current_head]
        break

for i in range(10):

    if i > 0:
        actual_sentence = []

    while True:
        next_word = find_word(freq_trigrams, current_head)
        if actual_sentence == []:
            if find_sentence_begin(next_word):
                actual_sentence.append(next_word)
                current_head = head_update(current_head, next_word)
            else:
                current_head = head_update(current_head, next_word)

        else:
            actual_sentence.append(next_word)
            current_head = head_update(current_head, next_word)
            if len(actual_sentence) >= 5 and find_sentence_end(next_word):
                break
            if len(actual_sentence) < 5 and find_sentence_end(next_word):
                actual_sentence = []

    print(' '.join(actual_sentence))

