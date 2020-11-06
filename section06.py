#파이썬 함수식 및 람다(lambda)

#함수 정의 방법
#def 함수명(arameter):
#code

#함수 호출
#함수명(parameter)

#함수 선언 위치 중요

#예제1

def hello(world):
    print("Hello ", world)

hello("Python!")

#예제 2
def hello_return(world):
    val = "Hello " + str(world)
    return val

str = hello_return("Python!!")
print(str)

#예제3(다중 리턴)

def func_mul(x):
    y1 = x*100
    y2 = x*200
    y3 = x*300
    return y1, y2, y3

val1, val2, val3 = func_mul(100)
print(type(val1), val1, val2, val3)

#예제4(데이터 타입 반환)
def func_mul2(x):
    y1 = x*100
    y2 = x*200
    y3 = x*300
    return [y1, y2, y3]
    
lt = func_mul2(100)
print(lt)

#예제4
# *args, *kwargs

def args_func(*args):
    # for t in args:
    #     print(t)
    for i,v in enumerate(args):
        print(i,v)
args_func('KIm', 'Park','Lee')

#kwargs

def kwargs_func(**kwargs):
    for k, v in kwargs.items():
        print(k,v)

kwargs_func(name1='kim', name2='park', name3='lee')


#전체 혼합
def example_mul(arg1, arg2, *args, **kwargs):
    print(arg1, arg2, args, kwargs)

example_mul(10,20)
example_mul(10,20, 'park', 'kim', 24, 35)

#예제5
#중첩함수(클로저)

def nested_func(num):
    def func_in_func(num):
        print('>>>>>',num)
    print("in func")
    func_in_func(num+10000)

nested_func(10000)

#예제6
def func_mul3(x: int) -> list:
    y1 = x*100
    y2 = x*200
    y3 = x*300
    return [y1, y2, y3]

print(func_mul3(5))

#람다식 예제
#람다식: 메모리 절약, 가독성 향상, 코드 간결
#함수는 객체 생성 -> 리소스(메모리) 할당
#람다는 즉시 실행(Heap 초기화) -> 메모리 초기화

#일밙거 함수 -> 변수 할당
def mul_10(num: int)-> int:
    return num*10

var_func = mul_10
print(type(var_func))

print(var_func(10))


lambda_mul_10 = lambda num: num*10

lambda_mul_10 = lambda num: num*10

print(">>>>", lambda_mul_10(10))


def func_final(x, y, func):
    print(x*y*func(10))

func_final(10,10,lambda_mul_10)

print(func_final(10,10,lambda x: x*1000))