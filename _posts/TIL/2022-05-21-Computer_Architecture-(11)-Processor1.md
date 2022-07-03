---
title: "Computer Architecture (11) Processor 1"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# Processor

## 1. Processor

### Processor Microarchitecture

Processor 내부 구조. 이제 까지 다뤘던 아래와 같은 것들과 연관이 크다.

- CPI, ISA, Storage formats 등

같은 ISA를 따르면서도 내부 하드웨어 구조는 당연히 다를 수 있다.

여기서는 다음과 같은 9가지 instr을 수행가능한 processor를 implement하는 방법을 보도록 한다.

- Memory-reference instructions
    - lw, sw
- Arithmetic-logical instructions
    - add, sub, and, or, slt
- Jump/branch instructions
    - j, beq

### Two Types of Digital Circuits

Processor에는 2가지의 circuit이 들어간다.

- Combinational circuits
    - Arithmetic/logical operations(ALUs)
    - Output values depend only on the current inputs. 마치 함수와 같은거다.
- Sequential circuits
    - Storing values(registers)
    - Internal storage에 state를 저장한다.
    - Can make the states persistent through saving/restoring

### Datapath Implement

Datapath와 Control에 대해 다룰 것이다. 먼저 Datapath에 대해 다룬다.

Circuit의 Op, input, output에 관한 부분이다.

**Step 1 : Arithmetic Logic Unit**

- ALU부터 시작해보자. ALU는 arithmetic, logic operation을 수행한다.
- 얘는 combinational circuit으로 만들어진다. output은 input에만 의존한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0521(1).png)               

**Step 2 : Inputs/Outputs of the ALU**

- 위의 사진에서 register file, ALU, MUX 부분을 들여다보자.
- ALU는 register(rs, rt)로부터 데이터를 읽고, register(rd)에 다시 쓴다.
    - register-register op이면 source register로 2개를 받을거고, register-immediate op이면 1개를 받는다.
- 따라서 ALU를 만들고 Register File을 배치한다. 그 후 wire을 이용해 port에 이어주는 식
- ALU inupt단에 있는 Multiplexer(MUX)를 통해 immediate를 받을 것인지, register로부터 값을 가져올 것인지에 대한 것을 제어할 수 있다.
- 마찬가지로 ALU output도 register로 가기전에 MUX를 거친다. Arithmetic/Logical op의 경우 output이 그냥 register에 씌워지면되는데, memory에서 data를 load하는 경우에 저게 쓰인다. 아래에 더 자세한 설명이 이어진다.

**Step 3 : Data Memory**

- Data와 Instr을 위한 memory가 물리적으로 나뉘어져있는건 아니다. 여기서는 편의상 나눠서 설명한다.
- Data Memory에서 Data를 가져오기 위해서는 먼저 memory address를 계산해야한다. 그후 load, store 작업이 진행된다.
- Data load 작업을 생각해보자. lw $t2, 0x1000($t1)
    - rs : $t1, rt : $t2, imm : 0x1000으로 배정된다.
    - rs와 imm가 ALU를 거치며 output으로 address를 뱉어낸다.
    - 해당 주소에서 data를 가져와 rt에 씌우는데, 이 때 MUX를 거친다.
- Store 작업을 생각해보자. sw $t2, 0x1000($t1)
    - rs : $t1, rt : $t2, imm : 0x1000
    - Memory의 data를 register로 불러오는게 아니라 register의 데이터를 mermory에 저장하는 것이다. source register가 2개인 것.
    - rs와 imm가 ALU를 거치며 output으로 address를 뱉어낸다.
    - 해당 주소에 rt의 값을 저장한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0521(2).png)                   

**Step 4 : Instruction Memory**

- instr을 읽기 위해 $pc가 항상 target memory address를 추적하고 있다.
    - instr을 가져온 후, 4씩 증가하며 다음 instr을 가리킨다.

**Step 5 : Branch-If-Equal Instruction**

- 하지만 $pc의 값은 그냥 4씩 증가만 하는건 아니다. Branch가 있을 땐 다시 값이 재조정 될 필요가 있다.
- beq $rs, $rt, offset이면 $pc = ($pc + 4 ) + offset으로 갱신한다. 이를 위해 Adder와 Multiplexer이 사용된다.

### Control Implement

Control에 관한 부분에 대해 다룬다. ALU, MUX 등에 적절한 signal을 할당하는 것에 대한 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0521(3).png)                   

다 위에서 다뤘던 부분들을 참고해서 생각해보면 된다. Instr의 종류에 따라 MUX 등을 조절한다.

beq의 경우 ALU의 zero 부분과 관련이 있는데, 사실 이 때 rs, rt를 빼는 연산이 실행된다고 한다. 그게 zero이면 위의 AND 부분에 해당 신호가 들어가고, 또한 beq는 branch이기 때문에 control단에서 1이 들어간다. 따라서 1 & 1로 AND는 1을 출력하고, 그 때야 MUX에서 해당 address를 PC에 넣어주도록 하게 된다.

### Steps to Execute an Instruction

**Instruction Fetch (IF)**

- $pc에 담긴 주소에서 lw를 시행해 instr을 가져오고, $pc + 4의 값을 준비시켜놓는다.

**Instruction Decode (ID)**

- 가져온 instr을 parse한다.
- 가져온 instr에 따라 hardware unit들에 알맞은 signal을 보낸다.
- source register에서 값을 가져온다.
    - immediate를 input으로 받으면 rt에 접근할 필요도 없겠지. 최적화하려면 그게 맞는데 일단 학부 수준이니 접근하고, 필요 없으면 버린다는 쪽으로 쉽게 생각하라고 한다.

**Execute (Ex)**

- Instr에 따라 정해진 input이 ALU에 들어가 연산이 수행된다.

**Memory Access (MEM)**

- Memory에 접근해야 하는 instr일 경우 수행된다.
- Store이면 MemWrite = 1, MemRead = 0이 되고, Load면 그 반대가 된다.

**Writeback(WB)**

- ALU를 통과한 결과 혹은 Memory에서 가져온 data를 rd에 저장한다.

### Per-Instruction Execution Paths

- Arithmetic (add, sub, and, or, slt) instr
    - IF → ID → EX → WB. No MEM
- Memory-reference (lw, sw) instr
    - IF → ID → EX → MEM → WB
- Branch (j, beq) instr
    - IF → ID → EX → WB. No MEM
    - WB to the pc register