---
title: "Computer Architecture (10) Arithmetic for Computers 3"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---
# Multiplication & Division

### Addition in Hardware

- 오른쪽부터 더해가며, 왼쪽으로 carry가 발생한다.

### Subtraction in Hardware

- Option 1 : direct subtraction
    - ex) 7 - 6 → 111(2) - 110(2)
- Option 2 : two’s complement를 더하는 방법. Signed number의 경우 LMB이 1일 경우 음수임을 의미한다.
    - ex) 7 - 6 → 7 + (-6) → 000...111(2) + ... ...010(2) ** 8byte로 표현됨을 가정했다. 그게 아니더라도 7, 6이 표현될 수 있는 정도의 크기면 상관 없긴 하다.
    - 크기(여기서는 8byte)가 넘어가서 1의 carry가 LMB 왼쪽에 생기면, 이는 버림한다. 2bit로 표현되는 숫자 01(2)(=1)과 11(2)(=-1)을 더했을 때 100이 될 경우 1을 버림하고 00으로 표기하는 것이다.

### Overflow

- 위 subtraction에서 LMB에 의해 carry가 생기는 것을 overflow가 발생했다고 한다.
- 다음과 같은 경우에 Overflow는 절대 발생하지 않는다. 
**32bit의 경우 음수부는 (-2^31 ~ -1), 양수부는 (0~2^31 - 1)
    - 부호가 다른 두 수를 더할 때
    - 같은 부호의 수를 뺄 때

### Detecting Overflow

- 다음과 같은 경우에 overflow가 발생한다
    - 양수 + 양수였지만 결과가 음수일 때 → 양수부 최대치를 넘어가는 경우
    - 양수 - 음수였지만 결과가 음수일 때 → 양수부 최대치를 넘어가는 경우
    - 음수 - 양수였지만 결과가 양수일 때 → 음수부 최소치를 넘어가는 경우
    - 음수 + 음수였지만 결과가 양수일 때 → 음수부 최소치를 넘어가는 겨우
- sign bit(31번째 bit)이 기대되는 결과와 다른 경우 overflow가 발생했음을 확인가능하다.

### Multiplication

Multiplicand * Mulitplier = Product

- 10진수의 곱셈과 같은 방식으로 이루어진다. 예시를 보자
    - 10진수 두개의 곱을 생각해보자. 110* 101의 경우 110*1*1 + 110*0*10 + 110*1*100이 된다. (자릿수의 수 * 자릿수 ex) 20의 경우 2 * 10)를 110에 곱해가며, 더해주는 방식이다.
    - 2진수의 곱도 같은 방식으로 이루어진다. 다만 인풋과 결과를 2진수로 읽어들이면 된다. 이걸 조금 더 2진수스러운 방법으로 표현해보려고 한다.

![0513(1)](https://gonnnnn.github.io/image/TIL/0513(1).png)

![0513(2)](https://gonnnnn.github.io/image/TIL/0513(2).png)

![0513(3)](https://gonnnnn.github.io/image/TIL/0513(3).png)

- Hardware 단에서 32bit 수의 곱셈이 이루어지는 과정은 위의 우측 상단 다이어그램으로 표현 가능하다.
    - 32bit의 곱셈 결과는 최대 64bit가 될 수 있다. 따라서 Product는 64bits register에 저장되며, 처음엔 0으로 초기화되어있다.
    - Multiplicand는 64bits register에 저장되는 것을 확인하자.
    - ***2진수의 곱을 10진수의 곱처럼 계산하는 것은 매 연산마다 Multiplicand를 shift left, muliplier를 shift right하고, multiplicand를 multiplier의 RMB(=LSB)에 곱해줌으로써 구현 가능하다. Multipicand의 경우 shift left를 계속 적용해줘야하기 때문에 64bits register에 저장하는 것이다.***
- 좌측의 다이어그램은 전체 logic을 표현한다. 이와 같은 과정으로 마치 10진수의 곱에서 자릿수 * 자릿수의 곱을 multiplicand에 곱해 더해나가는 것과 같은 식의 연산을 할 수 있다.
    - ***Multiplier의 LSB이 0인지 확인한다.***
    - ***1이라면 multiplicand를 product에 더하고, 0이라면 그냥 넘어간다.***
    - ***Multiplicand를 1 bit left shift, multiplier를 1 bit right shift한다.***
    - ***bit 수만큼 반복한다.***
- 우측 하단의 표는 0010 * 0011의 예시이다.

### Faster Multiplication

위의 방법은 직관적이지만, 너무 오래 걸린다.

→ shifting하고, muliplicand를 product에 더해주는 과정들을 병렬적으로 처리할 수는 없을까?

![0513(4)](https://gonnnnn.github.io/image/TIL/0513(4).png)

- Multiplier buffer가 사라졌다. 이는 ***초기에 product register의 lower 32bit(우측 32bit)에 저장된다. Product는 초기에 product register의 upper 32bit(좌측 32bit)에 저장된다.***
- Multiplicand register의 크기가 32bit으로 줄었다.
- ***매 iteration마다 product register안의 값의 LSB를 확인해 multiplicand의 값을 product에 더해주고, product register안의 값을 1 bit right shift한다***. 이로써 product는 자동으로 다음 iteration에 multiplicand를 더할 준비를 하게되고, multiplier 또한 동시에 right shift된다. 이로써 product는 1bit씩 늘어나고, multiplier는 1bit씩 줄어든다.
- ALU도 32bit으로 줄었다. Product register에서 product를 update할 때, 앞의 32bit만 update하면 되기 때문이다.

아래는 tree 구조를 채용한 parallel multiplier/adder tree이다.

![0513(5)](https://gonnnnn.github.io/image/TIL/0513(5).png)

`다시 들어봐야 할 듯 하다`

### Multiplication in MIPS

MIPS의 각 register은 32bit의 크기를 갖는다. 32bit integer끼리의 곱은 64bit로 표현된다. 따라서 MIPS는 ***곱셈 결과의 앞 32bit 부분을 hi, 뒤 32bit 부분을 lo register에 저장***한다.

- mult/multu : 2개의 32 bit signed/unsigned integer을 곱한다.
- mfhi(move from hi) : hi에 저장된 값을 가져온다.
- mflo : lo에 저장된 값을 가져온다.

### Division

Dividend = Quotient * Divisor + Remainder

곱셈과 같이 10진수의 그것과 같은 방법을 따르면 해결할 수 있으며, 더 빠른 방법도 존재한다.

![0513(6)](https://gonnnnn.github.io/image/TIL/0513(6).png)

![0513(7)](https://gonnnnn.github.io/image/TIL/0513(7).png)

![0513(8)](https://gonnnnn.github.io/image/TIL/0513(8).png)


- 우측 상단의 다이어그램으로 하드웨어를 단순화할 수 있다. Divisor, Quotient, Remainder buffer가 존재한다. Divisor은 64bit로 되어있는데, 앞 16bit는 0으로 채워져있다. 이는 Divisor을 shift right해야할 필요가 있기 때문이다. Divident는 초기에 Remainder register에 저장된다고 한다.
- 좌측의 다이어그램은 전체 logic을 표현한다.
    - Divisor value에서 remainder value를 빼고, 결과를 remainder에 저장한다.
    - 다음과 같은 경우가 존재한다.
        - Current remainder이 0 이상인 경우, 즉 prev remainder ≥ divisor인 경우, Quetient register을 shift left하고 RMB에 1을 넣는다.
        - Current remainder이 0 미만인 경우, 즉 prev remainder < divisor인 경우,  Remainder register에 다시 Divisor register을 더해 원래 값을 복원시키고, 그 결과를 remainder register에 저장한다. 그 후 Quotient register을 shift left하고 RMB에 0을 넣는다.
    - Divisor register을 1 bit shift right한다.
    - 위 과정을 총 33(Divisor register bit 크기 + 1)번 반복한다.
- 우측 하단의 예시를 보면 쉽게 이해할 수 있다.
    
    

### Faster Division

![0513(9)](https://gonnnnn.github.io/image/TIL/0513(9).png)

- Multiplication과 유사한 구조를 갖는다.
- Divisor을 고정하고, 처음에 divident를 remainder register 좌측 32bit에 저장한다. Remainder register을 1bit shift left하고 시작한다.
- 좌측 32bit에서 divisor을 뺀다
    - 연산 결과가 음수이면 좌측 32bit 값을 다시 복원하고, 전체 64bit을 1bit  shift left 후 우측 32bit의 RMB에 0을 기입한다.
    - 연산 결과가 양수이면 전체 64bit을 1bit shift left 후 우측 32bit의 RMB에 1을 기입한다.
- `Divisor register의 bit 크기만큼 수행한 후, remainder register의 좌측 32bit을 1bit shift right하면, 좌측은 remainder, 우측은 quotient가 된다.` 수업에서는 이게 아니긴했는데, 다시 좀 찾아보자

- Apply the model we make into our problem

### Division in MIPS

곱셈과 마찬가지로 MIPS는 ***나눗셈 결과(Remainder register)의 앞 32bit 부분(remainder)을 hi, 뒤 32bit 부분(quotient)을 lo register에 저장***한다.

- div/divu : 2개의 32 bit signed/unsigned integer로 나눗셈을 시행한다.
- mfhi(move from hi) : hi에 저장된 값을 가져온다.
- mflo : lo에 저장된 값을 가져온다.

### Multiplicatin & Division in MIPS

![0513(10)](https://gonnnnn.github.io/image/TIL/0513(10).png)