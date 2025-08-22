a=[1,1]
i=0
while len(a) <= 9:
    b = a[i]+a[-1]
    a.append(b)
    i+=1
    print (a)
