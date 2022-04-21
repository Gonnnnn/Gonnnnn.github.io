---
title: "Computer Architecture (3) Intro to MIPS"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# MIPS

## 1. What is MIPS?

### Talking with Computers

- Computer가 인식하는 단어들을 ***insturction***이라고 한다.
- 이런 vocabulary, a set of words를 ***instruction set***이라고 한다.
- ***ISA는 instruction set을 정의하는 documents이다. ISA는 instruction set외에도 소프트웨어 설계시 어떤 프로그래밍 모델을 써야하는지, 특정 instruction 뒤 다른 instruction이 오면 컴퓨터의 state이 어떻게 바뀌는지 등 해당 하드웨어를 사용하기 위해 알아야할 다양한 것들을 정의해준다***.
- MIPS ISA에 대해 중점적으로 다룰 것이다. 그러나 모든 컴퓨터들은 기본적으로 수행해야할 수 있는 basic operations들이 있어 ISA들은 꽤 비슷하다.

### A PL for MIPS CPUs

MIPS는

- MIPS CPU가 할 수 있는 것을 정의해 놓은 ISA
- 혹은 MIPS CPU가 해야하는 것을 specify하는 programming language라고 볼 수도 있다.

MIPS를 PL로 추상화하며 다음을 배워보려 한다. why? 이해하기 수월해지기 때문이다.

- programming model & paradigm
- syntax(자료형, operations 등)
    - MIPS ISA에 따르면 어떤 종류의 string/value들이 사용될 수 있는가?
- semantics(instructions 등)
    - MIPS ISA에서는 어떻게 strings/values에 meaning을 할당하는가?

***이러한 것을 Programmer-Visible State(PVS)라고 한다. HW를 쓰기 위해 프로그래머로서 참고하거나 사용할 수 있는 state나 set of valid instructions 정도로 이해할 수 있다.

### Imperative Programming

- MIPS instructions는 CPU의 state를 변경한다. (functional programming에서는 persistent state라는 개념이 없다고 한다.) Value들이 메모리에 저장된다.
- 모든 instructions들은 순서대로 실행된다.
    - jumps/branches와 같이 execution flow를 조절하는 도구를 제공한다.
- ***PVS of the MIPS ISA는 다음으로 구성된다***.
    - MIPS instructions를 실행하기 위한 ***CPU core***
    - CPU core들이 바로 접근 가능한 ***Registers***
    - Register에 데이터를 load할 수 있는 ***Memory***
    - PVS는 위 세가지 요소들 사이에서 데이터가 어떻게 이동하는지, 변하는지를 볼 수 있는 것이라고 생각하면 쉽다. 말 그대로 프로그래머가 볼 수 있는 state를 의미한다.

### Programming Model

- ***Load-Store architecture*** with ***32 registers***
    - CPU는 memory에 직접 접근하지 않는다. 또한 이 architecture에서 registers는 32개로 제한된다. 이 수는 요구되는 메모리의 크기에 무관하다.
    - Memory의 data를 registers로 가져오고, CPU는 이 register에 접근해 data를 읽고, 연산하고, 또 register에 쓴다. 그 후 다시 그 data를 memory에 올린다.

**C++와 같은 high-level language에서는 Memory의 주소값을 통해 value를 직접 얻어와 연산이 가능하다. Memory의 12, 24와 같은 것의 주소를 찾아가 직접 얻을 수 있다는 것.

![pvs(1)](Gonnnnn.github.io/image/til/pvs(1).png)

### Bits & Data Sizes

- Popular Data sizes!
    - Bit: 1-bit
    - Byte: 8-bit = “char” in C/C++
    - Halfword: 16-bit = 2-byte
    - Word: 32-bit = 4-byte. 인기 겁나 많았음!
    - Doubleword: 64-bit = 8-byte (아마 *Not supported by MIPS*)

48-bit를 표현하려면 doubleword를 쓰던지, halfword 3개를 사용하거나, word와 halfword를 사용할 수 있겠다.

### Numbers

- Unsigned: n-bit long positive binary numbers
    - range : 0~2^n - 1
- Signed: n-bit long two’s complement
    - 첫 번째 bit는 sign을 나타낸다. 0 : pos, 1 : neg
    - decimal로 변환시 첫 번째 bit에는 -1이 곱해지는 것
    - range : -2^(n-1) ~ 2^(n-1) - 1

### Model with data sizes

위의 것들을 종합해 시각화해보자. 아래는 PVS이다.

![pvs(2)](Gonnnnn.github.io/image/til/pvs(2).png)

- PVS의 구성 요소인 CPU core, registers, memory를 위와 같이 시각화했다.

**Register**

32 registers in the prgorammer visibe state defined by MIPS ISA

- MIPS이기에 registers 32개에는 각각 이름이 있다.(나중에 배운다)
- ISA는 각 register의 size를 명시한다.
    - MIPS에서는 32bit=4byte=word size 이다. 총 32*4bytes = 128B = 1kilo bit = 1 Kib)의 size를 가진다.

**Memory**

- ISA는 support되는 max size of memory도 명시한다. 여기서 ***MIPS ISA가 32bit ISA***인 이유가 나오는데, ***memory address를 specify하기 위해 32bit을 쓰기 때문***이다. 정확히는 32 bit unsigned address를 쓴다.
- each address는 1B의 data를 담는다. 즉 MIPS ISA는 2^32 bytes(=4GB)의 메모리를 갖고 있는 것이다.
    - 예로, 윈도우 xp는 4GB까지만 활용할 수 있다. 윈도우xp는 32bit x86 ISA용으로 설계됐기 때문이다. 메모리 주소를 32bit으로밖에 표현 못한다는 것이다.

### Registers & Memory

![registers](Gonnnnn.github.io/image/til/registers.png)

- 32개의 register들은 각기 다른 이름을 갖는다.
- 이 중 특정 register($zero 등..)들은 특정한 목적으로 밖에 사용할 수 없다. 어떤 것들은 프로그래머가 임의로 값을 쓰게 만들 수도 없다. 특정한 목적들은 이 후에 다시 다룬다!
- memory 크기를 2^30 words(=2^32 bytes)로 표현하기도 한다. words = 4Byte