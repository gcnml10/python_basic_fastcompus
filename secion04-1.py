#데이터 타입

v_str1 = 'Niceman'
v_bool = True
v_str2 = 'Goodboy'
v_float = 10.3
v_int =7
v_dict = {
    "name": 'Kim',
    "age": 25
}
v_list = [3,5,7]
v_tuple = 3, 5, 7
v_set = {7,8,9}

print(type(v_tuple))

i1 = 39
i2 = 939
big_int1 = 999999999999999999999
big_int2 = 7777777777777
f1 = 1.123
f2 = 3.423
f3 = .5
f4 =  10.

print(big_int1*big_int2)

result = f3 + i2
print(result,type(result))

a = 5.
b =4

print(type(a),type(b))
result2 = a +b
print(result2)


print(int(result2))
print(complex(3))
print(int(True))
print(int(False))
print(int('3'))
print(complex(False))

y = 100
y += 100
print(y)

#수치연산함수
print(abs(-7))
n, m = divmod(100, 8)
print(n, m)

import math

print(math.ceil(5.1))
print(math.floor(3.454))
