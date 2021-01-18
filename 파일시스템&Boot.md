## 파일 시스템
- 파일 시스템: 운영체제가 저장매체에 파일을 쓰기 위한 자료구조 또는 알고리즘

### 파일 시스템이 만들어진 이유
- 0과 1의 데이터를 어떻게 저장매체에 저장할까?
  + 비트로 관리하기에는 오버헤드가 너무 큼
  + 블록 단위로 관리하기로 함 (보통 4KB)
  + 블록마다 고유 번호를 부여해서, 관리 
- 사용자가 각 블록 고유 번호를 관리하기 어려움
  + 추상적(노리적) 객체 필요: 파일
- 사용자는 파일단위로 관리
  + 각 파일에는 블록 단위로 관리
- 저장매체에 효율적으로 파일을 저장하는 방법
  + 가능한 연속적인 공간에 파일을 저장하는 것이 좋음
  + 외부 단편화, 파일 사이즈 변경 문제로 불연속 공간에 파일 저장 기능 지원 필요
    * 블록 체인: 블록을 링크드 리스트로 연결
      - 끝에 있는 블록을 찾으려면, 맨 처음 블록부터 주소를 따라가야함
    * 인덱스 블록 기법: 각 블록에 대한 위치 정보를 기록해서, 한번에 끝 블록을 찾아갈 수 있도록 함

### 다양한 파일 시스템
- Windows: FAT, FAT32, NTFS
  +블록 위치를 FAT라는 자료구조에 기록
- 리눅스(UNIX): ext2, ext3, ext4
  + 일종의 인덱스 블록 기법인 inode 방식 사용

### 파일 시스템과 시스템 콜
- 동일한 시스템콜을 사용해서 다양한 파일 시스템 지원 가능하도록 구현
  + read/write 시스템 콜 호출시, 각 기기 및 파일 시스템에 따라 실질적인 처리를 담당하는 함수 구현 (각 파일 시스템마다 다르게)
    * 예: read_spec/write_spec 
  + 파일을 실제 어떻게 저장할지는 다를 수 있음
    * 리눅스의 경우 ext3 외 NTFS, FAT32 파일 시스템도 지원 (같은 open함수를 써도 동작하도록)
    
### inode 방식 파일 시스템
- 파일 시스템 기본 구조
  + 수퍼 블록: 파일 시스템 정보
  + 아이노드 블록: 파일 상세 정보
  + 데이터 블록: 실제 데이터 (1~4KB 등 특정 고정된 사이즈)
- 수퍼 블록: 파일 시스템 정보 및 파티션 정보 포함
![](https://ifh.cc/g/vwswfY.png)

### inode와 파일 
- 파일: inode 고유값과 자료구조에 의해 주요 정보 관리
  + '파일이름:inode'로 파일 이름은 inode 번호와 매칭
  + 파일 시스템에서는 inode를 기반으로 파일 엑세스 (파일 생성 -> inode번호 -> inode블록 <--파일 처리)
  + inode 기반 메타 데이터 저장
  ![](http://web.cs.ucla.edu/classes/fall14/cs111/scribe/12d/inodeBasedFileSystem.png)
  + inode 기반 메타 데이터(파일 권한, 소유자 정보, 파일 사이즈, 생성시간 등 시간 관련 정보, 데이터 저장 위치 등)
  ![](https://linoxide.com/wp-content/uploads/2013/02/inode-data-structure.png)
  출처: <https://linoxide.com/linux-command/linux-inode/>
  ![](https://ifh.cc/g/Nba0sk.png)
  
### 디렉토리 엔트리
- 리눅스 파일 탐색: 예 - /home/ubuntu/ink.txt
  1. 각 디렉토리 엔트리(dentry)를 탐색
    + 각 엔트리는 해당 디렉토리 파일/디렉토리 정보를 가지고 있음
  2. '/'emdtry에서 'home'을 찾고, 'home'에서 'ubuntu'를 찾고, 'ubuntu'에서 link.txt 파일 이름에 해당한느 inode를 얻음
  
### 가상 파일 시스템(Virtual File System)
- Network 등 다양한 기기도 동일한 파일 시스템 인터펭스를 통해 관리 가능
- 예: read/write 시스템콜 사용, 각 기기별 read_spec/write_spec 코드 구현 (하부코드) (운영체제 내부) (어떤 기기도 연결 가능)
![](https://postfiles.pstatic.net/20141231_229/wndrlf2003_1419991758681fyiri_PNG/6.png?type=w2)
출처: <https://blog.naver.com/PostView.nhn?blogId=wndrlf2003&logNo=220225485867>

### 참고: 리눅스(유닉스) 운영체제와 가상 파일 시스템
- 모든 것은 파일이라는 철학을 따름
  + 모든 인터렉션은 파일을 읽고, 쓰는 것처럼 이루어져있음
  + 마우스, 키보드와 같은 모든 디바이스 관련된 기술도 파일과 같이 다루어짐
  + **모든 자원에 대한 추상화 인터페이스로 파일 인터페이스를 활용**
  
### 참고: 특수 파일
- 디바이스
  + 블록 디바이스(Block Device)
    : HDD, CD/DVD와 같이 블록 또는 섹터 등 정해진 단위로 데이터 전송, IO송수신 속도가 높음 (대용량)
  + 캐릭터 디바이스(Character Device)
    : 키보드, 마우스 등 byte단위 데이터 전송, IO 송수신 속도가 낮음
  + cd/dev, cat tty
  ```
  brw-r-----                disk0
  crw-rw-rw-                tty
  ```
  
  ---
  
## Bott
- 컴퓨터를 켜서 동작시키는 절차
- Boot 프로그램
  + 운영체제 커널을 Storage에서 특정 주소의 물리 메모리로 복사하고 커널의 처음 실행 위치로 PC를 가져다 놓는 프로그램
  
### 부팅 과정
- 컴퓨터를 키면
  + BIOS가 특정 Storage 읽어와 bootstrap loader를 메모리에 올리고 실행함
  + bootstrap loader 프로그램이 있는 곳을 찾아서 실행시킴
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fee3wQ2%2FbtqDAC9bSf0%2FxKM7KJaLM1aQB1qk8kpdqk%2Fimg.png)
출처:<https://clownhacker.tistory.com/4>
0. 전원이 켜진다
1. CPU가 ROM 안에 BIOS를 찾고 실행. BIOS는 HW가 이상이 없는지 체크하고 초기화 한다.
  - CPU는 전원이 들어오면 메모리에 0x0000번째 명령어를 실행하고 순차적으로 0x0001번째 명령어를 실행한다. 하지만, RAM은 휘발성 메모리이기 때문에 전원이 꺼지면 메모리에 아무것도 없다. 그 뜻은 CPU는 전우너이 들오온 시점에 0x0000번째 주소에 실행할 명령어가 없다는 것이다. 
  그래서 CPU를 위해 비휘발성 메모리인 BIOS를 0x0000에 놓는다.
2. 초기화 한 후 BIOS는 Boot loader를 찾기 위해 MBR[Master Boot Record]를 찾는다. MBR은 HDD/SSD의 첫번째 512byte에 있다.
3. MBR을 찾으면 HDD/SSD의 Boot loader가 메모리에 로딩된다. Boot loader가 실행이 되면서 초기화를 한다. (파티션 Table에 관한 정보(어디가 메인 파티션인지 등)가 MBR에 같이 들어 있고)
  - 메인 파티션에는 부트 섹터가 있고 이를 저장매체로 부터 불러온다(부트 로더가 이를 수행) (부트 섹터는 해당 파티션에서 커널 이미지의 주소를 알아냄)
4. Boot loader가 커널 이미지를 로딩한다.
5. 이 지점이 main.c가 실행 되는 지점, 즉 커널 이미지가 실행되는 지점이다.
  
### Virtual Maxhine (가상 머신)
- 하나의 하드웨어(CPU, Memory 등)에 다수의 운영체제를 설치하고, 개별 컴퓨터처럼 동작하도록 하는 프로그램
- Virtual Machine Type1 (native 또는 bare metal)
  + 하이퍼 바이저(또는 VMM): 운영 체제와 응용프로그램을 물리적 하드웨어에서 분리하는 프로세스
  + 하이퍼바이저 또는 버추얼 머신 모니터 (VMM)라고 하는 소프트웨어가 Hardware 에서 직접 구동 (Xen, Kvm)
- Virtual Machine Type2
  + 하이퍼바이저 또는 버추얼 머신 모니터 (VMM)라고 하는 소프트웨어가 Host OS 상위에 설치(VMWare, Parallels Desktop (Mac))

![](https://kyulingcompany.files.wordpress.com/2017/06/1introduction-to-virtualization-27-638.jpg)
출처:<https://kyulingcompany.wordpress.com/2017/06/22/%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%EA%B3%BC-%EB%8F%84%EC%BB%A4%EC%9D%98-%EC%B0%A8%EC%9D%B4-%EC%84%B1%EB%8A%A5%EC%9D%98-%EA%B0%80%EB%B2%BC%EC%9B%80/>

### Full Virtualization(전가상화) VS Half Virtualization(반가상화)
- 전가상화: 각 가상머신이 하이퍼바이저를 통해서 하드웨어와 통신
  + 하이퍼바이저가 마치 하드웨어인 것 처럼 동작하므로, 가상머신의 OS는 자신이 가상 머신인 상태인지를 모름
  + VMM은 통역사
- 반가상화: 각 가상머신에서 직접 하드웨어와 통신
  + 각 가상머신에 설치되는 OS는 가상머신인 경우, 이를 인지하고, 각 명령에 하이퍼바이저 명령을 추가해서 하드웨어와 통신
  + VMM은 리소스 관리만 함, 바로 요청하므로 더 빠름, 하지만 OS를 수정해야해서(명령 수정 등) 복잡도가 올라감
- VMWare: 대중적인 가상머신 프로그램 (Type2)
- KVM: AWS(아마존 클라우드 컴퓨팅 서비스) 등에서 사용 (Type1) (CPU에서 지원해줘야함, 따지고 보면 리눅스 커널)

### 또 다른 가상 머신: Docker (가상 머신 vs Docker)
- 가상 머신은 컴퓨터 하드웨어를 가상화**(하드웨어 전체 추상화)**
  + 하이퍼바이저 사용, 추가 OS 필요 등 성능 저하 이슈 존재
- Docker는 운영체제 레벨에서 별도로 분리된 실행환경을 제공**(커널 추상화)**
  + 마치 리눅스 처음 설치했을 때와 유사한 실행환경을 만들어주는 리눅스 컨테이너 기술 기반
  + 리눅스 컨테이너 기술이므로 macOS나 windows에 서치할 경우는 가상 머신 기반 제공

### 가상 머신 정리
- Bare-Metal 방식이 가장 성능이 좋음
  + 하드웨어 직접 엑세스하기 때문
  + AWS(클라우드 컴퓨팅) 환경도 Bare-Metal 기반 가상 머신 기술 활용 (KVM)
- Docker는 경량 이미지로 실행환경을 통째로 백업, 실행 가능 (실무에 많이 사용됨)
  + Data Engineering에서 Docker로 시스템 환경 설정 + 프로그램을 한번에 배포
  + 예: 프로그램 업데이트 -> Docker 이미지 작성 -> Jenkins로 배치잡 생성 및 실행 (AWS EC2 재생성 및 Docker 이미지 설치, 실행)

### Java Virtual Machine
- 가상 머신과는 다른 목적 (응용프로그램 레벨 가상화)
- Java 컴파일러는 CPU dependency를 가지지 않는 bytecode를 생성함
- 이 파일을 Java Virtual Machine에서 실행함
- 각 운영체제를 위한 Java Virtual Machine 프로그램 존재
 










  
  
  
