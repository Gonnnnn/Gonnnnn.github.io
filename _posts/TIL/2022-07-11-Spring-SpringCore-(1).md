---
title: "Spring (12) SpringCore 객체 지향 설계와 스프링"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 1. 객체 지향 설계와 스프링

## 1) EJB

암울!

어렵고 복잡하고 느림!

구체적인건 알필요 없고 진짜 너무 별로여서 Spring, Hibernate를 만들었다.

얼마나 별로였으면 새로운 봄이왔다는 뜻으로 Spring이라는 이름을 지어줬다.

후에 이 Hibernate는 java 표준으로 채택되면서 JPA라는 interface를 이를 기반으로 만들었다. Hibernate, EclipseLink등의 JPA 구현체들이 현재 존재한다.

## 2) 스프링이란?

스프링 프레임워크, 스프링 부트, 스프링 데이터, 스프링 세션 등 다양한 라이브러리를 지원한다.

### 스프링 프레임워크

사실상 제일 중요한 것. 핵심 기술(스프링 DI 컨테이너, AOP, 이벤트 등), 웹, 데이터 접근 기술 등이 있지만 여기서 또 가장 중요한 것은 핵심 기술 부분

### 스프링 부트

다들 써봤듯이 스프링 프레임워크를 편리하게 사용할 수 있도록 해준다.

- Tomcat 같은 웹 서버를 내장해서 별도의 웹 서버 설치가 필요 없다.
    - 예전에는 빌드를 하고 tomcat 서버를 받아 별도를 설치하고, tomcat 서버에 또 빌드된 걸 넣고 어쩌고 복잡했다고 한다.
- 손쉬운 빌드 구성을 위한 starter 종속성. 특정 작업을 하는데 필요한 라이브러리들의 종속성을 고려해서 알아서 다 따라오게 해준다.
- 외부 라이브러리 들의 호환되는 버젼들을 알아서 지정해서 다운받게 해준다.

### 핵심 개념

기술을 이해할 때는 핵심 개념, 왜 만들어졌는지를 이해하자.

스프링의 핵심

- 스프링은 객체 지향 언어가 가진 강력한 특징을 살려내는 프레임 워크
- 좋은 객체 지향 애플리케이션을 개발할 수 있도록 도와주는 프레임워크

→ 객체 지향 애플리케이션을 만들지 않으면, 의미가 없나?

### 3) 좋은 객체 지향 프로그래밍

***“객체”들의 모임***, 객체는 메세지를 주고받으며 ***협력***한다.

 ***유연***하고 ***변경이 용이***하다. → 컴퓨터 부품을 갈아 끼우는거 같이

ex) 자동차라는  interface를 따라 K3, 아반떼를 만들기에,  운전자는 자동차라는 interface에 대해 숙지하면 어느 차든 바로 운전이 가능하다. 차량 번호는 각각의 고유한 차량을 나타내는 번호이다. K3, 아반떼가 class라면 이들은 객체이다.

자동차 (interface)

- K3 (class)
    - 가1234 (객체)
    - 나1256
- 아반떼
    - 서6439
    - 배2929

어쨋든 중요한 것은 ***역할을 만들고 구현을 분리한 것***은 “사용자”를 위한 것이라는 점이다. 다르게 말하면 ***client에게 영향을 주지 않고 새로운 기능을 구현할 수 있다***는 것이다. 새로운 자동차가 나와도, client는 새로운 것을 배울 필요가 없다.

### 역할과 구현의 분리

- 유연, 변경 편리
- 클라이언트는 대상의 역할(interface)만 알면 된다.
- 클라이언트는 구현 대상의 **내부 구조를 몰라도** 된다.
- 클라이언트는 구현 대상의 **내부 구조가 변경되어도 영향을 받지 않는다**.
- 클라이언트는 구현 **대상 자체를 변경해도 영향을 받지 않는다**.

자바 언어에서 역할 = interface, 구현 = 구현한 클래스, 객체로 이해할 수 있다.

***결론적으로, Interface를 안정적으로 잘 설계하는 것이 너무 중요하다. 다형성을 살려야하고, 스프링은 이 다형성을 극대화할 수 있게 해준다!***

→ IoC, DI 등을 활용할 것이다! 결국 이들은 다형성을 편리하게 활용하도록 지원하는 기능인 것이다.

# 2. 예제 만들기

## 1) 비지니스 요구사항 설계

회원

- 가입, 조회 가능
- 일반과 VIP 등급
- 자체 DB를 구축하거나 외부 시스템과의 연동 (미확정)

주문과 할인 정책

- 회원은 상품 주문 가능
- 모든 vip는 1000원을 고정 할인. 나중에 변경될 수 있다.
- 할인 정책은 변경 가능성이 높다. 할인 정책을 아직 못정했다. 오픈 직전까지 고민을 미루고 싶으며, 할인을 적용하지 않을 수도 있다.
    - 진짜 이거 한줄 읽었는데 복장이 터지려고 한다. 옛날에는 어떻게 했을까? 역시 개발자는 현실적인 문제에 대응을 잘해야 하는 사람들이다.

## 2) 회원 도메인 설계

![Untitled](https://gonnnnn.github.io/image/TIL/0711(1).png)
회원 도메인 협력 관계. 기획자들도 볼 수 있는 단계

![Untitled](https://gonnnnn.github.io/image/TIL/0711(2).png)  

회원 클래스 다이어그램. 개발자가 구체화하여 만들어낸 다이어그램. 관계를 나타내지만 실제 서버가 뜰 때 어떠한 객체가 들어가는지는 여기서는 모르고, 아래에 정의해놓음.

![Untitled](https://gonnnnn.github.io/image/TIL/0711(3).png)

회원 객체 다이어그램. 객체간의 메모리 참조 관계. ex) 클라이언트가 실제로 참조하는 주소 값에 있는 것은 MemberServiceImpl 객체

코드는 저번에 memoryMemberRepository를 사용했던 것처럼  implement했다. 다음과 같은 문제점을 생각해보자

- 다른 저장소로 변경할 때 OCP 원칙을 잘 준수하는가?
- DIP를 잘 지키고 있는가?

이 경우 DI를 위반한다. MemberService 단에서 인터페이스뿐만 아니라 구현까지 의존해버린다.

## 3) 주문 도메인 설계

![Untitled](https://gonnnnn.github.io/image/TIL/0711(4).png)

주문 도메인 협력, 역할, 책임

클라이언트는 controller 정도가 될 것이다. 주문 상세사항은 객체 형태가 되어야할 것이지만 단순한 예를 들기 위해 상품명으로 대체한다.

1. 주문 생성: 클라이언트는 주문 서비스에 주문 생성을 요청한다.
2. 회원 조회: 할인을 위해서는 회원 등급이 필요하다. 그래서 주문 서비스는 회원 저장소에서 회원을
조회한다.
3. 할인 적용: 주문 서비스는 회원 등급에 따른 할인 여부를 할인 정책에 위임한다.
4. 주문 결과 반환: 주문 서비스는 할인 결과를 포함한 주문 결과를 반환한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0711(5).png)

전체 역할 다이어그램

![Untitled](https://gonnnnn.github.io/image/TIL/0711(6).png)

클래스 다이어그램

![Untitled](https://gonnnnn.github.io/image/TIL/0711(7).png)

객체 다이어그램

이런식으로 설계하면 역할들의 협력 관계를 그대로 재사용할 수 있다. 객체를 바꿔끼워도 서비스 코드를 수정할 필요가 없고, 역할 관계는 유지된다는 것

# 3. 객체 지향 원리 적용

## 1) 새로운 할인 정책 적용과 문제점

RateDiscountPolicy를 만들고 OrderServiceImpl에서 적용하려한다. 

문제가 발생

```java
//OrderServiceImpl
public class OrderServiceImpl implements OrderService {

    private final MemberRepository memberRepository = new MemoryMemberRepository();
    // private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
    private final DiscountPolicy discountPolicy = new RateDiscountPolicy();
...
}
```

- 우리는 역할과 구현을 충실하게 분리했다.
- 다형성도 활용하고, 인터페이스와 구현 객체를 분리했다.

하지만, 의존관계를 잘 보면 다음과 같이 설계되어있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0711(8).png)                                                            

- Policy를 변경하는 순간 OrderServiceImpl의 소스코드도 함께 번경된다.
→ OCP 위반. 자신의 확장에는 열려있지만 주변의 변화에는 닫혀있어야한다.
- OrderServiceImpl은 아래와 같이 인터페이스(추상)뿐만 아니라 클래스(구체)에도 의존하고 있다.
→ DIP 위반. 추상에만 의존해야한다.

위 문제를 해결하기 위해서는, 코드가 인터페이스만 의존하도록 해야한다. 이는 OrderServiceImpl에 DiscountPolicy 구현 객체를 대신 생성해주고 주입해주는 다른 무언가가를 통해서 실현 가능하다.

## 2) 관심사의 분리

해당 강의에서는 어플리케이션을 하나의 공연으로 비유했다.

로미오와 줄리엣 공연에서 로미오와 줄리엣은 어느 배우나 할 수 있다.(추상과 구현)

하지만 로미오 역할의 배우가 줄리엣 역할을 할 배우를 선정하지는 않는다. 이러한 전반적인 계획과 지시는 감독이 한다.

### 관심사를 분리한다.

- 배우는 본인의 역할인 배역을 수행하는 것에만 집중한다.
- 배우는 다른 어떤 배우가 와도 똑같이 공연할 수 있어야한다.
- 공연을 구성하고, 배우를 섭외하는 책임을 담당하는 공연 기획자가 있어야한다.

***→ 역할과 관심사를 확실히 분리해야한다.***

### AppConfig

어플리케이션의 전체 동작 방식을 구성하기 위해 *구현 객체를 생성하고 연결*하는 책임을 가지는 클래스

```java
//AppConfig.java
public class AppConfig {

    private MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }

    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

    private DiscountPolicy discountPolicy() {
        return new RateDiscountPolicy();
    }
}

//OrderSerivceImpl.java
public class OrderServiceImpl implements OrderService {

    private final MemberRepository memberRepository;
    private final DiscountPolicy discountPolicy;

		public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
        this.memberRepository = memberRepository;
        this.discountPolicy = discountPolicy;
    }
...
}
```

- 각각의 구현체를 AppConfig.java에서 생성하며, 각각의 구현체를 생성할 때 의존하는 구현체를 지정해준다.
- OrderServiceImpl 및 기타 다른 구현체들은 “실행”에만 집중할 뿐이다. 인터페이스만 의존하고 있는 것을 확인가능하다. 생성자를 통해 필요한 구현을 “주입”했기 때문이다.
- OrderServiceImpl에서는 마치 의존관계를 외부에서 주입해주는 것 같다고해서 의존관계/의존성 주입(Dependency Injection)이라고 한다.

최종적으로 확인할 수 있는 어플리케이션 전체 구성은 다음과 같다.

![Untitled](https://gonnnnn.github.io/image/TIL/0711(9).png)                              
영역을 다음과 같이 구분할 수 있게 된다

![Untitled](https://gonnnnn.github.io/image/TIL/0711(10).png)
- 사용할 정책, 저장소 등이 변경되더라도 사용 영역의 코드는 건드릴 필요가 없다.

## 3) 좋은 객체 지향 설계의 5가지 원칙

이 중 3가지를 지켜 설계했다.

### SRP 단일 책임 원칙

- 한 클래스는 하나의 책임만 가져야 한다.
- SRP 단일 책임 원칙을 따르면서 관심사를 분리해야한다.
    - 구현 객체를 생성하고 연결하는 책임은 AppConfig가 담당

### DIP 의존관계 역전 원칙

- 프로그래머는 “추상화에 의존해야지, 구체화에 의존하면 안된다.” 의존성 주입은 이 원칙을 따르는 방법 중 하나다.
- 클라언트코드는 인터페이스에만 의존해야하지만 인터페이스만으로는 아무것도 실행할 수 없다. 따라서 AppConfig가 FixDiscountPolicy 객체 인스턴스를 클라이언트 코드 대신 생성했고 클라이언트 코드에 의존관계를 주입했다.

### OCP

- 소프트웨어 요소는 확장에는 열려 있으나 외부 변경에는 닫혀 있어야 한다.
- Appconfig를 생성해줌으로써 클라이언트 코드는 변경할 필요가 없게 된다.

## 4) IoC, DI, 컨테이너

### IoC (Inversion of Control)

- 인터페이스 뿐만 아니라, 객체에도 의존하게 개발하던 때를 생각해보자. 구현 객체가 스스로 필요한 다른 객체를 구현하고, 연결하고, 실행했다. 구현 객체가 프로그램의 제어 흐름을 스스로 조종한 것이다.
- AppConfig가 등장한 후로는 모든 객체들은 자신의 역할만 묵묵히 할 뿐이다. 프로그램 제어 흐름에 대한 권한은 AppConfig가 가져간다. 이렇듯 ***프로그램의 제어 흐름을 직접 제어하는 것이 아니라 외부에서 관리하는 것을 제어의 역전(IoC)라고 한다.***

프레임워크 vs 라이브러리

- 프레임워크 : 프레임워크가 내가 작성한 코드를 제어하고, 대신 실행하는 경우. 내가 작성한 코드가 마치 콜백 형식으로 불려와져서 돌아가는 경우 등이다.
- 라이브러리 : 내가 작성한 코드가 직접 제어의 흐름을 담당하는 경우

### DI (Dependency Injection)

의존관계는 “정적인 클래스 의존 관계와, 실행 시점에 결정되는 동적인 객체 의존 관계”를 분리해서 생각해야한다.

- 정적인 클래스 의존관계
    - 클래스가 import하는 것들만 보고 쉽게 판단할 수 있는 의존관계. 애플리케이션을 실행하지 않아도 분석 가능
- 동적인 객체 인스턴스 의존관계
    - 애플리케이션 실행 시점에서 실제 생성된 인스턴스의 참조가 연결된 의존 관계이다.
- ***Dependency Injection은 애플리케이션 “실행 시점(런타임)”에 외부에서 실제 구현 객체를 생성하고, 클라이언트에 전달해서 클라이언트와 서버의 실제 의존관계가 연결되는 것을 일컫는다.***
    - 객체 인스턴스를 생성하고, 그 참조값을 전달해서 연결된다.
    - 정적인 클래스 의존관계를 전혀 바꿀 필요 없이, 즉 애플리케이션 코드를 손대지 않고, 객체 의존관계를 쉽게 바꿀 수 있다.

### IoC 컨테이너, DI 컨테이너

- 그냥 AppConfig처럼 객체를 생성하고 관리하며 의존관계를 연결해주는 것을 의미한다. 얘는 IoC는 너무 범용적이라 DI 컨테이너라고 지칭한다.

## 5) Spring 사용

### Spring!

- `@Configuration`
    - 해당 클래스를 AppConfig의 역할을 하는 클래스로 등록
- `@Bean`
    - 해당 class를 bean으로 등록
- `ApplicationContext`
    - 스프링 컨테이너. 알아서 @Configuration이 붙은 class를 AppConfig처럼 사용한다. @Bean이 붙은 메소드를 모두 호출해서 반환된 객체를 스프링 컨테이너에 등록한다.
    - `AnnotationConfigApplicationContext()` bean을 관리하는 spring container객체. 생성시 AppConfig역할의 class를 안에 넣어줘야한다.
    
    ```java
    ApplicationContext h = new AnnotationConfigApplicationContext(AppConfig.class);
    MemberService memberService = h.getBean("memberService", MemberService.class);
    ```
    

자세한건 다음 시간에!

그냥 AppConfig를 그냥 만들어서 쓰는거랑 별 차이가 없는거같으면서, 부수적인 class들만 더 import하는거같은데 무슨 이점이 있을까?