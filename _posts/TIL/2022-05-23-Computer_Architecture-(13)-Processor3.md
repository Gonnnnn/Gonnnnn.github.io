---
title: "Computer Architecture (13) Processor 3"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

## Adding the Control Unit

- Datapath 혼자서는 할 수 있는게 없다. Configuration을 위해 Control unit이 필요하다.
- Control signals를 정의해서 각각의 datapath unit들이 해당 signal을 받을 때 특정한 동작을 수행하도록 한다.
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0523(1).png)       
    
- LW를 보면 load word instr임에도 불구하고 desired ALU action은 add임을 확인할 수 있다. 실제로 생각해보면, input register 안의 값에 imm << 2를 한 값을 더해준다는 것을 기억하자. 이러한 부분을 고려하여 Desired ALU action을 선정한다.
- 여기서는 ALU가 5개의 action만 수행하지만, 실제 모든 MIPS instr을 커버하려면 이를 표현하기 위해 우측 상단과 같이 4개의 bit는 필요하다.

### A Single-Cycle Processor

- Processor = Datapath + Control
- Control unit은 instruction의 op 부분을 input으로 받아 datapath의 각 요소들에 control signal을 줘야하므로, Instruction Decode 부분에 포함된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0523(2).png)           

- RegDst는 앞에서 들여다보지 않은거같은데, rt가 rd 대신 destination register로 쓰일 때가 있다. 그 때 알맞게 RegDst signal을 주게 된다.
- ALU control는 Control unit으로부터의 signal 외에도 R-type instr의 funct field를 받아드린다. 이 후 정확히 어떤 연산을 수행할지가 결정된다.
    - lw, sw 등의 instr에는 필요가 없을 것

### Control Signals for the Datapath

Control Signals에 대해 조금 더 자세히 봐보자

![Untitled](https://gonnnnn.github.io/image/TIL/0523(3).png)           

- ALUOp은 00, 01과 같은 signal로, ALU control이 어떤 op을 수행해야하는지, funct field를 확인해야하는지 등을 알려준다.
- RegDst
    - Register File 전의 MUX에 연결되어, rt가 destination register로 동작하는 특별한 경우를 가능케한다. I type instr의 경우가 그렇다. op - rs - rt - imm
    - addi의 경우 0, add의 경우 1이 신호로 들어간다.
- RegWrite
    - destination register에 데이터를 쓰는가에 관한 신호
    - add, addi 등은 1, sw 등은 0
- ALUSrc
    - rt와 imm중 어떠한 것이 input으로 들어가는지 결정
- PCSrc
    - PC + 4와 PC + 4 + (imm << 2) 중 PC에 들어갈 값을 결정
    - Control unit에서 바로 나온 신호를 지칭하는게 아니라, PC 레지스터에 연결된 MUX로 들어가기 전, AND gate를 지난 그 부분일 PCSrc라고 한다.
    - Branch(From Control Unit) && Zero(From ALU)
- MemRead, MemWrite
    - MemRead가 1일 경우 Memory에서 읽어오는 것, MemWrite가 1일 경우 Memory에 쓰는 것을 지칭
- MemtoReg
    - Data Memory 오른쪽의 MUX로 들어가는 신호. Memory에서 읽은 output과 ALU 연산 결과 중 어느 것이 register에 쓰여지는지를 결정하는 부분

### Example

- R-type instr
    - IF → ID → EX → WB
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0523(4).png)           
    
    - Add의 경우 Control Unit에서 나오는 signal들은 위부터 1, 0, 0, 0, 10, 0, 0, 1이 된다. 생각해보자. 쉽다.
    - PCSrc는 0이 될 것이고, ALU control은 ALUOp이 10이었으니 funct field를 읽은 후 적절한 4-bit를 뱉어낼 것이다.
- I-Type
    - IF → ID → EX → MEM → WB
        
        ![Untitled](https://gonnnnn.github.io/image/TIL/0523(5).png)           
        
    - lw의 경우 Control Signals : 0, 0, 1, 1, 00, 0, 1, 1
        - lw의 경우 target address 계산을 위해 addi가 실행되어야한다. 00을 받았는데 R-type과 다르게 funct field를 확인하지도 않고, 어떻게 이를 실행할까?라는 생각을 할 수 있다. 그냥 00받으면 addi가 실행되게 해놓으면 된다. ALU Control은 00을 받고 자동으로 0010을 뱉게 된다.
- Branch-If-Equal
    - IF → ID → EX → WB

![Untitled](https://gonnnnn.github.io/image/TIL/0523(6).png)           

- beq의 경우 Control Signals : 0(1이어도 된다. 상관이 전혀 없다. 뒤에 안쓰이는 부분들도 사실 signal이 의미 없다.), 1, 0, 0, 01(or 11. 정확하지는 않은데 어쨋든 sub), 0, 0, 0
    - ALU의 zero port는 rs = rt일 때 1, 아니면 0을 반환한다.
- PC updating 부분을 WB라고 하는 것은 정확하지 않지만, 그렇게 그냥 표현했다.

### Cons of Single-Cycle Processors

- Digital Circuit은 action을 trigger하는 positive event를 주기적으로 줘야한다. 따라서 Action은 가장 시간이 오래걸리는 instr시간을 기준으로 반복될 수 밖에 없다. Latency of single clock.
- 우리가 얘를 single-cycle이라고 하는 이유가 이거다. 매 cycle에 하나의 instr를 수행하기 때문. cycle 주기는 정해져있고, 당연히 가장 긴 놈을 중심으로 해야할 것. 이렇다 보면 비교적 짧은 시간에 수행될 수 있는 instr의 경우 한 cycle 동안 매우 빠르게 실행되고, 나머지 시간은 data path가 아무것도 안하게 된다.
- Solution : ***Pipelining***!