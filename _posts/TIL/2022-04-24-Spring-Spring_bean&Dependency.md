---
title: "Spring (1) Spring 기초 및 회원 관리 예제"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 1. 스프링 빈과 의존관계

## 1) 컴포넌트 스캔과 자동 의존관계 설정

회원 컨트롤러는 회원 서비스, 레포지토리를 사용해서 회원을 가입시키는 등의 처리를 진행한다. 즉, 의존관계에 있다. 그런데 사실 이건 너무 당연하다. 아니면 뭘쓰겠나

### 스프링 빈이란?

`@Controller` 이라는 annotation을 class 위에 붙여놓는다. Spring이 실행될 때 container라는 것이 저 annotation이 붙어있는 class를 controller로 인식하고 객체를 생성해서 저장해둔다. 그리고 이를 spring이 관리한다. 이를 spring container에서 spring bean이 관리된다고 표현한다.

![spring_boot](https://gonnnnn.github.io/image/TIL/spring_boot.png)

하나의 service를 사용할 때 굳이 controller마다 객체를 생성해서 쓸 필요가 없을 수도 있다. Spring은 이런 경우 하나를 만들어 서로 같이 쓰게 해주도록 한다. How? Spring container에 등록해서!!

```java
// MemberController.java
@Controller
public class MemberController {
    //    이렇게 하지 말자!
    //    private final MemberService memberSErvice = new MemberService();

    private final MemberService memberService;

    @Autowired
    public MemberController(MemberService memberService) {
        this.memberService = memberService;
    }
}

// MemberService.java
@Service
public class MemberService {
...

// MemoryMemberRepository
@Repository
public class MemoryMemberRepository {
...
```

`@Autowired`는 controller가 생성될 때 spring bean에 등록되어 있는 memberService라는 객체를 container에서 가져와 연결시켜야함을 알리는 것. 

***`Dependency Injection이다.`***

`@Service`, `@Repository`라는 annotiation 또한 service, repository 파일의 class에 걸어둬야 spring이 인식한다.

** `@Autowired`는 Bean으로 등록된 객체 내에서만 작동한다. 등록해주지 않으면 작동하지 않는다.(config에서 등록해주면 괜찮다! 이건 후에 나온다) 또한 Bean으로 등록할 객체들을 코드내에서 new를 통해 생성해 `@Autowired`를 붙여줘도 적용되지 않는다. Spring container에 bean으로 등록된 것들 안에서만 동작한다!

### 스프링 빈을 등록하는 두가지 방법

컴포넌트 스캔, 자동 의존관계 설정

- 위에서 사용한 방법이다. `@Component` 를 사용하면 된다. 위에서 사용한 annotation은 들어가보면 이 annotation이 다 붙어있다.
- 컴포넌트 스캔은 기본적으로 Application(main 함수가 있는 파일)파일이 속한 경로의 하위 경로를 스캔한다. 그 외의 부분에 annotation을 달아놔도 인지하지 못한다. (예외적으로 하게 하는 방법이 있긴하다)
- 대부분의 경우 빈을 등록할 때 싱글톤으로 등록한다. 유일하게 하나만 등록하고 공유하는 것이다. 같은 스프링 빈이면 모두 같은 인스턴스이다. 싱글톤이 아니게 설정할 수는 있다.

자바 코드로 직접 스프링 빈을 등록

- 아래에 다시 나온다!

### 정리

- Component Annotation : Bean에 등록
- Autowired Annotation : 연결

## 2) 자바 코드로 직접 스프링 빈 등록

위에서 썼던 annotation을 쓰지 않는다.

```java
// src/main/java/project_name/Springconfig.java
@Configuration
public class SpringConfig {

    @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository());
    }

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }

}
```

`@Configuration`, `@Bean annotation`을 이용해 쉽게 등록가능하다. 의존관계에 따라 parameter들도 넣어주면서 완성!

Controller의 경우 어차피 Spring이 관리하기 때문에 component scan 방법을 사용해서 하라고 한다.

### 참고

- Dependency Injection(DI)에는 필드 주입, setter 주입, ***생성자 주입***이 있다.
    - 위에서 MemberService가 memberRepository를 받는 것이 생성자 주입
    - 필드에 annotation을 달아주는 등의 방법으로 설정하면 그게 필드 주입. 별로 추천되지 않는다.
    - setter 달아주는게 setter 주입. public으로 노출되어야만 한다. 따라서 위험하다. 사실 한번 application 처음에 돌아가면서 setting되고 그 다음 바꿀일이 없어서 요즘은 생성자 주입을 권장한다.
- 정형화된 컨트롤러, 서비스, 리포지토리는 컴포넌트 스캔을, 정형화 되지 않거나, ***상황에 따라 구현 클래스를 변경***해야하면 ***코드(config.java)를 통해 스프링 빈을 등록***
    - 데이터 저장소가 아직 정해지지 않아서, Interface로 MemberRepository를 설계하고, 구현체로 MemoryMemberRepository를 쓰는 그림이 그려져있었다. 이 때 기존 member 코드 등 기존 코드를 거의 손보지 않고 이 저장소를 바꿔치기 할 수 있는데, 이를 가능하게 한다! 나중에 config파일의 memberRepository의 return 객체만 바꿔주며 된다고 한다.