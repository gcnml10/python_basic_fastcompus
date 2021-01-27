### Pthread 란?
- thread 표준 API
  + POSIX 스레드 또는 Pthread(피-스레드)라고 부름
- Pthread API
  + 저수준 API로 100여개의 함수 제공
  + 복잡하지만, 유닉스 시스템 핵심 스레딩 라이브러리
  + 다른 스레딩 솔루션도 결국 Pthread를 기반으로 구현이 되어 있으므로, 익혀둘 가치가 있음

### Pthread 라이브러리
- <pthread.h> 헤더 파일에 정의
- 모든 함수는 pthread_ 로 시작
- 크게 두 가지 그룹
  + 스레드 관리: 생성, 종료, 조인, 디태치 함수 등
  + 동기화: 뮤텍스(상호배제) 등 동기화 관련 함수
- 기본 라이브러리(glibc)와 분리된 libpthread 라이브러리에 pthread 구현되어 있으므로 컴파일 시 명시적으로 -pthread 옵션 필요
```c
gcc -pthread test.c -o test
```

### 스레드 생성
```c
// thread: 생성된 스레드 식별자 (포인터와 비슷)
// attr: 스레드 특정 설정(기본 NULL)
// start_routine: 스레드 함수(스레드로 분기해서 실행할 함수)
// arg: 스레드 함수 인자

int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg);

//예제
pthread_t thread1;
void *thread_function(void *ptr);

ret = pthread_create(&thread1, NULL, thread_function, (void*)message1);  // return 값이 0이면 정상, 아니면 에러코드
```

### 스레드 종료
```c
// exit와 유사, NULL 또는 0은 정상 종료
void pthread_exit(void *retval);

//예제
pthread_exit(NULL);
```

### 스레드 조인
```c
// thread: 기다릴 스레드 식별자
// thread_return: 스레드의 리턴 값을 가져올 수 있는 포인터
int pthread_join(pthread_t thread, void **thread_return);
```
- 예제
  + p_thread 식별자를 가진 스레드의 종료를 기다리고, status 포인터로 종료값을 가져옴
```c
pthread_join(p_thread, (void *)&status);
printf("thread join: %d\n", status);
```

### 스레드 디태치
- 해당 스레드가 종료될 경우, 즉시 관련 리소스를 해제(free)한다.
  + pthread_join를 기다리지 않고, 종료 즉시 리소스를 해제한다. (스레드 리소스는 자동으로 해제되지 않음)
  + pthread_join은 메인스레드에서 종료 상태값으로 추가처리를 할 수 있음 (스레드가 끝나기 전까지 다음 코드 실행 안됨)
  + pthread_detach를 쓰면 해당 스레드가 종료될 때까지 기다리지 않고 바로 다음 코드를 실행함
```c
// thread: detach할 스레드 식별자
int pthread_detach(pthread_t thread)
```

### Pthread 뮤텍스 - 상호 배제 기법
- 임계 영역/자원 관리를 위해 쓰임
- 뮤텍스 선언과 초기화
```c
pthread_mutex_t mutex_lock = PTHREAD_MUTEX_INITIALIZER; //선언 및 초기화 시킨 것
```
- 뮤텍스 락 걸기/풀기
```c
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

### 메모리와 파일 시스템 관련
### 동적 메모리 생성하기
- heap 영역에 생성 - malloc 함수 / free() 해제

### 파일 처리 성능 개선 기법 - 메모리에 파일 매핑
```c
#include <sys/mman.h>
void *mmap(void *start, size_t length, int prot, int flags, int fd, off_t offset);
```
- [start+offset] ~ [start+offset+length] 만큼의 물리 메모리 공간을 mapping할 것을 요청
- 보통 start:NULL 또는 0 사용, offset:mapping되기 원하는 물리 메모리 주소로 지정
- prot: 보호 모드 설정
  + PROT_READ(읽기 가능)/PROT_WRITE(쓰기 가능)/PROT_EXEC(실행 가능)/PROT_NONE(접근 불가)
- flags: 메모리 주소 공간 설정
  + MAP_SHARED(다른 프로세스와 공유 가능)/MAP_PRIVATE(프로세스 내에서만 사용 가능)/MAP_FIXED(지정된 주소로 공간 지정)
- fd: device file에 대한 file descriptor

### mmap 동작 방식으로 이해하는 실제 메모리 동작 총정리
> 운영체제, 가상 메모리 이해를 기반으로 실제 활용 총정리
> 컴퓨터 공학 이해 없이는 mmap동작을 이해하기 어려움
1. mmap 실행 시, 가상 메모리 주소에 file 주소 매핑(가상 메모리 이해)
2. 해당 메모리 접근 시 (요구 페이징, lazy allocation)
  - 페이지 폴트 인터럽트 발생
  - OS에서 file data를 복사해서 물리 메모리 페이지에 넣어줌
3. 메모리 read 시: 해당 물리 페이지 데이터를 읽으면 됨
4. 메모리 write 시: 해당 물리 페이지 데이터 수정 후, 페이지 상태 flag중 dirty bit를 1로 수정
5. 파일 close 시: 물리 페이지 데이터가 file에 업데이트됨(성능 개선)

### 파일, 메모리, 그리고 가상 메모리
- 장점
  + read() write() 시 반복적인 파일 접근을 방지하여 성능 개선
  + mapping 된 영역은 파일 처리를 윟나 lseek()(file에서 data주소를 찾아감)을 사용하지 않고 간단한 포인터 조작으로 탐색 가능  
    메모리에 올려 놓았기 때문에 메모리 변수에 접근하듯 빠르게 접근 가능
- 단점
  + mmap은 페이지 사이즈 단위로 매핑
    * 페이지 사이즈 단위의 정수배가 아닌 경우, 한 페이지 정도의 공간 추가 할당 및 남은 공간을 0으로 채워주게 됨

### 파일 처리 성능 개선 기법 - 메모리에 파일 매핑
```c
int munmap(void *addr, size_t length)
```
- *addr에 mapping된 물리 메모리 주소를 해제한다.
- length: mapping된 메모리의 크리 (mmap에서 지정했던 동일 값을 넣음)

### 파일 처리 성능 개선 기법 - 메모리에 파일 매핑
```c
int msync(void *start, size_t length, int flags);
```
- start: mmap()를 통해 리턴 받은 메모리 맵의 시작 주소
- lenght: 동기화를 할 길이. 시작 주소로 부터 길이를 지정하면 된다
- flags
  + MS_ASYNC: 비동기 방식, 동기화(Memory->File)하라는 명령만 내리고 결과에 관계 없이 다음 코드 실행(따라서, 동기화가 완료안된 상태로 다음 코드 실행 가능)
  + MS_SYNC: 동기 방식, 동기화가 될 때까지 블럭 상태로 대기
  + MS_INVALIDATE: 현재 메모리 맵을 무효화하고 파일 데이터로 갱신. File->Memory

### inode 메타데이터 - stat 함수
```c
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
int stat(const char *path, struct stat *buf);
int fstat(int filedes, struct stat *buf);
```
> fopen/read/write 등 기본 파일 시스템콜은 C언어 과목에서 다룸

### inode 방식 파일 시스템
- 프로세스에 pid가 있는 것 처럼 파일에도 inode번호가 있고 그 번호에 대응하는 inode 구조체를 가지고 있음
- Mode(파일 종류, 권한), Owner info(소유자 정보), Size(파일 사이즈), Timestamps(생성 및 수정 시간 정보)
- Direct blocks에는 어디에 해당 데이터가 저장되어 있는지 알려주는 직접 주소
- Single, Double, Triple은 간접적으로 나태내는 간접주소 (뒤로 갈수록 더더더 간접적으로)























