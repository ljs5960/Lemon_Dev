# LEMON Project
#### 최종업데이트 2022.01.25
----------------
### 프로젝트 실행방법
> 1. mysettings.py 파일을 프로젝트 최상단에 넣습니다.
> 2. ``` pip install -r requirements.txt ``` 명령어를 통해 프로젝트에 필요한 pip list 를 설치합니다.
> 3. ``` python manage.py runserver --settings=lemon.settings.local ``` 명령어를 통해 로컬 서버를 실행할수있습니다.
> 4. 기존방식인 ``` python.manage.py runserver ``` 명령어를 사용 하고싶으면, 명령어창에 ```  set DJANGO_SETTINGS_MODULE=lemon.settings.local ``` 입력후, 동일한 방법으로 로컬 서버를 실행하면 됩니다.
-------
### Changelog
#### 2022.01.25

[시스템]
1. accounts / admin / calendars / stock 4개의 앱으로 분리하였습니다.
2. accounts 앱 내의 templates 폴더 내 파일들을 각 앱에 맞는 html 파일들을 분리시켰습니다.
3. ```addlist.html```(포트폴리오페이지)를 ```portfolio.html``` 로 이름 변경하였습니다.

[로그인페이지]

1. Apple 계정으로 로그인 버튼을 삭제하였습니다.
2. ID,PW 입력을 통해 로그인 방식을 추가하였습니다.

[알리고 기능]

1. 현재 알리고 기능은 정상작동합니다. 다만 lemon앱 알리고 KEY가 아니여서 비활성화 한 상태 및 테스트(개발)모드로 작동중입니다. 인증번호는 cmd창에서 확인가능합니다.
#### 2022.01.24
[시스템]
1. settings.py 의 파일을 로컬서버, 배포서버로 분리하였습니다.

[로그인]

1. ID,PW 입력을 통해 로그인 방식을 제거하였습니다.
2. Apple 계정으로 로그인 방식을 추가하였습니다.

[공지사항]
1. 공지사항 페이지 내 상단바 레몬 로고 클릭시 오류나는 부분을 수정하였습니다.

[자산설정]

1. 가상자산을 입력받을수있는 기능을 추가하였습니다.
2. 가상자산이 null 값인 상태에서 자산설정시 오류가 나는 부분을 수정했습니다.

[pin번호 변경]

1. 핀번호 입력 기능을 추가하였습니다.

[홈]

1. 구현이 되지 않는 부분은 CSS 처리 ```display:none;``` 처리하였습니다.(주식 div, 총 자산 div)

[가계부]

1. 누적금액 영역의 지출,수입 금액 표기가 안되는 부분 수정하였습니다.
2. 페이지네이션에서 달력 -> TOP5 로 명칭 변경하였습니다.
3. 내역페이지에서 상세검색시 월이 구분되지 않은부분을 수정하였습니다.

---------
### HTML 템플릿 이름 정리
- ``` 404.html ``` : 404 페이지
- ``` 500.html ``` : 500 페이지
- ``` add_calendar.html ``` : 지출, 수입내역을 추가하는 페이지
- ``` base.html ``` : html 상속에 필요한 공통부분이 정리된 html
- ``` category_detail.html ``` : 가계부 내 TOP5 Chart.js 카테고리 클릭시 정렬된 카테고리를 보여주는 페이지
- ``` detail_search.html ``` : 내역페이지에서 날짜 지정해서 조회 해당 날짜에 맞는 내역 리스트를 보여주는 페이지
- ``` edit_myinfo.html ``` : 내정보 수정페이지
- ``` form_errors.html ``` : 장고 폼 오류시 에러문 출력해주는 페이지
- ``` history.html ``` : 가계부 내 내역 페이지
- ``` home.html ``` : 홈화면
- ``` iedit_calendar.html ``` : 수입내역 수정 페이지
- ``` input_pin.html ``` : 핀번호 수정 페이지
- ``` invest.html ``` : 내정보 페이지 내 가상자산 입력 페이지
- ``` login.html ``` : 로그인 페이지
- ``` main.html ``` : 홍보페이지(PC접속이 나오는 페이지)
- ``` myinfo.html ``` : 내정보 페이지
- ``` notice_detail.html ``` : 공지사항 게시글 페이지
- ``` notice.html ``` : 공지사항 페이지
- ``` portfolio.html ``` : 주식 포트폴리오 페이지
- ``` qna.html ``` : 카카오 채널 연결 페이지
- ``` stock.html ``` : 주식페이지
- ``` summary.html ``` : 가계부 내 요약 페이지
- ``` top5.html ``` : 가계부 내 TOP5 페이지
- ``` user_delete.html ``` : 회원탈퇴 페이지
