import json
import string
import itertools
import re
from collections import defaultdict
import numpy as np
# import scipy.stats as stat
import cPickle as pickle

class BabyNames:

    def __init__(self, gender):
        with open('mysite/namerator/overall_data.json', 'rb') as f:
            names_dict = json.load(f)
        self.names_dict = names_dict[gender]
        self.num_names = len(self.names_dict)
        self.gender = gender
        self.length_dist = np.round(np.random.normal(6.45182, 1.48867, 10000))
        self.length_probs = np.histogram(self.length_dist, bins=range(100), normed=True)[0]
        self.length_cdf = np.cumsum(self.length_probs)
        self.length_std = 1.48867
        with open('mysite/namerator/t_dict2%s.pck' % gender, 'rb') as f:
            self.tdict = pickle.load(f)

    def mega_stringify(self):
        mega_string = "".join([("<" + name_str + ">") * count for name_str, count in self.names_dict.iteritems()])
        return mega_string.lower()

    def stringify(self):
        long_string = "".join([("<" + name_str + ">") for name_str in self.names_dict])
        return long_string.lower()

    def get_freqs(self, mega_string):
        total_letters = len(mega_string)
        overall_freqs = dict([(letter, float(mega_string.count(letter))/total_letters) for letter in string.ascii_lowercase + "<>"])
        return overall_freqs

    def transition_freqs(self, mega_string, n=2):
        transition_dict = defaultdict(dict)
        total_counter = 0
        for i in range(1, n):
            args = [string.ascii_lowercase + "<>"] * i
            all_combos = itertools.product(*args)
            for combo in all_combos:
                total_counter += 1
                # for each combo, we're trying to find the probability of seeing
                # the last letter given the previous n - 1
                leader = "".join(combo)
                all_followers = re.findall(leader + '(.)', mega_string)
                total = len(all_followers)
                for follower in set(all_followers):  #.ascii_lowercase() + "<>":
                    transition_dict[leader][follower] = float(all_followers.count(follower))/total
        return dict(transition_dict)

    # def transition_freqs_from_dict(self):
    #     transition_dict = defaultdict(dict)
    #     total_counter = 0
    #     for i in range(1, n):
    #         args = [string.ascii_lowercase + "<>"] * i
    #         all_combos = itertools.product(*args)
    #         for combo in all_combos:
    #             print combo
    #             total_counter += 1
    #             # if total_counter % 10 == 0:
    #             #     print "String number:", total_counter
    #             # for each combo, we're trying to find the probability of seeing
    #             # the last letter given the previous n - 1
    #             leader = "".join(combo)
    #             all_followers = re.findall(leader + '(.)', mega_string)
    #             total = len(all_followers)
    #             for follower in set(all_followers):  #.ascii_lowercase() + "<>":
    #                 transition_dict[leader][follower] = float(all_followers.count(follower))/total
    #     return dict(transition_dict)


    def generate_name(self, transition_dict, start="<", n_gram=2):
        current_index = len(start)
        name = start.lower()
        real_name = False
        prob = 1
        # choices = string.ascii_lowercase + "<>"
        while True:
            if current_index - n_gram < 0:
                i = 0
            else:
                i = current_index - n_gram

            leader = name[i:current_index + 1]
            # print "FINDING NEXT LETTER BASED ON:", leader
            #print "POSSIBLE CHOICES: ", transition_dict[leader]
            options = transition_dict[leader].keys()
            probs = transition_dict[leader].values()
            next_letter = np.random.choice(options, p=probs)
            # print next_letter
            name += next_letter[0]
            prob *= probs[options.index(next_letter)]
            if next_letter == '>':
                print self.length_probs
                cdf = self.length_cdf[len(name) - 2]
                prob *= min(cdf, 1-cdf)
                # prob *= .01**(np.abs(9 - len(name)))
                if name[1:-1].title() in self.names_dict:
                    real_name = True
                return name, prob, real_name
            current_index += 1

    def regularize(self, transition_dict, alpha=1):
        choices = string.ascii_lowercase + "<>"
        divisor = len(choices) + alpha
        new_dict = {}
        for leader in transition_dict:
            new_dict[leader] = {}
            for follower in choices:
                if follower in transition_dict[leader]:
                    new_dict[leader][follower] = (transition_dict[leader][follower] + alpha) / divisor
                else:
                    new_dict[leader][follower] = float(alpha)/divisor
        return new_dict





if __name__ == "__main__":
    from sys import argv
    import cPickle
    with open('t_dict.pck', 'rb') as f:
        tdict = cPickle.load(f)
    x = BabyNames('M')
    start = argv[1]
    meg = x.mega_stringify()
    all_names = set()
    for i in range(int(argv[2])):
        name = x.generate_name(tdict, start="<"+start).strip("<>").title()
        
        all_names.add(name)
















