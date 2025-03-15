# after running format.py, run this file to get the final result
# input: pinyin sequence, separated by space
# output: hanzi sequence, separated by space
import json
import os
from math import log
from sys import stdin, stdout

pinyin_hanzi = {} # pinyin: [hanzi], 'ai': ['锿', '暧']
hanzi_count  = {} # hanzi: count,    '嫩': 4006
word_count   = {} # word: count,     '巴 嫩': 548
word3_count = {}

total_hanzi = 0
total_word = 0
total_word3 = 0
const_penalty = 20 # set to 20, 34.2 points gained
ratio = 0.95
omega = 0.5
# const        = json.load(open('const.json','r'))
# keywords     = json.load(open('keywords2.json','r'))
class Path:
    def __init__(self, string, final_char, length):
        self.string = string
        self.final_char = final_char
        self.length = length

def distance2(hanzi1, hanzi2): # conditional prob p(hanzi2|hanzi1)
    combine = hanzi1 + ' ' + hanzi2
    ratio1 = word_count.get(combine,0) / total_word
    ratio2 = hanzi_count.get(hanzi1,0) / total_hanzi
    ratio3 = hanzi_count.get(hanzi2,0) / total_hanzi
    if ratio2 == 0 or ratio3 == 0 or ratio1 == 0:
        return const_penalty
    else:
        ret = -log(ratio*(ratio1 / ratio2)+(1-ratio)*ratio3)
        # ret = -log(ratio1 / ratio2)
        return ret

def distance3(hanzi1, hanzi2, hanzi3): # conditional prob p(hanzi3|hanzi1,hanzi2)
    combine = hanzi1 + hanzi2 + hanzi3
    combine0 = hanzi2 + ' ' + hanzi3
    ratio1 = word3_count.get(combine,0) / total_word3
    ratio2 = word_count.get(hanzi1 + ' ' + hanzi2,0) / total_word
    ratio3 = hanzi_count.get(hanzi3,0) / total_hanzi
    ratio4 = word_count.get(combine0,0) / total_word
    ratio5 = hanzi_count.get(hanzi2,0) / total_hanzi
    if ratio2 == 0 or ratio3 == 0 or ratio1 == 0:
        return const_penalty
    else:
        ret = omega * ratio1 / ratio2 + (1-omega) * ratio * ratio4 / ratio5
        + (1-omega) * (1-ratio) * ratio3
        return -log(ret)


def viterbi(obs): # qing hua da xue
    paths = []
    for index in range(len(obs)):
        char_s = obs[index] # qing
        if index == 0:
            all_hanzi = pinyin_hanzi.get(char_s, [])
            if all_hanzi == []:
                print()
                return
            else:
                for hanzi in all_hanzi:
                    prob = hanzi_count.get(hanzi, 0) / total_hanzi
                    if prob == 0:
                        continue
                    prob = -log((1-ratio)*prob)
                    path = Path(hanzi, hanzi, prob) # to be determined, dont know probability of a single hanzi
                    paths.append(path) # path of generation 0
            # for path in paths:
            #     print(path.string, path.length)
        elif index == 1:
            new_paths = []
            all_hanzi = pinyin_hanzi.get(char_s, [])
            if all_hanzi == []:
                print()
                return
            else:
                for hanzi in all_hanzi:
                    min_path = Path('nonsense', hanzi, float('inf'))
                    for path in paths:
                        combine = path.final_char + ' ' + hanzi
                        if combine in word_count:
                            new_path = Path(path.string + hanzi, hanzi, path.length + distance2(path.final_char, hanzi))
                                # new_path = Path(path.string + hanzi, hanzi, 
                                #                 ratio*(path.length + distance2(path.final_char, hanzi))+(1-ratio)*hanzi_count[hanzi]/total_hanzi)
                        else:
                            var = hanzi_count.get(hanzi,0)/total_hanzi
                            if var !=0:
                                new_path = Path(path.string + hanzi, hanzi, path.length - log((1-ratio)*var))
                            else:
                                    # new_path = Path('nonsense', hanzi, float('inf'))
                                new_path = Path(path.string + hanzi, hanzi, path.length + const_penalty)
                        if new_path.length < min_path.length:
                                min_path = new_path
                    new_paths.append(min_path)
            paths = new_paths
            # for path in paths:
            #     print(path.string, path.length)
        else:
            new_paths = []
            all_hanzi = pinyin_hanzi.get(char_s, [])
            if all_hanzi == []:
                print()
                return
            else:
                for hanzi in all_hanzi:
                    min_path = Path('nonsense', hanzi, float('inf'))
                    for path in paths:
                        st = path.string
                        combine3 = st[len(st)-2] + st[len(st)-1] + hanzi
                        if combine3 in word3_count:
                            new_path = Path(st + hanzi, hanzi, path.length + distance3(st[len(st)-2],path.final_char, hanzi))
                                # new_path = Path(path.string + hanzi, hanzi, 
                                #                 ratio*(path.length + distance2(path.final_char, hanzi))+(1-ratio)*hanzi_count[hanzi]/total_hanzi)
                        else:
                            new_path = Path(path.string + hanzi, hanzi, path.length + const_penalty)
                            # combine = path.final_char + ' ' + hanzi
                            # if combine in word_count:
                            #     new_path = Path(path.string + hanzi, hanzi, path.length + distance2(path.final_char, hanzi))
                            # else:
                            #     var = hanzi_count.get(hanzi,0)/total_hanzi
                            #     if var !=0:
                            #         new_path = Path(path.string + hanzi, hanzi, path.length - log((1-ratio)*var))
                            #     else:
                            #         new_path = Path(path.string + hanzi, hanzi, path.length + const_penalty)
                        if new_path.length < min_path.length:
                                min_path = new_path
                    new_paths.append(min_path)
            paths = new_paths
            # for path in paths:
            #     print(path.string, path.length)

    mini = Path('', '514', float('inf'))
    for path in paths:
        if path.length < mini.length:
            mini = path
    stdout.write(mini.string + '\n')
    
with open('model/word2pinyin.json', 'r') as f:
    chars = json.load(f)
    for char in chars:
        pinyin = chars[char]
        if pinyin not in pinyin_hanzi:
            pinyin_hanzi[pinyin] = []
        pinyin_hanzi[pinyin].append(char)

with open('model/1_word.json', 'r') as f:
    single_pinyins = json.load(f)
    for single_pinyin in single_pinyins:
        dt1 = single_pinyins[single_pinyin]['words']
        # pinyin_hanzi[single_pinyin] = dt1
        dt2 = single_pinyins[single_pinyin]['counts']
        for hanzi, count in zip(dt1, dt2):
            total_hanzi += count
            if hanzi not in hanzi_count:
                hanzi_count[hanzi] = count
            else:
                hanzi_count[hanzi] += count

with open('model/2_word.json', 'r') as f:
    double_pinyins = json.load(f)
    for double_pinyin in double_pinyins:
        dt1 = double_pinyins[double_pinyin]['words']
        dt2 = double_pinyins[double_pinyin]['counts']
        for double_hanzi, count in zip(dt1, dt2):
            double_hanzi = double_hanzi.strip()
            total_word += count
            if double_hanzi not in word_count:
                word_count[double_hanzi] = count
            else:
                word_count[double_hanzi] += count

with open('model/3_word.json', 'r') as f:
    triple_pinyins = json.load(f)
    for triple_pinyin in triple_pinyins:
        dt1 = triple_pinyins[triple_pinyin]['words']
        dt2 = triple_pinyins[triple_pinyin]['counts']
        for triple_hanzi, count in zip(dt1, dt2):
            triple_hanzi = triple_hanzi.strip()
            total_word3 += count
            if triple_hanzi not in word3_count:
                word3_count[triple_hanzi] = count
            else:
                word3_count[triple_hanzi] += count

for line in stdin:
    observation = [e.strip() for e in line.split(' ')]
    viterbi(observation)

# with open('input.txt', 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         observation = [e.strip() for e in line.split(' ')]
#         viterbi(observation)