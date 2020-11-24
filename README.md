
# Implementation of Text Data Analysis and Human-Web Interaction for Improving Web Accessibility of Blind People

&nbsp;&nbsp;&nbsp;&nbsp;한국 시각장애인의 웹 접근성은 시각이 있는 인터넷 사용자와 비교했을 때, 현저히 낮은 수준에 있다. 시각장애 인터넷 사용자는 e-정부 사이트 이용과 같은 사회 활동적 측면 뿐만 아니라, e-캠퍼스와 같은 교육적 측면에서도 불편을 겪고 있다. 따라서, 본 연구는 한국의 **전맹** 시각장애인을 대상으로 웹 접근성을 높일 수 있는 방법을 새롭게 제안 및 구현하였다.

# How to use - Quick Start

 1. `git clone https://github.com/Gun-mIn/2020_KSC.git` 로 프로젝트를 복사한다.
 2. cmd 창에서 `pip install -r requirements.txt` 를 실행하여 필요한 모든 패키지를 설치한다.
 3. cmd 창에서 `pip install -r textrank.txt` 를 실행하여 [lovit의 textrank 패키지](https://github.com/lovit/textrank.git)를 설치한다.
 4. textrank를 이용하여 추출한 요약문과, 원문의 내용을 TTS의 합성음으로 듣고 싶다면, **TEXTRANK-namuwiki_and_TTS.py** 를 실행한다. 키보드 숫자 자판을 이용하여 실행 동작 제어가 가능하다.
 5. 나무위키 요약 프로그램의 성능을 알 수 있는 ROUGE 평가 결과를 보고 싶다면, **ROUGE_of_TEXTRANK.py**를 실행한다.

# Description

&nbsp;&nbsp;&nbsp;&nbsp;시각장애 인터넷 사용자에게 텍스트가 집약된 웹 문서(i.e., 인터넷 뉴스 기사, 백과 사전 사이트, etc)는 접근성에 있어서 특히나 장벽이 높은 경우라 할 수 있다. 따라서 우리는 웹 콘텐츠 재구성이 아닌, **데이터 전달적 측면**에서 문제에 새롭게 접근하고자 했다. 

&nbsp;&nbsp;&nbsp;&nbsp;스크린리더에서의 텍스트 데이터 전달 방식은 line by line으로 텍스트를 직렬화하여 순차적으로 출력하는 것이다. 하지만 출력하는 텍스트의 양이 많을수록 청자의 부담(오랜 시간 집중해야 내용을 놓치지 않는다)은 커질 수밖에 없다. 따라서 우리는 자동 요약 기법(Auto Summarization)을 이용하여 **문서를 요약하고(Text Summarization), 요약 정보를 제공 받은 이후 원문에 접근할지를 결정**할 수 있도록 하는 프로그램을 설계 및 구현하였다.


## Key Features

우리 프로그램의 중요 기능은 다음과 같다.

 1. 요약 정보(중요 단어와 중요 문장) 제공.
 2. 원문 제목, 원문 내용 제공.
 3. 중요 단어에 하이퍼링크가 연결되어 있는 경우, 해당 링크로의 이동 기능 제공.
 4. 숫자 키보드만을 이용하여 명령어를 입력 받음.
 5. 음성 인터페이스 기반.

## Limitation & Future Work

 - 현재 1)중요 단어와 연결된 하이퍼링크로의 url 접근 기능과, 2)html 태그를 이용한 원문 제목 크롤링 기능을 구현하기 위해 '[나무위키](https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8 "Go Namu Wiki")'에서만 사용이 가능하다.
 - 블로그 포스트와 같은 SNS의 감성적인 글은, 추출적 요약(Extractive Summarization)의 특성상 요약 정보 생성 결과가 유의미하지 않다.
 - 크롤링해 전처리한 원문 내용의 결과물이 깔끔하지 않다. 만약 위키 사이트 내에서만 구현하고자 한다면, 위키의 내용을 크롤링하는 것을 돕는 [API](https://www.mediawiki.org/wiki/API:Main_page "about Media Wiki API")를 이용하는 편이 훨씬 쉬울 것이다.
 - 추후 다양한 사이트에서 모두 활용이 가능하도록 개선하고, release 버전을 제작하여 사용성 테스트를 진행할 계획이다.


# Implementation
&nbsp;&nbsp;&nbsp;&nbsp;이 프로그램은 PyCharm 에디터를 사용하여 python 3.7로 구현되었다. 사용된 패키지 목록과 지원하는 환경은 아래에 설명되어 있다. 명시된 모든 패키지를 설치해야 실행이 가능하다.

## Supported Environment 

 - 지원하는 사이트는 **나무위키**이다. **위키** 사이트의 경우 하이퍼링크로의 이동에서 접속 오류가 발생하니, 주의해야 한다.
 - Windows 10 환경에서 개발되었고, 다른 환경에서 개발 혹은 실행시키지 않았다. 따라서 확실히 지원하는 환경은 Windows가 유일하다.
 - Chrome 브라우저 상에서 크롤링을 하고, 하이퍼링크로 걸린 url을 open한다. 
 
| OS | Browser | Site |
|--|--|--|
| <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Windows_10_Logo.svg" width = "300" height="60"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/512px-Google_Chrome_icon_%28September_2014%29.svg.png" width="90"/> |<a href = "https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4"><img src="https://w.namu.la/s/895d8eaf4bbb3b9b2ca614bbf22cc8229ce77b2e780d3b63abac8f04510493038affe6e8be4eea6e33a6d1fb5c50733697da8edec268c09b1a585af1df7d11fb9b0381a3638890a6cde85ebd84c5ef64c668ad266bb69863feb52937a5b262c0cd1615100f772c348a588a801574f4dc" width="100">|

## Program Requirements

 - KoNLPy 설치를 위해선, JDK가 준비되어 있어야 한다. 설치에서 참고했던 포스트를 링크해두었다.
 - textrank 패키지의 경우, GitHub Repo에서 `pip install git+https://~`을 이용하여 설치했다. 이론과 예제에 대한 포스트 글과 repo 링크를 걸어두었다.
 - ~~아래 패키지를 모두 설치해야 실행이 가능하다.~~
 - KoNLPy를 위한 환경을 구성했다면, How to use를 따라서 설치하는 것을 권한다.
 

|          |Package  |Version | Remarks     | Category |
|:----------:|:--------:|:--------:|:--------|:--------|
|1|selenium|3.141.0| |crawling|
|2|lxml|4.6.0| |crawling|
|3|[KoNLPy](https://webnautes.tistory.com/1394 "How to install")|0.5.2|JPype1(1.0.2) & Java(1.8.0_261)|text summarization|
|4|scikit-learn|0.23.2| |text summarization|
|5|[textrank](https://lovit.github.io/nlp/2019/04/30/textrank/ "You can see more details of this package!")|0.1.2|released by [*lovit*](https://github.com/lovit/textrank.git "Go to repo")|text summarization|
|6|pynput|1.7.1| |keyboard event|
|7|pyttsx3|2.90| |tts|
|8|urllib3|1.25.10| |go to hyperlinked page|

## Audio-based & Keyboard Interface 
- 프로그램을 실행시키면 아래와 같은 순서로 동작한다.

 1. 키보드 명령어에 대한 안내 음성 출력.
 2. 키보드 명령어 입력.
 3. 해당 기능 수행.
 4. *1*의 음성을 다시 출력.

- 키보드 명령어는 앞서 말했듯이 모두 숫자 자판으로만 입력받으며, 각 숫자별 수행 기능은 다음과 같다.

| 키보드 명령어 | 수행 기능 |
|:--:|:--|
|1|중요 단어, 중요 문장의 음성 출력|
|2|원문 제목, 내용의 음성 출력|
|3|중요 단어에 연결된 하이퍼링크로 이동|
|4|키보드 명령어 안내 음성 다시 출력|
|5|프로그램 종료|

- 프로그램의 시연 동영상은 [Youtube](https://youtu.be/gTFmJWGsmNE)에 업로드해두었다.

#  ROUGE-N Score
textrank를 이용하여 추출한 나무위키 사이트의 요약문에 대하여 ROUGE 평가를 진행하였다. Python의 [rouge 패키지](https://pypi.org/project/rouge/)를 이용했고, 실험 세팅과 결과는 다음과 같다.

## Setting

 1. 3개의 나무위키 글을 선정한 후, textrank 기능으로 요약문을 생성한다.
 2. 3개의 나무위키 글에 대한 요약문을 실험자가 직접 작성한다.
 3. *1*에서 생성된 요약문과 *2*에서 사람에 의해 생성된 요약문을 비교하여 ROUGE-1, ROUGE-2, ROUGE-l 평과 결과를 확인한다.
 4. ROUGE-N 평가의 점수는 F-measure로 계산된 값을 이용하고, 소수점 다섯째 자리에서 반올림한다.

> 이때,  *2*의 실험자가 작성한 요약문은,  textrank가 추출적 요약 기법임을 고려하여 나무위키 글에서 중요하게 생각하는 문장을 3줄 추출하는 방식으로 작성하였다. 물론 textrank로 생성된 요약문을 모르는 상태로 작성하였다.

> ROUGE 평가는 앞서 언급한 python의 [rouge 패키지](https://pypi.org/project/rouge/)를 이용하여 진행하였다. 

## Results
| URL | ROUGE-1 | ROUGE-2 | ROUGE-l |
|:--:|:--:|:--:|:--:|
|1|0.6279|0.5952|0.6835|
|2|0.9739|0.9381|0.9381|
|3|0.6408|0.5941|0.6316|
