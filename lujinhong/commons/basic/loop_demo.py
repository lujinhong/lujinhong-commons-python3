
num = 0;
while num in range(100):
    print(num)
    num += 1

names = ['jason', 'jim', 'lucy', 'lily']
for name in names:
    print(name)

i = 8
if i > 9:
    print("i is bigger than 9")
elif i < 9:
    print("i is smaller than 9")
else:
    print("i is 9")

name='Jason'
status = "friend" if name.endswith("Jason") else "stranger"
print(status)

list = ['1','2','3']
sep = '+'
result = sep.join(list)
print(result)

flag = False

try:
    x = int(input('Enter the first number:'))
    y = int(input('Enter the second number:'))
    print(x / y)
except:
    print('Error')
finally:
    del x


class FooBar:
    def __init__(self, value):
        self.somevalue = value


file = open('~/myfile.txt', '+')

file.read(5)
file.readline(5)
file.readlines()

file.write('hello\n')

import fileinput
for line in fileinput.input(file):
    print(line)



