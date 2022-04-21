---
title: "Computer Architecture (2) Performance"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---


# Performance

## 1. Defining Performace

어떻게 정의해야할까? Performance metrics! 다양한게 있지만 두가지를 다룬다.

### Execution time (Response Time)

- 컴퓨터가 task를 완료하는데 드는 총 시간.
- Single user desktops에 유용한 지표.

### Throughput (Bandwidth)

- 주어진 시간내에 완료한 총 **일의 양**
- 다양한 task를 동시에 하는 Server나 WSCs에 유용한 지표.

* Execution time이 더 뛰어나면서 Throughput이 더 안좋을 수 있다! 상황에 따라 Performance metrics를 잘 정의하는게 중요하다.

### Comparing the Performance

- Performance = 1/Execution Time의 관계를 갖는다
- X is fater than Y == The execution tiime on Y is longer than the one on X

### Quantifying the Performance

- Performance_X / Performance_Y = n = Execution Time_Y / Execution Time_X
- Y is **n times  slower than** X

## 2. CPU Performance

[좋은 설명](https://skyil.tistory.com/105)

### Measuring the CPU Performance

- wall clock time 을 performance metrics로 쓰는 것은 적절하지 않다.
    - 프로그램이 실행되고 종료 될 때까지 CPU, I/O, Sub Program 등의 모든 시간을 합친 것을 말한다.
    - OS는 다른 task도 병렬적으로 실행시키기 때문이다. 우리가 원하는 프로그램을 실행한 시간만을 얻어야 한다!
- ***CPU execution time(or CPU time)***
    - CPU가 I/O나 다른 task를 실행하는 시간을 제외하고, 우리의 target task를 실행하는데 할당했던 순수한 시간
    - OS에서 software layer에는 system(kernel) layer(OS, kernel이 돌아가는 곳), user level layer(Application이 돌아가는 곳)이 있다. 이 각각에 대해 할당된 시간으로 또 분류가 가능하다.
        - User CPU time : CPU가 우리의  target program(task)에 할당한 시간
        - System CPU time : CPU가 OS에 사용한 시간

### Clock Cycles(Clock Period Time) as the Measure

- 프로세서는 digital circuit이다. Digital circuit에서 모든 event는 clock signal에 의해 발생한다.
- 이런  ***Clock period***를 시간의 측정 수단으로 사용할 수 있다.
    - Clock period는 두개의 인접한 positive edge(clock signal이 0에서 1로 올라가는 부분) 사이의 시간을 말한다.
    - Clock rate는 Clock period의 역수이다. 초당 clock cycle 수를 의미한다.
    - 1-GHz clock(1초에 1G번의 clock cycle)을 위해서 clock period는 1ns여야 한다.
    ![clock_cycle](https://gonnnnn.github.io/image/TIL/clock_cycle.png)

- CPU execution time = CPU clock cycles * Clock cycle time(Clock period) = CPU clock cycles / Clock rate

### Adding INstructions to Performance

- 사실 프로그램이라는 것은 comiler/interpreter에 의해 생성, 해석된 instructions의 집합이라고 볼 수 있다. CPU의 실행시간을 측정하는데 있어서 더 작은 단위인 ‘instruction’을 활용할 수 있다.
- ***Cycles Per Instruction(CPI)***
    - CPU clock cycles = Instruction Count * Average clock cycles per instruction
    - Instruction마다 다른 시간이 걸릴 것이기 때문에 average CPI를 사용한다.
    - ex) Program A = 1000 instructions이고 이를 실행하는데 4초가 걸린다고 하자. Clock rate은 1000Hz라고 하면, CPI_A = 4s * 1000Hz/1000instructions = 4cycles/instructions
    

### The Classic Performance Equation

- CPI, CPU time를 사용할 수 있다.
    - CPU time = CPU clock cycles / Clock rate = Instruction count * CPI / Clock rate = Instruction count * CPI * Clock cycle time(Clock period)
- 풀어쓰면,
    - Time = seconds/Program = Instructions/Program * (Clock cycles/Instruction) * (Seconds/Clock cycle)
    - **Instructions/Program = Instruction count
    - **Clock cycles /Instruction = CPI
    - **Seconds/Clock cycle = Clock period

# The Power Wall & The Switch to Multiprocessors

왜  10GHz의 clock rate을 갖는 싱클 코어 대신 멀티 코어 CPU를 만드는지에 대한 해답을 확인할 수 있다.

## 1. Power Wall and Multiprocessors

Clock rate은 2.5~3.5GHz에서 정체되어 있다.(2004년에 이미 3.6GHz에 도달했었다. 이 때 103W를 잡아먹었다.) 더 올리면 발열이 너무 심해지기 때문이다. 또한 Power을 너무 많이 소비하게 된다. CPU 생산자들은 clock rate을 올리는 대신 power consumption을 줄이는 방향으로 CPU를 생산하게 되는 현상이 발생했다. Cooling 기술이 컨트롤 가능한 이 Power 수준의 한계를 Power Wall(아마 103W)이라고 한다.

### Clock Rate - Power Relationship

자세한 설명은 생략하고

- Power는 1/2 * Capacitive load * Voltage^2 * Frequency switched에 비례한다.
- Frequency switched = function(clock rate)

### The Switch to Multiprocessors

- Power wall에 막혀 Clock rate을 늘릴 수 없으니 core를 더 넣자는 결론에 도달했다.
- Multi core CPU를 잘 활용하는 것은 SW Developer의 몫이다.

### The Era of Parallel Programming

- 더 높은 performance를 위해서는 paralleism을 적용해야만 한다.
    - 어렵다. 각각의 processor가 거의 같은 양의 일의 처리하도록 application을 적절히 쪼개야할 것이다. 또한 Inter-processor communication, synchronization을 최소화하도록 프로그램을 설계해야할 것이다.

# Fallacies & Pitfalls

## 1. Make the Common Case Fast

Performance 향상에 가장 필수적인 부분이다.

### Amdahl’s Law

Optimization 후 execution time을 추정하는 방법 중 하나

성능에 영향을 가장 많이 미치는 부분을 개선하여 전체 성능의 큰 향상을 기대할 수 있다.

- Execution time after improvement = Execution time affected by improvent / Amount of improvement + Execution time unaffected
- 5초가 걸리는 app의 20%를 1.2배 빨리 실행되도록 개선!
→ 0.2 * 5 / 1.2 + 0.8 * 5 = 4.83

 

## 2. MIPS

### Million Instructions Per Second(MIPS)

- MIPS = Instruction count / (Execution time * 1,000,000)

**적절하지 않은 지표이다. 이유는 다음과 같다.

- Instruction의 특성을 고려하지 않았다. 어떤 경우 arithmetic operation만 할 수도 있고, 더 복잡한 operation을 할 수도 있다. CPU에서 수행되는 instruction보다는 low level operation을 고려해야한다.
- 두 개의 다른 프로그램은 같은 수의 instructions를 가질 수 있지만, 그 종류가 다를 수 있다. 이 경우 execution time이 달라지는 것은 명백하다. 같은 hardware에 대해 다른 지표값이 나와버리는 결과가 발생한다.