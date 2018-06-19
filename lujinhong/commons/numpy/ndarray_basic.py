import numpy as np

# 1、创建ndarray
# （1）最基本的方式
data1 = [4, 5.5, 9, 0.2, 3]
arr1 = np.array(data1)
print(arr1)
print(arr1.shape)
print(arr1.dtype)
'''
[4.  5.5 9.  0.2 3. ]
(5,)
float64
'''
data2 = [[1, 2, 3], [4, 5, 6]]
arr2 = np.array(data2)
print(arr2)
print(arr2.shape)
print(arr2.dtype)
'''
[[1 2 3]
 [4 5 6]]
(2, 3)
int64
'''
# （2）数组创建函数 P85
# array asarray arange ones/ones_like zeros/zeros_like empty/empty_like eye/identity
a1 = np.arange(15)
print(a1)
# [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14]

a2 = np.ones((4, 3))
print(a2)
'''
[[1. 1. 1.]
 [1. 1. 1.]
 [1. 1. 1.]
 [1. 1. 1.]]
'''
data = [[1, 2, 3], [4, 5, 6]]
a3 = np.zeros_like(data)  # 相同形状的全0数组
print(a3)
'''
[[0 0 0]
 [0 0 0]]
'''
a4 = np.eye(5)
print(a4)
'''
[[1. 0. 0. 0. 0.]
 [0. 1. 0. 0. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 1.]]
'''

# 2、数组类型
# numpy是同构数组，也就是说数组中的数据要求相同类型。
# 完整数据类型P86
print(a2.dtype)
# float64

print(a3.dtype)
# int64

# （1）创建数组是指定类型
a5 = np.ones((4, 3), dtype=np.int64)
print(a5.dtype)
# int64

# （2）类型转换
a6 = a5.astype(np.float64)
print(a6.dtype)
# float64


# 3、数组的基本运算
# 形状相等的数组之间的任何算术运算都会将运算应用到元素级。
# （1）数组之间的运算
arr3 = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
print(arr3 * arr3)
'''
[[ 1.  4.  9.]
 [16. 25. 36.]]
'''
# （2）数组与标量的运算
print(arr3 / 1)
print(arr3 + 1)
print(arr3 ** 0.5)
'''
[[1. 2. 3.]
 [4. 5. 6.]]
[[2. 3. 4.]
 [5. 6. 7.]]
[[1.         1.41421356 1.73205081]
 [2.         2.23606798 2.44948974]]
'''

# 4、数组索引和切片
#（1）一维数组
arr4 = np.arange(10)
print(arr4)
#[0 1 2 3 4 5 6 7 8 9]
print(arr4[2])
#2
print(arr4[2:5])
#[2 3 4]
print(arr4[:2])
#[0 1]
print(arr4[5:])
#[5 6 7 8 9]

#（2）多维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);
print(arr2d[0])
#[1 2 3]
print(arr2d[1][2])
print(arr2d[1,2])
#6 以上2种表达方式等效
print(arr2d[1:,1:])
'''
[[5 6]
 [8 9]]
'''
print(arr2d[:,:2])
'''
[[1 2]
 [4 5]
 [7 8]]
 '''
#（3）切片的赋值
#数组切片是原始数组的视图，这意味这数据不会被复制，视图是的任何修改都会直接反应到源数据中。
#因为numpy是被设计用于处理大数据量的计算的，如果复制数据会导致大量的开销。
arr4[5:8] = 5;
print(arr4)
#[0 1 2 3 4 5 5 5 8 9]
arr4 = np.arange(10)
arr4_slice = arr4[5:8]
arr4_slice[1] = 12345
print(arr4)
#[    0     1     2     3     4     5 12345     7     8     9]

# （4）布尔值索引
#只取布尔值为true的那些值
names = np.array(['Bob', 'Jason', 'Jim', 'Tom', 'Jason2'])
print(names == 'Jason')
#[False  True False False False]
scores = np.array([98, 68, 55, 30, 88])
print(scores[names == 'Bob'])
#[98]
#常用的一种情形：将<0（或者>0）的数值置为0
data = np.random.randn(7)
print(data)
#[-1.11749059  0.17593291 -1.10335147  0.55520366 -0.68369121  1.55940795  -2.80657835]
data[data < 0] = 0
print(data)
#[0.         0.17593291 0.         0.55520366 0.         1.55940795  0.        ]

# （5）花式索引 P97

# 5、数组的转置
# 还有一个函数transpose可以用于处理复杂的转置功能
arr5 = np.arange(15).reshape(3,5)
print(arr5)
'''
[[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]]
'''
print(arr5.T)
'''
[[ 0  5 10]
 [ 1  6 11]
 [ 2  7 12]
 [ 3  8 13]
 [ 4  9 14]]
'''
print(np.dot(arr5.T, arr5))
'''
[[125 140 155 170 185]
 [140 158 176 194 212]
 [155 176 197 218 239]
 [170 194 218 242 266]
 [185 212 239 266 293]]
'''
