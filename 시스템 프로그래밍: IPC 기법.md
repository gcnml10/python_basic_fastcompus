### 다양한 IPC 기법
- IPC: InterProcess Communcation
1. file 사용
2. Message Queue
3. Shared Memory
4. Pipe
5. Signal
6. Semaphore
7. Socket
(2~7은 커널 공간의 공유를 바탕으로)
  ...

### 파이프
- pipe(파이프)
  + 기본 파이프는 단방향 통신, 커널 영역에 pipe 생성
  + fork()로 자식 프로세스 만들었을 때, 부모와 자식간의 통신
- 예제
```c
char* msg = "Hello Child Process!";
int main()
{
    char buf[255];
    int fd[2], pid, nbytes;
    if (pipe(fd) < 0) // pipe(fd) 로 파이프 생성
        exit(1);
    pid = fork(); // 이 함수 실행 다음 코드부터 부모/자식 프로세스로 나뉘어짐
    if (pid > 0) { // 부모 프로세스에는 자식 프로세스 pid값이 들어감
        write(fd[1], msg, MSGSIZE); //fd[1]에 씁니다.
        exit(0);
    }
    else { // 자식 프로세스에는 pid값이 0이 됨
        nbytes = read(fd[0], buf, MSGSIZE); // fd[0]으로 읽음
        printf("%d %s\n", nbytes, buf);
        exit(0);
    }
    return 0;
}
```
### 메시지 큐(message queue)
- 큐이므로 기본은 FIFO 정책으로 데이터 전송
- 예제
```c
msqid = msgget(key, msgflg) // key는 1234, msgflg는 옵션
```
- msgflg 설정
  + IPC_CREAT: 새로운 키면 식별자를 새로 생성, IPC_CREAT|접근권한
  + 예: IPC_CREAT|0644 -> rw-r--r--
```c
msgsnd(msqid, &sbuf, buf_length, IPC_NOWAIT)
```
- msgflg 설정: 블록 모드(0)/비블록모드(IPC_NOWAIT)
- 메세지큐 전송 프로그램 일부 코드 예
```c
msqid = msgget(1234, IPC_CREATT|0644
msgsnd(msqid, &sbuf, buf_length, IPC_NOWAIT)
```
- 예제
```c
ssize_t msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg)
msgrcv(msqid, &rbuf, MSGSZ, 1, 0) // msgrcv 예
```
  + msgtyp 설정: 0이면 첫번째 메세지, 양수이면 타입이 일치하는 첫번째 메세지
  + msgflg 설정: 블록 모드(0)/비블록모드(IPC_NOWAIT)
- 메시지큐 수신 프로그램 일부 코드 예
```c
msqid = msgget(1234, IPC_CREAT|0644) // key는 동일하게 1234로 해야 해당 큐의 msgid를 얻을 수 있음
msgrcv(msqid, &rbuf, MSGSZ, 1, 0)

msgctl(msgid, IPC_RMID, 0); //메시지큐 삭제 명령
```

### 참고: ftok()
- ftok(): 키 생성을 위한 함수
  + path 경로명의 inode 값과 숫자값(id)를 기반으로 키 생성
  + 경로 삭제 후 재생성시 inode 값이 달라지므로, 이전과는 다른 키값이 리턴
```c
#include <sys/ipc.h>
key_t ftok(const char *path, int id);

//예
key = ftok("keyfile", 1);
id = msgget(key, IPC_CREAT|0640);
```
### IPC 기법과 커널 모드
> pipe, message queue는 모두 kernel 공간의 메모리를 사용함

### 공유 메모리(shared memory)
- 노골적으로 kernel space에 메모리 공간을 만들고, 해당 공간을 변수처럼 쓰는 방식
- message queue처럼 FIFO방식이 아니라, 해당 메모리 주소를 마치 변수처럼 접근하는 방식
- 공유 메모리 key를 가지고, 여러 프로세스가 접근 가능
- 공유 메모리 코드 예제
  1. 공유 메모리 생성
  ```c
  #include <sys/types.h>
  #include <sys/ipc.h>
  #include <sys/shm.h>
  // key: 임의 숫자 또는 ftok 함수로 생성한 키 값
  // size: 공유 메모리 크기
  // shmflg: 공유 메모리 속성
  // 리턴 값: 공유 메모리 식별자 리턴
  int shmget(key_t key, size_t size, int shmflg);
  // 예
  shmid = shmget((key_t)1234, SIZE, IPC_CREAT|0666))
  ```
  2. 공유 메모리 연결
  ```c
  #include <sys/types.h>
  #include <sys/shm.h>
  // shmid: shmget 함수로 생성한 공유 메모리 식별자
  // shmaddr: 공유 메모리 연결 주소 (보통 (char *)NULL으로 설정하면, 알아서 적절한 주소로 연결)
  // shmflg: 공유 메모리의 읽기/쓰기 권한 (0이면 읽기/쓰기 가능, SHM_RDONLY면 읽기만 가능)
  // 리턴 값: 성공시 연결된 공유 메모리의 시작 주소를 리턴
  void *shmat(int shmid, const void *shmaddr, int shmflg);
  // 예
  shmaddr = (char *)shmat(shmid, (char *)NULL, 0)
  ```
  3. 공유 메모리 해제 
  ```c
  #include <sys/types.h>
  #include <sys/shm.h>
  int shmdt(char *shmaddr); // 변수만 해제 공유 메모리는 커널에 남아있음
  ```
### 공유 메모리 읽기/쓰기
- 포인터 변수처럼 사용하면 됨
  4. 공유 메모리에서 읽기
  ```c
  printf("%s\n", (char *)shmaddr)
  ```
  5. 공유 메모리에서 쓰기
  ```c
  strcpy((char *)shmaddr, "Linux Programming")
  ```
  6. 참고: shmctl() 삭제
  ```c
  #include <sys/types.h>
  #include <sys/ipc.h>
  #include <sys/shm.h>
  // shmid: shmget 함수로 생성한 공유 메모리 식별자
  // cmd: 수행할 제어 기능 (예: IPC_RMID - shmid로 지정한 공유 메모리 제거)
  // buf: 제어 기능에 사용되는 공유 메모리 구조체의 구조
  int shmctl(int shmid, int cmd, struct shmid_ds *buf);
  // 예
  shmctl(shmid, IPC_RMID, (struct shmid_ds *)NULL);
  ```
































