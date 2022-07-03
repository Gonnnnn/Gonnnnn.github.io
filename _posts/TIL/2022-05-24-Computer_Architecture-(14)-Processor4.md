---
title: "Computer Architecture (14) Processor 4"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

## Pipelining

### Pipelining

- 여러개의 instruction이 중첩되어 실행될 수 있게 한다. 최근 프로세서 들은 모두 적용된다.
- 빨래를 예로 들어보자. 빨래 과정(1pile)은 세탁기-건조기-빨래접기-옷장에넣기 와 같은 4개의 stage로 이루어져있다. 각각 1시간이 걸린다고 했을 때 이 과정을 단순히 4회 반복하면 총 4*4 = 16시간이 걸린다.
- 하지만 세탁기를 돌리는 동안 이미 세탁한 옷을 건조기에 넣고 돌릴 수도 있고, 이미 건조된 옷은 건조기를 돌리는 동안 정리하고 있을 수 있다. ***다른 stage에 있는 서로 독립적인 task끼리는 영향을 받지 않고 같은 시간에 수행 가능한 것이다.***
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0524(1).png)                       
    
    - ***다만 이런 경우 throughput은 개선되지만, latency는 그렇지 못한다.***
    - 위 경우 잘 중첩하면  모든 과정이 7시간만에 끝난다. 0.25piles/h에서 0.57piles/h로 throughput은 증가하지만, latency는 여전히 4hours/pile이다.

### Can Instructions Be Pipelined?

- Instr의 실행은 IF - ID - EX - MEM - WB으로 이루어져 있었음을 기억하자
- ID와 WB는 모두 Register File을 사용한다. 서로 독립적이지 않아보이지만, 한 cycle에서 앞쪽 절반은 WB단계에서 RF를 사용하고, 뒤쪽 절반은 ID단계에서 RF를 사용하는 식으로 구현하여 서로 영향을 미치지 않도록 한다고 한다.
- IF, EX, MEM 단계에서는 겹치는 하드웨어들이 없다. 이 단계들은 cycle 전체에 걸쳐 이루어져도 무방하다.

### Benefits of Pipelining

- 모든 stage들이 perfectly balanced하다면, 즉 모든 stage들이 각각의 수행 시간이 같다면, 즉 latency가 같다면 benefit이 최대화된다.
    - Latency가 같을 때 expected benefit은
    $Time BtwInstrs_{Pipelined} = TimeBtwInstrs_{NonPipelined}/NumPipeStages$
    - 이 경우 cycle마다 하나의 instr를 initiate하게 된다. → IPC = 1(instr/cycle)
        - 당연하다. stage 하나가 끝나면 바로 다음 instr를 실행할 수 있게 되기 때문. 되게 optimal한 경우라고 한다.
- 모든 stage의 시간이 같다면 overlap 딱 맞게 된다! 그렇지 않은 경우를 보자.
    - A1A2B1[공백]
             A1A2B1
    - A가 2t초, B가 t초가 걸리는 (A-B) instr이 있다고 하자. A시행 후 B를 시행하며 그 다음 instr의 A를 바로 시행할 수 있지만, 이 두번째 A가 끝나기전에 첫번째 B가 끝나고, B에 공백 시간이 생긴다.
- 아래와 같은 latency를 상정하고, 실제 throughput 개선이 일어나는지 확인해보자
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0524(2).png)                           
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0524(3).png)                           
    
    - Non-Pipelined : 3 instr / 2400 ps = 1 / 800 (instr/ps). 명령어 사이의 평균 시간 = 800ps
    - Pipelined : 3 instr / 1300 ps (교수님은 1400ps라고 하셨다.) 명령어 사이의 평균 시간 = 200ps
        - stage들을 독립적으로 만들기 위해 공백 시간을 IF, WB뒤에 100ps씩 넣으며 오히려 single instr execution latency가 증가했다. 하지만 이건 pipelining의 목적이 아니다. 일단 throughput은 증가했다!!

### Implementing Pipelining

![Untitled](https://gonnnnn.github.io/image/TIL/0524(4).png)                           

- 첫번째 instr의 CC2(ID)를 주목해보자. Register File의 resource conflict를 방지하기 위해 cycle의 후반부에 RF에 접근하는 것을 확인할 수 있다.
    - Negative Edge를 detect하면 initiate하도록 설계된 것이다.
- 첫번째 instr의 CC1이 끝나며 IF stage가 끝나자마자 IM(Instr Memory)가 idle한 상태가 된다. 따라서 두번째 instr이 CC2에서 바로 시작하는 것을 볼 수 있다.
- 참고로 IF에서 positive edge일 때 PC를 update하고, negative edge일 때 PC값을 읽어들인 후 instr을 가져온다.

![Untitled](https://gonnnnn.github.io/image/TIL/0524(5).png)                           

Single Cycle Processor을 5개의 stage로 구분하여 나누면 다음과 같다.

- IF
    - PC에 들어있는 주소에 접근하여 IM로부터 instr를 가져와야 한다.
    - 또한, pipelining하려면 해당 단계가 끝나자마자 또 다시 실행되어 다음 instr를 가져와야한다. 따라서 PC값을 바로 update시킬 수 있도록 Adder또한 IF단계에 포함시켜놓는다.
    - PC, IM, Adder
- ID
    - Instr를 split해서 register, imm 등을 구분하고, register indices를 참고해서 그 안의 값을 가져와야한다.
    - RF, sign-extender
- EX
    - Arithmetic, Logical op 수행. Branch instr이면 barnching condition이 맞는지 아닌지를 판단하고 ALU에서 zero를 뱉어내는 것까지 EX 단계에 포함된다. 조건이 맞다면 PC를 다르게 업데이트해야할 것이고 이를 위해 Adder도 여기에 포함
        - 잘 생각해보면, branch instr의 IF단계가 끝나면, 이미 다음 instr의 IF 단계가 시작될 것이다. 하지만 branching condition은 다음 instr의 IF단계보다 늦게 시작되므로, 논리에 맞지 않게 된다. 이 부분에 대해서는 후에 다시 알아볼 것이다!
    - ALU, Adder, MUX
- MEM
    - DM에 접근해 값을 쓰거나, 값을 가져온다.
    - DM
- WB
    - RF로 값을 보내 destination register에 값을 쓰게 한다.
    - MUX, RF

Latch라는 것이 등장했다.

- Latch는 두개의 연속된 pipeline stage 사이에 존재하며, 데이터의 임시 저장 장소 정도로 생각하면 된다.
    - 첫번째 instr의 IF가 실행된 후, latch에 값을 저장시킨다.
    - 첫번째 instr의 ID가 실행됨과 동시에, 두번째 instr의 IF가 실행된다. 첫번째 instr의 ID가 실행될 때 IF/ID latch에서 값을 가져온다.
    - 각각의 stage가 끝나며 각각의 다음 latch에 값을 저장시킨다.
- 각 stage마다 latency가 달라서 바로 바로 데이터를 전달하지는 못할 수 있다. 이를 위해 임시 저장시켜놓는 것이다.

### Executing lw, sw on the Pipeline

1. lw

![Untitled](https://gonnnnn.github.io/image/TIL/0524(6).png)                           

IF

- PC에 해당하는 메모리의 주소에 접근하여 instr을 가져온다. PC 값은 4만큼 증가시킨다
- Instr과 PC+4값은 IF/ID latch에 저장한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0524(7).png)                           

ID

- IF/ID latch에 저장된 instr과 PC+4값을 가져온다. Instr은 parsing하고, PC+4값은 그대로 ID/EX latch로 바로 보낸다.
- 해당 예시는 lw instr기준임을 기억하자. Parsing한 값으로부터 target register들을 찾아 그 안의 값을 가져오고, imm값을 sign-extend한 후, ID/EX latch에 저장한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0524(8).png)                           

EX

- ID/EX latch에서 rs와 imm을 가져와 Add연산을 수행, Data memory address를 계산한다.
- Data memory address, rt, PC+4+imm, ALU의 zero port output은 EX/MEM latch에 저장된다.
    - lw의 경우 rt값과 PC+4+imm값, ALU의 zero port output 또한 읽어와지거나 계산되어 EX/MEM latch에 저장되지만, lw instr이므로 사용되지는 않을 것이다.
    - 교재에서는 rt값이 latch로 넘어가지는 않는다고 한다. 넘어가도 상관은 없지만. 이건 디자인하기 나름인듯

![Untitled](https://gonnnnn.github.io/image/TIL/0524(9).png)                           

MEM

- EX/MEM latch에서 data memory address를 가져와 해당 address의 값(32-bit data)을 읽는다.
- 32-bit data, ALU output을 MEM/WB latch에 저장한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0524(10).png)                          

WB

- MEM/WB latch에서 32-bit data를 가져와 destination register에 data를 저장한다.

1. sw

IF, ID, EX 부분은 lw와 동일

![Untitled](https://gonnnnn.github.io/image/TIL/0524(11).png)                           

MEM

- EX/MEM latch로부터 target memory address와 rt값을 가져온다. address에 rt값을 저장한다.

WB

- 아무것도 하지 않는다.

### A Closer Look at the Pipeline

![Untitled](https://gonnnnn.github.io/image/TIL/0524(12).png)                           

![Untitled](https://gonnnnn.github.io/image/TIL/0524(13).png)                           

5개의 instr를 실행하는 것을 HW와 함께 도식화 한 것이다. CC 5에서 각 stage마다 실행되는 instr은 두번째 그림과 같다.

### Adding the Control Signals

Control Signals를 추가해보자.

![Untitled](https://gonnnnn.github.io/image/TIL/0524(14).png)                           

- Control unit은 instr의 op 부분을 필요로 한다. 이는 ID 부분에서만 얻을 수 있으므로, Control unit은 ID에 속하게 된다.
- RegWrite은 ID 단계에서 바로 전달해도 될 것처럼 보이지만, 사실 잘 생각해보면 얘는 WB 단계에서 보내져야 한다. 이 외에도 다른 signal들도 마찬가지로 보내져야 하는 단계가 있다. 따라서 Control Signal들을 다음 단계로 넘기기 위한 방법이 필요하며, latch를 사용한다.
- Latch에 저장할 때, 각 signal들을 쓰이는 stage에 맞게 그룹화한 후, 해당 단계에 도달할 때까지만 넘겨준다.

### Pipeline Hazard

- Pipelining했을 때 이상적으로는 IPC가 1이되어야한다.
- 하지만 hazards에 의해 pipelining이 stall하는 경우가 생긴다.
    - hazard : the situations which incur pipeline stalls
    - stalls : the clock cycles which a pipeline stage cannot execute the next instr

### Three Types of Pipeline Hazard

학부 수준에서 확인할만한 Hazard들

- Structual hazard
    - 제한된 hardware에 의해 stall이 발생하는 경우
    - 임의로 IM, DM을 나눴지만 실제로는 모두 같은 하나의 memory이다. conflict 발생 가능. 새 instr의 IF 단계 혹은 MEM 단계가 1 clocky cycle만큼 딜레이 되어야 할 것이다.
- Data hazard (Read-After-Write dependency)
    - 하나의 stage가 다른 stage로부터의 결과를 기다려야할 때 발생
    - add $t2, $t0, $t1 → sub $t4, $t2, $t3인 경우 $t2의 값이 구해져야할 때까지 기다려야할 것
    - 이 경우 add instr의 WB부분과 sub instr의 ID 부분이 겹치게 만들어야할 것이다.
- Control hazard
    - Execution/control flow가 바뀔 때 발생
    - Branch instr에 의해 nextPC가 currPC+4가 아니게 될 때