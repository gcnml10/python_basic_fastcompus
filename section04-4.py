#파이썬 데이터 타입(자료형)
#딕셔너리, 집합 자료형

#딕셔너리(Dictionary): 순서x, 중복x, 수정, 삭세

a= {'name':'Kim', 'phone':'0102323322', 'birth':939399}
b = {0:'hello python', 1:'hello coding'}
c = {'arr':[1,2,2,4]}

print(a['name'])
print(a.get('name'))
print(a.get('address'))
print(c['arr'][1:3])

a['address'] ='seoul'
print(a)
a['rank'] = [1,2,4]

print(a.keys())
temp = list(a.keys())
print(temp[1:3])
print(a.values())
print(list(a.values()))

print(list(a.items()))
temp2 = list(a.items())
print(temp2[0][0],'-------')
print(2 in b)
print('name' in a)


#집합 set (순서x, 중복x)
a = set()
b = set([1,2,3,4,])
c = set([1,2,4,5,6,6])

print(c)

t = tuple(b)
print(t)

l = list(b)
print(l)

s1 = set([1,2,3,4,5,6])
s2 = set([4,5,6,7,8,9])

print(s1.intersection(s2))
print(s1 &s2)

print(s1 | s2)
print(s1.union(s2))

print(s1 - s2)
print(s1.difference(s2))

s3 = set([7,8,9,10])
s3.add(14)
print(s3)

s3.remove(8)
print(s3)