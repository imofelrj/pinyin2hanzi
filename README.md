<<<<<<< HEAD
# pinyin2hanzi
=======
# Report of Input Method for Pinyin to Hanzi
Qiuzhen College, Tsinghua University
imofelrj, li-rj22@mails.tsinghua.edu.cn, Mar 15th, 2025

## Abstract
This project is a coursework in the course "Introduction to Artificial Intelligence" in the spring term of 2025, at Tsinghua University. Using Viterbi algorithm, we implemented a pinyin-to-hanzi input method. The project is written in Python and the code is available at [GitHub](https://github.com/imofelrj/pinyin2hanzi).

There are in total 4 folders in the project:
- `data/`: the input data, answer data and the output data
- `src/`: the source code
- `corpus/`: the corpus used in the project
- `model/`: generated from the corpus

The corpus file is not uploaded to the GitHub, since it's too large. 
The models are generated from corpus, hence neither included.
You can download the corpus (sina_news_gbk, 2016) from [here](https://cloud.tsinghua.edu.cn/d/88327bd9678a45428abf/) and put it in the `corpus/` folder.

## How to run the source codes
To run the project, install necessary packages with
```pip install -r requirements.txt```.

`format.py` is used to format the corpus. The default corpus path is `corpus/sina_news_gbk` and the default output path is `model/`. By running
```python3 src/format.py```
we can get three json files from the corpus: `1_word.json`, `2_word.json` and `word2pinyin.json`, which record the frequency of 1-gram, 2-gram and the mapping from a single character to pinyin.

`run.py` is the core program, which uses Viterbi algorithm to find the most probable sentence, and the default model path is `model/`. By running
```python3 src/run.py```
you can input a pinyin sentence and get the most probable sentence in Chinese characters. The program stops until it gets a EOF.

`rate.py` is used to calculate the accuracy of the program. The default output path is `data/input.txt` and the default answer path is `data/answer.txt`. Run the following command to show the accuracy of single character and the whole sentence.
```python3 src/rate.py```

`main.py` is the main program, and it reads the input from given file and writes the output to the given file. 
```python3 src/main.py < "path_to_input" > "path_to_output"```

## How I process the corpus
The corpus is some texts from sina news, and I use the following steps to process the corpus:
- Read the corpus with `encoding='gbk'` and pick all Chinese characters in the original order.
- Record the pinyin and frequency of each character.
- Record the frequency of 2-grams consisting of adjacent characters.
- Save the data to `model/`.
Thanks to `Python`, it's easy to process such huge amount of data, which can be very difficult in other languages without specifical optimization(`C++`).

## How to get the most probable sentence
Suppose the input pinyin sentence is $O$, the output Chinese sentence is $I$. We need to find
$$I = \arg\max_{I} P(I|O) = \arg\max_{I} \frac{P(O|I)P(I)}{P(O)}$$
where $P(O|I)$ is the probability of the pinyin sentence given the Chinese sentence, and $P(I)$ is the probability of the Chinese sentence.

$P(O)$ is a constant, and if we ignore characters with multiple pinyin, one can assume $P(O|I)=1$. That is, we should find $$I=\arg\max_{I} P(I)$$

The probability function $P$ here is obtained from the model : when the corpus is good enough (which we hope so), the probability of a single character or a word is proportional to its frequency in the corpus. 

Suppose $I=\omega_1\omega_2\dots\omega_n$, using conditional probability, we obtain
$$P(I)=P(\omega_1)P(\omega_2|\omega_1)\dots P(\omega_n|\omega_1\dots\omega_{n-1})$$
This is a HMM model (Hidden Markov Model, we don't know what the transition is). For approximation, we can consider it as a 2-model, that is, the transition probability is only related to the previous ONE character. Now, it suffices to calculate
$$P(I)=P(\omega_1)P(\omega_2|\omega_1)\dots P(\omega_n|\omega_{n-1})$$
with $P(\omega_i|\omega_{i-1})=\frac{P(\omega_{i-1}\omega_i)}{P(\omega_{i-1})}$, both of which can be DIRECTLY obtained from the model.

Take the logarithm, it suffices to calculate
$$\argmin_{I} \{-\log P(I)\} =\argmin_{\omega_1\dots\omega_n} \sum_{i=1}^{n-1} -\log P(\omega_{i+1}|\omega_{i})$$

This is where the Viterbi algorithm comes in. Suppose the corpus is of size $V$, equi-distributed in $N$ pinyin(finite), and the length of the sentence is $n$. During the dynamic programming, we compare $V^2$ distances for $n$ times, and the time complexity is $O(nV^2)$, and the space complexity is $O(nV)$, since with DP we always maintain an extra array to store intermediate computations for reuse to avoid repeated calculations.

## Optimize the 2-model
- Add a parameter $\lambda$ to the model, which is the weight of the 2-gram model. The probability of a word is replaced with
$$\lambda P(\omega_2|\omega_1)+(1-\lambda)P(\omega_2)$$
- Record the most common 2-words in advance, and when doing DP, their distance is considered as $0$. For example, whenever `ge` appears in the sentence, after `gai`, it means `改革` with very high probability.
- Also, there are some long words, whose components are not common, but the whole pronunciation is unique. For example, `hong lou meng` is `红楼梦` with very high probability. We can also record them in advance, and do one more replacement after the DP.
It's worth mentioning that by doing last two steps, my score on Tsinghua OJ is improved from 30.3 to 34.2.

## The accuracy of the program
Run following command to get the accuracy of the program:
```python3 src/run.py < data/input.txt > data/output.txt && python3 src/rate.py```
| $\lambda$ | char acc% | line acc% |
| --------- | --------- | --------- |
| 0.999       | 87.64     |  47.90    |
| 0.95        | 87.67     |  47.70    |
|0.8      | 87.31     |  46.51    |
|0.5      | 85.39     |  39.92   |

The actual running time (training model not included) is about 7 seconds for the given input (501 lines).

## Sample Analysis
### Perfect Cases
- Input: `xian shi li wo zhong quan chu ji`
  Output: `现实里我重拳出击`
- Input: `zai zhong guo gong chan dang de ling dao xia wo men bi jiang sheng li`
  Output: `在中国共产党的领导下我们必将胜利`

### Wrong Cases
- Input: `tan xin suan fa`
  Output: `谈心算法`
  Answer: `贪心算法`
This is due to the fact that `tan` is more likely to be `谈` than `贪`, and the model doesn't consider the whole word `贪心算法`. (Single character frequency)

- Input: `wo xin li zong shi jue de bu tai shu fu`
  Output: `我心理总是觉得不太舒服`
  Answer: `我心里总是觉得不太舒服`
This output is nearly perfect, except for the confusion between `心理` and `心里`. The texts from the corpus are from news, so they are more formal and. However, in daily life, when someone speaks `xin li`, they usually mean `心里` instead of `心理`. (Corpus is comprehensive)

- Input: `xiao hong shi yi ge neng ge shan wu de xiao gu niang`
  Output: `小红十一个能歌善物的小姑娘`
  Answer: `小红是一个能歌善舞的小姑娘`
There are two mistakes. For the first one, the verb is missing. If our program can recognize parts of speech, it could avoid this mistake. (One possible improving direction)
For the second one, the model doesn't consider the whole word `能歌善舞`,
which and its pronunciation is unique. Our program is lack of vision: it only considers the current character and the previous one. (Use $m$-model, $m>2$)
>>>>>>> b35368d (commit)
