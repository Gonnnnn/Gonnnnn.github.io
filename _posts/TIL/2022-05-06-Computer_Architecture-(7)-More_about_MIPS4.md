---
title: "Computer Architecture (7) More about MIPS 4"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# More about MIPS

### MIPS Addressing Modes

32bit의 주소를 instruction에 다 담을 수 없으니 고안한 방법들. 그냥 앞의 것들을 정리한 것이다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7b087821-1275-4088-af91-3f99017a5ae9/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dff108e3-4a6f-4fb9-a181-662c613d808b/Untitled.png)

- Immediate
    - 최대 16bit의 immediate의 표현. 그 이상을 가지고 연산하려면 lui, ori 등 사용
- Register
    - Register의 값을 활용. 최대 32bit까지 표현
- Base/Displacement
    - 배열등의 값을 읽어올 때 사용하는 방법. Register의 값에 immediate를 더하여 새 주소를 표현
- PC-relative
    - PC에 immediate를 더해서 주소를 표현
    - Branch, loop으로 이동할 때 그렇게 멀리 떨어진 곳으로 가지 않는다는 가정하에 사용. Base/Displacement의 특별한 경우 정도
    - 16bit immediate를 2번 left shift해서 사용. address를 byte로 보지 않고 word 단위로 본다.
- Pseudodirect
    - J-type에 해당. PC에 immediate를 더해서 주소 표현
    - 이 역시 address를 word단위로 본다.
    - {PC[31:26], address[25:0]}로 jump한다.
    

### Decoding the Machine Language

CPU가 어떤 연산을 수행하려면 binary number로 표현되는 data와 instruction을 이해해야한다. Decode한다고 표현한다. 그 순서는 다음과 같다.

- Instruction의 첫 6bit field(op)를 확인한다.
- Format(R, I, J)를 확인한다.
- Format에 맞게 32bit를 field별로 나눈다.
- 각 field의 값을 계산한다.

위의 과정은 MIPS ISA manual을 기반으로 이루어진다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6bb294ed-0606-4465-99fe-79a6aef4757f/Untitled.png)

- op에 해당하는 부분이다. 첫 3bit(31~29번째 bit)는 row, 뒤 3bit(28~26번째 bit)는 col에 표현되어 있다.
- 000000과 같은 경우 R-format이라는 것만 확정된다. 아직 어떤 instruction인지 알 수 없는 것이다. 이렇게 여러 Instruction들이 op field 값을 공유하는 경우에는 funct field에 의해 확정된다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6276f206-1950-4303-a444-f0e355cf0664/Untitled.png)

- op에 따라 format이 정해지고, 그 format에 따라 봐야할 table이 다르다. 위는 op가 010000, 000000일 때 rs, func를 decode하기 위해 참고해야할 table이다. 보는 법은 같다.

Register의 경우 0~31로 표현된다. 그냥 binary number로 표현해주기만 하면 된다.

### MIPS Istruction Encoding

Assembly code를 Binary number로 변환하는 과정

# Supporting Parallelism

멀티코어의 시대이다. Parallelism에 대해서 ISA들이 잘 정의해줘야하는 것은 main memory의 data를 각 CPU core에 어떻게 잘 synchronize시키냐이다. 하나의 코어가 특정 주소의 data를 사용하던 중, 그 부분에 다른 코어가 data를 load할 수도 있는 것이다. 정말 복잡한게 많지만 여기서는 synchronization을 위한 instruction들을 배워볼 것이다.

### Parallelism & Data Races

- Parallelism을 통해 threads/processes를 병렬적으로 실행해 성능을 향상시킬 수 있다.
    - matrix 연산등의 경우 뭐 어떻게 병렬적으로 실행 가능하다고 하다.
- Data races
    - 서로 다른 두개 이상의 threads(CPU core 정도로만 생각하자 일단)에서 같은 memory 주소에 접근이 일어나며,
    - 그 중 하나이상은 write인 경우
    - ISA에 이런 경우 어떻게 해야하는지 명시되어야 한다.

### Lock & Unlock Synchronization

Data race를 방지할 수 있는 가장 간단한 방법 중 하나

- Data race를 만족하는 2가지 조건 중 첫번째인 “서로 다른 두개 이상”의 threads에서 접근하는 것을 방지한다.
- 이런 방식으로 data race를 방지하는 것을 “*mutual exclusion*”이라고 한다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9742fe28-cb96-4a05-9525-fafb4769760f/Untitled.png)

&mutex는 하나의 CPU core만이 lock할 수 있는 globally shared variable이다.

- processor1이 &mutex를 lock해버렸다고 하면 processor1이 unlock할 때까지 processor2는 이걸 lock할 수 없다. 그때까지 그냥 기다린다. 다만 프로그램을 여러번 돌리다보면 processor2가 먼저 lock하는 상황도 당연히 발생한다.
- 위의 시나리오의 경우 1 2 3 4의 순서대로 진행된다. Processor2가 먼저 lock했다면 결과는 21, 24이 될 것이다.

### MIPS: Atomic Instructions

- x86 ISA에서는 synchronization primitives들이 존재하고, 이를 통해 lock을 조절할 수 있다. ex) single atomic exchange/swap operations.라고 하는데 뭔지는 모른다.
- MIPS에서는 다른 instruction들을 이용해 Lock을 비슷하게 수행한다.
    - ll : Load linked
        - memory에서 register로 value를 load한다.
        - 해당 memory address에 reservation을 register한다. → 나중에 설명
    - sc : Store conditional
        - register의 value를 memory에 store한다
        - 성공하면 register의 value를 1로, 실패하면 0으로 바꾼다.

### MIPS: ll & sc Instructions

- ll에 의해 specified된 memory location의 value가 변경되었는지 여부에 따라 결과가 달라진다.
    - ll $t1, 0x1000으로 50의 값을 가져왔다고 하자.
    - 연산을 쭉 수행한 후 sc $t2, 0x1000을 했을 때, 0x1000의 값이 여전히 50이라면 $t2는 1을 받고 0x1000의 값을 갱신한다.
    - 그게 아니라면(다른 CPU core가 조작했다던지, 그런 이유로) $t2는 0을 받고 0x1000의 값을 갱신하지 않는다.

아래는 $s1에 저장된 address에 대한 atomic exchange operation을 수행하는 코드 예제이다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e0068996-fc0e-4150-b231-2e26dfccd6ac/Untitled.png)

- ll을 통해 $s1에 있는 값을 $t1으로 가져오고, sc를 통해 $s1에 $t0의 값을 저장하는 것을 시도한다. 실패하면 $t0에 0, 성공하면 1이 담긴다. $t0이 0이면 다시 again으로 이동하고, 그게 아닐 경우 $s4에 $t1의 값을 더한다.