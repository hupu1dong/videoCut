s ='r,f,s,h,s,h,h,s,f,f,f'
s2 = s.split(",")
print(len(s2))
r = 0
f = 0
s = 0
h = 0
for i in s2:
    if i=='r':
        r+=1
    if i=='f':
        f+=1
    if i=='s':
        s+=1
    if i=='h':
        h+=1

print("r的个数：",r)
print("f的个数：",f)
print("s的个数：",s)
print("h的个数：",h)
