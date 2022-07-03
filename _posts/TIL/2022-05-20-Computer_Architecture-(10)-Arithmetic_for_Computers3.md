---
title: "Computer Architecture (10) Arithmetic for Computers 3"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

### Representing Unusual Events

무한대 등의 수를 표현할 필요가 있다. 각각의 수, 상황들은 아래의 표와 같이 정의된다. 각각을 표현하기 위해 exponent와 fraction에 들어갈 수 있는 값들을 확인할 수 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0520(1).png)          

- denormalized number는 floating point로 표현할 수 있는 수보다 작은 수들을 의미한다. 정상적인 규약대로 표현할 수 없으니 denormalized라고 칭한다. Exponent에 0을 기입함으로써, fraction 앞에 1.이 아니라 0.을 붙여 읽는다.
- NAN은 비 정상적인 연산(0/0, inf-inf 등)이 이루어졌을 때 출력되는 값이다.
- Single precision의 경우 8bit의 exponent를 갖는다. 최댓값은 255이며, infinity와 NaN을 표현하기 위해서는 exponent의 모든 bit가 1이여야한다는 것을 볼 수 있다.

[http://egloos.zum.com/studyfoss/v/4960394](http://egloos.zum.com/studyfoss/v/4960394)

[http://studyfoss.egloos.com/4956717](http://studyfoss.egloos.com/4956717)

### Comparison-Friendly Format

하드웨어는 재사용이 가능하면 좋다. Integer를 위해 사용하는 comparison logic을 여기서도 적용할 수 있는 것이 좋다는 것이다. 실제로 이를 준수하며 만들어졌다.

- (-1)^s * (1 + f) * 2^e임을 다시 한번 떠올려보자
- MSB는 sign bit이다. 이 때문에 부호를 통해 먼저 비교가 가능하다.
- 1+f < 2이기 때문에, e의 크기에 따라 대소 관계가 먼저 비교된다. 따라서 s 뒤에 e가 오고, 그 후에 f가 오는 것이다.

### Handling Negative Exponents

- two’s complement는 comparison-friendly하지 않다. Integer처럼 비교할 수 없다. 지수가 음수일 경우 0111...과 같은 꼴이 될 것이기 때문이다.
- IEEE 754는 biased notation을 사용한다.
    - 정확히는 (-1)^s * (1+F) * 2*(E-Bias)가 된다.
    - Single/Double precision에서 bias는 127, 1023이다. 예를 들어 E가 124라면, 실제로 124승을 의미하는게 아니라 124-127=-3승을 의미한다는 것이다.
    - 따라서 Single precision의 경우 -127~128승을, Double precision의 경우 -1023~1024승을 나타낼 수 있다.

### Example : Biased Exponents

10진수 -0.75를 예시로 들어보자.

- -0.75 = -3/4 = -3/2^2 = -11(2)/2^2(10) = -0.11(2) = -1.1(2) * 2^(-1)
- 정규화시키면, (-1) * (1 + 0.1) * 2^(-1)이 된다.
- s = 1, F = .10000..00(2), E = -1 + 127 = 126(10) = 01111110(2)
- 즉, 1 01111110 1000...000(2)가 된다.

`10진수 실수 2진수 변환 확인`

### Floating-Point Addition

9.999(10) * 10^1 + 1.610(10) * 10^-2를 예로 들어보자. four-digit significand와 two-digit exponent로 표현해보려한다.

- Decimal points를 정렬한다.
    - exponent가 같아질 때까지 더 작은 수의 sifgnificand를 shift한다.
    - 1.610 * 10^-2는 0.01610 * 10^1이 되며, 유효숫자는 4자리까지로 볼 것이므로 0.016 * 10^1로 변환한다.
- 9.999 * 10^1 + 0.016 * 10^1 = 10.015 * 10^1가 된다.
- 1.0015 * 10^2로 다시 normalize한다.
- 1.0015 * 10^2를 1.002 * 10^2로 유효숫자에 맞춰서 round한다.

다음과 같은 다이어그램으로 표현할 수 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0520(2).png)              

1. exponent가 같아질 때까지 shift
2. significands를 더한다
3. normalize한다.
4. overflow/underflow가 발생하면 exception을 호출하고, 그게 아니라면 fraction bit에 맞게 round한다.
5. normalize가 되어있지 않다면 다시 3번과정으로 돌아가 반복한다.

### Floating-Point Multiplication

1.110(10) * 10^10 + 9.200(10) * 10^-5를 예로 들어보자. four-digit significand와 two-digit exponent로 표현해보려한다.

- Exponent를 먼저 계산한다.
    - 최종 exponent는 단순 합으로 구해질 수 있다. 10 + (-5) = 5이다.
    - bias를 고려해서 다시 표현해준다. 10 + 127 + (-5 + 127) - 127 = 5 + 127 = 132
- Significands를 곱한다.
    - 1.110 * 9.200 = 10.212000이다. 유효숫자를 고려하여 10.212로 줄인다.
- normalize한다.
    - 10.212 * 10^5 = 1.0212 * 10^6
- round한다.
    - 유효숫자를 고려하여 1.021 * 10^6으로 round한다.
- sign을 결정한다.
    - 두 operands의 sign이 같았다면 +, 아니라면 -로 지정한다.

다음과 같은 다이어그램으로 표현할 수 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0520(3).png)              

1. exponent를 더하고 bias를 고려해 다시 표현한다.
2. significands를 곱한다.
3. 필요하다면 normalize한다.
4. overflow/underflow가 발생하면 exception을 호출한다. 그렇지 않다면 significand를 round한다.
5. normalize가 되어있지 않다면 다시 3으로 돌아간다.
6. sign을 결정한다.

### MIPS: Floating-Point Support

MIPS ISA에서도 floating point를 지원한다.

- $f0 ~ $f31 : foating-point register이다. 4bytes의 크기를 갖기에 one single-precision floating-point만 표현 가능하다. double precision은 두개의 register을 통해 표현해야한다.
- 이를 위한 instruction도 제공된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0520(4).png)              