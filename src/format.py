'''
this file reads corpus data, and generates statistics in data/1_word.json, data/2_word.json, data/word2pinyin.json
(reconstructing my original code is exhausting, so run.py is almost the copy)
'''
import json
import os
from collections import Counter
from pypinyin import lazy_pinyin, Style

corpus_path = "corpus/sina_news_gbk"

pinyin_map = {} # pinyin for each unique Chinese character in char_freq
ans1 = {}
ans2 = {}

def is_chinese(ch):
    return '\u4e00' <= ch <= '\u9fff'

def get_pinyin(word):
    py = lazy_pinyin(word, style=Style.NORMAL)
    return [py[0],py[1]]

def main():
    char_freq = Counter() # single Chinese character frequency
    two_char_freq = Counter()
    for filename in os.listdir(corpus_path):
        file_path = os.path.join(corpus_path, filename)
        with open(file_path, 'r', encoding='gbk') as f:
            text = f.read()
            # single Chinese character frequency
            chinese_chars = [ch for ch in text if is_chinese(ch)]
            tmp1 = Counter(chinese_chars)
            char_freq = char_freq + tmp1;
            # two-character words frequency
            tmp2 = Counter()
            for i in range(len(chinese_chars) - 1):
                two_char_seq = ''.join(chinese_chars[i:i+2])
                tmp2[two_char_seq] += 1
            two_char_freq = two_char_freq + tmp2
    # Generate pinyin for each unique Chinese character in char_freq
    for ch in char_freq.keys():
        py = lazy_pinyin(ch, style=Style.NORMAL)
        py = py[0]
        pinyin_map[ch] = py
        if py not in ans1:
            ans1[py] = {"words":[ch], "counts":[char_freq[ch]]}
        else:
            ans1[py]["words"].append(ch)
            ans1[py]["counts"].append(char_freq[ch])
    # Generate pinyin for each two-character word in two_char_freq
    for word in two_char_freq.keys():
        py = get_pinyin(word)
        py = py[0] + ' ' + py[1]
        nw = word[0] + ' ' + word[1]
        if py not in ans2:
            ans2[py] = {"words":[nw], "counts":[two_char_freq[word]]}
        else:
            ans2[py]["words"].append(nw)
            ans2[py]["counts"].append(two_char_freq[word])

    json.dump(ans1, open('model/1_word.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(ans2, open('model/2_word.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(pinyin_map, open('model/word2pinyin.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()