
#get input
n = input()
ar = map(int,raw_input().split())
max_number=101	# max_number of any element in ar, assuming min=0

xlist = [0] * max_number
for x in ar:
    xlist[x]+=1
	
# now do stuff with xlist
print sum(xlist)-max(xlist)
