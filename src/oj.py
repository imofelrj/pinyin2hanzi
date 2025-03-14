import json
from math import log
from sys import stdin, stdout

pinyin_hanzi = {} # pinyin: [hanzi], 'ai': ['锿', '暧']
hanzi_count  = {} # hanzi: count,    '嫩': 4006
word_count   = {} # word: count,     '巴 嫩': 548

total_hanzi = 0
total_word = 0
const_penalty = 20 # set to 20, 34.2 points gained
ratio = 0.95
# const        = json.load(open('const.json','r'))
# keywords     = json.load(open('keywords2.json','r'))
const = {
    "gai ge"    : "改革",
    "xia ao"    : "夏奥",
    "bai ke"    : "百科",
    "jin tian"  : "今天",
    "ming tian" : "明天",
    "zuo tian"  : "昨天",
    "zheng fu"  : "政府",
    "fa lv"     : "法律",
    "ren min"   : "人民",
    "kong ju"   : "恐惧",
    "guo jia"   : "国家",
    "xue sheng" : "学生",
    "xue xiao"  : "学校",
    "da xue"    : "大学",
    "fei ji"    : "飞机",
    "wen hua"   : "文化",
    "ke xue"    : "科学",
    "shi jie"   : "世界",
    "ke ji"     : "科技",
    "gong si"   : "公司",
    "di tu"     : "地图",
    "gong an"   : "公安",
    "zi ran"    : "自然",
    "zi ben"    : "资本",
    "di qiu"    : "地球",
    "xin wen"   : "新闻",
    "shang dian": "商店",
    "chuang hu" : "窗户",
    "jia zhi"   : "价值",
    "li xiang"  : "理想",
    "sheng huo" : "生活",
    "guan xi"   : "关系",
    "xue xi"    : "学习",
    "huan jing" : "环境",
    "chuang zao": "创造",
    "zhan lve"  : "战略",
    "zhan lue"  : "战略",
    "zhan zheng": "战争",
    "zhan dou"  : "战斗",
    "nei juan"  : "内卷",
    "ying xiong": "英雄",
    "yi qing"   : "疫情"
}

keywords = {
    "bing dun dun": [
        "冰墩墩",
        3
    ],
    "xiao xue ren": [
        "小雪人",
        3
    ],
    "jing jin ji": [
        "京津冀",
        3
    ],
    "tian an men": [
        "天安门",
        3
    ],
    "shan hai guan": [
        "山海关",
        3
    ],
    "zhong guo meng": [
        "中国梦",
        3
    ],
    "dong ao hui": [
        "冬奥会",
        3
    ],
    "zhang jia kou": [
        "张家口",
        3
    ],
    "da xing an ling": [
        "大兴安岭",
        4
    ],
    "di qiu cun": [
        "地球村",
        3
    ],
    "jiu zhai gou": [
        "九寨沟",
        3
    ],
    "tai ping yang": [
        "太平洋",
        3
    ],
    "zhong qiu jie": [
        "中秋节",
        3
    ],
    "zhong hua min zu": [
        "中华民族",
        4
    ],
    "sheng dan jie": [
        "圣诞节",
        3
    ],
    "long feng cheng xiang": [
        "龙凤呈祥",
        4
    ],
    "chang e ben yue": [
        "嫦娥奔月",
        4
    ],
    "dong fang hong": [
        "东方红",
        3
    ],
    "he xie hao": [
        "和谐号",
        3
    ],
    "fu xing hao": [
        "复兴号",
        3
    ],
    "hong lou meng": [
        "红楼梦",
        3
    ],
    "xi you ji": [
        "西游记",
        3
    ],
    "bao qing tian": [
        "包青天",
        3
    ],
    "shui hu zhuan": [
        "水浒传",
        3
    ],
    "chang e hao": [
        "嫦娥号",
        3
    ],
    "long fei tian": [
        "龙飞天",
        3
    ],
    "xi jing ping": [
        "习近平",
        3
    ],
    "li ke qiang": [
        "李克强",
        3
    ],
    "deng xiao ping": [
        "邓小平",
        3
    ],
    "wen tian xiang": [
        "文天祥",
        3
    ],
    "tang bo hu": [
        "唐伯虎",
        3
    ],
    "jiang ze min": [
        "江泽民",
        3
    ],
    "yang li wei": [
        "杨利伟",
        3
    ],
    "zhong hua min guo": [
        "中华民国",
        4
    ],
    "zhong guo ren min": [
        "中国人民",
        4
    ],
    "guang ming ri bao": [
        "光明日报",
        4
    ],
    "xin hua she": [
        "新华社",
        3
    ],
    "ren min ri bao": [
        "人民日报",
        4
    ],
    "da shi guan": [
        "大使馆",
        3
    ],
    "bo wu guan": [
        "博物馆",
        3
    ],
    "guo wu yuan": [
        "国务院",
        3
    ],
    "ke xue yuan": [
        "科学院",
        3
    ],
    "ke xue jia": [
        "科学家",
        3
    ],
    "qing shao nian": [
        "青少年",
        3
    ],
    "da xue shi sheng": [
        "大学师生",
        4
    ],
    "da xue sheng": [
        "大学生",
        3
    ],
    "gong chan dang": [
        "共产党",
        3
    ],
    "zai guang li": [
        "在光里",
        3
    ],
    "ji xiang wu": [
        "吉祥物",
        3
    ],
    "yu sheng jie xian": [
        "羽生结弦",
        4
    ],
    "zui you jie": [
        "最优解",
        3
    ],
    "min zhu zhuan zheng": [
        "民主专政",
        4
    ],
    "zi qiang bu xi": [
        "自强不息",
        4
    ],
    "hou de zai wu": [
        "厚德载物",
        4
    ],
    "guan zhuang bing du": [
        "冠状病毒",
        4
    ],
    "ji tou gong": [
        "记头功",
        3
    ],
    "wang zhe rong yao": [
        "王者荣耀",
        4
    ],
    "wan li chang cheng": [
        "万里长城",
        4
    ],
    "bu rong xiao qu": [
        "不容小觑",
        4
    ],
    "sheng huo dang zhong": [
        "生活当中",
        4
    ],
    "shu tu tong gui": [
        "殊途同归",
        4
    ],
    "xiao hua mao": [
        "小花猫",
        3
    ],
    "ka bu qi nuo": [
        "卡布奇诺",
        4
    ],
    "shu xue fen xi": [
        "数学分析",
        4
    ],
    "ming yue guang": [
        "明月光",
        3
    ],
    "gan dao kuai le": [
        "感到快乐",
        4
    ],
    "jian bing guo zi": [
        "煎饼果子",
        4
    ],
    "guo yu fang si": [
        "过于放肆",
        4
    ],
    "qing kuai su": [
        "请快速",
        3
    ],
    "wei sheng zhi": [
        "卫生纸",
        3
    ],
    "xiao si le": [
        "笑死了",
        3
    ],
    "hou yan wu chi": [
        "厚颜无耻",
        4
    ],
    "liang zi li xue": [
        "量子力学",
        4
    ],
    "chang jiang da qiao": [
        "长江大桥",
        4
    ],
    "xian shi zhong": [
        "现实中",
        3
    ],
    "wei wei nuonuo": [
        "唯唯诺诺",
        4
    ],
    "bi zhe yan": [
        "闭着眼",
        3
    ],
    "zhong quan chu ji": [
        "重拳出击",
        4
    ],
    "xiang jian ni": [
        "想见你",
        3
    ],
    "wo fa shi": [
        "我发誓",
        3
    ],
    "jing zhuang ti": [
        "晶状体",
        3
    ],
    "chi zha ji": [
        "吃炸鸡",
        3
    ],
    "miao miao jiao": [
        "喵喵叫",
        3
    ],
    "tai wu liao le": [
        "太无聊了",
        4
    ],
    "xin shang ren": [
        "心上人",
        3
    ],
    "qu yin hang": [
        "去银行",
        3
    ],
    "you xian sou suo": [
        "优先搜索",
        4
    ],
    "bian yi yuan li": [
        "编译原理",
        4
    ],
    "shou ji ping": [
        "手机屏",
        3
    ],
    "tian xuan zhi ren": [
        "天选之人",
        4
    ],
    "yu zhong zhi lei": [
        "雨中之泪",
        4
    ],
    "yi wu shi chu": [
        "一无是处",
        4
    ],
    "bu zi jin": [
        "不自禁",
        3
    ],
    "ru he shi hao": [
        "如何是好",
        4
    ],
    "zi si zi li": [
        "自私自利",
        4
    ],
    "sheng hua huan cai": [
        "生化环材",
        4
    ],
    "yi hui er": [
        "一会儿",
        3
    ],
    "nao dong da kai": [
        "脑洞大开",
        4
    ],
    "gong cheng ming jiu": [
        "功成名就",
        4
    ],
    "tai qi tou": [
        "抬起头",
        3
    ],
    "san shi yi ting": [
        "三室一厅",
        4
    ],
    "san guo yan yi": [
        "三国演义",
        4
    ],
    "kuai ji": [
        "会计",
        2
    ]
}

class Path:
    def __init__(self, string, final_char, length):
        self.string = string
        self.final_char = final_char
        self.length = length

def distance(hanzi1, hanzi2): # conditional prob p(hanzi2|hanzi1)
    combine = hanzi1 + ' ' + hanzi2
    ratio1 = word_count.get(combine,0) / total_word
    ratio2 = hanzi_count.get(hanzi1,0) / total_hanzi
    ratio3 = hanzi_count.get(hanzi2,0) / total_hanzi
    if ratio2 == 0 or ratio3 == 0 or ratio1 == 0:
        return float('inf')
    else:
        ret = -log(ratio*(ratio1 / ratio2)+(1-ratio)*ratio3)
        # ret = -log(ratio1 / ratio2)
        return ret

def refresh(string, obs):
    res = ''
    for syllable in obs:
        res += syllable + ' '
    for keyword_pinyin in keywords:
        pos = res.find(keyword_pinyin)
        if pos != -1:
            count = 0
            for i in range(0,pos):
                if res[i] == ' ':
                    count += 1
            
            keyword_hanzi = keywords[keyword_pinyin][0]
            length = keywords[keyword_pinyin][1]
            replace_text = ''
            for i in range(0,length):
                replace_text += string[count+i]
            string = string.replace(replace_text, keyword_hanzi)
    return string

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
                    prob = -log(prob)
                    path = Path(hanzi, hanzi, prob) # to be determined, dont know probability of a single hanzi
                    paths.append(path) # path of generation 0
        else:
            new_paths = []
            if obs[index-1]+' '+obs[index] in const:
                const_word = const[obs[index-1]+' '+obs[index]]
                for path in paths:
                    if path.final_char == const_word[0]:
                        new_paths.append(Path(path.string + const_word[1], const_word[1], path.length)) # high priority when matching const
                        break
            else:
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
                                new_path = Path(path.string + hanzi, hanzi, path.length + distance(path.final_char, hanzi))
                                # new_path = Path(path.string + hanzi, hanzi, 
                                #                 ratio*(path.length + distance(path.final_char, hanzi))+(1-ratio)*hanzi_count[hanzi]/total_hanzi)
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

    mini = Path('', '514', float('inf'))
    for path in paths:
        if path.length < mini.length:
            mini = path
    mini.string = refresh(mini.string, obs)
    stdout.write(mini.string + '\n')
    
with open('word2pinyin.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        hanzi, pinyin = line.split(' ')
        pinyin = pinyin.strip()
        if pinyin not in pinyin_hanzi:
            pinyin_hanzi[pinyin] = [hanzi]
        else:
            pinyin_hanzi[pinyin].append(hanzi)

with open('1_word.txt', 'r') as f:
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

with open('2_word.txt', 'r') as f:
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

for line in stdin:
    observation = [e.strip() for e in line.split(' ')]
    viterbi(observation)

# with open('input.txt', 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         observation = [e.strip() for e in line.split(' ')]
#         viterbi(observation)
