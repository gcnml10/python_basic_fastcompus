#파이썬 클래스 상세이해
#self, 클래스, 인스턴스 변수

#클래스, 인스턴스 차이 중요
#네임스페이스: 객체를 인스턴스화 할 때 저장된 공간
#클래스 변수: 직접 사용 가능, 객체 보다 먼저 생성
#인스턴스 변수: 객체마다 별도로 존재, 인스턴스 생성후 사용

#선언
# class 클래스명:
#     함수
#     함수
#     함수

# 예제1
class UserInfo:
    def __init__(self, name):
        self.name = name
    def user_info_p(self):
        print("Nmae: ", self.name)


user1 = UserInfo('Kim')
print(user1.name)
user1.user_info_p()
user2 = UserInfo('Park')
user2.user_info_p()

print(id(user1))
print(id(user2))

print(user1.__dict__)
print(user2.__dict__)

#예제2
#self의 이해
class SelfTest:
    
    def function1():
        print('function1 called!')
    
    def function2(self):
        print(id(self))
        print('function2 called!')    

self_test = SelfTest()
SelfTest.function1()
self_test.function2()

print(id(self_test))
SelfTest.function2(self_test)

#예제3
#클래스 변수, 인스턴스 변수

class WareHouse:
    #클래스 변수
    stock_num = 0
    def __init__(self, name):
        self.name = name
        WareHouse.stock_num += 1
    def __del__(self):
        WareHouse.stock_num -= 1

user1 = WareHouse('Kim')
user2 = WareHouse('Park')
user3 = WareHouse('Lee')

print(user1.__dict__)
print(user2.__dict__)
print(user3.__dict__)
print(WareHouse.__dict__) #클래스 네임 스페이스, 클래스 변수(공유)

print(user1.stock_num)
print(user2.stock_num)
print(user3.stock_num)

del user1
print(user2.stock_num)
print(user3.stock_num)
 