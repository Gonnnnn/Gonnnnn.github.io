---
title: "Computer Architecture (4) More about MIPS"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# More about MIPS

### Data Placement

1B가 넘어가는 양의 Data를 배치하는 방법

0x111001로 표현되는 data를 저장한다고 하자. hexadecimal 이기에 하나의 숫자는 4bit(=2^4개 숫자)으로 표현될 수 있고, 2개의 숫자는 8bit, 즉 1byte로 표현 가능하다.

- Big-Endian
    - Most-Significant Byte(MSB)를 먼저 배치한다 → 11 10 01
- Little-Endian
    - Least-Significant Byte(LSB)를 먼저 배치한다 → 01 10 11

많은 ISAs는 little-endian만을 지원한다.

- 많은 경우에 이게 더 낫기 때문이라고 한다.
- Big endian의 경우 target memory address를 계산하는데 복잡함이 있다고 한다.

### Two Key Principles

- Instructions는 numbers(Binary)로 표현된다.
    - ASCII code를 따르는 String등을 Binary number로 전환하는 규칙(format)이 있다. 이를 따라 전환된다.
- Stored-program concept
    - MIPS ISA에서는 instruction과 data를 모두 main memory에 저장한다.
    - CPU core가 Instruction을 읽을 때, register을 거치는 과정을 생략한다.
    - Text editor같은걸 켜면, instruction이 binary number로 compiler 등에 의해 MIPS ISA에 따라 변환되어 memory에 올라간다. 그리고 여기에 CPU core가 접근하는 것.

![파란색은 binary number로 표현되는 machine instruction, 빨간색은 data를 나타낸다.](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled.png)

파란색은 binary number로 표현되는 machine instruction, 빨간색은 data를 나타낸다.

### Design Principles

- Simplicity favors regularity
    - arithmetic/logic instruction들의 형식이 다 같다. 항상 3개의 operands를 가져와서 연산한다. 나중에 무슨말인지 더 이해가 잘 될 것
- Smaller is faster
    - 당시의 하드웨어 technology를 고려하여 최적으로 고려된 것이라고 한다. 나중에 설명된다고 한다.
- Good design demands good compromises
    - 모든 소프트웨어, 하드웨어를 동시에 고려하는 그런 solution은 없다!
    - add라는 insturction을 잘 설계하면 16bits로 표현할 수 있다고 치자. MIPS ISA는 그럼에도 불구하고 이를 32bits로 정하기도 한다. 편의를 위해 모든 instruction의 길이(size)를 하나로 정하기 때문이다. → 임베디드의 경우 단점으로 작용할 수 있다는 것!
    

### Instructions

- Arithmetic Instructions
    - Register를 이용하여 arithmetic operation을 수행한다.
    - Two input operands : either a register or an immediate
        - 변수와 변수를 더하는 경우는 register에서 값을 가져오지만 a = a + 1과 같이 상수를 더하는 경우는 다르다. 이런 상수를 immediate value라고 하며, 이런 경우 다른 add 연산을 수행한다.
    - One output operand
- Data transfer instructions
    - Register와 memory 사이에서 data를 옮긴다.
    - address도 필요하지만 data의 size가 필수적으로 필요하다.
        - 8bit의 크기를 갖는 integer을 연산한다고 하면, 4byte 크기의 register에서 8bit에만 저 정보가 할당되고 나머지 3byte의 경우 invalid한 정보들이 담겨있을 수 있다. 애초에 8bit만 가지고 놀려고 할당을 했었으니 말이다. 그런데 size 정보가 없으면 register의 4byte 정보를 모두 memory로 다시 넘겨야할 것이고, invaid한 정보가 함께 넘어갈 것이다.

### Arithmetic Instructions

- 하나의 op과 3개의 variables로 이루어져있다.
    - ex) add t0, t1, t2. t1, t2 : input, t0 : output
- constant가 input operand로 들어올 수도 있다. addi의 3번째 operand로 immediate가 들어온다.
    - ex) addi t0, t1, 20 → t0 = t1 + 20

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%201.png)

### Data Transfer Instructions

32개의 register보다 더 큰 크기를 갖는 array등은 어떻게 access할 수 있을가?

- 두 개의 register(t0, t1)에 idx와 array[idx](value)를 각각 저장하는 방식으로 접근한다.

좀 더 정확히, data transfer instruction이 어떻게 이루어지는지 들여다보자

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%202.png)

→ lw t1, 0x40(t0) 의 예시이다.

- data의 size, offset과 base register, destination register가 필요하다.
- 먼저 op을 통해 transfer하고자 하는 data의 size를 명시한다. 위의 경우 op은 lw인데, load a word의 약자로, 4bytes의 data를 memory에서 register로 load하라는 뜻이다.
- t1은 destination register로, output이 저장될 곳이다.
- 0x40은 offset, t0은 base register이다. base register에 저장된 주소 값에 offset을 더한 값에서 시작하여 op에서 정의한 크기만큼 data를 긁어온다. 위의 예시의 경우 base register에 0x1000이 저장되어있었기에 0x1000 + 0x40 = 0x1040에서부터 word(4bytes)만큼의 data를 긁어온다.

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%203.png)

이렇게 다양한 op들이 있다. 간단히 들여다보자.

- store의 경우 operands들이 load와 같게 들어오지만, destination register에 있는 값을 해당 address에 저장하는 작업을 수행한다.
- op에는 size에 대한 힌트도 들어있지만, 해당 data를 어떻게 볼것이냐(signed or unsigned)에 대한 것도 있다.
- load linked word, store condition word는 특별한 경우를 위해 쓰인다. 나중에 소개된다.

### Instruction Format

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%204.png)

Memory에서 instruction이 표현되는 layout 정도로 생각하면 된다.

위와 같이 MIPS ISA에서 instructions는 32bits로 표현되며 fields로 구성된다.

- op : opcode; operation. add, sub 등
- rs, rt : 1st, 2nd register source operands. 32개의 register을 표현하기 위해 5bits
- rd : destination operand
- shamt : shift amount. conditional branch, shift instruction등에 사용된다. 나중에 알게된다!
- funct : function; selects the specific variant of the op. 나중에!

예시

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%205.png)

add $t0, $s2, $t0를 예로 들어보자. op rd rs rt로 구성된다.

이는 000000 10010 01000 01000 00000 100000이 된다.

why??!!@# 위 테이블의 첫번째 행을 보자.

add의 경우 op은 0, shmat은 0, funct는 32의 값을 갖는다고 한다.

따라서 000000(op) rs rt rd 00000(shamt) 100000(funct)와 같이 변환되며, 각 register의 index를 고려해주면 위의 결과가 나오게 된다.

### MIPS: Instruction Types - R, I Type

각 Instruction들은 다른 format을 갖고 있다.

R-type

TWO source registers & ONE destination register

- ex) add

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%206.png)

I-type

ONE source register, ONE destination register, ONE immediate

- rd가 없다. rt가 destination을 나타낸다.
- constant immediate, address 등은 arithmetic op이나 conditional branch 등에 쓰인다.
- ex) addi

![Untitled](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%207.png)

### Logical Operations

- Shift - sll(shift left logical), sr(right)l
    - doubleword내의 모든 bit을 지정한만큼 shift한다. 빈 bit은 0으로 채워넣는다.
    - I-type. ***multiply, devide 할 때*** 많이 쓴다.
    - ex) sll x11, x19, 4 ← x11 = x19 << 4bits
    x19가 ...00001111이었다면, x11은 ...000011110000이 될 것
    - 근데 ***format은 R-type***을 쓴다. **rt, rd를 통해 source, destination**을 나타내주고, **shamt에 shift할 bit수**를 적는다.
    
    ![sll $t2, $s0, 4](3%2024,%2029%2098448c0eeae344d897eed0fc162e9412/Untitled%208.png)
    
    sll $t2, $s0, 4
    
- Bitwise/Bit-by-bit operations
    - and, andi : bitwise logical AND
        - I-type. Instruction에서 field를 분리할 때 유용하다.
        - 가령 instruction & **111111**00...00을 수행하면 op 부분의 bit만 추출될 것!
    - or, ori : bitwise logical OR
    - nor : bitwise logical NOT

### MIPS: Representing Text

- MIPS는 ASCII characters 지원
    - 0~127. 8bits = 1byte. 각각의 character은 memory에서 1byte의 크기를 차지한다.

### MIPS: Text Processing

- Text processing은 Byte-by-byte의 operations들 밖에 없다.
    - Character하나가 1byte를 잡아먹으니 당연한 소리다.
    - 예로 string에서 character 개수를 세거나(len) C statement를 parse하는 등의 작업 등이 있겠다.
- lb : Load byte
    - ex) lb $t0, 0($sp)
    - 메모리 주소 $sp+0에서 1byte만큼 data를 읽고, $t0의 rightmost 8bits에 저장한다.
    - MIPS ISA가 제공하는 load instruction중 가장 작은 단위를 load한다. 메모리 주소 각각은 1byte의 저장공간을 갖기 때문이다.
    - Load word instruction도 이전에 봤다. 얘는 4 byte를 load한다.
- sb : Store byte
    - ex) sb $t0, 0($gp)
    - $t0의 rightmost 8bits를 가져와서 메모리 주소 $gp+0에 저장한다.