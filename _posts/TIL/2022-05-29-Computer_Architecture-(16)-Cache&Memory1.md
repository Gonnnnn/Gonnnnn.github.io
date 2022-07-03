---
title: "Computer Architecture (16) Cache & Memory 1"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

### Memory Technologies

Sequential circuit vs Combination circuit

- Seq : 특정 정보를 일정 시간 저장 가능. Memory
- Com : output이 input에 의존. ALU

Memory를 implement하는 방법은 여러가지가 있고, 각기 특성이 다르다.

Volatile memory

- Static Random Access Memory (SRAM)
- Dynamic Random Access Memory (DRAM)

Non-volatile memory

- Flash memory (ex) SSDs)
- Magnetic disks (ex) HDDs)

다른점이 많지만, 아래로 갈 수록 data에 access하는데 시간이 얼마나 걸리는 시간이 길어지고, 용량 당 가격이 저렴해진다.

### SRAM Technology

- memory array로 이루어진 Integrated circuit이다. 주로 하나의 access port를 갖는다.
- Static이란, 값이 무기한으로 유지될 수 있다는 뜻이다. 전원이 공급된다는 가정하에!
- Data access time이 항상 일정하다. 해당 data를 Read, write하는 시간은 다를 수 있다.
- ***주로 CPU의 Cache memory에 사용된다. GPU에서 shared memory에 해당하는 부분.***
    - Cache란 이미 사용된 data나 processor에 의해 사용될 data를 일시적으로 저장하는 hardware component이다.

### DRAM Technology

- Capacitor에 값을 charge로 저장한다.
- Dynamic이란, 시간이 지날 수록 값이 천천히 decay된다는 뜻이다.
    - Charge가 시간이 지날 수록 조금씩 새는 것
- SRAM보다 더 dense하고 싸다
    - 1bit에 transistor하나를 쓴다.
- ***컴퓨터의 main memory로 사용된다.***
- 값을 주기적으로 refresh하면서 유지시켜야한다.
    - cell의 값을 읽은 후 다시 쓰는 방식으로 유지한다.

### Flash & Disk Memory

- Non-volatile
    - 전원이 공급되지 않아도 값을 유지한다.
- Flash memory
    - Non-volatile electricity devide에 값을 저장한다.
    - 같은 cell에 10M번 이상 write할 수 없다. write할 수록 flash memory bits를 wear-out한다.
    - wear-leveling이라는 알고리즘으로 cell들을 균등하게 쓸 수 있도록 한다.
- Disk memory
    - data를 platter에 저장한다.
    - platter은 빙빙 돌기 때문에 target surface-track-sector을 먼저 찾아야한다.
- ***Flash, Disk memory는 주로 secondary storage로 쓰인다.***
    - Main memory가 값을 읽어들이는 back-up storage로 쓴다!

### Unlimited Fast Memory?

메모리들은 성능과 가격의 trade off가 존재한다. 필요한 부분 부분에 따라 적절한 것을 써야한다.

- 작고 빠른 SRAM같은 memory를 processor와 가까운 곳에
- 크고 느린 SSD같은 memory를 processor로부터 먼 곳에

배치하여 최적화할 수 있다!

### Principle of Locality

***Software 관점에서 정말 중요한 것!***

이를 활용해 메모리를 다루는 퍼포먼스를 향상시킨다.

언제 어디에 데이터 올리고 내려야하는지를 instr 실행 관점에서 봐보면,

- Temporal Locality
    - If an item is referenced, ***the item is likely to be referenced again soon***
    - ex) loop iterators
- Spatial Locality
    - If an item is referenced, ***items whose addresses are close by are likely to be referenced soon***
    - ex) adjacent elements in an array

위와 같은 성질이 있다. 타당한 말이다. MIPS도 이를 고려한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0529(1).png)                                                                   

### Memory Hierarchy

- Memory Hierarchy는 Principle of Locality를 이용하기 위해 디자인되었다. 이제까지 봐왔던 다른 memory access time과 size를 갖는 memory들로 이루어져있다.
- 그냥 Principle of Locality를 고려해서 자주 쓰는 애들을 위주로, 그 때 그 때 필요한 애들을 Processor 쪽으로 가져오면 빨리 빨리 접근 가능한 SRAM의 장점도 살리면서, 마치 거의 모든 data를 쓸 수 있는 듯한, 큰 용량이 있는 듯한 효과를 내어 Magnetic Disk의 장점도 살릴 수 있는 것

![Untitled](https://gonnnnn.github.io/image/TIL/0529(2).png)                                                                       

- Higher level에 빠르고 비싼 memory, lower level에 느리지만 싼 memory 배치
- 일반적으로 SRAM - DRAM - Magnetic Disk 순으로 배치하여 쓴다.
- 이렇게 하면 최적화되어 size, memory access time에서 이득을 볼 수 있다고는 하는데, size야 이해가 가도, memory access time에서는 어떻게 이득을 볼 수 있는 것일까? ***Principle of locality를 통해 가능하다!!***

### Data in a Memory Hierarchy

먼저 실제로 어떻게 data를 memory hierarchy에 배치하는지 확인해보자

- Similarly hierarchical
    - ***Processor에 가까운 level의 data는 더 먼 level의 부분집합***이다. 가까운 level의 모든 data는 더 먼 level에 포함되어 있다는 뜻!
    - 모든 data는 lowest level에 저장되어있다.
- ***인접한 두 level에서만 복사***가 일어난다.
    - Memory 마다 특성이 다르기 때문에, Memory마다 data access time, throughput 등이 다르다. Memory 사이에 전달될 수 있는 size에는 한계치가 있다. 이런 ***전달 가능한  data단위를 block 혹은 line이라고 한다.***

![Untitled](https://gonnnnn.github.io/image/TIL/0529(3).png)                                                                       

### Hits & Misses

***Highest level memory에 Processor가 원하는 data가 있을 수도 있지만 없을 수도*** 있다. 이럴 때는 lower level에서 가져와야할 것. 어쨋든 이렇게 있거나 없는 상황을 ***hit, misses***라고 한다.

- Memory level’s effectiveness는 hit rate, miss rate으로 측정할 수 있다.
    - ***Hit rate = # hits / # reqeusts***
    - ***Miss rate = # misses / # requests = 1 - hit rate***
- 위 두 rate은 perforamcne-impacting factors이다. 아래와 같은 것을 계산하는데 쓰인다.
    - ***Hit time : 현재 level에서 data에 접근하는데 걸리는 평균 시간***
    - ***Miss penalty : missing block/line을 lower level에서 현재 level로 전달하는데 걸리는 평균 시간***

### Hits & Misses in a 2-Level Memory

![Untitled](https://gonnnnn.github.io/image/TIL/0529(4).png)                                                                       

- Block #1의 경우 level-1에 있으므로 바로 hit
- Block #2의 경우 level-1에 없다. level-2에서 가져오는 시간(HitTime L2)이 추가로 걸린다.

### Caches

- Processor와 Main memory(DRAM) 사이의 level. SRAM을 쓴다.
- 그럴리는 없지만 0개도 가능하고, 보통 1개 이상의 level로 이루어져있다.
- Processor는 먼저 cache한데 read/write request를 보낸다.

Cache에 접근할 때, 우리는 다음과 같은 것을 알아야한다.

- data item이 해당 cache안에 있는가? → hit or miss
- 그 많은 data중 해당 data를 어떻게 찾을 것인가? → data access

### Direct-Mapped Caches: Concept

Request가 Hit/Miss를 판단하고 접근하기 위해서는 먼저 Cache의 유형을 알아야한다. Direct-Mapped Cache, Fully Associative Cache, Set Associative Cache가 있다. 여기서는 Direct-Mapped Cache만 본다.

Direct-mapped caches

- Assumptions
    - ***Processor request는 항상 one word 크기***를 갖는다.
    - ***Cache의 block은 single word***로 이루어진다.
- Direct-Mapped Cache에서 특정 memory address는 특정 block에 mapping된다.
- 이를테면 X_n이라는 data는 몇번을 load, store되던 해당 cache로 들어올 때 항상 일정한 block(아래 사진의 block2)에 매치되는 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0529(5).png)                                                                       

### Mapping a Word Block

- 각 word는 cache의 하나의 block으로만 간다! 어떻게?
- cache location, 즉 block id는 word의 block address에 의해 할당된다.
    - cache location =  block address % # cache blocks
    - cache block의 개수가 2^N이면, modulo는 단순히 block address의 least-significant bits N개가 된다.
    - cache가 4=2^2의 word-long block을 갖는다면, 00, 01, 10, 11 → block 0, 1, 2, 3에 할당되는 것

![Untitled](https://gonnnnn.github.io/image/TIL/0529(6).png)                                                                       

위 예시를 보자

- ***32bit로 이루어진 byte address***는 우리가 아는 그 memory address이다. cache의 block은 word 단위로 이루어져있으므로, 이를 ***block address로 계산하기 위해 먼저 30bit으로 바꿔준다.***
- ***block address의 N least-significant bits를 가지고서 block index를 정한다***. 해당 data는 cache block들 중 하나의 block에 저장될 것이다.
- 후에 ***참조할 때는, byte address에서 버린 2개의 bit를 쓴다. offset***이다.
    - 1 block의 size가 4byte이기 때문에 2개의 bit을 버려 block address를 만들었던 것이다. 이 2개의 bit으로 block내의 data를 참조한다.

### Validating the Target Block

Tag

- 위와 같은 방법을 쓸 때, lower level memory가 higher level memory보다 size가 크면 당연히 같은 block에 여러개의 data가 mapping될 수 있다.
    - 2^M word를 2^N개의 block에 mapping하면 M-N words가 하나의 block에 겹치게 된다.
- 이 때 이를 구분하기 위해 Tag라는 것을 사용한다.
    - Tag는 cache block이 필요한 word를 갖고 있는지를 확인하기 위해 쓰이며, address 정보를 저장한다.
    - Block Address의 upper portion을 저장한다! block index 정하는데 쓰인 2개의 bit을 제외한 28개의 bit
- Tag가 match하면 Hit, 아니면 miss!

Valid bit

- cache block이 비어있는지 확인해야할 필요가 있다.
- 이를 위해 valid bit을 도입한다.
    - 1이면 해당 block이 valid word를 담고 있는 것이고, 0이면 비어있는 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0529(7).png)                                                                       

- 2 LSB로 block index를 확인하고, valid bit으로 해당 block에 유요한 data가 있는지 확인한다. 그 후 valid bit이 1이면 tag를 통해 실제 찾고 있던 data인지 확인한다.

### Summary - Accessing a Cache Block

1. Target Cache Block을 확인한다.
    1. Memory address를 block size만큼 Right-shift해서 block address를 얻는다. Right-size만큼은 같은 block내에서의 offset으로 쓰인다.
    2. Block address의 N LSB를 확인한다. (이 때 cache block의 개수는 2^N)
2. Cache block이 valid word를 갖는지 확인한다.
    1. valid bit이 1이면 valid한 것. 비어있지 않은 것
3. Cache block이 올바른 word를 갖는지 확인한다.
    1. Cache에 저장된 tag가 request가 찾고 있는 block address의 tag부분과 같은지 확인한다. 

### Example

8-block direct-mapped cache를 사용한다고 하자

- Empty → valid bit은 모두 0으로 초기화 되어 있다.
- 8 blocks → Block address의 3 LSB를 이용해 block index를 정할 것이다.
- Direct-mapped → block address % # blocks 방식으로 mapping한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0529(8).png)                                                                       

위 table의 가장 위쪽부터 시작한다.

- 1번째 reqeust는 10110에 접근한다.
    - tag : 10, index : 110
    - empty이므로 miss. valid bit을 1(Y)로 바꾼다. Lower level에서 data를 가져와야할 것
- 2번째 request는 11010에 접근한다.
    - tag : 11, index : 010
    - empty이므로 miss.
- 3번째 request는 10110에 접근한다.
    - tag : 10, index : 110
    - 첫 번째 request에서 해당 block을 채웠었다. index로 해당 block에 접근한 후, valid bit은 1임을 확인하게 된다. Tag가 match하므로 해당 data는 원하던 data이다.
    - → hit!!

7번째 request까지 시행한 후,

- 8번째 request는 10010에 접근한다.
    - tag : 10, index : 010
    - 010에 block의 valid bit은 Y이다. 4번째 request때 갱신된 data가 들어있다. Tag는 11로, 8번째 tag와 다르기 때문에 찾는 data가 아니다.
    - Miss!