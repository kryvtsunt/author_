
import math

def clean_text(txt):
        """returns a list containing the words in txt after it has been “cleaned”"""
        clean_string = ''
        for ch in txt:
            ch = ch.lower()
            if ch in "'abcdefghijklmnopqrstuvwxyz ":
                clean_string += ch
        s = clean_string.split()
        return s


def stem(s):
    """returns the stem of s"""
    while True:
            if s[-3:] == 'ing':
                s = s[0:-3]
            elif s[-3:] == 'ies':
                s = s[0:-3] + 'i'
            elif s[-1:] == 's':
                s = s[0:-1]
            elif s[-1:] == 'y':
                s = s[0:-1] + 'i'
            elif s[-1:] == 'e':
                s = s[0:-1]
            elif s[-2:] == 'er':
                s = s[0:-2]
            elif s[-3:] == 'est':
                s = s[0:-3]
            elif s[-2:] == 'ed':
                s = s[0:-2]

            elif s[:2] == 're' or s[:2] == 'un' or s[:2] == 'de':
                s = s[2:]
            elif s[:3] == 'dis' or s[:3] == 'mis' or s[:3] == 'non' or s[:3] == 'pre':
                s = s[3:]
            else:
                break
    return s


def compare_dictionaries(d1, d2):
    """takes two feature dictionaries d1 and d2 as inputs,
       computes and returns their log similarity score"""
    score = 0
    total = 0
    for i in d1:
        total += d1[i]

    for ch in d2:
        if ch in d1:
            score += math.log(d1[ch]/total)*d2[ch]
        else:
            score += math.log(0.5/total)*d2[ch]

    return score



class TextModel:
    """models, analyzes, and scores the similarity of text samples"""

    def __init__(self, model_name):
        """constructs a new TextModel object"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}

    def __repr__(self):
        """returns a string representing a TextModel object"""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lenghts: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of special characters: ' + str(len(self.punctuation))

        return s

    def add_string(self, s):
        """analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model"""

        text_wo_q = s.replace('?', '.')
        text_wo_e = text_wo_q.replace('!', '.')
        sentences_list = text_wo_e.split('.')
        sentences_list = sentences_list[0:-1]

        word_list = clean_text(s)

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1

        for w in word_list:
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1

        for el in sentences_list:
            el = el.split(' ')
            if len(el) not in self.sentence_lengths:
                self.sentence_lengths[len(el)] = 1
            else:
                self.sentence_lengths[len(el)] += 1


        for ch in s:
            if ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ':
                if ch not in self.punctuation:
                    self.punctuation[ch] = 1
                else:
                    self.punctuation[ch] += 1



    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        r = f.read()
        self.add_string(r)
        f.close()




    def save_model(self):
        """A function that demonstrates how to write a
           Python dictionary to an easily-readable file"""

        filename = self.name + '_' + 'words'
        d = self.words
        f = open(filename, 'w')
        f.write(str(d))
        f.close()

        filename = self.name + '_' + 'word_lengths'
        d = self.word_lengths
        f = open(filename, 'w')
        f.write(str(d))
        f.close()

        filename = self.name + '_' + 'self.stems'
        d = self.word_lengths
        f = open(filename, 'w')
        f.write(str(d))
        f.close()

        filename = self.name + '_' + 'self.sentence_lengths'
        d = self.word_lengths
        f = open(filename, 'w')
        f.write(str(d))
        f.close()

        filename = self.name + '_' + 'self.punctuation'
        d = self.word_lengths
        f = open(filename, 'w')
        f.write(str(d))
        f.close()


    def read_model(self):
        """A function that demonstrates how to read a
           Python dictionary from a file."""

        filename = self.name + '_' + 'words'
        f = open(filename, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.words = d

        filename = self.name + '_' + 'word_lengths'
        f = open(filename, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.word_lengths = d

        filename = self.name + '_' + 'self.stems'
        f = open(filename, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.word_lengths = d

        filename = self.name + '_' + 'self.sentence_lengths'
        f = open(filename, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.word_lengths = d

        filename = self.name + '_' + 'self.punctuation'
        f = open(filename, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.word_lengths = d

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores
           measuring the similarity of self and other"""

        score_words = compare_dictionaries(other.words, self.words)
        score_word_lengths = compare_dictionaries(other.word_lengths, self.word_lengths)
        score_stems = compare_dictionaries(other.stems, self.stems)
        score_sentence_lengths = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        score_punctuation = compare_dictionaries(other.punctuation, self.punctuation)

        list_scores = [round(score_words, 3), round(score_word_lengths, 3), round(score_stems, 3), round(score_sentence_lengths, 3), round(score_punctuation, 3)]

        return list_scores

    def classify(self, source1, source2):
        """determines which of two "source" texts is the more likely source of the called TextModel)"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for', source1.name,':' , scores1)
        print('scores for', source2.name,':' , scores2)

        weighted_sum1 = 8*scores1[0] + 10*scores1[1] + 5*scores1[2] + 10*scores1[3] + 3*scores1[4]
        weighted_sum2 = 8*scores2[0] + 10*scores2[1] + 5*scores2[2] + 10*scores2[3] + 3*scores2[4]

        if weighted_sum1 > weighted_sum2:
           print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)



def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
        
    source1 = TextModel('John Green')
    source1.add_file('_fault_stars.txt')

    source2 = TextModel('Stephen King')
    source2.add_file('_desperation.txt')

    new2 = TextModel('The Running Man')
    new2.add_file('_the_running_man.txt')
    new2.classify(source1, source2)

