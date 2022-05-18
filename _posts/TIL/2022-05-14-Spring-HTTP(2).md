---
title: "Spring (5) HTTP 기본, HTTP 메서드"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---
# 3. HTTP 기본

## 1) 모든 것이 HTTP

HTTP는 HyperText Transfer Protocol이다. 시작은 HTML 전송 프로토콜이었지만 이제는 모든 것을 담는다

- HTML, TEXT, JSON, XML
- IMAGE, 음성, 영상, 파일
- 서버간에 데이터를 주고 받을 때 마저도
- 거의 모든 형태의 데이터 전송

### 기반 프로토콜

- TCP기반 : HTTP/1.1, HTTP/2
- UDP기반 : HTTP/3

UDP 기반으로 넘어가는 추세

### HTTP 특징

- 클라이언트-서버 구조
- 무상태 프로토콜, 비연결성
- 메시지로 통신
- 단순하고 확장이 용이

아래에서 설명한다!

## 2) 클라이언트 서버 구조

- Request-Response 구조이다.
- 클라이언트는 서버에 요청을 보내고, 응답을 무지성으로 기다린다.
- 서버는 요청에 대한 결과를 만들어 응답한다!

단순해보이는데, 예전에는 클라이언트와 서버의 개념이 없어서 둘이 분리되어있지 않았다고 한다.

지금은 당연해보이지만, 이게 사실 중요한 개념인 것이다.

서버에는 데이터나 비지니스 로직을 다 집어넣고, 클라이언트는 사용성에 집중할 수 있게되는데, 이러면 클라이언트와 서버가 각각 따로 진화할 수 있게 된다.

## 3) Stateful,  Stateless

### Stateful

- 서버가 클라이언트의 상태를 보존한다는 것이다.
- 예시를 보자.
    - Customer : 이 노트북 얼마인가요?
    - Staff : 100만원 입니다.
    - C : 2개 구매할게요
    - S : 200만원 입니다. 신용카드, 현금중 어떤걸로 구매하시겠어요?
    - C : 신용카드요
    - S : 200만원 결제 완료되었습니다.
- Staff는 customer가 노트북을 구매하는 것, 2개를 구매하는 것을 계속 인지하고 있었기에 마지막에 ”신용카드요“라는 말에 별다른 질문 없이 결제를 도왔다.
- 중간에 staff가 바뀌면, 해당 staff에게 관련 정보를 모두 넘겨야 결제를 도울 수 있었을 것이다.

### Stateless

- 상태를 보존하지 않는 것이다.
- 예시를 보자.
    - Customer : 이 노트북 얼마인가요?
    - Staff : 100만원 입니다.
    - C : 노트북 2개 구매할게요
    - S : 노트북 2개는 200만원입니다. 신용카드, 현금중 어떤걸로 구매하시겠어요?
    - C : 노트북 2개를 신용카드로 구매할게요
    - S : 200만원 결제 완료되었습니다.
- Staff는  customer가 요구하는 것을 기억하고 있지 않는 상황이다. **서버는 클라이언트의 상태를 보존하지 않는 것이다. 따라서 customer는 요구사항이 있을 때마다, 이를 staff가 수행하기 위해 필요한 정보를 모두 제공했다**.
- 중간에 staff가 바뀌었어도, customer는 모든 정보를 제공하기 때문에 아무 무리가 없었을 것이다.
- 이런 경우 갑자기 클라이언트 요청이 증가해도 서버를 대거 투입할 수 있다. 서버 증설을 무한히 할 수 잇게 되는 것이다.

![0514(1)](https://gonnnnn.github.io/image/TIL/0514(1).png)

### Stateless의 한계

- 로그인의 경우 로그인 했다는 상태를 서버에 유지해야한다.
- 일반적으로 쿠키와 서버 세션을 사용해 상태 유지
- 상태 유지는 최소한만 사용하도록 한다.
- 데이터를 너무 많이 보내는 단점이 있기도 하다.

## 4) Connectionless

- 클라이언트의 요청에 서버가 응답하면 더 이상 해줄게 없다. 따라서 연결을 유지하지 않고 끊어내는 것을 비연결성이라고 한다.
- HTTP는 기본이 연결을 유지하지 않는 모델이다.
- 1시간 동안 수천명이 서비스를 사용해도 실제 서버에서 동시에 처리하는 요청은 수십개 이하로 매우 작을 수 있다. 웹에서는 계속 연속해서 검색 버튼을 누르는건 아니잖아?!

### 한계

- TCP/IP 연결을 그때 그때 새로 해야한다. 3 way handshake 시간 추가 ㅠㅠ
- 프론트엔드단을 조금 봐봤으면 알겠지만, 페이지 하나 렌더링한다고 HTML뿐만 아니라 js, css, 기타 리소스 한번에 다 보내야한다.
- 지금은 ***HTTP Persistent Connections***로 문제를 해결했다. 내부적으로 구현은 좀 다르지만 연결을 조금 오래동안 유지하며 요청, 응답 필요한게 모두 해결되면 연결을 끊는다.

HTTP 초기 - 연결, 종료 낭비 vs Persistent Connections

![0514(2)](https://gonnnnn.github.io/image/TIL/0514(2).png)

![0514(3)](https://gonnnnn.github.io/image/TIL/0514(3).png)

### 무시무시 덜덜

- 같은 시간에 딱 맞춰서 발생하는 대용량 트래픽은 무섭다.
- 선착순 이벤트, KTX 예약, 선착순 이벤트 등등
- ***어떻게든 머리를 쥐어짜내서 stateless하도록 개발하자***!
- 보통 정적페이지 하나 뿌려놓고, 사람들이 거기서 좀 확인할거 확인하게 한다음에 이벤트 참여하도록 유도한다고. 그럼 거기서 뭘 좀 보다가 누르고 그러게 되니까

## 5) HTTP 메시지

### 구조

- Start-line
- header
- CRLF(공백, 엔터)
- message body

![0514(4)](https://gonnnnn.github.io/image/TIL/0514(4).png)

### Start-line

request-line / status-line으로 나뉜다.

- request-line
    - method SP(공백) request-target(path) SP HTTP-version CRLF 으로 이루어진다.
    - method에는 GET, POST등이 있으며 서버가 수행해야할 동작을 지정한다.
    - path는 ’/’로 시작하는 절대 경로로 시작하며 query를 이어쓴다.
- status-line
    - HTTP-version SP status-code SP reason-phrase CRLF
    - status-code는 요청에 대한 응답의 성공과 실패를 종류별로 나타낸다.
    - reason-phrase는 상태코드를 사람이 이해할 수 있도록 간략하게 표현하는 부분이다.

### HTTP 헤더

- field-name “:” OWS(띄어쓰기를 허용한다는 뜻) field-value OWS
    - Host: ..., Content-Type: ... 등이 들어간다.
    - Field name은 대소문자를 구분하지 않는다.
- HTTP 전송에 필요한 모든 부가 정보가 들어간다.
    - 메시지의 크기, 타입, 웹브라우저 정보, 인증에 관한 정보, 캐시 관리 정보 등등..
    - 메시지 바디 빼고 필요한 메타 정보는 여기 다 때려박는다.
    - 임의의 헤더를 추가할 수도 있다.

### HTTP 메시지 바디

- 실제 전송할 데이터
- HTML, 이미지, 영상, JSON 등 byte로 표현 가능한 모든 정보를 담을 수 있다.

# 4. HTTP 메서드

## 1) 리소스와 행위의 분리

- 리소스의 의미가 뭔지 생각해보자
    - 회원을 등록하고 수정하고 조회하는건 리소스가 아니다
    - ***회원이라는 개념 자체가 리소스***이다.
- 행위는 회원(리소스)를 조회, 등록, 수정, 삭제 등등.. 을 하는 것이다.
- 리소스 식별은 리소스를 가지고 하자! /read-every-member같이 행위를 집어 넣지 마라는 것. 다른거 하지 말고 회원 ***리소스를 URI에 매핑***하라는 소리다.
- 설계해본다면 아래와 같다. 계층 구조상 상위를 컬렉션으로 보고 복수단어 사용을 권장한다. member가 아니라 members와 같이
    - 회원 목록 조회 : /members
    - 회원 조회, 등록, 수정, 삭제 : /members/{id}
- ***행위는 method를 통해 구별***한다.

## 2) GET, POST, PUT, PATCH, DELETE

### GET

GET /members/100 HTTP/1.1

- 리소스 ***조회***
- 서버에 전달하고 싶은 ***데이터는 query를 통해*** 전달
- 메시지 바디를 사용해 데이터 전달은 가능하다. 하지만 지원하지 않는 곳이 많다.
- 보통 200으로 응답

### POST

POST /members HTTP/1.1

- 요청 ***데이터 처리, 주로 등록에 사용***
- ***메시지 바디를 통해 서버로 요청 데이터 전달***
- 서버는 요청 데이터를 처리한다. 주로 신규 리소스 등록, 프로세스 처리
- 보통 201로 응답
- 자원이 신규 생성된 location도 응답에 포함해 보내주기도 한다.

### POST에서 리소스 “처리”란?

- 새 리소스 생성
- ***요청 데이터 처리***
    - 단순히 데이터 생성을 넘어서서 프로세스를 처리해야하는 경우
    - 상품 주문, 결제완료, 배달시작, 배달완료 처럼 단순 값 변경을 넘어서 프로세스의 상태가 변환다.
    - EX) 사장님이 음식이 다 되어가면 배달요청 버튼을 누를 것이고 이는 라이더를 호출할 것
    - 따라서 ***꼭 새로운 리소스가 생성되지 않을 수도 있다는 것***
    - 행위는 URI에 넣지 말라고 했지만, 어쩔 수 없이 그렇지 못할 때도 있다 ㅠㅠ. 이런 것을 컨트롤 URI라고 한다. ex) POST /orders/{orderID}/start-delivery
- 다른 메서드로 처리하기 어려운 경우
    - JSON으로 조회 데이터를 넘겨야 하는데, GET 메서드를 사용하기 어려운 경우. ***어쩔 수 없을 때, 애매하면 POST***

### PUT

PUT /members/100 HTTP/1.1

- 리소스를 ***대체***
    - 리소스가 있으면 대체, 없으면 생성. 있으면 덮어쓰는 것이다.
    - 다만, “완전히” 덮어써버린다. 기존 리소스를 완전히 대체해버린다. 부분 수정 안된다.
- 중요한건 PUT은 POST와 달리, 리소스의 정확한 위치를 GET마냥 명시한다. 당연히 그래야 해당 리소스가 있는지 없는지 확인하고, 있으면 대체하고 없으면 생성할 수 있겠지?

### PATCH

- 리소스를 ***부분 변경***

### DELETE

- 리소스를 ***제거***

HEAD, OPTIONS, CONNECT, TRACE와 같은 기타 메서드 들도 있다.

## 3) HTTP 메서드의 속성

### 안전 SAFE

- ***호출해도 리소스가 변경되지 않는다***. GET은 당연히 안전하고, POST, PUT 등은 그렇지 않다.
- 계속된 호출로 로그가 쌓여 장애가 발생할 수 있다. 여기서의 ***안전은 해당 리소스만 고려***한다. 그 외의 부분은 고려 X

### 멱등 IDEMPOTENT

- 한번이든, 두번이든 100번 ***호출***하든 ***결과가 똑같다***.
- GET, PUT, DELETE을 보자. 똑같은 요청을 3501481204번을 해도 결과는 같다.
- ***POST는 아니다. 두 번 호출하면 같은 결제가 중복해서 두번 발생할 수도***!
- 따라서 ***자동 복구 메커니즘***에 쓴다.
    - 서버가 TIMEOUT 등으로 정상 응답을 못주었을 때, 클라이언트가 같은 요청을 다시 해도 되는가?에 대한 판단 근거가 된다!
- 재요청 중간에 다른 곳에서 리소스를 변경해버렸을 수도 있다. 멱등은 외부 요인으로 중간에 리소스가 변경되는 것 까지는 고려하지 않는다.

### 캐시가능 CACHEABLE

- 응답 결과 리소스를 캐시해서 사용해도 되는가에 관한 것이다.
- 이미지를 보내줬을 때, 안그래도 용량이 큰데 굳이 또 보내야하나? 웹 브라우저에 이걸 저장시키는 것이다.
- GET, HEAD, POST, PATCH는 캐시가 가능하다.
    - 하지만 실제로 GET, HEAD 정도만 캐시로 사용한다. GET은 URL만 키로 잡고 구현하면 되기에 쉽다.
    - POST, PATCH는 본문 내용까지 캐시 키로 고려해야하는데, 구현이 쉽지 않다.