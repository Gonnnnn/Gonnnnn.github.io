---
title: "Spring (13) SpringCore Spring Container and Singleton"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 4. 스프링 컨테이너와 스프링 빈

### 빈 조회 정리

- `ac.getBean`
    - Bean 하나 조회. 타입 혹은 이름
- `ac.getBeansOfType`
    - 타입으로 두개 이상의 빈 조회. 부모 타입으로 조회시 자식이 하나이면 오류
- `ac.getBeanDefinitionNames`
    - bean들 이름 쭉 불러옴
- `ac.getBeanDefinition`
    - 위에서 얻어온걸 여기에 넣으면 해당
    - `beanDefinition.getRole`을 통해 메타데이테서 해당 bean의 role(어플리케이션단의 것인지, 아니면 기본적으로 컨테이너에 올라가는 놈인지 등) 확인

## 1) 스프링 컨테이너

Spring에게 환경정보를 던져주고, container로부터 필요한 것을 받아서 사용하는 형식이다.

- `ApplicationContext`는 인터페이스
- `AnnotationConfigApplicationContext`가 클래스이다.
    - XML 기반인 것도 있지만 요즘은 annotation 사용하는 방식 채용
    - 초기화시 구성정보를 담는 class를 주입
- 빈 이름은 메서드 이름이 기본이고 직접 부여할 수 있지만 중복되면 안된다.

스프링 컨테이너 생성시 다음과 같은 일이 일어난다.

- 컨테이너는 하나의 테이블을 갖고 있다. 여기에 구성 정보로 넘어오는 class를 기반으로 스프링 빈을 등록해 놓는다. 빈 이름과 빈 객체를 mapping!
- 의존관계를 설정한다. AppConfig를 기반으로 객체 의존관계를 확인해가며 참조 값 연결! DI
- 단순히 자바 코드를 호출하는 거랑 다를게 없어보이긴 한다. 다만 싱글톤이라는 개념을 알고 나서 다시 생각해보면 다르게 보일 것이라고 한다!

![Untitled](https://gonnnnn.github.io/image/TIL/0712(1).png)                                                                                                                                                                                                                                                                          

## 2) 빈 조회 1

### 컨테이너에 등록된 모든 빈 조회

제대로 모두 등록되었나 확인해보자

```java
AnnotationConfigApplicationContext h = new AnnotationConfigApplicationContext(AppConfig.class);

@Test
@DisplayName("모든 빈 출력하기")
void findAllBean() {
    String[] beanDefinitionNames = h.getBeanDefinitionNames();
    for (String beanDefinitionName : beanDefinitionNames) {
        Object bean = h.getBean(beanDefinitionName);
        System.out.println("beanDefinitionName = " + beanDefinitionName + " object = " + bean);
    }
}

@Test
@DisplayName("애플리케이션 빈 출력하기")
void findApplicationBean() {
    String[] beanDefinitionNames = h.getBeanDefinitionNames();
    for (String beanDefinitionName : beanDefinitionNames) {
        BeanDefinition beanDefinition = h.getBeanDefinition(beanDefinitionName);

        if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
            Object bean = h.getBean(beanDefinitionName);
            System.out.println("beanDefinitionName = " + beanDefinitionName + " object = " + bean);
        }
    }
}
```

- `getBeanDefinitionNames`: 컨테이너에 있는 bean 이름 리스트 반환
- `getBean`: 객체 반환
- `getBeanDefinition`: 해당 bean의 meta data 반환
    - `getRole`: 컨테이너 내부에서 바로 등록시켜 사용하는 bean도 있고, 우리가 만든 것처럼 우리가 직접 등록하는 것도 있다. Role이 다 다르다. 두번째 method처럼 role을 확인해 우리꺼만 찍어볼 수도 있다.

### 각각 확인

```java
AnnotationConfigApplicationContext h = new AnnotationConfigApplicationContext(AppConfig.class);

@Test
@DisplayName("빈 이름으로 조회")
void findBeanByName() {
    MemberService memberService = h.getBean("memberService", MemberService.class);
    assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
}

@Test
@DisplayName("빈 타입으로 조회")
void findBeanByType() {
//        type명만으로도 getBean으로 조회 가능
    MemberService memberService = h.getBean(MemberService.class);
    assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
}

@Test
@DisplayName("빈 구체 타입으로 조회")
void findBeanByType2() {
//        객체 자체의 타입으로도 조회 가능하긴 하다. 좋은건 아니겠지
    MemberService memberService = h.getBean("memberService", MemberServiceImpl.class);
    assertThat(memberService).isInstanceOf(MemberServiceImpl.class);
}

@Test
@DisplayName("빈 이름으로 조회X")
void findBeanByNameX() {
//        MemberService xxxx = h.getBean("xxxx", MemberService.class);
//        해당 예외가 터지면 성공!

    assertThrows(NoSuchBeanDefinitionException.class, () -> h.getBean("xxxx", MemberService.class));
}
```

- 이름, 타입, 객체 타입으로 조회가 가능하다.
- 조회 불가능하면 `NoSuchBeanDefinitionException`

## 3) 빈 조회 2

### 동일한 타입이 둘 이상

```java
@Configuration
static class TempAppConfig {
    @Bean
    public MemberRepository memberRepository1() {
        return new MemoryMemberRepository();
    }

    @Bean
    public MemberRepository memberRepository2() {
        return new MemoryMemberRepository();
    }
}

AnnotationConfigApplicationContext h = new AnnotationConfigApplicationContext(TempAppConfig.class);

@Test
@DisplayName("타입으로 조회시 같은 타입이 둘 이상 있으면, 중복 오류")
void findBeanByTypeDuplicate() {
//        NoUniqueBeanDefinitionException
    Assertions.assertThrows(NoUniqueBeanDefinitionException.class, () -> h.getBean(MemberRepository.class));
}

@Test
@DisplayName("타입으로 조회시 같은 타입이 둘 이상이면, 빈 이름을 지정하자")
void findBeanByName() {
    MemberRepository bean = h.getBean("memberRepository1", MemberRepository.class);
    org.assertj.core.api.Assertions.assertThat(bean).isInstanceOf(MemberRepository.class);
}

@Test
@DisplayName("특정 타입을 모두 조회하기")
void findAllBeanByType(){
    Map<String, MemberRepository> beansOfType = h.getBeansOfType(MemberRepository.class);
    for (String key : beansOfType.keySet()) {
        System.out.println("key = " + key + " value = " + beansOfType.get(key));
    }
    System.out.println("beansOfType = " + beansOfType);
    org.assertj.core.api.Assertions.assertThat(beansOfType.size()).isEqualTo(2);
}

@Test
@DisplayName("내 임의로 하는 특정 타입 모두 조회 테스트")
void findAllBeanByType2() {
    Map<String, DiscountPolicy> beansOfType = h.getBeansOfType(DiscountPolicy.class);
    for (String key : beansOfType.keySet()) {
        System.out.println("key = " + key + " value = " + beansOfType.get(key));
    }
}
```

- 타입으로 조회시 같은 타입이 둘 이상이면 `NoUniqueBeanDefinitionException`
- 빈 이름을 지정하면 당연히 잘 조회가 되고
- 특정 타입을 모두 조회할 수 있다. 하나의 interface를 상속하는 두개의 policy class들도 bean으로 둘다 등록해놓으면 잘 나온다. `getBeansOfType`

### 상속 관계

***빈 조회시 부모 타입으로 조회하면 자식 타입도 조회된다.***

***→ 자바 객체의 최고 부모인 `object` 타입으로 조회하면 다 끌려나온다.***

```java
@Configuration
static class TempAppConfig {
    @Bean
    public DiscountPolicy fixDiscountPolicy() {
        return new FixDiscountPolicy();
    }

    @Bean
    public DiscountPolicy rateDiscountPolicy() {
        return new RateDiscountPolicy();
    }
}

AnnotationConfigApplicationContext h = new AnnotationConfigApplicationContext(TempAppConfig.class);

@Test
@DisplayName("부모 타입으로 조회시 자식이 둘 이상이면 에러")
void findBeanByParentTypeDuplicate() {
    assertThrows(NoUniqueBeanDefinitionException.class, () -> h.getBean(DiscountPolicy.class));
}

@Test
@DisplayName("자식이 둘 이상이면 빈 이름을 지정하면 된다")
void findBeanByParentTypeBeanName() {
    DiscountPolicy rateDiscountPolicy = h.getBean("rateDiscountPolicy", DiscountPolicy.class);
    assertThat(rateDiscountPolicy).isInstanceOf(RateDiscountPolicy.class);
}

@Test
@DisplayName("특정 하위 타입으로 조회")
void findBeanBySubType() {
    RateDiscountPolicy bean = h.getBean(RateDiscountPolicy.class);
    assertThat(bean).isInstanceOf(RateDiscountPolicy.class);
}

@Test
@DisplayName("부모 타입으로 모두 조회")
void findAllBeanByParentType() {
    Map<String, DiscountPolicy> beansOfType = h.getBeansOfType(DiscountPolicy.class);
    assertThat(beansOfType.size()).isEqualTo(2);
    for (String key : beansOfType.keySet()) {
        System.out.println("key = " + key + " value" + beansOfType.get(key));
    }
}

@Test
@DisplayName("부모 타입으로 모두 조회 - Object")
void findAllBeanByObjectType() {
    Map<String, Object> beansOfType = h.getBeansOfType(Object.class);
    for (String key : beansOfType.keySet()) {
        System.out.println("key = " + key + " value" + beansOfType.get(key));
    }
}
```

- 같은 타입이 두개 이상인 친구들을 다룰 때와 비슷하다. 다만 이 경우는 부모 타입으로 조회시 자식이 두개 이상인 경우를 다뤘다는 것만 인지하자.
- ***어찌 됐든 조회는 타입으로 할 수 있는데, 이 때 자식 타입까지 다 딸려나온다.***
- ***따라서 같은 타입이 두개 이상이거나, 자식이 두개 이상인 경우가 발생할 수 있을 것이고 이 경우 중복이라 오류가 뜬다. 따라서 위와 같은 방법으로 이름을 지정해주거나, `getBeansOfType`을 사용해 모두 조회가 가능하다.***

## 4) BeanFactory와 ApplicationContext

사실 `BeanFactory`<interface> → `ApplicationContext`<interface> → `AnnotationConfigApplicationContext` 와 같은 상속 관계를 갖는다.

`BeanFactory`

- 빈을 조회하고 관리하는 기능을 갖고 있다. `getBean`도 여기서 제공

`ApplicationContext`

- `BeanFactory`외에 다른 많은 interface를 상속한다. 애플리케이션 개발에는 빈 관리, 조회 기능 외에도 많은 것이 필요하기 때문이다.
- `MessageSource` 메시지소스를 활용한 국제화 기능
    - 국가에 따라 다른 출력이 가능하도록 한다.
- `EnvironmentCapable` 환경변수
    - 로컬, 개발, 운영등을 구분해서 처리할 수 있게 한다.
- `ApplicationEventPublisher` 애플리케이션 이벤트
    - 이벤트를 발행하고 구독하는 모델을 편리하게 지원. 뭔 소리인지는 모르겠다.
- `ResourceLoader` 편리한 리소스 조회
    - 파일, 클래스패스 등을 추상화해서 편리하게 조회 가능하도록 한다.

## 5) 다양한 설정 형식 지원 - 자바 코드, XML

그냥 아~ 이렇게 이루어져있구나 정도로 알아두면 편하다.

`GenericXmlApplicationContext` class를 사용하면 되며, annotation 기반의 그것을 쓰는 것과 방법은 동일하다. Annotation과 달리 얘는 내용을 바꾸더라도 추가적인 빌드 없이 돌아간다.

xml파일은 main - resources에 저장하면 된다. Java 파일이 아닌 것은 모두 여기에!

```xml
<bean id="memberService" class="hello.core.member.MemberServiceImpl">
        <constructor-arg name="memberRepository" ref="memberRepository" />
```

의 형식을 따른다. 이거말고 넣어줘야할 tag 및 내용이 조금 더 있긴하다.

- id: 빈의 이름
- class: 클래스. package 명까지 적어줘야한다.
- constructor-arg: 생성자에 들어가는 인자이다. memberService의 경우 memberRepository가 필요하다.
- ref: 생성자 인자의 출처

요즘에는 잘 쓰지 않는다. 이런거구나~ 정도로 알아두고 필요한 경우가 오면 문서를 뒤져 열심히 공부하자

## 6) 스프링 빈 설정 메타 정보 - BeanDefinition

![Untitled](https://gonnnnn.github.io/image/TIL/0712(2).png)                                                                                                                                                                                                                                                                              

각각의 ApplicationContext class는 각 형식에 맞는 reader를 가지고 있다. 어떤 형식의 appConfig를 제공하던, 이 reader가 BeanDefinition이라는 메타 정보를 생성한다. 그 후 컨테이너는 이 것을 가지고 노는 것. 다~ 추상화되는 것이라는 것 정도만 이해하면 된다.

아래와 같은 방법으로 조회 가능하다.

```java
AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AppConfig.class);
@Test
@DisplayName("빈 설정 메타정보 확인 - annotation")
void findApplicationBeanAnnotation() {
    String[] beanDefinitionNames = ac.getBeanDefinitionNames();
    for (String beanDefinitionName : beanDefinitionNames) {
        BeanDefinition beanDefinition = ac.getBeanDefinition(beanDefinitionName);
        if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
            System.out.println("beanDefinitionName" + beanDefinitionName +
                    " beanDefinition = " + beanDefinition);
        }
    }
}
```

- 참고로 `getBeanDefinition`을 쓰기 위해서는 `ApplicationContext` interface로 불러오면 안된다. 다른 interface가 필요하기 때문
- 사실 이런거 뽑아서 쓸일까지는 없다.


# 5. 싱글톤 컨테이너

## 1) 웹 애플리케이션과 싱글톤

웹 애플리케이션은 request가 정말 많다. 이런 request가 올 때마다 매번 객체를 생성한다면 과연 효율적일까?

초당 5만개의 요청이 들어온다면? 하나의 객체를 생성할 때 의존관계에 있는 객체들까지 생성하게 되는데, 5만개면 최소한 5만*n개의 객체를 생성하고 지워야하는 상황이 발생한다. 메모리 낭비가 심하다.

→ 그래서 싱글톤!

## 2) 싱글톤 패턴

클래스 인스턴스가 딱 1개만 생성되는 것을 보장하는 디자인 패턴

→ ***private 생성자를 사용해서 외부에서 임의로 new 키워드를 사용하지 못하도록 막아야한다.***

```java
public class SingletonService {
//    test case 작성은 아니고 그냥 시험해보는 class이다.

//    static 키워드! class 레벨에 올라가기 때문에 딱 하나만 만들어져 올라간다.
    private static final SingletonService instance = new SingletonService();

//    얘를 조회하는 함수만 만들어놓는 것이다!!!
    public static SingletonService getInstance() {
        return instance;
    }

//    private 생성자를 만들어 밖에서 new 키워드로 생성하지 못하게 막아버린다!
    private SingletonService() {
    }

    public void logic() {
        System.out.println("싱글톤 로직 호출됨");
    } 
}
```

- static 영역에 instance를 미리 하나 생성해서 올려두고
- 이게 필요하면 `getInstance` 메서드를 통해서만 조회할 수 있게 한다. 이러면 항상 같은 instance에 접근할 수 있게 된다.
- 누군가가 실수로라도 new 키워드를 통해 새로운 객체를 생성하려고 하면 알아서 막아준다! 컴파일 오류!

이게 singleton이라고 아무리 주석 달아놓더라도 다른 개발자들이 그냥 써버리면 소용이 없다. 자바 언어 특성을 기반으로 그렇게 쓸 수 밖에 없도록 강제하면 된다!

다만, 싱글톤 패턴은 다음과 같은 문제를 갖고 있다.

- 싱글톤 패턴을 구현하는 코드 자체가 위와 같이 조금 번거롭다.
- 의존 관계상 클라이언트가 구체 클래스에 의존한다. → DIP 위반
    - `구체클래스.getInstance`로 instance를 가져오게 되기 때문이라고 한다.
- 유연하게 테스트하기 어렵다. 인스턴스를 미리 받아서 내부적으로 설정이 다 끝나버리기 때문이다. 내부 속성을 변경하거나 초기화 하기 어렵다.
- private 생성자라 자식 클래스로 만들기 어렵기도 하다.

***spring은 이렇게까지 직접 설계하지 않아도 이런 단점을 다 극복하면서 싱글톤으로 관리해준다..!!!!!(얘의 능력은 어디까지인건가?)*** 

## 3) 싱글톤 컨테이너

싱글톤 패턴의 문제를 해결하며 싱글톤으로 관리!

잘 생각해보면 스프링 컨테이너의 빈 저장소에 이름-객체 매핑을 했었다. 애초에 컨테이너는 객체를 하나만 만들어서 관리하고 있었던 것이다.

- 이렇게 싱글톤 객체를 생성, 관리하는 기능을 싱글톤 레지스트리라 한다.
- 싱글톤 패턴을 위한 지저분한 코드, DIP, OCP, 테스트, private 생성자로부터 자유롭게 싱글톤 사용 가능!

```java
@Test
@DisplayName("스프링 컨테이너와 싱글톤")
void springContainer() {
    ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfig.class);

    MemberService memberService1 = ac.getBean("memberService", MemberService.class);
    MemberService memberService2 = ac.getBean("memberService", MemberService.class);

    System.out.println("memberService1 = " + memberService1);
    System.out.println("memberService2 = " + memberService2);
    Assertions.assertThat(memberService1).isSameAs(memberService2);
}
```

돌려보면 같은 주소값이 찍힌다. 우리는 MemberService 인터페이스와 구체 클래스를 설계할 때 싱글톤이 되게끔 하지 않았지만, ***스프링이 알아서 관리를 싱글톤처럼 해주게 된다.***

## 4) 싱글톤 방식의 주의점

이렇게 여러 클라이언트가 하나의 같은 ***객체 인스턴스를 공유하는 경우에는 객체를 stateful하게 설계하면 절대 안된다.***

***Stateless하게 해야 한다.***

- 특정 클라이언트에 의존적인 필드가 있으면 안된다.
- 특정 클라이언트가 값을 변경할 수 있는 필드가 있으면 안된다.
- 가급적 읽기만 가능해야 한다.
- 필드 대신에 자바에서 공유되지 않는 지역변수, 파라미터, ThreadLocal등을 사용해야한다.

***`공유 필드는 제바 제발 조심하고 쓰지 말자!!!`***

아래는 좋지 않은 예시

```java
// StatefulService.java
public class StatefulService {
//    실무 장애 예시를 위한 임의의 service 파일

    private int price; // 상태를 유지하는 필드

    public void order(String name, int price) {
        System.out.println("name = " + name + " price = " + price);
        this.price = price; // 여기가 문제!
    }

    public int getPrice() {
        return price;
    }
}

// StatefulServiceTest.java
class StatefulServiceTest {
    // 공유 변수를 사용하는 잘못된 예시

    @Test
    void statefulServiceSingleton() {
        ApplicationContext ac = new AnnotationConfigApplicationContext(TestConfig.class);
        StatefulService statefulService1 = ac.getBean(StatefulService.class);
        StatefulService statefulService2 = ac.getBean(StatefulService.class);

        //ThreadA: A사용자 10000원 주문
        statefulService1.order("userA", 10000);
        //ThreadB: B사용자 20000원 주문
        statefulService2.order("userB", 20000);

        //ThreadA: A사용자가 주문 금액 조회
        int price = statefulService1.getPrice();
        System.out.println("price = " + price);
				// -> 당연히 20000이 튀어나옴
        Assertions.assertThat(statefulService1.getPrice()).isEqualTo(20000);
    }

    static class TestConfig {
        @Bean
        public StatefulService statefulService(){
            return new StatefulService();
        }
    }
}
```

## 5) @Configuration과 싱글톤

이상한 점이 있다. AppConfig.java를 보면

```java
@Configuration
public class AppConfig {

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }

    @Bean
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

    @Bean
    public DiscountPolicy discountPolicy() {
        return new RateDiscountPolicy();
//        return new FixDiscountPolicy();
    }
}
```

`memberRepository` method이 `memberService`, `orderService`에서 한번씩 불리게 되고, 즉 new 키워드로 생성자가 두번 호출되게 된다.(여기에 스프링이 `memberRepository` 처음에 한번 호출하는 것까지 총 3번) 다른 객체가 만들어져야할 것같다. 하지만 그럼 싱글톤을 위배되게 된다.

과연 그럴까? 아래 코드로 테스트 가능하다.

```java
public class ConfigurationSingletonTest {
    @Test
    void configurationTest() {
        ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfig.class);
        // 테스트를 위해 memberServiceImpl, orderServiceImpl에 repository getter를 미리 추가해놓았다.
        // 따라서 interface가 아니라 구체 클래스로 가져왔다. interface에는 getter가 없으니까
        MemberServiceImpl memberService = ac.getBean(MemberServiceImpl.class);
        OrderServiceImpl orderService = ac.getBean(OrderServiceImpl.class);
        MemberRepository memberRepository = ac.getBean("memberRepository", MemberRepository.class);

        MemberRepository memberRepository1 = memberService.getMemberRepository();
        MemberRepository memberRepository2 = orderService.getMemberRepository();
        System.out.println("memberService -> memberRepository1 = " + memberRepository1);
        System.out.println("orderService -> memberRepository2 = " + memberRepository2);
        System.out.println("memberRepository = " + memberRepository);

        Assertions.assertThat(memberRepository1).isSameAs(memberRepository);
        Assertions.assertThat(memberRepository2).isSameAs(memberRepository);
    }
}
```

놀랍게도 이를 실행시켜보면 모두 같은 참조값을 반환하는 것을 알 수 있고, 테스트가 성공적으로 진행된다.

***AppConfig.java의 각 method에 print문을 기입해 각 method가 몇번 호출되는지도 직접 확인해보라. 모두 한번씩만 호출된다!!***

대체 무슨 일이 일어나는걸까?

## 6) @Configuration과 바이트코드 조작의 마법

스프링 컨테이너는 싱글톤 레지스트리이다. 싱글톤을 보장해야한다.

하지만 어떻게?@?!#!@

아래 코드를 실행시켜보자

```java
@Test
void configurationDeep() {
    ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfig.class);
    AppConfig bean = ac.getBean(AppConfig.class);
    System.out.println("bean = " + bean.getClass());
}
```

결과를 보면 `class hello.core.AppConfig`가 아니라 CGLIB… 라는 이름이 추가적으로 붙은 이름이 출력된다.

***→ 스프링은  CGLIB라는 바이트코드 조작 라이브러리를 사용해 우리가 만든 `AppConfig`를 상속받는 다른 클래스를 만들고, 이를 빈으로 등록한다.***

*`AppConfig`의 자식 클래스이기 때문에 조회가 되는 것이기도 하다.

실제 코드는 아니지만, 이 클래스는 다음과 같은 로직을 통해 객체가 반복적으로 생성되는 것을 막아준다.

```java
@Bean
public MemberRepository memberRepository() {
 
 if (memoryMemberRepository가 이미 스프링 컨테이너에 등록되어 있으면?) {
 return 스프링 컨테이너에서 찾아서 반환;
 } else { //스프링 컨테이너에 없으면
 기존 로직을 호출해서 MemoryMemberRepository를 생성하고 스프링 컨테이너에 등록
 return 반환
 }
}
```

`@Configuration`이 바로 이 기능을 가능케 한다. 이를 붙임으로써 `AppConfig`를 상속하는 다른 클래스를 만들게 된다.

이 annotation을 붙이지 않아도, bean 등록은 잘 된다. 하지만 `AppConfig`를 상속하는 클래스가 아닌 `AppConfig` 자체가 bean에 등록되게 되고, `AppConfig`를 그대로 읽어 bean을 등록하게 되니, `memberRepository`가 총 3번 호출되게 된다. 우리가 처음에 생각했던 그 일이 일어나게 되는 것이다. 물론 이 3개의 instance들은 모두 다른 참조값을 갖게 된다. 또한 `orderService`, `memberService`에 들어가는 `memberRepository` instance들은 bean으로 등록되지도 않는다.

`Autowired`라는 것을 사용해 이를 해결할 수도 있다. 자동 의존관계 주입이라고 한다. 나중에 알아보자!