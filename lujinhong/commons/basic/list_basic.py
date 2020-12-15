# coding=utf-8


def list_demo():
    #（一）序列通用操作
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    #1、索引
    print(l[1])
    print(l[-1], l[-4])

    #2、切片
    print(l[2:5]) #基本切片，提供2个索引来指定切片的边界，切片包含第一个索引指定的元素，但不包含第二个索引指定的元素。
    print(l[-3:-1])
    print(l[:2]) #如果切片始于序列开头，可省略第一个索引
    print(l[2:]) #同理，如果切片结束与序列末尾，可省略第二个索引
    print(l[:]) #两个索引都不指定时，则表示从开头到结尾整个序列

    print(l[1:9:2]) #第三个数字表示步长
    print(l[::2])
    print(l[::-1]) #负值表示从后往前

    #3、基本运算
    print([1, 2, 3] + [4, 5, 6]) #加法，和join类似，见join的说明
    print('hello' + ' world')
    print([1, 2, 3] * 3)

    #4、长度、最大值、最小值
    print(len(l), max(l), min(l))

    #（二）列表
    # 1、创建列表
    lst1 = [1, 2, 3] #直接使用[]来创建
    lst2 = list('hello') #使用list类创建。由于字符串是不能直接修改里面内容的，于是可以先转为列表再操作。
    print(lst1, lst2)
    print(''.join(lst2)) #反过来，将列表转为字符串。

    #2、基本操作：赋值、删除元素
    lst = [1, 1, 1]
    lst[1] = 3  #赋值
    print(lst)
    del lst[0]  #删除元素
    print(lst)
    name = list('perl')
    name[2:] = list('ar') #替换部分元素
    print(name)
    name[1:] = list('ython') #替换后的列表可以与原有列表长度不同
    print(name)
    name[1:1] = list('hello') #指定替换一个空切片，等于插入了一些元素
    print(name)

    # 3、常用函数


    #（三）元组
    t = (1, 2, 3, 4, 5)
    print(t)
    print(tuple(lst))
    print(tuple('hello'))



if __name__ == '__main__':
    list_demo()


