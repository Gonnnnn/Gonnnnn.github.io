---
title: "Googld Cloud Kubernetes (1) - What's Docker?"
categories:
    - TIL
tags:
    - CS
    - Google Cloud
    - Kubernetes
    - Docker
---
# 1. Docker 기본

Dockerfile 작성하고, 빌드, 실행 및 중지, 디버깅, hub에 push하는 아주 기본적인 절차에 대해 알아봤다.

```powershell
// 컨테이너 실행
docker run [container]

// 이미지 확인
docker images

// 실행중인 컨테이너 확인
docker ps

// 실행중인, 실행했던 모든 컨테이너 확인
docker ps -a

```

## 1) 빌드

### Dockerfile

```powershell
cat > Dockerfile <<EOF
# 공식 노드 런타임을 상위 이미지로 사용합니다.
FROM node:6
# 컨테이너의 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app
# 현재 디렉토리 내용을 /app에 있는 컨테이너에 복사합니다.
ADD . /app
# 컨테이너의 포트 80을 외부에 공개합니다.
EXPOSE 80
# 컨테이너가 시작될 때 노드를 사용하여 app.js를 실행합니다.
CMD ["node", "app.js"]
EOF
```

- FROM : 상위 이미지 지정
- WORKDIR : 작업 디렉토리 지정
- ADD : 현재 디렉토리의 내용을 컨테이너에 추가
- EXPOSE : 컨테이너 포트 공개, 포트 연결 허용
- CMD : 노드 명령어를 실행

### 이미지 빌드

app.js 파일 생성 후

```powershell
docker build -t node-app:0.1 .
```

- -t는 name:tag 구문을 사용하여 이미지의 이름과 태그 지정
- 이미지 이르은 node-app, 태그는 0.1
- 태그를 지정하지 않으면 태그가 기본 값인 latest로 지정되어 최신 이미지와 기존 이미지 구분이 어렵기에 태그를 추가하는 것을 권장
- `docker images`를 찍어보면 node, node-app이 모두 보인다. node를 제거하기 위해서는 node-app을 제거해야한다. node:slim, node:alpine과 같은 노드 이미지 등을 사용하면 더 작은 이미지를 제공하기에 이식성을 높일 수 있다. 뭔말인지는 모르겠다 넘어가자

## 2) 실행

```powershell
// 실행
docker run ([option]) [image_name]:[image_tag] ([command]) ([param])
docker run -p 4000:80 --name my-app node-app:0.1
// 백그라운드에서 컨테이너 시작
docker run -p 4000:80 --name my-app -d node-app:0.1

// 확인
curl http://localhost:4000

// 중단
docker stop my-app && docker rm my-app

// 컨테이너 확인
docker ps
```

- --name 플래그를 사용하면 컨테이너 이름을 지정할 수 있다.
- -p는 docker가 컨테이너의 포트 80에 호스트의 포트 4000을 매핑하도록 지시하는 플래그이다.
- 컨테이너는 터미널이 실행되는 동안 유지된다. 터미널 세션에 종속 시키지 않고 백그라운드에서 실행하려면 -d 플래그를 추가한다.
- 

## 3) 수정

위에서 만들었던 app.js를 수정하고, 다시 image를 build해보자

`docker build -t node-app:0.2 .`

실행해보면 2단계에서 기존 cache 레이어를 사용하고 있음을 알 수 있다. app.js를 변경했기에 3단계 이후부터만 레이어가 수정된다.

1, 2)와 같은 방법으로 빌드, 실행하면 된다.

## 4) 디버깅

```powershell
// 로그 확인
docker logs [container_id]
// 컨테이너가 실행중일 때 로그 확인 ---> 무슨 차이인지 아직 모르겠다.
docker logs -f [container_id]

// 실행 중인 컨테이너에서 Bash 세션을 시작해야할 때
docker exec -it [container_id] bash
	exit 을 통해 나올 수 있다.

// 컨테이너의 메타데이터 조회
docker inspect [container_id]
// 반환된 JSON의 특정 필드 검사
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container_id]
```

- `exec`의 -it 플래그는 pseudo-tty를 할당하고 stdin을 열린 상태로 유지하여 컨테이너와 상호작용할 수 있게 한다. 해당 라인을 실행해보면 `Dockerfile`에 지정된 `WORKDIR`에서 bash가 실행된 것을 확인할 수 있다.
    - tty(teletypewriter)은 리눅스 디바이스 드라이브중에서 콘솔이나 터미널을 의미한다.

## 5) 게시

```powershell

// hub으로 올릴 이미지를 복사
docker tag [old_img_name]:[old_img_tag] [hub_account]/[hub_repository]
docker tag node-app:0.2 gcr.io/[project-id]/node-app:0.2
// hub으로 push
docker push [hub_account]/[hub_repository]
```

## 6) 테스트

```powershell
// 중지 및 제거
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

// 현 excercise의 경우 노드 이미지를 제거하기 전 node:6의
// 하위 이미지들을 먼저 제거해야한다. 그냥 알아만 두자
docker rmi node-app:0.2 gcr.io/[project-id]/node-app node-app:0.1
docker rmi node:6
docker rmi $(docker images -aq) # remove remaining images
docker images

// pull
docker pull [hub_account]/[hub_repository]
docker pull gcr.io/[project-id]/node-app:0.2

// 실행 및 확인
docker run ..해당이미지..
curl http://localhost:...
```