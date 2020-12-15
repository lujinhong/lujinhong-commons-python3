
params = {
    "name": "lujinhong",
    "age": 10
}

# ss = "My name is {name}, I am {age}".format(name = 'lujinhong', age = '10')
ss = "My name is {name}, I am {age}".format(**params)
print(ss)


words = [1,2,3,4,5,6,7,8,9]
insert_sql ='insert_sql("{1}",  "{2}",  "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{0}")'.format( *words)
print(insert_sql)

