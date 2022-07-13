---
title: "Spring (13) SpringCore Component Scan"
categories:
    - TIL
tags:
    - CS
    - Spring
    - Backend
---

# 6. 컴포넌트 스캔

## 1) 컴포넌트 스캔과 의존관계 자동 주입

사실 스프링은 Configuration 클래스에서`@Bean`으로 빈 등록을 해주지 않아도, `@Component`가 붙은 class를 알아서 스캔 후 빈 등록을 해주고 의존관계까지 이어주는 기능이 있다.

```java
@Configuration
// 기존의 AppConfig 파일은 이 예시와는 별개의 것이니 제외해야한다!
// @Configuration이 붙은 class를 배제하게 함으로써 AppConfig 파일을 제외시켰다
@ComponentScan(
        excludeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = Configuration.class)
)
public class AutoAppConfig {
    // @Bean으로 등록하는게 하나도 없다!! 자동등록되게 해놨으니 당연 :)

}
```

- 아무 설정 정보 없이 `@ComponentScan`이라는 어노테이션 하나만 추가해주면 된다.

```java
@Component
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository;

    @Autowired // ac.getBean(MemberRepository.class)로 객체를 받아와 넣어주는 것 같은 방식
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

		...

}
```

- 기존과 다르게 `@Component(”name”)`을 붙여줬다. 스프링은 클래스들을 모두 스캔하며 해당 어노테이션이 붙은 클래스들을 알아서 bean으로 등록해준다. name 속성으로 이름을 부여할 수도 있다.
    - 이름을 따로 지정하지 않으면 class명의 가장 앞글자만 소문자로 바꾼채 그대로 사용
- `@Autowired` 어노테이션을 생성자에 붙여줌으로써 의존관계를 자동으로 주입하도록 할 수 있다.
    - 생성자에 인자로 들어가는 것의 타입을 기준으로 스프링 컨테이너에서 빈을 찾아서 주입한다.
    - 같은 타입이 여러개면 충돌! 나중에 설명

## 2) 탐색 위치와 기본 스캔 대상

### 탐색 위치 설정

`@ComponentScan(attrb = …)` 시작 위치에 관한 속성

- basePackages
    - 컴포넌트 스캔을 시작하는 루트 위치를 지정할 수 있다.
    - java 디렉토리 밑을 기준으로 경로를 넣어주면 된다. ex) src/main/java/hello/core/member이면 “hello.core.member”
    - {경로1, 경로2, …}와 같은 형식으로 여러 경로도 설정 가능
- basePackageClasses
    - 넣어준 클래스의 패키지를 탐색 시작 위치로 지정한다.
    - default는 `@ComponentScan` 어노테이션을 붙여놓은 class의 패키지를 시작으로 탐색. 그러니까 config class의 패키지가 시작 위치가 되는 것
    - ***패키지 위치를 지정하지 말고, 설정 정보 클래스를 프로젝트 최상단에 두면 그냥 제일 편하다.***
    - ***사실 spring boot를 사용하면 자동으로 만들어지는 CoreApplication class에 붙어있는 `@SpringBootApplication`에 `@ComponentScan`이 포함되어있다.  spring boot 쓰면 얘 때문에 알아서 컴포넌트 스캔 잘 된다.***

### 컴포넌트 스캔 기본 대상

다음과 같은 경우도 스캔된다. 얘들 소스 코드를 보면 사실 `@Component`를 포함하고 있다.

- `@Controller` 스프링 mvc 컨트롤러
- `@Service` 스프링 비니지스 로직
- `@Repository` 스프링 데이터 접근 계층에서 사용
    - DB를 바꾸면 데이터 접근 계층의 예외도 바뀌게 되는데 예외가 바뀌면 다른 비니지스 로직 코드 등에도 영향을 줄 수 있다. 그렇지 않도록 스프링이 중간에서 스프링 예외로 변환해주고, 사용자는 이 스프링 예외를 다루는 코드를 작성하게 된다.
- `@Configuration` 스프링 설정 정보

** 참고

어노테이션에는 상속 관계라는 것이 없다. 따라서 어노테이션에 어노테이션을 추가로 이어붙였다고 해서 인식하는 것은 java 언어의 기능은 아니고 스프링이 지원하는 기능이다.

## 3) 필터

### 필터

`@includeFilters`컴포넌트 스캔에 추가할 대상

`@excludeFilters`컴포넌트 스캔에서 제외할 대상

예시

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface MyIncludeComponent {
}
--------------
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface MyExcludeComponent {
}
--------------
@MyIncludeComponent
public class BeanA {
}
--------------
@MyExcludeComponent
public class BeanB {
}
```

- 어노테이션을 직접 만들어주고, `@ComponentScan`에 넣어주는 방식이다.
- 어노테이션을 만들 때는 target, retentionm, documented 세 개의 어노테이션을 붙여줘야한다고 하는데, 이 부분은 따로 공부해보자
- 원하는 class들에 annotation을 달아주기만 하면 된다.

```java
@Test
void filterScan() {
    AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ComponentFilterAppConfig.class);
    BeanA beanA = ac.getBean("beanA", BeanA.class);
    assertThat(beanA).isNotNull();
    assertThrows(NoSuchBeanDefinitionException.class, ()->ac.getBean("beanB", BeanB.class));
}

@Configuration
@ComponentScan(includeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyIncludeComponent.class),
               excludeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyExcludeComponent.class)
)
static class ComponentFilterAppConfig {
}
```

해당 test를 실행하면 통과한다.

- includeFilters, excludeFilters에 위와 같이 집어넣으면 filter로 인식한다.
- beanA의 경우 include해야하니 당연히 null이 아니게 되고, beanB는 exclude되니 exception이 터진다.

### FilterType 옵션

사실 Annotation을 이용해 filter하는 방법을 포함해 총 5가지가 있다.

annotation, assignable_type 외에 사실 잘 사용하지는 않는다.

`@Component`면 충분해서 애초에 filter도 exclude나 가끔 사용하는 정도?

- ANNOTATION
    - 어노테이션을 인식해서 동작하는 방식
    - Default값이라서 사실 위 코드에서 `type = Filtertype.ANNOTATION`을 생략해도 잘 돌아간다.
- ASSIGNABLE_TYPE
    - 직접 타입을 지정해주는 방식. 지정한 타입과 자식 타입을 인식해서 동작
    - BeanA도 빼버리려면 이런식으로 넣어줄 수 있겠다.

```java
@ComponentScan(includeFilters = {
								@ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyIncludeComponent.class),
							 },
				       excludeFilters = {
								@ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyExcludeComponent.class),
								@FilterType = FilterType.ASSIGNABLE_TYPE, classes = BeanA.class
							 }
)
```

- ASPECTJ
    - ASPECTJ 패턴으로 바로 찾아오는 것. PARC에서 개발한 자바 전용 AOP 확장 기능이라는데 뭔지는 잘 모르겠다.
- REGEX
    - 정규 표현식을 사용해 필터링한다
- CUSTOM
    - `TypeFilter`라는 인터페이스를 구현해서 처리하는 방식

## 4) 중복 등록과 충돌

컴포넌트 스캔으로 빈이 등록될 때, 같은 이름을 등록하려하면 어떻게 될까?

두 가지 상황이 발생할 수 있다.

- 자동 빈 등록 vs 자동 빈 등록
    - 같은게 있으면 알아서 `ConflictingBeanDefinitionException`이 터진다.
- 수동 빈 등록 vs 자동 빈 등록
    - 수동 등록 빈이 우선권을 갖는다. 수동 빈이 자동 빈을 override한다. 로그로 다 찍히긴 한다고 한다.
    - 이게 잡기 애매한 버그라서 최근 스프링 부트에서는 수동 빈 등록과 자동 빈 등록이 충돌나면 오류가 나도록 기본 값이 설정되어있다고. `CoreApplicatoin`을 돌려보면 알 수 있다.

개발은 혼자하는게 아니다. 난 괜찮아도 다른 사람들은 아닐 수 있고, 모두에게 전파를 명확히 할 수 있는 것도 아니라서 명확하고 확실한 것을 선택하는 것이 낫다.