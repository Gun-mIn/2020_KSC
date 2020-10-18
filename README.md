# Implementation of Text Data Analysis and Human-Web Interaction for Improving Web Accessibility of Blind People

&nbsp;&nbsp;&nbsp;&nbsp;한국 시각장애인의 웹 접근성은 시각이 있는 인터넷 사용자와 비교했을 때, 현저히 낮은 수준에 있다. 시각장애 인터넷 사용자는 e-정부 사이트 이용과 같은 사회 활동적 측면 뿐만 아니라, e-캠퍼스와 같은 교육적 측면에서도 불편을 겪고 있다. 따라서, 본 연구는 한국의 **전맹** 시각장애인을 대상으로 웹 접근성을 높일 수 있는 방법을 새롭게 제안 및 구현하였다.


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

## OS & Browser Support
| OS | Browser  |
|--|--|
| <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Windows_10_Logo.svg" width = "200" height="80"> | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/512px-Google_Chrome_icon_%28September_2014%29.svg.png" width="100"/> |

 
https://youtu.be/gTFmJWGsmNE

## References
1. [lovit textrank Git Repo](https://github.com/lovit/textrank/)
2. [링크 텍스트](https://colab.research.google.com/drive/1Xi7VsbFSpxo3--Ejwv4khE7lFzBjx2Ct#scrollTo=6DAcEokJX7CC)
