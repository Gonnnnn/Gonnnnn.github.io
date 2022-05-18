---
title: "Spring (7) HTTP 헤더, 인증"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 7. HTTP 헤더 - 일반

## 1) 헤더

- field-name: field-value
- HTTP 전송에 필요한 모든 정보
- 필요시 임의의 헤더 추가 가능

### Message body - RFC7230

- 메시지 본문(body)을 통해 표현 데이터 전달
    - 표현 = 표현 데이터 + 표현 메타 데이터
    - 표현은 요청이나 응답에서 실제 전달할 데이터
- 메시지 본문은 페이로드라고도 한다.
- 표현 헤더는 표현 데이터를 해석할 수 있는 정보 제공
- 표현 헤더와 페이로드 헤더를 구분해야하지만, 어려우니 생략

## 2) 표현

특정 리소스를 어떠한 표현(json, html 등..)으로 전달할 것인지에 대해 명시해야한다. 리소스는 추상적인 단어이다. 리소스는 DB에 있을 수도 있고, 서버 내의 파일일 수도 있고 제 각각이다.

- Content-Type
    - body의 내용이 뭐야?!
    - text/html;charset=UTF-8, applilcation/json 등등
- Content-Encoding
    - 표현 데이터의 압축 방식
    - gzip, deflate, identity(압축 안함) 등
- Content-Language
    - 표현 데이터의 자연 언어
    - ko, en, en-US 등
- Content-Length
    - 길이. 바이트 단위
    - 정확히는 페이로드 헤더인데 그냥 표현 헤더에 넣었다고 강사님이 언급
    - Transfer-Encoding을 사용하면 Content-Length를 사용하면 안됨. 나중에 언급

## 3) 협상(Contents Negotiation)

클라이언트가 선호하는 표현 요청. 서버는 클라이언트가 원하는 방식으로 주려고 노력할 것

- Accept
    - 선호하는 데이터 타입 등
    - 구체적인 것이 더 높은 우선순위를 갖는다
    - Accept: text/*, text/plain, text/plain;format=flowed, */*
    에서 가장 높은 우선순위를 갖는 것은 text/plain’format=flowed
    - Media type과 quality를 매치시켜놓은 표가 있다. 여기에 해당하지 않는 것의 경우 이와 가장 가까우면서 구체적인 것에 끼워맞춘다. text/*은 text/plain에 끼워맞춰 q=0.3이 되는 것. 이렇게 까지 구체적으로 가는 경우는 드물다고 하신다.
- Accept-Charset
    - 선호하는 문자 인코딩
- Accept-Encoding
    - 선호하는 압축 인코딩
- Accept-Language
    - Quality Values(q) 값을 사용해 우선순위를 지정할 수도 있다. q값이 클 수록 높은 우선순위를 갖는다.
    - Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
    - ko-KR과 같이 생략된 경우 q=1이다.
- 당연히 협상 헤더는 request시에만 사용한다.

## 4) 전송 방식

- 단순 전송
    - 말 그대로 그대로 데이터를 전송하는 것
- 압축 전송
    - gzip같은걸로 압축해서 전송. Content-Length가 줄어든다 당연히. 이 때 Content-Encoding을 명시해줘야할 것
- 분할 전송
    - Transfer-Encoding: chuncked 헤더를 추가
    - Content-Length를 넣으면 안된다.
    - 분할해서 보낼 때 chunk마다 byte 정보가 다 있다.
    - 용량이 큰 무언가를 보낼 때 좋다. 클라이언트가 먼저 보게될거 위주로 보내면 되겠네
- 범위 전송
    - 전송하다가 끊기거나 했을 때, 처음부터 다시 받으면 아깝잖아? 그래서 범위를 지정해서 줄 수 있다.
    - Client에서 Range: bytes=1001~2000 과 같이 헤더를 포함해 request하면
    - Server에서 이에 맞는 데이터를 준다. Content-Range: bytes 1001-2000 / 2000(끝 길이) 과 같은 헤더 추가

## 5) 일반 정보

단순한 정보 관련 헤더들이다

- From
    - 유저 에이전트의 이메일 정보
    - 일반적으로는 사용 안하지만, 검색 엔진에서 사용.
    - Request에서 사용
- ***Referer***
    - ***이전 웹 페이지의 주소***
    - A → B로 이동하는 경우 Referer: A를 포함해서 요청한다.
    - Referer를 사용해서 유입 경로 분석도 가능하다.
    - Referrer이 맞는 단어인데 그냥 쓴다.
    - Request에서 사용
- User-Agent
    - 웹 브라우져, 클라이언트 어플리케이션 정보
    - 통계 정보로 활용 가능하다.
    - 장애가 막 생긴다던가 할 때 어떤 브라우저에서 발생하고 있는 것인지 등등 파악 가능
    - Request에서 사용
- Server
    - 요청을 처리하는 ORIGIN 서버의 소프트웨어 정보
    - HTTP 요청을 보내면 중간에 많은 proxy 서버를 거치게 된다. 실제 HTTP 응답을 해주는 그 마지막 서버를 ORIGIN 서버라고 한다.
    - Response에서 사용
- Data
    - 메시지가 발생한 날짜와 시간
    - Response에서 사용

# 7. HTTP 헤더 - 특별한 정보

## 1) Host

요청한 호스트 정보(도메인)

- 필수!!! 중요!!
- 하나의 서버가 여러 도메인을 처리해야 할 때, 하나의 IP 주소에 여러 도메인이 적용되어 있을 때
    - 가상호스트를 통해 여러 도메인을 한번에 처리할 수 있는 서버에서 여러 애플리케이션이 구동되고 있을 수 있다.
- Request에서 사용

## 2) Location

페이지 리다이렉션

- 앞에서 길게 했다. 3xx 응답이 오면 Location 위치로 자동 이동
- 201에서도 새로 생성된 리소스의 URI를 여기에 넣어서 반환 가능

## 3) Allow

허용 가능한 HTTP 메서드

- 405 (Method Not Allowed)에서 응답에 포함해야함.
- 이런 method 지원 안한다~라고 알려주는건데 서버에서 보통 구현은 딱히 안함

## 4) Retry-After

유저 에이전트가 다음 요청을 하기까지 기다려야 하는 시간

- 503 (Service Unavailable): 서버가 언제까지 불능인지 알려줄 수 있다.
- 날짜 표기도 가능하고, 초단위 표기도 가능하다.

# 8. 인증

## 1) Authorization

클라이언트 인증 정보를 서버에 전달

- Authorization
    - Authorization: Basic xxxx…value….
    - 인증 방법에 따라 value는 다르다. 메커니즘에 상관 없이 헤더는 넣어줘야한다.

## 2) WWW-Authenticate

리소스 접근시 필요한 인증 방법 정의

- 401 Unauthorized 응답과 함께 사용
- WWW-Authenticate: Newauth ralm=”apps”, ….
- 위와 같은 정보를 헤더에 포함시켜 넣어준다. 이러한 정보를 가지고 인증 정보를 만들어서 반환하라는 것을 알려주기 위함이다.