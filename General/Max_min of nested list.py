
nested_list=[["winner",10],["loser",0]]

print max(nested_list, key=lambda x: x[1])
print min(nested_list, key=lambda x: x[1])
