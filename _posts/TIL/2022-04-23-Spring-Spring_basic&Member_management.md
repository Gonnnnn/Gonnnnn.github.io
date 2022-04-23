---
title: "Spring (1) Spring 기초 및 회원 관리 예제"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 1. 스프링 웹 개발 기초

## 1) 정적 컨텐츠

서버에서 뭐 하는거 없이 서버에서 웹 브라우져로 파일을 그대로 보내주는 것

### 정적 파일 반환

`src/main/resources/static` 내부에 있는 파일을 자동으로 읽어준다.

개발 단계시에는 `[localhost:8080/{file_name}.확장자](http://localhost:8080/{file_name}.확장자)` uri로 접근 가능하다

### 순서

1. 웹 브라우저에서 해당 uri로 요청을 보낸다
2. 내장 톰켓 서버에서 요청을 받고, 이를 spring에 넘긴다
3. controller 쪽에서 mapping된 controller가 있는지 확인한다.
    1. controller가 우선순위를 갖는 것이다.
4. 없으면 static내부에서 해당 파일을 찾고, 반환한다!

## 2) MVC와 템플릿 엔진

MVC(model, view, controller) 모델. 역할에 따라 파일을 구분지어 쪼개기!

html을 적절히 변형, 동적으로 제공해주는 방식

### 받은 요청을 토대로, template을 바꿔 띄워주기

Method에 uri mapping하기

`@GetMapping`

Get 방식으로 해당 uri에 요청이 오면 연결된 method를 실행해준다.

이 후 return 값을 view resolver에게 던져준다. 자세한 프로세스는 생략한다.

Request에서 Query String 받기

`@RequestParam` 을 활용한다.

`ctrl+P`는 함수에 들어가는 파라미터를 조회할 수 있게 해준다. 유용하게 사용하자!

model 활용

model 객체에 Attribute를 key-value 쌍으로 추가해줌으로써 템플릿 엔진이 해당 data를 활용할 수 있게 되고, 이를 이용해 html을 변경해준 후 rendering한다. 자세한 프로세스는 추후에 확인한다.

```java
@GetMapping("hello-mvc")
    public String helloMvc(@RequestParam("name") String name, Model model){
        model.addAttribute("name", name);
        return "hello-template";
    }
```

## 3) API

Json이라는 data format을 client에게 전달. React같은 녀석들과 협업할 때 쓴다. server끼리 통신할 때도 그렇다!

### 응답하기

http body 부분에 데이터를 직접 넣어줘보자

`@ResponseBody` 를 method 위에 붙여줌으로써, body부에 return하는 값을 직접 넣어줄 수 있다.

이 때, ***객체를 반환하게 되면, JSON으로 알아서 변환해서 반환***해준다..!@#wow

Spring은 `@ResponseBody`를 확인하고, return 값을 view resolver에게 주지 않고 HttpMessageConverter로 넘긴다. return 값이 string인 경우 stringconverter, 객체인 경우 JsonConverter가 default로 동작해서 값을 적절한 형식으로 바꿔주고, 브라우져에게 보내준다. 

```java
@GetMapping("hello-api")
    @ResponseBody
    public Hello helloApi(@RequestParam("name") String name) {
        Hello hello = new Hello();
        hello.setName(name);
        return hello;
    }

    static class Hello {
        private String name;
        public String getName() {
            return name;
        }
        public void setName(String name){
            this.name = name;
        }
    }
```

### 짜잘한 Intellij 팁

window 기준 `alt + insert`를 누르면, class에서 주로 쓰이는 함수의 기본 틀을 제공해준다.

# 2. 회원 관리 예제

## 1) 비지니스 요구사항 정리

아주 간단하게, 회원id, 이름을 저장하고, 회원을 등록, 조회할 수 있는 정도만!

### 구조

- controller : MVC의 controller
- service : 핵심 비지니스 로직. 회원은 중복 가입이 안된다던지
- repository : DB에 접근, domain 객체를 DB에 저장하고 관리
- domain : 회원, 주문, 쿠폰과 같이 DB에 저장, 관리되는 비지니스 도메인 객체

## 2) 회원 도메인과 리포지토리 만들기

- repository : 실질적인 데이터 저장공간 및 저장 interface 구축. 어떤 DB를 사용할지 정해지지 않았을 때, 이렇게 interface를 구축해놓으면 얘만 바꾸면 된다.

## 3) 회원 리포지토리 테스트 케이스 작성

코드를 코드로 검증하기! main 메서드를 돌리거나, 컨트롤러를 통해서 해당 기능을 실행하는 것은 너무 오래걸리고 번거러워, junit이라는 프레임워크를 통해 테스트한다.

Test case는 method implement 순서와 상관 없이 따로 동작하게 만들어야한다. 앞서 test한 method에 의해 조작된 data가 있을 것이다. 차 후 다른 method에 대한 test가 이 data에 영향을 받으면 안되기 때문에, data clear를 해줘야한다. 이는 `@AfterEach`를 통해 해결 가능하다. 각 method에 대한 test가 끝날 때마다 불리는 callback 함수를 지정한다고 보면 된다.

```java
// src 파일
public class MemoryMemberRepository implements MemberRepository{
    private static Map<Long, Member> store = new HashMap<>();

		...
		
		public void clearStore() {
		        store.clear();
		    }
}

// 위 src 파일의 test 파일
class MemoryMemberRepositoryTest {
    MemoryMemberRepository repository = new MemoryMemberRepository();

    @AfterEach
    public void afterEach() {
        repository.clearStore();
    }

		...

}
```

### TDD

먼저 프로그램을 만들고,  test case들을 만들 수 있으나, 먼저 내가 작동했으면 하는 방식을 생각하고, test case라는 틀을 먼저 만든 후 그에 맞게 프로그램을 개발하기도 한다. 이런 것을 테스트 주도 개발, TDD라고 한다.

## 4) 회원 서비스 개발

service는 DB에 접근해서 데이터를 조작하는 것이 아닌, 비지니스단에서 이루어지는 로직들을 말한다. 회원가입, 회원 찾기 등등

예시 코드

```java
private final MemberRepository memberRepository = new MemoryMemberRepository();
/**
 * 회원 가입
 */
public Long join(Member member) {
    //같은 이름의 중복 회원 x
    validateDuplicateMember(member); // 중복 회원 검증
    memberRepository.save(member);
    return member.getId();
}

// 원래 method로 뽑지 않았었는데, 이렇게 logic이 길어지면 하라고 하네
private void validateDuplicateMember(Member member) {
    memberRepository.findByName(member.getName())
            .ifPresent(m -> {
                throw new IllegalStateException("이미 존재하는 회원입니다.");
            });
}
```

## 5) 회원 서비스 테스트

test case는 give-when-then으로 쪼개서 구현하는게 좋다. 무엇을 가지고 언제 어떤 상황에 이런걸 하면 무엇이 일어나야한다! 방식

사실 올바르게 실행되는 것, 그 때의 로직을 테스트하는 것도 중요하지만, 예외가 발생해야하는 상황에 정확히 발생하는지 확인하는 것도 매우 중요하다.

코드

```java
// test 파일
try {
            memberService.join(member2);
            fail();
        } catch (IllegalStateException e) {
            assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
        }
```

와 같이 try catch를 쓸 수 있지만, `assertThrows`라는 좋은 method가 존재한다.

```java
memberService.join(member1);
IllegalStateException e = assertThrows(IllegalStateException.class, () -> memberService.join(member2));
assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
```

`assertThrows(터져야할 예외, 예외가 터지기 위해서 실행되어야할 로직)`

위와 같이 예외 발생시 예외 객체를 반환해준다. 이를 가지고서 메세지를 뽑아 검증 가능

### Dependency Injection

test case는 서로 독립적이어야 한다. 해당 연습 코드에서 기존의 service 객체는 내부적으로 repository 객체를 생성하여 사용하는 방식이었다. 하지만 이럴 경우 test case 작성시 repository를 초기화할 수 없게 된다. (static으로 선언되었어서 이 경우는 괜찮았다고 한다. 어쨋든,,) 이런 경우를 위해 [Dependency Injection](https://tecoble.techcourse.co.kr/post/2021-04-27-dependency-injection/)을 사용한다. 사용할 repository를 외부에서 선언하고, service 객체를 선언할 때 넣어주는 형식으로 사용하는 것이다.