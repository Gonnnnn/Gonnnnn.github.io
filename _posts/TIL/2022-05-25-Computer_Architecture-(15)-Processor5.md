---
title: "Computer Architecture (15) Processor 5"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

### Data Hazard

- 이전 instr의 output에 다음 instr의 연산이 영향을 받으므로, 이전 instr이 끝날때까지 기다려야한다.
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0525(1).png)              
    
- 위 상황은 add $t2, $t0, $t1 → sub $t4, $t2, $t3이다. $t2에 data dependency가 발생한 것이다.
- 위와 같이 instr 실행을 미루기 위해 bubble이라는 것을 추가한다. operation이 일어나지 않는(no-operation) cycle을 의미한다. add $zero, $zero, $zero와 같은 것을 사용하기도 한다.
- 그림이 조금 잘못됐다. bubble은 두개만 필요하고 이 경우 add의 WB과 sub의 ID가 정렬된다. 해당 cycle의 첫번째 절반(pos edge)에 WB이 진행되고, 두번째 절반(neg edge)에 ID가 진행되므로 성립 가능하다.

### Resolving Data Hazard

Structural Hazard는 대학원 과정에서 보고, 여기서는 Data, Control Hazard를 보자

- Bubble을 추가하면 PVS에 영향을 주지 않는 instr을 추가하는 것이기에 시간이 지연된다. 당연히 performance 저하를 야기한다.
    - IPC가 1이 되지 않는 것
- Data forwarding (a.k.a data bypassing)
    
    ![Untitled](https://gonnnnn.github.io/image/TIL/0525(2).png)                  
    
    - Add extra hardware to retrieve the missing item early from the internal resources.
    - ***Bubble을 추가할 필요 없이, 계산된 data를 미리 다음 instr에서 사용할 수 있도록 하는 하드웨어를 추가해서 Data Hazard를 해결하는 방법을 data forwarding이라고 한다.***
        - Internal resources는 latch를 의미한다. missing item은 여기서는 $t2의 값이 되겠다.
    - add instr의 EX 단에서 $t2에 들어갈 값은 이미 계산된다. $t2에 저장되기 전에 이미 값은 계산되어있기에, 사용할 수 있다.
    - ***전 단계의 instr의 EX단에서 계산된 것이 다음 단계의 instr의 EX단에서 바로 쓰일 수 있는 경우, bubble을 추가할 필요가 없는 것***

### We Still Need Bubbles tho :(

***Load-Use data hazard***

워낙에 유명한 constraint라 이름도 있다.

- lw로 가져온 data가 다음 instr의 EX단계에서 쓰일 때

![Untitled](https://gonnnnn.github.io/image/TIL/0525(3).png)                  

- lw $1, 0($2) → sub $4, $1, $5를 예시로 들어보자
- 위 경우 Bubble이 없다면 애초에 계산도 안된 값을 sub instr에서 써야하는 상황이 온다.
- 시간을 역행하는건 당연히 안된다. destination stage가 source stage보다 먼저 발생하는 경우는 bubble이 필요하다.
- sub-lw 순으로 실행하며, lw의 register가 sub에 의존한다고 했을 때, 이 때는 bubble이 필요 없을 것이다. 이 전 예시와 같은 경우이다.

** 추가

- $1에 data를 load하는 lw 후에 bubble 없이 $1의 data를 store하는 sw가 온다고 하자. 이 경우 lw의 MEM 단계 후 $1에 data load를 마치기 전에 sw의 ID와 EX가 불리는 것은 맞지만, sw의 MEM단계가 lw의 MEM단계보다 늦게 온다는 사실에 주목해보자. lw의 MEM단계가 끝난 직후 $1에 저장될 값을 sw의 MEM단계에서 바로 쓸 수 있기에 bubble이 필요 없다.
    - ***Load-Use data hazard는 lw에 의해 load하는 data가 다음 instr의 EX단계에서 쓰일 때 발생하는 것! 이처럼 MEM단계에서 쓰이는 경우는 bubble이 필요 없는 것이다.***
- 이렇게 register 의존관계를 살펴보고, bubble을 넣어주는 것을 compiler가 한다.

### Data Forwarding in Hardware

![Untitled](https://gonnnnn.github.io/image/TIL/0525(4).png)                  

위와 같은 instr들에 대해 pipeline을 만들어보자

예시를 단순화하기 위해 EX stage에서의 data forwarding만을 이용해보자

![Untitled](https://gonnnnn.github.io/image/TIL/0525(5).png)                  

- and instr의 $2는 이전 sub instr의 결과에 의존한다. sub의 EX단 결과를 가져올 필요가 있다. ***Data Forwarding needed!***
- or instr의 $2는 sub instr의 결과에 의존한다. sub의 MEM 직후 결과(sub은 실제로 Memory access를 하지 않지만 시간의 흐름상 해당 instr은 MEM단계를 거친 후가 된다. 그 이후의 latch를 확인해야하는 것)를 가져올 필요가 있다. ***Data Forwarding needed!***
- add instr의 $2는 and instr의 결과에 의존한다. 하지만 and의 WB과 add의 ID는 같은 cycle에서 시행되어도 된다. WB은 앞쪽 절반, ID는 뒤쪽 절반에서 이루어지기 때문이다.
- sw instr의 $2는 아무 의존관계가 없다. 이미 관련 연산이 다 끝난 상태이기 때문이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0525(6).png)                  

- 이렇게 값을 가져오는 것은 MUX를 통해 조절할 수 있다.
- 잘 보면, EX단의 두번째 MUX에 EX/MEM latch에서 나오는 ALU result가 연결되는 것을 볼 수 있다. EX 후 바로 다음 instr의 EX에서 이 값이 쓰여야하는 경우가 있기 때문이다! → 위 예시의 and instr의 경우
- MEM/WB latch에서 나오는 결과가 ALU input으로 들어가는 MUX로 이어져있다. → 위 예시의 or instr의 경우
- 저 MUX를 컨트롤하기 위해 새 컨트롤 유닛 Forwarding unit이 추가된다.
- 결론적으로, ALU input으로 rs, rt 대신 EX/MEM, MEM/WB latch에서 나온 값도 들어갈 수 있게된 것!

### Detecting EX Hazard

Data forwarding을 위해 하드웨어를 어떻게 구성해야하는지까지 알아봤다.

실제로 Data forwarding을 하기 위해 먼저 Data forwarding을 언제 해야하는지에 대해 알아보자.

먼저 1st instr의 EX단 다음 값이 2nd instr의 EX에서 쓰이는 경우이다.

만약 ***EX-MEM latch***단계에 있는 instr이

- ***register에 값을 write하는 작업을 한다면 = destination register을 갖는다면***
    - ex) add, addi 등
- ***$0이 아닌 register에 write한다면***
    - $0에 write한다면 그 instr은 의미 없는 intrt일 뿐. register 의존관계에 대해 생각할 때 고려할 필요가 없을 것
- ***ID-EX latch단계에 있는 instr의 1, 2번째 ALU input 중 하나인 register에 write한다면***

→ ***Data Forwarding 필요!***

다음과 같은 조건문으로 분류 가능할 것

```python
# forward as the 1st ALU operand
if (EX/MEM.RegWrite and (EX/MEM.RegisterRd != 0)
		and (EX/MEM.RegisterRd == ID/EX.RegisterRs))
# forward as the 2nd ALU operand
if (EX/MEM.RegWrite and (EX/MEM.RegisterRd != 0)
		and (EX/MEM.RegisterRd == ID/EX.RegisterRt))
```

### Detecting MEM Hazard

1st instr의 MEM단 다음 값이 3rd instr의 EX단에서 쓰이는 경우는 다음과 같은 경우가 발생할 수 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0525(7).png)                  

- 3번째 instr의 경우 두번째 instr의 EX단 후의 값을 받아와야한다. MEM-WB latch가 아닌, EX-MEM latch에서 값을 가져와야하는 것
- 따라서 EX/MEM latch의 값에 더 높은 우선순위를 준다.

다음과 같은 경우를 만족하면 Data forwarding을 해야할 것

만약 ***MEM-WB*** latch단의 instr이 

- register에 값을 write하는 작업을 한다면 = destination register을 갖는다면
- $0이 아닌 register에 write한다면
- ***EX-MEM latch단의 instr과 destination register이 겹치지 않는다면***
- ID-EX latch단계에 있는 instr의 1, 2번째 ALU input 중 하나인 register에 write한다면

```python
# forward as the 1st ALU operand
if (MEM/WB.RegWrite and (MEM/WB.RegisterRd != 0)
		and 
		not(EX/MEM.RegWrite and (EX/MEM.RegisterRd != 0)
		and (EX/MEM.RegisterRd != ID/EX.RegisterRs))
		and (MEM/WB.RegisterRd == ID/EX.RegisterRs))
# forward as the 2nd ALU operand일 경우 Rs가 아닌 Rt를 확인해야할 것
```

### Hazard Detection in Hardware

이러한 Hazard, 즉 register 의존 관계는 Hazard detection unit에서 파악하고, 적절한 signal을 주게 된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0525(8).png)                  

- 현재 instr의 rs, rt가 Hazard detection unit으로 들어가게 된다.
- ***Forwarding unit은 data forwarding***이 필요한 상황인지를 감지하고, 그에 맞는 signal을 보낸다.
- ***Hazard detection unit은 Load-use data hazard***와 같이 data forwarding으로 해결할 수 없는 상황을 확인하고, ID/EX latch 전의 MUX에 신호를 보내 모든 control signals가 0을 갖게 만들어 bubble instr을 집어넣는다.
    - ***lw의 경우 Rt를 destination register로 사용한다. ID/EX.RegisterRt를 가져와 확인해 lw의 destination register이 다음 단에서 쓰는지 확인하는 식으로 Load-use data hazard를 판단한다.***
    - 예정되지 않은 bubble을 하나 집어 넣게 되면, 그 다음 instr에 해당하는 값들이 덮어씌워진다. ***PC register과 IF/ID값이 그 다음단으로 넘어가는 것을 방지해야함으로써 이를 해결할 수 있다.*** 잘 생각해보면 bubble을 하나 추가한다는 것은 원래 실행됐어야하는 instr을 한단계 뒤로 미루는 것과 같은 일이니 당연한 것이다.

### Control Hazard

- Branch 유무는 MEM 단에서 정해진다.
- Branch 해야할 경우 뒤에 연이어서 실행된 3개의 instr은 무시되어야할 것이다.
- 따라서 Branch할 경우 IF/ID, ID/EX, EX/MEM latch의 값을 모두 0으로 바꿔버린다!

### Minimizing Control Hazard

- 위와 같이 wrong path를 탔을 경우, 즉 branch문 후의 3개의 instr이 무시되어야하는 경우 pipeline을 flush해야한다. 위와 동일하게 latch들을 inalidate한다는 뜻이다. 근데 이러면 performance적으로 손실이 많다 ㅠㅠ
- Branch 여부를 예측함으로써 손실을 줄일 수 있다!! How?!@#!@#
    - 예를 들어 loop의 경우 마지막 단에서 높은 확률로 branch한다.
    - 다만, 높은 prediction accuracy가 보장되어야만 의미있는 방법이 될 것!

### Dynamic Branch Prediction

- One-bit branch prediction
    - 가장 최근의 branch history를 저장하고 이를 기준으로 branch 여부를 예측한다.
- Two-bit branch prediction
    - bit 두개 사용. 연속으로 같은 결과가 두번 나와야만 state가 바뀐다.

![Untitled](https://gonnnnn.github.io/image/TIL/0525(9).png)                  

### Summary

![Untitled](https://gonnnnn.github.io/image/TIL/0525(10).png)                 

- IF.Flush가 추가되었다. Branch하는 경우 Control unit이 Flush신호를 보내 3개의 instr을 invalidate한다.
- Hazard detection unit은 PC, IF/ID latch의 값을 조절하는 signal을 보낸다.
- 또한 ID/EX latch 전의 MUX에 bubble을 생성에 관한 signal을 보낸다.
- Data Forwarding unit은 EX/MEM, MEM/WB latch에서 값을 받고, forwarding한다.
- 이제까지 설명에서는 생략됐지만, ID stage에 shift left 2의 값이 Adder로 들어가는 부분이 있는 것을 확인할 수 있다. Branch가 발생하는 것을 더 빨리 확인하여 flush되는 instr 수를 줄이기 위한 최적화 방법 중 하나이다.