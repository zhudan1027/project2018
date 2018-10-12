import pymysql
##工资
# changeN = 1
# if re.search("元", test) is not None:
#     changeN = changeN/1000
#     print(changeN)
#     if re.search("小时", test) is not None:  # 3-5元/小时 3.66-5.88元/小时
#         changeN = changeN * 24 * 30
#         print(changeN)
#     if re.search("天", test) is not None:  # 元/天
#         changeN = changeN * 30
# if re.search("万", test) is not None:
#     changeN = changeN * 10
#     # if re.match("月", js) is not None:  # 万/月
#     if re.search("年", test) is not None:  # 万/年
#         changeN = changeN / 12
# # if re.match("千",js) is not None: # 千/月
# if re.search("-", test) is not None:
#     money = re.findall("(.*)-((\d|\.)*)", test)
#     # print(money)  #不知道为什么会出来这个8 [('3.66', '5.88', '8')]
#     print(money[0][0])
#     print(money[0][1])
# else:
#     money = re.findall("((\d|\.)*)", test)
#     test = float(money[0][0]) * changeN
#     print(money[0][0])

# #市格式转换
# result=re.sub("、"," ",test)
# r=re.sub("市"," ",result)


# #城市Test
# #导入城市字典（用字符串分割方式练习）
# with open("city.txt",encoding="utf-8") as f:
#     str = f.readlines()
#     cityDict = {}
#     for line in str:
#         line = line.strip() #去掉/n
#         aList=line.split(":")   #将省和城市分开
#         cityDict [aList[0]] = aList[1].split(" ")   #存储在字典里
#     print(cityDict)

# #查询出不知道的城市添加到字典里
# unknowcity = set()
# for listcity in list:
#     if listcity not in bigCity:
#         if listcity not in city:
#             unknowcity.add(listcity)
# print(unknowcity)
db = pymysql.connect("localhost", "root", "123456", "51job")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
# sql = "INSERT INTO aaa (a,b,c) VALUES ( '%s', '%s' ,'%s')" % \
#       ("ddd","1254","124")
sql = "INSERT INTO data (jobName, companyName, \
    jobAddProvince, jobAddCity, jobAddDistrict, \
    jobSalaryMin, jobSalaryAvg, jobSalaryMax, \
    jobContent, jobWord, \
    jobexperience, education, peopleNumber) \
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
      ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13")
# cursor.execute('insert into test1 (name) values (%s)',['juno'])
try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()
db.close()

