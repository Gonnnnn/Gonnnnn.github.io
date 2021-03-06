---
title: "Spring (6) HTTP 메서드 활용, 상태 코드"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---
# 5. HTTP 메서드 활용

## 1) 클라이언트에서 서버로 데이터 전송

### 전송 방식

쿼리

- GET
- 주로 정렬 필터(검색어)를 쓸 때 사용

메시지 바디

- POST, PUT, PATCH
- 회원 가입, 상품 주문, 리소스 등록, 변경 등

### 정적 데이터 조회

- 이미지, 정적 텍스트 문서를 조회하는 경우
- ***GET***
- 쿼리 파라미터 주로 불필요

### 동적 데이터 조회

- 주로 검색, 게시판 목록에서의 정렬 필터
- ***GET***
- 쿼리 파라미터 사용. 서버에서는 이걸가지고 데이터를 필터링해서 반환해주곤 한다

### HTML Form 데이터 전송

1. Form 태그를 사용하면 안에 입력된 정보에 맞게 ***HTTP 메시지가 자동 생성***된다. Form 태그는 get, post 방식만 지원

```html
<!-- POST -->
<form action="/save" method="post">
	<input type="text" name="username"/>
	<input type="text" name="age"/>
	<button type="submit">전송</button>
</form>

<!-- GET -->
<form action="/members" method="get">
	<input type="text" name="username"/>
	<input type="text" name="age"/>
	<button type="submit">전송</button>
</form>
```

```
# 생성되는 HTTP 메시지
# POST
POST /save HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded

username=kim&age=20
--> 마치 쿼리와 비슷한 형식으로 메시지 바디에 들어간다.

#GET
GET /members?username=kim&age=20 HTTP/1.1
Host: localhost:8080
```

1. 파일을 전송할 때는 encoding type을 “***multipart/form-data***”로 해야한다. 이에 맞게 HTTP 메시지도 다르게 생성된다. 예시는 아래와 같다.

```html
<!-- POST -->
<form action="/save" method="post" enctype="mulitpart/form-data">
	<input type="text" name="username"/>
	<input type="text" name="age"/>
	<input type="file" name="file1"/>
	<button type="submit">전송</button>
</form>
```

```
POST /save HTTP/1.1
Host: localhost:8080
Content-Type: multipart/form-data; boundary=---XXX
Content-Length: 10457

------XXX
Content-Disposition: form-data; name="username"

kim
------XXX
...
...생략
------XXX
Content-Disposition: form-data; name="file1" filename="intro.png"
Content-Type: image/png

10231asdf1s5d...(바이트 정보)
------XXX--
```

- 다른 종류의 여러 파일과 폼의 내용을 함께 전송해서 multi part이다.
- 위 방법은 주로 파일 업로드같은 ***바이너리 데이터 전송시 사용***한다.
- ——XXX로 데이터를 알아서 나눈다.

### HTTP API 데이터 전송

보통 클라이언트에 라이브러리들이 잘 돼있다. 그냥 데이터 넣고 넘기면 된다.

```
POST /members HTTP/1.1
Content-Type: application/json

{
	"username": "young",
	"age": 20
}
```

- 서버 to 서버 통신, 앱 클라이언트에서의 데이터 전송
- 웹 클라이언트에서 form 전송 대신 js 등을 통신에 사용할 때
- GET, POST, PUT, PATCH로 전송 가능
- Content-Type: application/json을 주로 사용 (사실상 표준)

## 2) HTTP API 설계 예시

회원관리용 API를 설계한다고 가정해보자.

### HTTP API - 컬렉션

POST 기반 등록

- 그냥 서버에 데이터를 던져주면, 새로 생성되는 리소스의 URI를 서버에서 알아서 만들고, 넘겨준다
    - /members에 던져주면 알아서 /members/100과 같이 URI를 만들어 리소스를 저장하는 것
- Location 헤더에 새로운 URI를 반환해주기도 한다. 혹은 그냥 id값을 메시지 바디에 넣어 주던지
- ***컬렉션***
    - ***여기서 이 /members를 컬렉션이라고 한다.***
    - ***서버가 관리하는 리소스 디렉토리이다.***
    - ***서버가 리소스의 URI를 생성하고 관리하게 된다.***
- ***대부분 컬렉션 쓴다.***

### HTTP API - 스토어

PUT 기반 등록

- 애초에 데이터를 넘겨줄 때 특정한 URI로 넘겨준다. 클라이언트에서 직접 리소스의 URI를 지정하는 것이다.
    - /files/{filename}
- 이 때 /files → POST의 경우 뭐.. 대량으로 파일을 등록하는 기능이라던지 아무거나 자유롭게 만들어 쓸 수 있겠지
- ***스토어***
    - ***여기서 이 /files를 스토어라고 한다.***
    - ***클라이언트가 관리하는 리소스 저장소이다.***
    - ***클라이언트가 리소스의 URI를 알고 관리한다.***

### HTML FORM 사용

- 순수한 HTML FORM을 사용한다고 하면, GET, POST 밖에 못 쓴다.
- 회원 등록 폼과 회원 등록을 하는 URI를 같게 두고, 각각 GET, POST를 쓰는 것을 개인적으로 추천하신다고 한다. 사람마다 다르다. 나도 이게 더 낫긴했다.
- ***GET, POST만 가지고는 같은 URI가 너무 많은 기능을 담당할 수는 없다. 어쩔 수 없을 때는, 혹은 HTTP메서드로 해결하기 애매한 경우 컨트롤 URI를 써야한다.***
    - ***POST의 /new, /edit, /delete 등***
    - ***다만 남발하는게 아니라, 리소스 기준으로 짜지만, 어쩔 수 없을 때 사용하자.***
    - ***동사를 사용한다.***

### 참고하면 좋은 URI 설계 개념

https://restfulapi.net/resource-naming

좋은 practice 정도. 정답은 아니지만 따르는 걸 권장한다.

### 정리

- 문서
    - 단일 개념. 파일 하나, 객체 인스턴스, 데이터베이스 row
    - /members/100, /files/star.jpg
- 컬렉션
    - 서버가 관리하는 리소스 디렉토리
    - 서버가 리소스의 URI를 관리하고 생성
    - /members
- 스토어
    - 클라이언트가 관리하는 자원 저장소
    - 클라이언트가 URI 생성, 관리
    - /files
- 컨트롤러, 컨트롤 URI
    - 문서, 컬렉션, 스토어로 해결하기 어려운 추가 프로세스 실행
    - 동사를 직접 사용
    - /members/{id}/delete

# 6. HTTP 상태코드

## 1) 상태코드

클라이언트가 보낸 요청의 처리 상태를 응답에서 알려주는 기능

- 1XX (Informational): 요청이 수신되어 처리중
- 2XX (Successful): 요청 정상 처리
- 3XX (Redirection): 요청을 완료하려면 추가 행동이 필요
- 4XX (Client Error): 클라이언트 오류, 잘못된 문법 등으로 서버가 요청 수행 불가
- 5XX (Server Error): 서버 오류, 서버가 정상 요청을 처리하지 못함

새로운 상태코드가 와도, 상위 코드로 해석해서 처리하면 된다. ex) 299 → 200

꼭 상태코드를 세세하게 다 사용할 필요까지는 없다. 개발할 때 팀에서 내부적으로 좀 정의해서 써야 오히려 신경쓸게 줄어든다.

이번엔 그냥 알아나 보자

## 2) 2XX- 성공

- 200 OK
- 201 Created
    - 자원 생성 후 응답으로 Location 헤더에 새로운 자원의 URI를 넣어준다.
- 202 Accepted
    - 요청이 접수되었으나 처리가 완료되지는 않음.
    - 요청 접수 후 1시간 뒤에 배치 프로세스가 요청을 처리하는 등의 경우. 잘 쓰지는 않음
- 204 No Content
    - 요청은 성공적으로 수행했는데, 응답 페이로드 본문에 보낼 데이터가 없음
    - 웹 문서 편집기에서 save 버튼의 경우, 당연히 저장을 해도, 그 결과를 무언가를 받을 이유는 없다. 같은 화면을 유지해야할 것이다.

## 3) 3XX - 리다이렉션1

### 리다이렉션

- 웹 브라우저는 3XX 응답의 결과에 Location 헤더가 있으면, Location 위치로 자동 이동한다.
- 서버가 URI를 바꿨을 때, 기존 사용자들은 북마크를 해두는 등의 이유로 기존 URI로 올 수도 있다. 이 때 3XX 응답을 주면 Location 헤더 값으로 자동 리다이렉트를 한다. 다시 해당 URI에 요청을 하고 응답을 받게 된다.
- 영구/일시/특수 리다이렉션으로 나뉜다.
- 영구 리다이렉션 - 특정 리소스의 URI가 영구적으로 이동
- 일시 리다이렉션 - 일시적인 변경
    - 주문 완료 후 주문 내역 화면으로 이동 등등
    - POST/REDIRECT/GET
- 특수 리다이렉션
    - 클라이언트 캐시 기간이 만료된거 같아서, 관련 정보를 서버에 넘겨주는 경우
    - 결과 대신 캐시를 사용

### 영구 리다이렉션

301, 308

- 리소스 URI가 영구적으로 이동
- 검색 엔진등에서 자동으로 인식
- 301 Moved Permanently
    - 리다이렉트시 GET 요청을 보내며, 기존의 바디 내용은 사라질 수 있다.
- 308 Permanent Redirect
    - 301과 달리 POST를 유지하며, 바디 내용도 유지한다.
- 근데 요구되는 데이터가 다 바뀌는 경우도 많고, 이래저래 경우가 너무 많아서 다시 GET으로 돌리는게 낫다고 한다. 둘다 많이 쓰지는 않는다.

### 일시 리다이렉션

302, 307, 303

- 리소스 URI가 일시적으로 변경. 나중에 안바뀔수도 있는거긴하다.
- 따라서 검색 엔진 등에서 URL을 변경하면 안된다.
- ***302 Found***
    - ***리다이렉트시 GET 요청을 보내며, 본문이 제거될 수 있다. (대부분 변한다 ㅋㅋ)***
- ***307 Temporary Redirect***
    - ***302와 기능은 같다!***
    - ***리다이렉트시 요청 메서드와 본문을 꼭 유지해야한다.***
- ***303 See Other***
    - ***302와 기능은 같다!***
    - ***리다이렉트시 요청 메서드가 GET으로 명확히 변경된다.***

***근데 실무에서는 그냥 302를 보통 쓴다.***

### PRG: Post/Redirect/Get

웹 브라우저에서 새로고침을 하면 마지막 요청을 다시 보낸다.

주문과 관련된 POST 요청 후, 제대로 주문이 처리가 되어 응답으로 200 OK, 그리고 html 파일을 받았다고 하자. 여기서 ***실수로 바로 새로고침을 누르면 재주문이 되는 꼴이다.***

***원칙적으로는 서버에서 “이는 이미 사용된 주문번호입니다”와 같이 막아주는 기능을 확실히 해두어야 하지만, 클라이언트에서도 막아두는게 좋다.***

따라서

- ***POST로 주문후, 주문 결과 화면을 GET 메서드로 리다이렉트 (PRG)한다.***
- ***새로고침해도 결과 화면을 GET으로 조회하게될 뿐이다.***
- ***이 경우 응답으로 302/303을 주고, Location 헤더에 URI를 넣어줘야할 것이다.***

사용자가 뭘 건드릴만한 부분들을 끊어서 생각하는게 맞겠네

### 정리

- 302 → GET으로 변할 수 있음
    - HTTP 메서드를 유지하는게 의도였는데, 웹 브라우저들이 대부분 GET으로 바꾸어버려서 이래됨 ㅠㅠ
- 307 → 메서드가 변하면 안됨
- 303 → GET으로 변경

### 기타 리다이렉션

- 300 Multiple Choices: 안 씀
- ***304 Not Modified***
    - 캐시를 목적으로 사용한다
    - 클라이언트에게 리소스가 수정되지 않았음을 알려준다. 따라서 클라이언트는 로컬PC에 저장된 캐시를 재사용한다. (캐시로 리다이렉트 한다)
    - 클라이어트야, 캐시에 있는 데이터를 써!라는 것이다.
    - 304는 메시지 바디를 포함하면 안된다!
    - 조건부 GET, HEAD 요청시 사용한다.

## 4) 4XX - 클라이언트 오류

- 클라이어트의 요청에 문제가 있어서 서버가 요청 자체를 수행할 수 없을 때
- 오류의 원인이 클라이언트에 있는 것이다.
- ***클라이언트가 이미 잘못된 요청을 보내고 있어서, 재시도 해봤자 계속 실패한다.***

### 4XX

- 400 Bad Request
    - 요청 구문, 메시지 등등 오류. 요청 내용 검토 받고 다시 보내야한다.
    - 백엔드 개발자들이 입구에서부터 스펙 맞는지 아닌지 철저하게 validation해줘야한다.
- 401 Unauthorizd
    - 클라이언트가 해당 리소스에 대한 인증이 필요하다.
    - 응답에 WWW-Authenticate 헤더와 함께 인증 방법을 설명
    - 참고
        - ***인증(Authentication): 본인 확인. 로그인의 경우이다***
        - ***인가(Authorization): 권한 부여. ADMIN 같이 특정 리소스에 접근할 수 있는 권한 레벨에 관한 것***
        - 사실 401 Unauthorized이지만 인증에 관한 부분인 것이다.
- 403 Forbidden
    - 서버가 요청은 이해했는데, 승인을 거부한 것이다.
    - Authentication은 됐는데, Authorization은 불충분한 경우
- 404 Not Found
    - 요청 리소스를 찾을 수 없는 경우. 이런거 서버에 없다는 것이다.
    - 혹은 클라이언트가 권한이 부족한 리소스에 접근할 때, 리소스를 숨기기 위해 사용. 403이런거 하기 싫고 그냥 숨길 때

## 5) 5XX - 서버 오류

- 오류의 원인이 서버에 있다.
- ***서버에 문제가 있기에 재시도 하면 성공할 수도 있다.(복구가 되거나 등등)***

### 5XX

- 500 Internal Server Error
    - 서버 내부 문제로 오류 발생
    - ***애매하면 500***
- 503 Service Unavailable
    - 서버가 일시적인 과부화 또는 예정된 작업으로 잠시 요청을 처리할 수 없을 때
    - Retry-After 헤더 필드로 얼마뒤에 복구되는지 보낼 수도 있지..만...
        - 장애는 예상치 못하게 오니까 대부분 이런건 못봄..

5XX 에러는 진짜 서버에 문제가 터졌을 때 써야한다. API 스펙도 다 맞고, 서버까지 다 잘 들어와서 요청이 처리가 되었는데, 고객의 잔고가 부족하다고 하자. 혹은 고객이 나이 제한에 걸렸다고 하자. 이런걸로 쓰면 안된다. 모니터링 툴들도 5XX 에러가 발생하면 인지하고 그러는데, 저런건 비지니스 로직상 정상적인 예외 케이스일 뿐인거잖아. 당연한 소리이긴한데.. 많이 실수하나보다. 짚으시는거 보니