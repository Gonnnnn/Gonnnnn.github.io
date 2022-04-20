---
title: "Computer Architecture (1) Basics"
# lasat_modified_at: 2022-04--19T11:36
categories:
    - TIL
tags:
    - CS
    - Computer Architecture
---


# Under the Covers & Building Processors and Memory

컴퓨터 하드웨어 구성에 대해 간단하게 다뤄본다.

## 1. Components of a computer

### Processor(Datapath and Control)

- 메모리로부터 instructions이나 data를 가져온 후, data를 사용해 instructions를 실행하는 부분

### Memory

- 프로세서와 I/O 사이에서 data와 Insturctions의 중간 저장소 역할을 한다.
- Hierarchical fashion으로 organized되어 있다. (무슨 말일까)
    - ex) two-level memory hierarchy with SRAM and DRAM

*data가 메모리와 storage(SDD/HDD) 중 어느 곳에 올라갈 것인지는 OS가 정한다.

### I/O

- 메모리에 data를 쓰거나, 메모리로부터 data를 읽어온다.
- 키보드, 마우스, 모니터 등등. 메모리의 특정 부분이 특정 I/O 장치를 위해 할당되에 있고, 그 부분 data를 특정 주기로 읽어오는 식이라고 한다. 오..

## 2. Microprocessor(CPU)

### Datapath

- arithmetic operations

### Control

- Instructs the datapath, memory, and I/O devices

## 3. Interfaces

### ISAs (Instruction Set Architectures)

[설명](https://hojak99.tistory.com/537)

- 하드웨어와 가장 밑단의 소프트웨어 사이의 interface
- 하드웨어가 준비되지 않아도 소프트웨어 개발이 가능하다. 얘 덕분에
- Binary machine language program이 잘 작동하기 위해 프로그래머가 알아야 할 것들이 포함된다.
- 다음을 포함한다.
    - 하드웨어가 support할 수 있는 instructions(add operation, load data on RAM/register, copy from RAM/register ...). instructions는 processor에 의해 실행된다. Processor의 control logic부분이 이 instructions를 해석할 수 있기 때문이다! 해석된 것을 가지고 data path를 instruct할 것이다.
    - I/O 장치 조작법

### ABIs (Application Binary Interfaces)

- 시스템 소프트웨어와 응용 소프트웨어 사이의 interface
- POSIX가 리눅스에서 쓰인다.
- Application 프로그래머에게 Basic Instruction과 OS interface를 제공한다.
    - OS interface : fwrite, fread API functions. ABIs의 예이다. 이진파일을 쓰고 읽을 수 있게 해주는 함수 API이다.
- I/O, memory allocation에 관한 상세한 부분을 encapsulate 한다는 점이 중요하다. OS에 의해 결정된다. (당연하다. 이 interface의 아래부분이 system software이니까!)

## 4. How do we store data? (메모리란?!)

메모리에는 두가지가 있다! 쓰는 재료에 따라 차이가 나게 된다.

[원리 설명](https://m.blog.naver.com/ycpiglet/221984934010)

### volatile memory - 휘발성 메모리

- 전력이 중단되면 데이터가 날아간다.(덜덜)
- 우리가 일반적으로 ‘메모리 ex) DRAM’라고 칭하는 부분이다. → **Primary Memory**
- 빠르지만 용량이 작다.

### non-volatile memory - 비휘발성 메모리

- 전력이 중단되도 데이터가 보존된다!(오우!)
- HDD나 SDD가 여기에 해당된다. → **Secondary Memory**
- 느리지만 용량이 크다.

# Performance

## 1. Defining Performace

어떻게 정의해야할까? Performance metrics! 다양한게 있지만 두가지를 다룬다.

### Execution time (Response Time)

- 컴퓨터가 task를 완료하는데 드는 총 시간.
- Single user desktops에 유용.

### Throughput (Bandwidth)

- 주어진 시간내에 완료한 총 **일의 양**
- 다양한 task를 동시에 하는 Server나 WSCs에 유용.

* Execution time이 더 뛰어나면서 Throughput이 더 안좋을 수 있다! 상황에 따라 Performance metrics를 잘 정의하는게 중요하다.

### Comparing the Performance

- Performance = 1/Execution Time의 관계를 갖는다
- X is fater than Y == The execution tiime on Y is longer than the one on X