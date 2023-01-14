import math

a = [10, 10.001, 10.49999, 10.5, 10.5001, 10.777777, 10.9999]
result1 = []
result2 = []
result3 = []

for i in a:
    result1.append(int(i))  # int 去尾法 及舍掉小数位
    result2.append(round(i))  # round 四舍五入
    result3.append(math.ceil(i))  # math.ceil 进一法 加一取整

print("去尾法的结果是： ", result1)
print("四舍五入的结果是： ", result2)
print("进一法的结果是： ", result3)
