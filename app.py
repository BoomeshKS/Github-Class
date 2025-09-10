# Variables & Data Types
# a = int(input())
# print(type(a))


# function
# def add(a,b):
#     return a+b
# print(add(2,3))

l = [2,4,5,6]
a = list(map(lambda x: x if x%2==0 else None,l))
print(a)