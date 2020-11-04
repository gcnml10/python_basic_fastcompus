
#파이썬 데어터 타입

#리스트(순서, 중복, 수정, 삭제)

a=[]
b= list()
c = [1,2,3,4]
d = [10, 200, 'pan', 'banana']
e = [10, 2000, [10, 200, 'pan', 'banana']]

#인덱싱
print(d[3])
print(d[-2])
print(d[0]+d[1])
print(e[-1][-2])

#슬라이싱
print(d[0:2])
print(e[2][1:3])

#연산
print(c+d)
print(c*3)
print(str(c[0])+'hi')

#리스트 수정 삭세
c[0] = 77
print(c)

c[1:2] = [100,1000,1000]
print(c)
c[1] = ['a', 'b', 'c']
print(c)

del c[1]
print(c)
print('\n\n')
#리스트함수
y = [5,3,4,2,5]
print(y)
y.append(6)
print(y)
y.sort()
print(y)
y.reverse()
print(y)
y.insert(2,7)
print(y)
y.remove(2)
print(y)
y.remove(7)
print(y)
y.pop()
print(y) #LIFO
ex = [88,77]
y.extend(ex)
print(y)

#튜플 (순서 중복 수정x 삭제x)
a = ()
b = (1,)
c = (1,2,3,4)
d = (10, 100, ('a', 'b', 'c'))

print(c[2])
print(c[3])
print(d[2][2])

print(d[2:])
print(d[2][0:2])

print(c+d)

#튜플 함수
z = (5,4,3,2,1)

print(z)
print(3 in z)
print(z.index(5))
print(z.count(1))