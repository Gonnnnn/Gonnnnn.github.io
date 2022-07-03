---
title: "Computer Architecture (17) Cache & Memory 2"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

### Implementation

- 다음과 같은 경우를 가정해보자
    - 32-bit memory addresses
    - Direct-mapped cache
    - 2^N cache blocks
        - N bits for the cache index!
    - 2^M !!!words!!! per cache block (= 2^(M+2) bytes) = Cache block size!
        - M bits for specifying a word, 2 bits for the byte offset
- 총 bit 수는 다음과 같게 된다.
    - (Cache block 개수) * (block size + tag size + valid bit size)
    - 2^N * (2^M * 32 + (32 - (N + M + 2)) + 1) bits
    - *Block : 2^M words = 2^M * 32 bits
    - *Tag : 32 - (M+2) - N = 32 - (N+M+2) bits
        - Byte addr : 32 bits
            - 32-bit memory address를 가정했기 때문이다.
        - Block addr : 32 - (M+2) bits
            - Cache block의 size는 M+2이다. 해당 부분만큼의 LSB를 byte addr에서 덜어주면 block addr이 된다. M+2 LSB는 Block 내에서 데이터에 접근할 때 쓰는 offset
            - Tag : 32 - (M+2) - N = 32 - (N+M+2) bits. Block addr의 N LSB 앞의 bits
            - Block index : Block addr의 N LSB
- Example
    - N = 10 → 2^10개의 cache block
        - cache index : 10 bits
    - M = 0 → 2^0 words/block
        - Block 안의 word 참조 : 0 bit
        - Block 안의 word 안의 byte 참조 : 2 bits
    - Tag : 32 - (0 + 2) - 10 = 20 bits
- 4 KiB cache!
    - Block size (4 byte) * # of blocks (2*10) = 4 * 1024 bytes = 4KiB

![Untitled](https://gonnnnn.github.io/image/TIL/0530(1).png)                                                               

- 보다시피 valid bit, tag, 실제 data 부분으로 구성된다.
- Block index를 찾아 접근(초록) → tag 매치 여부 확인(빨강) → valid bit 확인(파랑) → hit일 경우 target cache block에서 byte offset에 따라 알맞는 data를 return. 00이면 첫 번째 byte

### Miss Rate vs Cache Block Size

특정 capacity의 cache memory를 만들 때, cache block 개수를 줄이는 대신 size를 늘릴 수 있고, 그 반대의 경우도 가능할 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0530(2).png)                                                                   

위 표는 block size에 따른 miss rate을 capacity별로 나타낸 것이다.

Block size가 256일 때, 4K의 경우 256개의 block, 16K의 경우 1024개의 block으로 이루어져있을 것이다.

- Cache block size가 크고 cache block 수가 적을 수록, spatial locality를 더 활용하게 된다. 한번에 많이 가져오니까
- 하지만 block 수 자체가 적기 때문에, 다른 주소의 data들이 같은 block에 mapping되는 경우가 많아진다. 따라서 block size가 커질 수록 miss rate이 일정 부분 감소하다가, 결국 다시 증가하는 경향을 보이는 것

### Handling Cache Misses

- Cache miss는 다음과 같은 경우 발생한다.
    - Cold miss : target cache block이 invalid한 경우. valid bit = 0인 경우
    - Conflict miss : target cache block의 tag가 해당 block address의 tag와 일치하지 않는 경우
- 이 경우 해당 block을 memory에서 fetch해와야할 것이다.
    - memory에 해당 부분을 읽어와줄 것을 request
    - memory가 작업을 완료할 때까지 기다린 후, 완료되면 target cache block의 valid bit, tag, data를 갱신해준다.
    - 그 후 miss한 memory request를 다시 시도해 해당 cache block에서 data를 fetch한다!

### Handling Writes

Processor - Cache - Memory 구조에서

Processor에서 Cache의 한 block에 write request를 보냈다고 하자. write 직후를 보면 해당 block의 data는 바뀌어 있을 것이지만, 이에 mapping 되는 memory 주소의 data는 아직 그 전의 값을 갖고 있을 것이다.

이런 inconsistency를 해결할 방법이 필요하다.

- Write-through
    - ***cache에 data를 write하는 경우***, hit이라면 cache에 data를 쓰고, ***lower level의 memory들까지 data를 갱신***해주면 된다. 이렇게 lower level까지 propagate하는 것을 write-through라고 한다.
- Write buffer
    - Write-through를 할 때, ***lower level의 memory들은 접근 시간이 길기에*** 전반적으로 performance가 저하된다.
    - 이를 해결하기 위해 ***Buffer을 도입한다***. ***Write-through request를 write buffer에 집어넣고***, ***processor는*** write-through가 lower level 전반에 걸쳐 완료되기 전에 ***할일을 계속한다***.
    - 어느 정도 시간 후에 buffer에 있던 write request를 lower level들에 실행해가면서 inconsistency를 해소한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0530(3).png)                                                                   

- Write-back
    - Write buffer가 꽉차면 processor가 stall할 수 있다.
    - Write-back 기법을 도입한다. 일단은 새로운 data를 cache에는 write하지만 memory까지는 가지 않는다.
    - ***그 후 다른 data에 의해 이 cache block이 교체될 때만 새로운 cache block data를 memory에 write한다.***
    - 사실 processor는 먼저 cache에 접근하니 여기에만 제대로된 data가 들어있어도 일단은 상관 없다. 이런 경우는 memory간 inconsitency가 존재해도 무관

![Untitled](https://gonnnnn.github.io/image/TIL/0530(4).png)                                                                   

### Measuring Cache Performance

Cache Performance는 얼마나 더 latency가 늘어나냐로 측정된다.

CPU time을 두개로 쪼개보자

- Memory Hierarchy를 도입한 후 부터는 다음과 같이 생각할 수 있다. 1 clock cycle만에 instruction을 딱딱 바로 가져오는게 안되기 때문
- ***CPU time = (CPU execution cycles + memory-stall cycles) * clock cycle time***
- Processor가 instr을 실행하는 시간 + Memory가 store/load 작업을 끝낼 때 까지 processor가 기다리는 시간!
- 일단 여기서는 간소화를 위해 **memory stall은 cache에 의해서만 발생한다고 하자**. Main memory, storage등 무시!
    - ***Memory-stall cycles = Read-stall cycles + Write-stall cycles***로 나눌 수 있다.
    - Read-stall cycles는 read/load와 관련된 write-stall cycles는 write/store과 관련된 cycle

Stalls for reads

- cache miss에 의해 발생한다.
- ***Read-stall cycles = Reads / Program * Read Miss Rate * Read Miss Penalty***

Stalls for writes → 두가지 경우로 나뉜다.

- cache miss에 의해 발생한다.
- ***Write-sall cycles = Writes / Program * Write Miss Rate * Write Miss Penalty***
- Write buffer을 다시 떠올려보자. Write buffer이 꽉 차지 않는다면, write-buffer contention이 일어나지 않는다면 위 식으로 write-stall cycles를 구할 수 있다. 하지만 write-buffer이 꽉 차버리면 buffer stall이 해결되는 시간을 고려해야할 것이다.
    - 이 경우 위 식 + Write Buffer Stalls!
    - Buffer가 꽉 차는 일이 일어나지 않으면 Write Buffer Stalls = 0

Write-through cache의 Read/Write penalty

- 대부분의 write-through cache에서는 read/write penalty가 같다.
- Read/Write miss rate가 같다는 가정하에
    - Memory-stall cycles = Read-stall cycles + Write-stall cycles
    = MemoryAccesses/Program * Miss Rate * Miss Penalty
    = Instructions / Program * Misses / Instruction * Miss penalty
    - 이 때 세 번째 식 관점에서 보면, Memory Access하는 instruction을 구분할 필요가 없어진다! Program 전체 instruction 수와 miss 횟수만 알면 memory-stall cycles를 구할 수 있다!
- Program이 정해지면 하드웨어단에서는 instruction 수를 조절할 수 없다. 또한 lower level 하드웨어 스펙이 fix되면 miss penalty도 정해진다. Miss를 줄여야하는 것이다.
    - Block size, total capacity of cache, block number 등을 조절해서 miss rate을 줄일 수 있었다는 것을 기억하자!

### Example : Cache Performance

- Assumptions
    - Cache miss rates: 2% for instr, 4% for data
    - Cache miss penalty = 100 cycles
    - Processor’s Cycles-Per-Instruction (CPI) = 2
    - Frequencies of all loads and stores = 36%
- Q : miss가 전혀 발생하지 않는 완벽한 cache를 도입하면 processor가 얼마나 더 빨리 동작할까?
- Answer!
    - Instr을 수행하기 위해서는 program instr 수 만큼 cache에 access해 fetch해 와야한다. Cache에 access하는 수를 I라고 하자
    - Instr Miss Cycles = I * 2% * 100(Miss penalty) = 2 * I
    - Data Miss Cycles = (I * 36%) * 4% * 100 = 1.44 * I
    - Memory-stall Cycles = Inst Miss Cycles + Data Miss Cycles = 3.44 * I
    - Total CPI = CPI w.o Stalls(그냥 기본 Processor CPI) + CPI Due to Memory Stalls = 2 + 3.44 = 5.44
    - CPU Time w Stalls / CPU Time w Perfect $
    = (I * CPI w stall * clock cycle) / (I * perfect CPI * clock cycle)
    = CPI w stall / perfect CPI = 5.44 / 2 = 2.72
- Perfect cache를 사용하면 2.72배 빨라진다!

### Average Memory Access Time

실제로 cache는 single clock cycle에 돌아가지 않는다. 진작 말하지 ㅋㅋㅋㅋ

Cache hit만해도 여러 cycle에 거쳐 일어나고는 한다.

***Average Memory Access Time (AMAT)***를 도입해야한다.

- AMAT = Hit Latency + Avg Miss Latency = Time for a Hit + Miss Rate * Miss Penalty
- 예를 들어 cache access time은 1 cycle, miss penalty는 20 cycles, miss rate은 0.05 misses/instr이라면,
    - AMAT = 1 + 0.05 * 20 = 2 cycles

### Reducing Cache Misses

Direct-Mapped cache만 배웠었는데, cache miss를 줄이기 위해 다른 방식으로도 cache를 구성할 수 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0530(5).png)                                                                   

- N-way set-associative : 하나의 data block을 N cache blocks에 mapping. N개의 cache block이 있고, 그 중 하나에 들어가게 되는 것
- Fully associative : 하나의 data block을 아무 cache block에 mapping. 이 중 하나에 들어가게 되는 것. Direct-Mapped와 N-way set-associative 사이의 trade-off정도. Set이라는 개념이 있는데 여기서는 set이 하나고 거기에 cache block이 다 들어가있는 셈인 것이다.

### Set-Associative Caches

- Set : cache block을 그룹화한 것. data block은 이 set 내의 N개의 cache block 중 하나에 mapping될 수 있는 것이다.
- 따라서 target set 내의 모든 tag를 확인해봐야 원하는 cache block을 찾을 수 있다.
- 여기서 Index field는 cache block이 아니라 set을 가리키게 된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0530(6).png)                                                                   

### Real-World Implementation

- 4-way set-associative cache를 가정해보자

![Untitled](https://gonnnnn.github.io/image/TIL/0530(7).png)                                                                   

- byte offset이 2bit이다. 1block의 크기가 4bytes = 1word라는 것
- 4-way이므로 set하나에 4개의 cache block이 들어간다.
- 2^8만큼의 set이 있다. 8개의 bit을 index bit으로 사용한다.
- Tag를 각각의 tag field로 이어주고, 찾고 있는 tag와 같은지 확인, valid bit도 확인한다.
    - index field로 set을 찾고, 각각의 block은 tag를 하나하나 비교하며 찾게 된다.
- 결과를 바탕으로 Hit 처리하고, data를 가져온다.

### Fully-Associative Caches

- 모든 tag를 확인해야한다. 따라서 index field가 필요가 없다.
- Block address 전체를 그냥 tag로 쓰면 된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0530(8).png)                                                                   

### Handling Cache Misses

- Direct-Mapped cache에서는 miss가 발생하면 그냥 해당 cache block에 넣을 data를 memory에서 가져오고 같은 cache block에 넣어줬으면 됐다.
- Fully/set-associative cache에서는 어떤 cache block에 대해 위 행위를 수행할지 지정해줘야한다.

Least-Recently Used (LRU) policy

- Target cache blocks중 가장 덜 사용된 cache block을 선택하는 방법!
- Temporal locality를 최대한 살리기 위해서 쓴다.

### Reducing the Miss Penalty

Memory-stall cycles를 줄이기 위해 Miss를 줄이는 방법을 알아봤다. Miss Penalty는 lower level memory에 의해 정해지지만 cache단에서 줄일 수 있는데,

- Multi-level caches를 도입하는 것이다.
- Average memory access latency는 조금 늘어나겠지만, capacity가 늘어난다.
- 그래도 어쨋든 cache의 겨우 main memory보다 latency가 낮기 때문에, AMAT를 줄이는 것에 도움이 된다고 한다. Single level cache를 쓰는 것 보다 main memory에 access할 확률이 줄어들기 때문이다.

### Summary : From Processor to Main Memory

- Processor이 memory request를 쏴준다.
    - 필요한 data나 instr을 fetch하려는 request
- Caches를 도입해서 data access time을 줄인다.
    - 최근에 쓴 애들을 여기다가 임시로 두는 것
- Main memory는 backup storage 개념으로 쓴다.
    - Program의 instr, data를 저장해둔다.
- Miss rate을 줄이기 위해서는 cache 구성 방법(Direct-mapped, fully/set-associative)을 바꾸고, latency를 줄이기 위해서는 multi-level cache를 도입한다.
- Memory간의 inconsistency를 해결하기 위해 write-buffer, write-back 등을 도입한다.
- Cache performance를 계산하는 방법도 배웠다.

Programmer, compiler는 main memory의 detail을 잘 고려해서 설계해야한다!

PC가 shut down될 때 보존해야할 중요한 data가 있으면, cache, main memory에 있는 것들을 flash memory나 magnetic disk같은 secondary storage에 저장한다!