from textrank import *
import urllib.request
from bs4 import BeautifulSoup
import re
import pyttsx3
from pynput.keyboard import Listener, KeyCode
import webbrowser


# global variable to store every info
store = []
# keywords[0], keysentences[1], keyword of heyperlink[2], url of hyperlink[3], origin title[4], origin text[5]

# check string contains korean or not
def isKo(sent):
    encText = sent
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

# get every info(keywords, keysents, hyperlinked keywords and url, origin title and context) and add store
def get_info_from_wiki(origin_url):
    print("start the program !\n\n")

    ##### crawl txt data #####
    req = urllib.request.Request(origin_url, headers={'User-Agent': 'Mozilla/5.0'})  # add header because of error in wiki
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, "lxml")  # add parser

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # 태그, 문자열 제거 이후 남은 태그와 문자열 반환


    ##### get origin title #####
    h1 = soup.find_all("h1")    # get all <h1> contents -> title of wiki page
    origin_title = str(h1[0])          # title still contains html tag
    origin_title = origin_title.replace(">", "\n")    # to remove tag
    origin_title = origin_title.replace("<", "\n")    # to remove tag
    title_txt = origin_title.split("\n")       # to remove tag

    for txt in title_txt:   # get only title(text) without html tags
        if(isKo(txt)):
            origin_title = txt


    ##### pre-processing to get origin context and summarization #####
    text = soup.get_text()  # get every text data

    # get every hyperlinks and title of hyperlink
    hyper_list = []

    if (origin_url.find("wiki") != -1):
        for href in soup.find_all('a'):
            hyper = href.get('href')
            word = href.get('title')
            if (word != None):
                if (hyper != None):
                    word_url = "https://namu.wiki" + hyper
                    hyper_list.append((word, word_url))

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
    text = text.replace(' |', '\n')
    text = text.replace('-', '\n')

    # remove citation of origin text
    for i in range(50):
        tmp1 = '[{}]'.format(i)
        tmp2 = '{}.'.format(i)
        text = text.replace(tmp1, ' ')
        text = text.replace(tmp2, '\n')

    # origin contents of wiki page
    origin_text = text.split('\n')

    # list of sentences to get key sentences
    sents = text.split('\n')

    # remove short terms(useless info; e.g., ad, copyright, etc)
    new_sents = []  # to get pure sentences without useless info
    for sent in sents:
        if len(sent.encode("utf-8")) > 60:
            if (sent.find("http") == -1):
                if (isKo(sent)):
                    new_sents.append(sent)

    # pre-process to get pure origin text(str type)
    origin_text_result = ""

    for sent in origin_text:
        if(sent.find("원본 주소") != -1) or (sent.find("이 저작물") != -1):
            break
        num = len(sent.encode("utf-8"))
        if (num > 70):
            if(isKo(sent)):
                origin_text_result += sent


    ##### get key sents and words #####
    # remove duplicated sentences to get key sentences
    tmp_set = set(new_sents)
    new_sents = list(tmp_set)

    # tokenize function using KoNLPy
    from konlpy.tag import Komoran
    komoran = Komoran()

    def komoran_tokenize(sents):
        words = komoran.pos(sents, join=True)
        words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
        return words

    keyword_extractor = KeywordSummarizer(
        tokenize=komoran_tokenize,
        window=-1,
        verbose=False
    )

    keywords = keyword_extractor.summarize(new_sents, topk=30)
    summarizer = KeysentenceSummarizer(tokenize=komoran_tokenize, min_sim=0.3)
    keysents = summarizer.summarize(new_sents, topk=3)


    ##### Preprocess keywords and key sentences for TTS #####
    keyword_tts = ""
    keysents_tts = ""

    # remove duplicated sentences, must have to consider the order of elements
    new_keywords = []
    for elem in keywords:
        x, y = elem

        # remove tags of ward classes
        x = x.replace("/NNP", "")
        x = x.replace("/NNB", "")
        x = x.replace("/NNG", "")
        x = x.replace("/VA", "")
        x = x.replace("/XR", "")
        x = x.replace("/VV", "다")

        if x not in new_keywords:
            if (x != "하다" and x != "되다" and x != "있다" and x != "들다" and x != "분명" and x != "경우"):  # exception of keywords
                new_keywords.append(x)


    ##### get hyperlink page (if keywords have linked page) #####
    # check whether keywords and hyperlink words equal or not
    key_hyperlink = []
    for word in hyper_list:
        x, y = word
        for elem in new_keywords:
            if (x == elem):
                key_hyperlink.append(word)

    if (key_hyperlink != []):
        for hyper in key_hyperlink:
            x, y = hyper
            link_word = x
            store.append(link_word)  # store[0]
            link_url = y
            store.append(link_url)  # store[1]
            break

    if (key_hyperlink == []):
        store.append('none')
        store.append('none')

    ##### extract & print keywords and keysents as str type #####
    i = 0
    for word in new_keywords:
        if (i == 6):
            break

        if len(word.encode("utf-8")) > 3:
            if (word.find("뉴스") != -1):
                continue
            else:
                if (i < 5):
                    keyword_tts = keyword_tts + word + ", "
                else:
                    keyword_tts = keyword_tts + word + "."
                i = i + 1

    for line in keysents:
        x, y, z = line
        if (z.find(".") == -1):
            z = z + "."
        keysents_tts = keysents_tts + z + "\n"

    # print keywords and key sentences
    print("<키워드>\n" + keyword_tts)
    print("<주요 문장>\n" + keysents_tts)

    # store info(str)
    store.append(keyword_tts)           # store[2]
    store.append(keysents_tts)          # store[3]
    store.append(origin_title)          # store[4]
    store.append(origin_text_result)    # store[5]


# initialize TTS engine and return engine
def initialize_TTS():
    # initialize TTS engine
    engine = pyttsx3.init()

    # initialize TTS rate
    engine.setProperty('rate', 160)

    # initialize TTS volume
    engine.setProperty('volume', 1)  # 0~1

    # initialize gender of voice
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)  # 남성

    return engine


# print summarization by voice
def print_summarization_voice(keywords, keysents):
    engine = initialize_TTS()

    engine.say("중요 단어는 다음과 같습니다")
    engine.say(keywords)
    engine.say("중요 문장은 다음과 같습니다")
    engine.say(keysents)

    engine.runAndWait()
    engine.stop()  # stop the TTS engine
    #engine.stop()  # stop the TTS engine


# open the hyperlinked word's wiki page
def go_to_hyperlink(word, url):
    engine = initialize_TTS()

    if(url.find("wiki")):
        engine.say("하이퍼링크로 연결된 단어는")
        engine.say(word)
        engine.say("입니다")
        engine.say("하이퍼링크로 이동합니다")
        webbrowser.open(url)

    else:
        engine.say("하이퍼링크로 연결된 중요 단어가 없습니다.")

    engine.runAndWait()
    engine.stop()  # stop the TTS engine


# print origin title and text by voice
def print_origin_voice(title, context):
    engine = initialize_TTS()

    engine.say("원문 제목은 다음과 같습니다")
    engine.say(title)
    engine.say("원문 내용은 다음과 같습니다")
    engine.say(context)

    engine.runAndWait()
    engine.stop()  # stop the TTS engine


def notice_status():
    engine = initialize_TTS()

    engine.say("프로그램 사용이 준비되었습니다.")
    engine.say("중요 단어와 문장은 일번,, 원문 제목과 내용은 이번,, 중요 단어의 하이퍼링크 페이지로의 이동은 삼번,,  다시 듣기는 사번,, 프로그램 종료는 오번을 눌러주세요.")

    engine.runAndWait()
    engine.stop()  # stop the TTS engine

def notice_exit_program():
    engine = initialize_TTS()
    engine.say("프로그램을 종료합니다.")

    engine.runAndWait()
    engine.stop()

def get_url():
    engine = initialize_TTS()
    engine.say("문서요약을 원하시는 링크를 입력해주세요.")
    engine.runAndWait()
    engine.stop()

    origin_url = input("Wiki url :  ")
    return origin_url

def handlePress(key):
    if key == KeyCode(char='1'):
        print_summarization_voice(store[2], store[3])
        notice_status()

    elif key == KeyCode(char='2'):
        print_origin_voice(store[4], store[5])
        notice_status()

    elif key == KeyCode(char='3'):
        go_to_hyperlink(store[0], store[1])
        notice_status()

    elif key == KeyCode(char='4'):
        notice_status()


def handleRelease(key):
    print('Released: {}'.format(key))

    # 종료
    if key == KeyCode(char='5'):
        notice_exit_program()
        return False



origin_url = get_url()
get_info_from_wiki(origin_url)
notice_status()

with Listener(on_press=handlePress, on_release=handleRelease) as listener:
    listener.join()
