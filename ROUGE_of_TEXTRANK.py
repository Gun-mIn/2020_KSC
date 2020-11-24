# -*- coding: UTF-8 -*-

from textrank import *
import urllib.request
from bs4 import BeautifulSoup
import re

from rouge import Rouge

# global variable to store every info
store = [''] * 6

# check string contains korean or not
def isKo(sent):
    encText = sent
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

# get every info(keywords, keysents, hyperlinked keywords and url, origin title and context) and add store
def get_info_from_wiki(origin_url, store_idx):
    ##### crawl txt data #####
    req = urllib.request.Request(origin_url, headers={'User-Agent': 'Mozilla/5.0'})  # add header because of error in wiki
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "lxml")  # add parser

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # 태그, 문자열 제거 이후 남은 태그와 문자열 반환

    ##### pre-processing to get origin context and summarization #####
    text = soup.get_text()  # get every text data

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # remove some words from text data
    text = text.replace(']', ']\n')
    text = text.replace('뉴스)', '\n')
    text = text.replace(')"', '\n "')
    text = text.replace('[편집]', ' ')
    text = text.replace('광고', '')
    text = text.replace('(.)', '')
    text = text.replace('<p>', '\n')
    text = text.replace('/>', '\n')
    text = text.replace('</p>', '\n')
    text = text.replace('갱신중...', '')
    text = text.replace('00:00', '')
    text = text.replace('...', '.\n')
    text = text.replace('다.', '다. ')
    text = text.replace('. ', '.\n')
    text = text.replace('.', '.\n')
    text = text.replace(' |', '\n')
    text = text.replace('-', '\n')

    # remove citation of origin text
    for i in range(50):
        tmp1 = '[{}]'.format(i)
        tmp2 = '{}.'.format(i)
        text = text.replace(tmp1, ' ')
        text = text.replace(tmp2, '\n')

    # list of sentences to get key sentences
    sents = text.split('\n')


    # remove short terms(useless info; e.g., ad, copyright, etc)
    new_sents = []  # to get pure sentences without useless info
    for sent in sents:
        if len(sent.encode("utf-8")) > 60:
            if(sent.find("나무위키는 백과사전") == -1):
                if (sent.find("http") == -1):
                    if (isKo(sent)):
                        new_sents.append(sent)

    # tokenize function using KoNLPy
    from konlpy.tag import Komoran
    komoran = Komoran()

    def komoran_tokenize(sents):
        words = komoran.pos(sents, join=True)
        words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
        return words

    summarizer = KeysentenceSummarizer(tokenize=komoran_tokenize, min_sim=0.3)
    keysents = summarizer.summarize(new_sents, topk=3)


    ##### Preprocess keywords and key sentences for TTS #####
    keysents_tts = ""


    ##### extract & print keywords and keysents as str type #####
    for line in keysents:
        x, y, z = line
        if (z.find(".") == -1):
            z = z + "."
        keysents_tts = keysents_tts + z + "\n"

    # print keywords and key sentences
    print("<주요 문장>\n" + keysents_tts)

    # store info(str)
    store[store_idx] = keysents_tts

# constructor of ROUGE class
rouge = Rouge()

# ROUGE score of URL1
get_info_from_wiki("https://namu.wiki/w/Rouge", 0)
key_sentences1 = store[0]

reference1 = """2000년 4월 17일에 발매된 백지영의 두번째 정규 앨범.
약 36만장의 판매고를 올리면서, 백지영 역대 앨범 중 가장 높은 판매고를 기록한 앨범으로 남아있다.
팬들 사이에서도 오랜 시간동안 제일 퀄리티가 높은 앨범으로 평가되고 있으며, 테크노, 살사, R&B 등 다양한 장르의 곡들로 수록되어 있다."""
print("<Reference>\n", reference1, "\n")
scores1 = rouge.get_scores(key_sentences1, reference1)
print(scores1, "\n")

print("\n")

# ROUGE score of URL2
get_info_from_wiki("https://namu.wiki/w/%EC%A0%95%EC%B9%98%EC%B2%A0%ED%95%99", 1)
key_sentences2 = store[1]
reference2 = """정치철학은 정부, 시민, 국가에 대한 물음을 다룬다.
과거의 정치철학이 자유를 중시하는가 혹은 평등을 중시하는가에 따라서 좌, 우파를 나누었다면, 현대의 정치철학 이론들은 '평등'이라는 단어를 어떻게 해석해야 하는지에 대한 의견 차이를 통해서 나누어지기 때문이다.
이를테면 과거의 자유주의자들은 자유를 사회 구성의 이념의 근본으로 두어야 한다고 여겼던 반면 롤즈를 위시하는 현대의 자유주의자들은 '평등'이라는 말을 정의하기 위해서 자유 개념을 사용하는 사람들이다.
"""
print("<Reference>\n", reference2, "\n")
scores2 = rouge.get_scores(key_sentences2, reference2)
print(scores2, "\n")

print("\n")

# ROUGE score of URL3
get_info_from_wiki("https://namu.wiki/w/CUDA", 2)
key_sentences3 = store[2]
reference3 = """CUDA 플랫폼은 GPU 의 가상 명령어셋을 사용할 수 있도록 만들어주는 소프트웨어 레이어이며, NVIDIA가 만든 CUDA 코어가 장착된 GPU에서 작동한다.
CUDA 프로그램은 스트림 프로세싱에 기반하며, 그 작성에는 C/C++ 언어에 동시에 실행할 쓰레드 개수 등을 선언하는데 사용되는 CUDA 전용 문법을 추가한 언어를 사용한다.
CUDA는 GPU의 메모리 모델을 추상화해서 좀 더 편하게 GPU을 이용할 수 있도록 했다.
"""
print("<Reference>\n", reference3, "\n")

scores3 = rouge.get_scores(key_sentences3, reference3)

print(scores3, "\n")
