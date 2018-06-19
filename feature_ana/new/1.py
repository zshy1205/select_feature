import copy
dic = {2:3}
dd = {4:5}

dic = dd
print dd
print dic

dd[5] = 32
print dic

aa = [1,2]
bb = copy.copy(aa)
aa.append(3)
print aa, bb

