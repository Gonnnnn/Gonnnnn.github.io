---
title: "Computer Architecture (5) More about MIPS 2"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# More about MIPS

### Conditional Branches

- 실행 순서를 바꾸는 instructions
- beq : Branch if equal
    - beq r1, r2, L1
    - r1과 r2에 저장된 value가 같으면 L1으로 label된 statement로 이동한다.
    - MIPS assembly programming language인 경우 L1은 ASCII code, MIPS binary machine language인 경우 L1은 memory address에 대응한다.
- bne : Branch if not equal
    - bne r1, r2, L1
    - r1과 r2에 저장된 value가 다르면 L1으로 label된 statement로 이동한다.

예시

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c0f45eb0-caf4-4ad9-b583-233ddb0c238f/Untitled.png)

### Loops

- beq, bne를 통해 loop 탈출 등을 결정할 수 있다. 근데 loop은 대소관계 비교같은 것도 필요한 경우가 많다.
- slt : Set on less than
    - slt rd, rs, rt
    - R-type이지만, rd에 source register의 값을 연산한 결과가 아니라, rs, rt의 대소관계 결과가 저장된다.
    - set rd = 1 if rs < rt, rd = 0 if rs ≥ rt
- slti : An immediate viersion of slt
    - slti rd, rs, const
    - set rd = 1 if rs < const, rd = 0 if rs ≥ const

### Case/Switch Statements

- Indirect branches 구현으로 해결! 아래는 high level description이다.
    - target address를 branceh(address) table에 저장한다
    - Switch문에 들어오는 val을 확인한다. if, else 논리를 사용해 계속 비교하다가 제대로 대응하는 경우가 발생하면, target address를 branch table에서 register로 load한다
    - jump register(jr) instruction을 사용해 target address로 뛰어넘는다!

### Supporting Procedures/Functions

Function이 실행되면, control(flow? logic?정도로 받아들이면 될 것 같다. 지금 실행중인, 따라가는 그 logic)을 거기로 옮겨가야하고, 또 input이 요구되는 경우 data도 가져가야 하고, 또 함수가 종료되면 원래 위치로 돌아와야하며 return하는 값이 있으면 그것도 가져와야한다. 따라서 hw 입장에서 생각해보면 function을 실행하기 꽤 어렵다.

1) Register allocation convention for functions

- a0~a3 : caller function에서 callee function으로 parameter를 넘겨주기 위한 argument registers
- v0~v1 : value를 return하기 위한 value registers
- ra : origin(caller function에서 읽고 있던 부분) address를 저장하기 위한 return address register

2) Instructions

- jal : Jump-and-link
    - jal ProcedureAddress
    - ProcedureAddress로 jump하고 ra에 return address를 저장한다. Return address는 현재 address + 4이다. MIPS instruction은 4byte이기 때문에, 다음 instruction의 address는 현재보다 4bit만큼 크기 때문이다.
    ** memory에서 주소는 bit로 표현되고, 각 주소는 1byte 크기의 공간을 갖고 있음을 잊지말자
- jr : Jump register
    - jr $ra
    - ra register에 저장된 address로 jump한다.

3) How to invoke a callee function from a caller function

- caller : a0~a3에 파라미터를 저장한다.
- caller : jal [callee]를 통해 callee로 넘어간다. 이 때 $ra에는 현재 address + 4가 담긴다.
- callee : 연산을 수행하고, v0~v1에 return 값을 저장한다.
- callee : jr $ra를 통해 다시 돌아온다.

4) Program Counter (PC) register

- $pc는 현재 instruction의 memory address를 저장한다.
- jal에서 $ra에 다음 instr의 address를 저장할 때 쓰인다.
- address를 저장하기 때문에 $pc의 granularity는 byte이다.
- $ra = $pc + 4 인 것

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ee6a006e-e99e-4c50-a10f-0c84d8076527/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/24f5108c-8970-4951-84ad-92823eaf0255/Untitled.png)

간단한 예시이다. pc, ra, a0, a1, v0에 어떤 값이 들어가게 될지 생각하며 한줄 씩 읽어내려가보자.

** jr $ra의 경우 $pc에 $ra값을 overwrite한다고 한다.

** jal addTwoSums로 썼지만, MIPS binary machine code일 때는 jal 0x1000이  들어가야한다.

### What if we need more registers?

argument registers 4개는 너무 적잖아!

- Use a ***stack*** to spill registers!!!
    - **argument가 4개가 넘어가면, argument register 대신, memory의 잉여공간을 활용한다**.
    - 여기에 value들을 stack 형태로 저장(push)하고, callee를 부른다. callee는 여기서 value를 빼(pop)와 register에 저장해 사용한다. 한번에 다 빼올 수도 있고, 절반을 빼온 후 연산하고 또 절반을 뺄 수도 있는 등, 순서는 다양하다.
    - stack이 queue보다 memory 관리에 더 flexible하기에 쓴다고 한다. (OS를 공부하면 배운다고)
    - s**tack의 address는 $sp로 추적한다**. stack의 가장 윗(가장 마지막으로 allocated된) 부분의 address를 저장한다. stack에 아무것도 없을 때는 가장 밑단의 address를 저장하고 있다.
        - stack은 higher address부터 lower address로 쌓아진다.
        - decrement $sp when pushing/spilling a register to the stack
        - increment $sp when popping/restoring a register from the stack
        - ex) 16개의 int형(4byte) 변수들을 넘겨준다고 하면 $sp에서 16*4를 빼서 16*4byte만큼의 공간을 먼저 allocate한다. 그 후 값들을 이 공간에 저장한다. 그 후 $sp의 값을 callee에게 전달하고 callee는 이 값을 base address로 사용하며 stack내의 value들에 접근한다. 연산 후 다시 control이 caller로 돌아왔을 때 caller단에서 $sp의 값을 다시 늘려 제자리로 돌려놓는다.
        

### MIPS: Register Spilling

다음과 같은 register을 추가로 배워보자!

- **$t0~t9** : **temporary register**. function call이 불렸을 때 값이 보존되지 않을 수 있다. callee function에 의해 바뀔 수도 있기에 **caller단에서 jal instr을 실행하기 전에 먼저 값을 memory나 saved register에 저장해놔야한다**.
- **$s0~s7** : **saved register**. function call이 불린 후에도 값이 보존된다. callee function에 의해 바뀌지 않는다.
    
    

### Spilling Registers with a stack

**참고! $sp는 하나의 프로그램 내에서는 공유된다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9912a8cc-4df9-48d0-8186-6c5ccb2e23ab/Untitled.png)

- **$t는 $s보다 2개가 많기에** 모든 값을 $s에 backup할 수 없다. 이 때는 **$sp를 조정해가며 memory에 register을 spill**한다.
- callee가 또 다른 function을 call할 수 있다. **A가 B를 불렀고 B가 C를 부른다**고 하자. B에서 몇개의 값을 $s에 backup해놓느냐에 따라 A가 $s에 저장해놓은 값이 사라지는 경우가 발생할 수 있는데, 그럴 때 위와 같이 **A가 $s에 저장해둔 값을 memory에 추가로 backup해놓는다. 이는 B단에서 이루어져야 한다.**

아래 예시로 모든 것을 정리할 수 있다.

![1. 0x1ffC에서 시작. $t들에 값이 담겨있고, $sp는 초기 상태이다.](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6795fc99-05cf-432d-a64a-d55a30b724b2/Untitled.png)

1. 0x1ffC에서 시작. $t들에 값이 담겨있고, $sp는 초기 상태이다.

![3. $a에 parameter들을 저장하고, jal을 통해 $ra에 PC+4의 값을 저장한 후, callee를 부른다. ](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/af1c958d-6540-44c9-a69c-243d2f1f36d5/Untitled.png)

3. $a에 parameter들을 저장하고, jal을 통해 $ra에 PC+4의 값을 저장한 후, callee를 부른다. 

![5. stack의 값들을 $t로 다시 가져오고, $sp를 원상태로 돌려놓는다. 끝!](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/eaacfaa9-b162-40a4-94ca-e105ca391492/Untitled.png)

5. stack의 값들을 $t로 다시 가져오고, $sp를 원상태로 돌려놓는다. 끝!

![2. $t값들을 보존하기 위해 callee를 부르기 전에 memory에 stack을 allocate한 후 값들을 저장한다.](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9af71c5d-82b0-4cce-839f-3443856e6b64/Untitled.png)

2. $t값들을 보존하기 위해 callee를 부르기 전에 memory에 stack을 allocate한 후 값들을 저장한다.

![4. $t의 값들이 callee들에 의해 바뀐 것을 볼 수 있다.](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/93071d8f-3191-4798-9c37-60f53a552343/Untitled.png)

4. $t의 값들이 callee들에 의해 바뀐 것을 볼 수 있다.