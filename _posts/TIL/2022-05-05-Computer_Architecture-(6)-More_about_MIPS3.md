---
title: "Computer Architecture (6) More about MIPS 3"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

# More about MIPS

### Nested Procedures

- callee가 또 다른 function을 invoke 할 수 있다.
- $ra는 jal에 의해, $a0~3는 programmer에 의해 overwritten 될 것이다.
- **SPILL** 해야 한다!
    - ***caller에서는 $a0~3(최대 16bytes), $t0~9(최대 40bytes)를 spill***
    - ***callee에서는 $ra와 $s0~7(최대 32bytes)를 spill***
- preserved되거나 되지 않는 register들은 다음과 같다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c77c7e52-bfdf-4074-bd07-d36f43e135ea/Untitled.png)

### Allocating Space on the Stack

- callee는 $sp 기준 위쪽(주소가 더 작은쪽)을 사용한다. 그렇지 않으면 caller가 저장한 것들이 overlap될 것이기 때문이다.
- callee가 caller의 local variable에 마음대로 접근하는 것은 high level programming language에서도 허용되지 않는다. **function이 memory의 어느 부분에 접근하는지를 기억하기 위해 OS, compiler 수준에서 activation record라는 개념을 도입**한다.
- $fp (frame pointer) : memory address region을 제한하기 위해 사용된다.
    - frame의 first word를 가리킨다. frame이란 현재 function에 할당된 stack space이다.
    - local variable등에 접근하기 위한 base register 역할을 할 수 있다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/95ad699e-32c1-44f9-ae60-e60a0d86c983/Untitled.png)

→ function은 $fp보다 작고 $sp보다 큰 address에만 접근가능하도록 제한된다.

### Allocating Space on the Heap

- Stack
    - function에 관한 전반에 관련되어 있다.
    - **base address를 감소시킴으로써 추가 공간을 할당**할 수 있다.
- heap
    - application의 어떤 instruction이든 접근할 수 있는 공간이다. 주로 전역변수들이 저장된다.
    - **base address를 증가시킴으로써 추가 공간을 할당**할 수 있다.

### MIPS Register Conventions

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d6c9c166-de32-448c-b778-139a91283ec4/Untitled.png)

### MIPS Addressing

Address에 접근하는 다양한 방법이 있다.

### Addressing: 32-bit Imediates

잘 기억해보면 I-type instruction의 경우 16bit의 immediates를 위한 공간을 가지고 있다. memory address와 같이 16bit 이상의 값으로 표현되는 immediate를 다루려면 어떻게 해야할까? ‘lui’를 활용하는 것!

- lui (Load upper immediate)
    - upper 16bits를 register에 저장하는 operation이다.
    - 16진수 003D0900을 $s0에 저장하는 예시를 보자. 각 숫자는 16개의 값을 표현할 수 있으므로, 4bit로 표현된다. 즉, 위 숫자를 표현하기 위해서는 총 32bit가 필요한 것이다. 현재 $s0에는 0이 들어있다.
        - lui $s0, 61 → $s0에 003D0000을 저장한다.
        - ori $s0, $s0 2304(=0900(16)) → $s0에 0900이 추가로 저장되어 003D0900이 된다.
    - copiler, assembler들이 큰 constant의 경우 잘게 쪼개서 register에 넣어주는 역할을 담당한다.

### Addressing: Branches & Jumps

특정 address로 jump하기 위해서는 16bit의 여유공간(I-type에서 immediate등을 위해 존재했던 그것)으로는 부족하다. 그래서 **J-type instruction**이 존재한다. 오로지 jump instruction만이 이에 해당한다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3ed15423-c70e-4aae-8891-548f224fcaab/Untitled.png)

- Branch에 주로 이용되는 기존 I-type의 경우 0~2^16 - 1까지의 주소에 접근가능했다면, J-type은 ***0~2^26 - 1***까지 접근이 가능한 셈이다.

### PC(Program Counter)-Relative Addressing

bne 등의 instruction은 I-type이다. 조건이 맞으면 해당 주소로 이동하는 것인데, 이 역시도 16bit라는 제한된 크기를 잘 이용하면 좋을 것이다.

- 잘 생각해보면, branch의 경우 근처의 address로 이동하는 경우가 대부분이다.
- 따라서 어떠한 ***‘기준’***을 두고 거기서부터 2^16정도 만큼 떨어진 곳으로 이동하는 식으로 이를 사용하면, 충분히 branch 등을 위해 잘 사용할 수 있다.
- Programer Counter라는 개념을 도입한다.
***$pc + branch address(16bit)***
- ***$pc는 현재 instruction의 address를 담는다.*** 이 $pc의 값은 위와 같은 연산에서 base address가 되는 것이다. 다만 실제로는 하드웨어 디자인에 관련된 이유로 base address는 $pc+4가 된다고 한다. 나중에 조금 더 다룬다.
    - 또한, MIPS에서 모든 instruction은 4bytes의 크기를 갖는다. 주소 끝의 두자리가 항상 0인 것이 보장이 된다고 한다. 어쨋든 결국 이렇게 4bytes의 간격을 갖기 때문에, ***MIPS는 I-type의 16bit field를 word(4byte)로 받아들인다.***
    - 16bit field에 left shift를 두번하면 18bit로 표현되는 양의 주소를 표현할 수 있게 되는 것이다.
    - byte로 읽었을 때는 -2^15~2^15 - 1, word로 읽었을 때는 -2^17~2^17 - 4까지의 주소를 표현 가능하다.
    - ***결론적으로, $pc+4의 base addreess에, 16bit의 immediate에 left shift를 두번 한 것을 더해 target address를 계산하는 것이다.***
    
    J type instruction과 branch를 이용해 jump할 때 주소값을 연산하는 논리를 다이어그램으로 표현하면 다음과 같다.
    

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cd399a34-3255-47e0-a4a8-eff8f564e040/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8ff113c2-6d45-496e-bb78-b2d863392996/Untitled.png)

예시이다

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/daedef95-1d3b-4b05-a2e9-2c6159120ad2/Untitled.png)

- ******Loop 레이블이 메모리 주소 80000에 있다고 가정하자.
- bne $t0, $s5, Exit 에서 PC + 4가 80016이다. 여기에서 offset은 2이기 때문에 Exit의 주소, 즉 target address는 PC + 4 + offset x 4므로 80016 + 2 x 4 = 80024이다.
- j Loop 에서 address에 들어있는 주소는 20000이고 여기에 4를 곱하면 80000이다. PC의 상위 4비트는 0000이다. 따라서 Loop의 주소, 즉 target address는 PC의 상위 4비트를 가져오고 address x 4 므로 80000이다.