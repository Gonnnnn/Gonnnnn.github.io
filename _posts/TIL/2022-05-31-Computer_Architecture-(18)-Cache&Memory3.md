---
title: "Computer Architecture (18) Cache & Memory 3"
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---

Summary

- Processor이 memory request를 쏴준다.
    - 필요한 data나 instr을 fetch하려는 request
- Caches를 도입해서 data access time을 줄인다.
    - 최근에 쓴 애들을 여기다가 임시로 두는 것
- Main memory는 backup storage 개념으로 쓴다.
    - Program의 instr, data를 저장해둔다.
- Miss rate을 줄이기 위해서는 cache 구성 방법(Direct-mapped, fully/set-associative)을 바꾸고, latency를 줄이기 위해서는 multi-level cache를 도입한다.
- Memory간의 inconsistency를 해결하기 위해 write-buffer, write-back 등을 도입한다.
- Cache performance를 계산하는 방법도 배웠다.

Main Memory

Programmer, compiler는 main memory의 detail을 잘 고려해서 설계해야한다. 예를 들어 main memory를 1GB로 잡고 전 범위를 활용하는 방식으로 프로그래밍했을 때, 512MB main memory에서는 안돌아갈 것이다. 다시 프로그램을 짜서 recompile해야할 것

→ ***Then just provide an illusion of having a large, fixed-size main memory to a program!!***

### Virtual Memory

Low level computer hardware와 operating system단에서 동시에 고려해 만든 개념

4GB에 프로그램 2개를 돌린다고 할 때 그냥 0 ~ 2^31 - 1, 2^31 ~ 2^32 - 1처럼 구간을 단순히 나눠도 되긴하겠지만, 이런식으로 하려면 프로그램이 한번에 몇개가 돌아가고 있는지, 프로그램 하나당 필요한 memory 크기는 어느정도인지 모두 하나하나 그때마다 따져봐야한다.

- 따라서 virtual memory 개념을 도입한다.
- 실제로 사용 가능한 memory가 아니라, 프로그램은 virtual memory를 활용하게 된다. 각 프로그램마다 virtual memory가 할당되는 것이다.
- Virtual memory에 저장되는 data들은 OS와 ISA, 하드웨어를 기반으로 잘 정리되어 실제 memory에 잘 저장된다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(1).png)      

### Implementing Virtual Memory

근데 그렇다고 프로그램마다 virtual memory를 무작정 할당해대면 당연히 실제 main memory size를 넘어갈 것이다. 어떻게 virtual memory 개념을 잘 활용할 수 있을가?

- Secondary storage가 필요하다
    - Main memory에 적재된 data를 임시로 저장해두거나 하기 위해서
- OS도 필요하다.
    - 다른 application들의 instr을 스케쥴링하고, process에 virtual memory를 제공하기 위해서
- Virtual-to-physical address translation
    - Virtual memory address에서 실제 memory address로 mapping하는 방법도 정해놔야 할 것. 얼마나 많은 프로그램들이 실행되고 있느냐 등에 따라 패턴은 바뀐다.

### Steps of Utilizing Virtual Memory

Add Secondary Storage

- Cache는 main memory를 cache한다.
- ***Main memory는 secondary storage를 cache한다***!!
    - Secondary storage에 저장된 data에 접근하는 것을 더 빠르게 해주는 셈
    - ***보통 main memory block size는 4KiB이다. Main memory의 block을 page라고 해서 page size라고도 한다.***
    - Main memory와 secondary storage 사이의 data tranfer은 OS에 의해 관리된다.

Address Translation

- Per-process page table을 도입한다. 이는 OS에 의해 관리된다. Process마다 할당된다.
- Virtual address, 그리고 그와 연결되는 physical address를 매치시켜 저장해놓는다. 정확히는 VPN과 PPN의 매칭이다. 아래를 보자.
- 아래와 같이 2개의 page가 있다고 하자. lw, sw등의 instr을 실행한다면, 먼저 해당 page을 virtual memory에서 찾고, vaddr과 매치되는 paddr을 확인, 실제 memory의 paddr에 접근한다.
- 실제로는 이렇게 작동한다.
    - 먼저 vaddr을 두 파트로 나눈다.
    - `Virtual Page Number (VPN) : MSBs, tag와 비슷하다. 앞 30 bit을 쓴다.`
    - Page offset : cache의 byte offset과 비슷하다. 4KiB의 page를 사용하기에, 12bits(=4096)이 필요하다. 4096 * Byte = 4KiB!
    - 실제로는 table에서 VPN과 Physical page number(PPN)을 매치시켜 놓는다.
    - VPN과 매치되는 PPN에 Page offset을 다시 붙여서 paddr을 찾는다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(2).png)          

![Untitled](https://gonnnnn.github.io/image/TIL/0531(3).png)          

Handle Page Faults

- Memory page가 main memory에 없을 때 발생한다. Cache miss같은 것이다. OS가 처리한다.
- 하드웨어 단에서는 사실 process단에서 발생하는 일들에 대해서는 알 수 가 없다. 알 수 있는 것은 접근하고자 하는 data가 main memory에 없는 경우가 발생했다는 것 정도. 아래 그림과 같이 0x1000 VPN에 매칭되는 PPN을 확인 후 data에 접근하려고 하는데 data가 없는 것.
- 하드웨어는 OS에게 page fault가 발생했다고 말해준다. Interrupt를 날리는 것이다. OS가 이를 처리한다. Main memory에 공간을 확보해두고, Secondary storage에서 data를 가져온다.
- 그 후 page fault를 야기한 instr을 다시 시행!
- Secondary storage에 데이터를 저장하는 방식을 file system이라고 한다. OS가 관리한다. 이런것도 알아야하는데 하드웨어는 모르니까 응애응애 OS야 도와줘 하는 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(4).png)          

### Short Summary

- Processor가 page table을 훑으면서 target vaddr 앞 부분에서 따온 VPN을 찾는다
- 매치되는 PPN이 있다면 이를 기반으로 paddr를 만들고, main memory에 접근한다.
- 매치되는 PPN이 없다면, processor에 의해 page fault가 야기된다.
- Page fault는 OS의 page fault handler에 의해 처리된다.
- Handler는 main memory에서 공간을 확보하고, secondary storage에서 data를 복사해온다.
- 해당 공간의 paddr을 이용해 Page table을 갱신한다.
- Processor은 page fault를 야기한 instr을 다시 실행한다. 매치되는 PPN을 찾고, main memory에 접근한다.

### Pros & Cons of Virtual Memory

![Untitled](https://gonnnnn.github.io/image/TIL/0531(5).png)          

Pros

- Uniform virtual addrss space
    - 실제 main memory size와 상관 없이 일정한 virtual address space를 갖는다. 프로그래밍에 더 간편
- Protection between processes
    - Process는 다른 process의 memory page에 접근할 수 없게 된다. Page table단에서 걸러지기 때문이다.

Cons

- Potential performance degradation
    - Main memory에 접근할 때마다 virtual-to-physical address translation
    - Page table은 main memory에 존재한다. DRAM은 SRAM보다 느리기에, 여기에 계속 접근한다고 좋을게 없다.

### Adding Virtual Memory Support

사실 virtual memory를 사용하려면,  processor는 다음의 것이 필요하다.

- page table이 어떻게 생겼는지에 관한 정보. storage format. bit 몇개 쓰는지, VPN, PPN 등이 어떻게 정렬되는지 등등. OS에 의해 정의된다. Processor는 이 정보를 미리 받아야한다. 일종의 약속
- page table을 가리키는 page table register. 여러 page table 중 어떤 애에 접근해야하는지에 대한 정보를 갖게 되는 register. 다른 process의 instr을 실행하기 전에 OS에 의해 적절한 page table의 시작 주소를 입력받는다.

Assumptions

- 48-bit virtual addresses
- 40-bit physical addresses
- Page Table Entry (PTE)
    - A valid bit : PPN to VPN 매칭이 valid한 경우 1. 0이면 매칭된게 없는 것이고, 해당 vaddr로 접근시 page fault가 발생할 것
    - PPN for a VPN
    - Page table register에서 page table의 시작주소를 받아 접근, vaddr에서 VPN을 얻어 이를 index로 활용해 해당 PPN을 찾는다. Valid bit이 1인지 확인하고, 1이면 paddr을 계산 후 main memory로 접근
        - Valid bit이 0이면 interrupt 발생
    - 아래의 경우 VPN이 36이므로 2^36개의 entry가 존재. Page offset이 12bits이었으므로, PPN은 40-12=28bits. valid bit까지 고려하면 하나의 entry는 29bit이 된다. → Page table은 총 29*2^36 bits

![Untitled](https://gonnnnn.github.io/image/TIL/0531(6).png)          

### Problem #1: Large Page Tables

- 위 처럼 page table을 만들면 대충 2^38byte정도의 크기가 된다. 너무 크다.
- 심지어 저게 process 하나를 위한건데, process 수가 많으면 어우..

다음과 같은 해결방안이 있다.

- Large memory pages
    - Memory page size를 키워서 VPN, PPN 수를 줄인다.
- Inverted page tables
    - VPN이 아닌 PPN을 기반으로 만든 page table
    - 최악의 경우 Main memory를 다 훑어야하게 돼서 memory 크기가 작지 않으면 별로라고
- Mutli-level page tables
    - PPE를 group화한다.

### Mutli-level Page Tables

- Page table을 level별로 나눈다.
    - Level-0인 경우 vaddr[47:39], level-1인 경우 vaddr[38:30]에 대해 저장
- 전체 page table을 메모리에 저장할 필요가 없어진다.
    - 부분부분만 access하면 되기 때문이다.
    - 2^9개의 PTEs for level-0, 2^9개의 PTEs for level-1 …
    - Level-0의 각 PTE들은 연결되는 2^9개의 다른 Level-1의 시작 주소를 담고 있는다. 마지막 level의 page table에서 접근되는 PTE가 PPN을 담고 있는다. 트리처럼 뻗어져 나가는 것
- 프로그램이 virtual memory를 전부 다 쓴다면 효율이 떨어지는데 실제로 그러는 일은 별로 없다. Multi-lvel page table을 쓰면 virtual memory 중 쓰지 않는 곳에 대해서는 트리를 쳐내버리는 것 처럼 아예 저장하지 않으면 되기 때문에 좋다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(7).png)          

### Problem #2: Slow Page Table Accesses

Page table access는 main memory access와 같다.

- Page table은 main memory에 저장되어 있다.
- Translation할 때 마다 main memory access latency를 감수해야한다.

***Translation Lookaside Buffers (TLBs)***

- PTE를 위한 cache이다.
- SRAM으로 만든다.
- 최근에 translated된 VPN, PPN 쌍을 저장한다.
- Miss가 발생하면 main memory에 접근한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(8).png)          

### Problem #3: Which Address for $s?

생각해보면 서로 다른 프로그램들은 서로 다른 paddr을 가리키지만 같은 vaddr을 갖게될 수 있다.

***Physically-addressed caches***

- Cache는 paddr를 이용해서 접근한다. vaddr을 이용하지 않는다.
- Processor이 lw, sw instr을 실행하려고 하면, program은 vaddr은 TLB & Page Table을 통과하여 paddr을 얻게 되고, 이를 가지고서 cache & memory에 접근한다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(9).png)          

### Virtual Memory + Caches + TLBs

![Untitled](https://gonnnnn.github.io/image/TIL/0531(10).png)         

- Processor가 TLB에게 vaddr을 제공한다.
- VPN, PPN 쌍을 기반으로 paddr을 확인한다.
    - Miss라면 page table에서 해당 PTE를 가져온다.
- paddr을 가지고서 cache에 접근하고, 해당 data 등을 가져온다.

### Characterizing a Memory Hierarchy

- 시스템마다 memory hierarchy가 다르다. 어떤 경우 2 level caches를 사용할 수도 있고, 또 여러개의 secondary storage를 사용할 수도 있다.
- 상황에 따라서 더 나은 hierarchy가 있을 것이지만, 무엇이 더 나은지 비교하기 위해서는 공통된 policy와 feature를 정의해야한다.

### Questions for the Characterization

![Untitled](https://gonnnnn.github.io/image/TIL/0531(11).png)          

- total size, block size, miss penalty, miss rate등을 design parameter로 생각해볼 수 있다.
- 하지만 다음과 같은 것도 고려해볼 수 있을 것이다.
    - Where can a block be placed? Only in main momory? or also in caches
    - How is a block found? ex) fully-associative cache의 경우 모두 scan해야함. miss가 일어났을 때는 어떻게 해야하는지 등등
    - Which block should be replaced on a miss?
    - What happens on a write?

### Where Can a Block Be Placed?

- Associativity가 높아지면 miss rate이 내려가는 경향이 있다. Fully가 가장 작고 direct mapped가 가장 높은 격
- 다만 cost가 올라가고 access time이 느려진다는 단점이 있다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(12).png)          

![Untitled](https://gonnnnn.github.io/image/TIL/0531(13).png)          

### How is a Block Found?

- 이 역시 cache에 달려있다.
- miss penalty와 cost사이에서의 trade-off를 고려해야한다.
    - PTE를 cache하는 TLB를 떠올려보자. Full associativity는 다음과 같은 이유로 좋을 수 있다.
    - TLB miss는 expensive하다. Page table은 main memory에 있기 때문이다.
    - 소프트웨어가 sophisticated한 replacement schemes를 사용하게끔 한다.
    - 추가 하드웨어 없이 full map이 index될 수 있기 때문이다.

→ 2, 3번째 이유는 뭔소린지는 잘 모르겠다.

** data cache는 set associative 자주 쓴다고

### Which Block Should be Replaced?

- Random vs Least-Recently Used (LRU)
    - Random하게 고르기 vs사용된지 가장 오래된 애를 고르기
    - 요즘에는 random하게 많이 한다고 한다.
- LRU는 associativity가 작을 때 쓰고, random은 큰거에 쓴다.
    - LRU는 block마다 가장 최근 accessed time을 track해야한다.

### What Happens on a Write?

- Write-through, write-back을 배웠다. 별거 없다.

### The Three “C”s

모든 miss들은 3개의 C로 분류될 수 있다.

- Compulsory misses
    - First access에 의해 발생하는 miss
    - Cold miss라고도 한다.
- Capacity misses
    - Cache가 모든 block을 담을 수 없을 때 발생한다. Cache size가 부족할 때 발생하는 것이다.
    - 프로그램 수행 시 접근하는 데이터의 양이 cache size를 넘어가는 것. 128k array에 접근하는데 32k direct mapped cache면 발생
- Conflict misses
    - 여러 block이 하나의 set을 두고 경쟁할 때 발생한다.
    - 다른 주소더라도 index bits가 같게 되면 같은 set에 위치하게 된다. 이 때문에 우연히 해당 set에 여러번 접근하게 되면 특정 set에 way가 부족하여 miss가 발생한다.
    - Fully-associative cache에서는 발생하지 않는다.

### Controller Design

직접 읽어보기

### Caches in Multiprocessors

Multi-core를 쓸 때는 어떻게 할까? 이 친구들은 memory를 공유한다.

- 각 processor는 private cache를 갖기도 한다. processor는 private cache에 우선적으로 접근한다.
- A가 0x1000의 값을 123에서 321로 바꿨다고 해보자. B가 0x1000에 접근한다면 123이 아니라 321을 봐야할 것이다.
- 정보 공유가 일어나야만 한다. Cache coherence! Read request가 있었을 때 어떤 value를 return해줘야하는지를 정의해주는 것이다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(14).png)          

### Multiprocessor Example

다음과 같은 상황이 발생했다고 하자

- 0x1000에는 321이 담겨있다.
- A가 0x1000의 값을 읽는다.
- B가 0x1000의 값을 읽는다.
- A가 0x1000에 123을 기입한다.
- B가 0x1000의 값을 읽는다.

B는  Cache coherence를 가정하면 123을, 가정하지 않으면 321을 읽는다.

![Untitled](https://gonnnnn.github.io/image/TIL/0531(15).png)          

![Untitled](https://gonnnnn.github.io/image/TIL/0531(16).png)          

### Valid-Invalid(VI) Protocol

Cache coherence는 valid-invalid protocol에 의해 implement될 수 있다.

- 사실 얘 말고도 MSI, MESI, MOESI와 같은 protocol들도 존재한다.

### Snooping Protocols

- Snooping bus는 multi processor CPU에서 서로 다른 cache들에 의해 공유되는 bus이다.
- Snooping protocol은, cache가 bus에게 traffic을 보내면, 다른 모든 cache가 해당 메세지를 듣게 되는 것이라고 한다.
- VI protocol은 snooping protocol이라고 한다.

1:41:00정도부터 정리