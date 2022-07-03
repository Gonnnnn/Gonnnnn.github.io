---
title: "Computer Architecture (9) Arithmetic for Computers 2"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# Floating Point

Adding Support for Numbers with Fractions

### Floating Point

- numbers with fractions : Signed/Unsigned integer만으로는 표현이 안되는 숫자들
- 다양한 표현법이 있지만 우리는 scientific notation을 채택한다.
    - 1.xxxxxx(2) * 2^(yyyyyy) 와 같은 형식이다.
    - dot(.) : binary point
    - xxxxxx : fraction/mantissa
    - yyyyyy : exponent
- Floating point : binary point를 지원하는 computer arithmetic을 의미한다. 컴퓨터가 Floating point를 지원한다는 것은 scientific notation등을 따르는, fraction으로 표현되는 두 수의 산술 연산을 지원한다는 것이다.

### Floating-Point Representation : Single Precision

(-1)^s * F * 2^E 로 표현 가능하다.

![Untitled](https://gonnnnn.github.io/image/TIL/0519(1).png)          

Single Precision이다.

- 1bit의 s (sign), 23bit의 F(fraction), 8bit의 E(exponent)로 이루어져있다. F, E는 정확하게 fraction과 exponent를 나타내지는 않는다. 이는 나중에 다룬다.
- Overflow뿐만 아니라 underflow도 발생할 수 있다.
    - overflow : positive exponent가 field 내에 표현되기에는 너무 큰 경우
    - underflow : negative exponent가 field내에 표현되기에는 너무 큰 경우

### Floating-Point Representation : Double Precision

![Untitled](https://gonnnnn.github.io/image/TIL/0519(2).png)              

Double Precision은 위와 같다. 훨씬 더 큰 Exponent를 표현할 수 있어서 underflow, overflow가 덜 일어난다.

- 1bit의 s, 52bit의 F, 11bit의 E로 이루어져있다.

### IEEE 754 Standard

- 수를 fraction과 exponent를 이용해 Binary number 형식으로 변환하고 이를, 다시 원래 우리가 원하던 수로 변환할 때 참고되는 기준이다.
- 위에서 확인했던 single precision등과 같은 형식과  Rounding rules, opertions, exception handling 등이 정의된다.

23, 52bit의 fraction만으로는 정확히 수를 표현하기 힘들어서 가상의 1bit을 추가한다.

- fraction : 23 or 52bit number
- significand : 1 + 23 or 52bit number

→ **23bit의 fraction이 모두 0인 경우, 이는 사실 24bit의 100...00(2)을 의미한다.**

- **결론적으로 (-1)^s * (1 + Fraction) * 2^E가 된다.**
    - = (-1)^s * (1 + s1*2*-1 + s2*2^-2 + s3*2^-3 + ...) * 2^E가 된다.
    - s1, s2는 fraction field의 가장 좌측에서부터 첫번째, 두번째 숫자이다.
    → fraction의 모든 수는 1보다 작은 수를 표현한다.
    - scientific notation인 1.xxxxxx(2) * 2^(yyyyyy)의 형식을 갖게 됨을 볼 수 있다.

** bias : Exponent는 0~255로 표현된다. 실제 지수에 127을 bias로 더해줘 표현한다. -3승을 표현하기 위해서는 -3 + 127 = 124, 10승은 10 + 127 = 128로 표현하는 것이다. 이 때 0, 255는 실제 숫자 0과 무한대,NaN을 표현하는데 사용되어 실질적으로 1~254가 쓰인다.

** 항상 유효숫자의 최상위 비트가 1이 되도록 소수점의 위치를 결정하고 이를 정규화 한다고 한다. 43.25는 101011.01로 표현할 수 있고,  정규화를 거치면 1.0101101 * 2^5가 된다. 지수에 bias를 더하면 132가 되니 실제 지수 값은 1000100이 된다. 즉 부호는 0, 지수는 1000100, 유효숫자는 1010 1101 0000 0000 0000 000이 된다. 여기서 최상위 비트는 항상 1이 되도록 하기로 약속했으므로, 이는 굳이 표현하지 않는다. 따라서 1을 제외하고 다시 표현하면 0101 1010 0000 0000 0000 000이 된다.