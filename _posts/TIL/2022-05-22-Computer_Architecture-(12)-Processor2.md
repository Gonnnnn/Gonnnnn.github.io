---
title: "Computer Architecture (12) Processor 2"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

## A Closer Look at the Processor

프로세서 하드웨어 디테일에 대해 알아보자

- ex) what is the width of an input port to a register file?

앞서 살펴봤던 9개의 instr만을 위한 하드웨어를 만든다고 가정하자

## Hardware for Fetching Instructions

![Untitled](https://gonnnnn.github.io/image/TIL/0522(1).png)       

- ***PC 레지스터***는 ***32bit unsigned*** number를 저장한다.
- ***Instruction memory***(실제로는 memory는 하나뿐)
    - 1 x 32-bit input port
        - target address를 받는다. address는 32bit
        - Instruction memory는 read only이므로 input port가 하나
    - 1 x 32-bit output port
        - 32bit instruction을 반환한다.
        - MIPS에서 모든 instruction은 32bit. 하나의 포트면 충분
- ***32-bit adder***
    - unsigned integer addition
    - imm 4는 32bit unsigned integer로 encode 되어 들어간다.

## Hardware for R-type Instructions

![Untitled](https://gonnnnn.github.io/image/TIL/0522(2).png)           

- R-type은 레지스터 두개로 값을 받아와 연산을 수행하는 instruction들
- Resigter File은 포트가 6개!
    - 3 x 5-bit input ports
        - 레지스터 indices 받기용. 레지스터가 32개라 5bit
    - 1 x 32-bit input port
        - rd 레지스터에 write할 값을 받는 포트. WB stage에 여기로 값이 들어올 것
    - 2 x 32-bit output ports
        - rs, rt 레지스터의 값을 읽어서 밖으로 빼주기 위한 포트
    - control port (input)
        - control signal을 받는다. sw이면 Write back을 할 필요 없다. 이 때 여기로 0이 들어온다. 그게 아니면 1
- 32-bit ALU
    - 2 x 32-bit input ports
    - 1 x 32-bit output port
    - 1-bit output port. branch instr를 위한 output port
    - 4-bit control port (input)
        - 어떤 operation을 수행해야하는지 알려주는 부분. 단순한 예로, Add를 해야하면 0001, Sub이면 0010.. 이런식

## Hardware for Loads & Stores

![Untitled](https://gonnnnn.github.io/image/TIL/0522(3).png)           

- lw, sw 모두 target address를 계산하고, register에 값을 저장하거나, register의 값을 memory에 올린다.
- Data memory
    - 2 x 32-bit input ports
        - target address와 store할 data를 받는 곳
    - 1 x 32-bit output port
        - load할 data를 반환하는 곳.
        - lw라서 32bit이지만, 다른 load instr이면 size가 다른 port를 추가로 만들 수도 있다. 하지만 이건 이해타산이 안맞아서 보통 32bit에서 필요한만큼 데이터를 채우고 나머지는 0으로 채우는 식으로 쓴다고 한다.
    - Control ports
        - Memory에서 data를 읽어올지(MemRead), memory에 data를 쓸지(MemWrite)에 대한 control signal을 주는 곳. 둘다 한번에 활성화되지는 않을 것
- Sign-extend unit
    - 16bit imm을 32bit으로 바꾸는 부분
    - lw, sw에서는 imm가 16bit였던 것을 기억하자. offset! 얘는 물론 음수일 수 있다.
    - signed 16bit을 signed 32bit으로 sign extend해준다. 음수면 앞을 1로 채우고, 양수면 0으로 채울 것

## Hardware for Branch Instructions

![Untitled](https://gonnnnn.github.io/image/TIL/0522(4).png)           

- Branch instr은 target address를 계산하는 부분과 두 레지스터의 값을 비교하는 부분으로 나뉜다.
- 두 register indices가 register file로 들어가고, imm(offset)은 sign-extend로 들어간다. 그 후 이는 shifter로 넘어간다.
- Shifter!
    - 레지스터의 값을 비교한 후, 조건이 맞을 경우 next PC = PC + 4 + (offset << 2)였던 것을 기억하자. offset을 shift하는 놈이다.
    - input, output은 모두 32-bit이다.
- Adder
    - Shifter의 output은 PC + 4과 함께 32-bit Adder로 들어간다.
    - output 역시 32bit. branch target address이다.
- ALU
    - beq의 경우 두 레지스터(rs, rt)의 값이 같으면 1, 아니면 0을 반환한다.
    - 1이면 위에서 나온 branch target address를 PC에 overwrite할 것

## A Single-Cycle “Datapath”

![Untitled](https://gonnnnn.github.io/image/TIL/0522(5).png)           

- 위와 같이 구성했을 경우, 한 싸이클 당 하나의 instr을 수행할 수 있게 된다.