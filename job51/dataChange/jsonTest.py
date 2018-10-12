import json
import re
import pymysql

dataList=[]

# 读取爬取下来的json格式的十个文件
def toLoad():
    messageList = []
    i = 1
    while i == 1:
        path = "E:\\Workspaces\\Pycharm\\job51\\a" + str(i) + ".json"
        f = open(path, encoding="utf-8")
        alist = json.load(f)
        print("正在读取第",i,"个文件",len(alist),"条招聘信息,请稍后...")
        for x in alist:
            messageList.append(x)
        i = i + 1
    print("文件读取完毕！")
    return messageList

# 数据进行格式转换【工资】【城市地址】【工作经验】【需求人数】
def change(datalist):
    moneyFormat(dataList)
    addFormat(toLoadCity(), dataList)
    experienceFormat(dataList)
    peoplenumFormat(dataList)

# 工资进行格式转换  max min avg
# 工资: 10{'', '-万/月', '千以下/月', '元/小时', '-千/月', '万以下/年', '元/天', '万以上/年', '-万/年', '万以上/月'
# 【""为面议】先不赋值【null】
# 【不带区间（ xx以上工资取xx，xx以下工资取xx）】
# 【区间工资{'', '-千/月','千以下/月',【不变】'元/小时=/1000^^^^*30*24', '元/天'=/1000^^^^^*30,  【/1000】'-万/月=*10', '万以上/月', '万以下/年=*10^^^^/12', '万以上/年', '-万/年=/12*10'}【*10】
def moneyFormat(list):
    for x in list:
        js = x['jobsalary']
        changeN = 1
        if re.search("元", js) is not None:
            changeN = changeN / 1000
            if re.search("小时", js) is not None:  # 3-5元/小时 3.66-5.88元/小时
                changeN = changeN * 24 * 30
            if re.search("天", js) is not None:  # 元/天
                changeN = changeN * 30
        if re.search("万", js) is not None:
            changeN = changeN * 10
            # if re.match("月", js) is not None:  # 万/月
            if re.search("年", js) is not None:  # 万/年
                changeN = changeN / 12
        # if re.match("千",js) is not None: # 千/月
        # XXX - XXX
        if re.search("-", js) is not None:
            money = re.findall("(.*)-((\d|\.)*)", js)
            # print(money)  #不知道为什么会出来这个8 [('3.66', '5.88', '8')]
            min = money[0][0]
            max = money[0][1]
            x['jobsalary'] = str(round(float(min)*changeN,3))+"-"+str(round(float(max)*changeN,3))
        else:
            if js is not "":
                # XXX - 取该城市最大值
                if "以上" in js:
                    money = re.findall("((\d|\.)*)", js)
                    m=money[0][0]
                    x['jobsalary'] = str(round(float(m) * changeN,3))+"-"
                # 取该城市的最小值- XXX
                if "以下" in js:
                    money = re.findall("((\d|\.)*)", js)
                    m=money[0][0]
                    x['jobsalary'] = "-"+str(round(float(m) * changeN,3))
                # XXX
                else:
                    money = re.findall("((\d|\.)*)", js)
                    m = money[0][0]
                    x['jobsalary'] = str(round(float(m) * changeN, 3))

    #薪资的长度emmmm16.666666666666668-25.0 想用(round(x,2)保留两位小数失败    (float)(Math.round(float(min)*10*3))/(10*3)
    #错误原因 str(round(float(m),2) * changeN)  应该整体计算完毕转小数长度 str(round(float(m) * changeN,2))
    print("【薪资格式转换完毕】")

# 城市地址进行格式转换【有省没市的】【有市没省的】【有市没省的】
def addFormat(dictlist,list):
    for x in list:
        add = x['jobadd']
        add = add.replace("省", "").replace("市", "")
        if re.search("-",add) is None:
            for y in dictlist.keys():
                if add == y and add!="异地招聘" and add!="国外":#..........................【有省没市的】分配直辖市value的第一个值给-后面           广东-广州
                    x['jobadd'] = add + "-"+dictlist[y][0]
                else:
                    if add in dictlist[y]:#..............................................【有市没省的】把省Key赋到前面         广东-广州
                        x['jobadd'] = y + "-" + add
        else:
            city = re.findall("(.*?)-",add)
            for y in dictlist.keys():
                if city[0] in dictlist[y]:  # .........................................【有市没省的】把省Key赋到前面     广东-珠海-珠海高新区
                    x['jobadd'] = y + "-" + add
    print("【城市地址格式转换完毕】")

# 工作经验进行格式转换【全换成数字，无经验要求为0】{'无', '8-9', '1', '3-4', '10年以上经验', '5-7', '2'}
def experienceFormat(list):
    for x in list:
        ex = x['jobexperience']
        x['jobexperience'] = re.sub("工作经验","",ex)
        x['jobexperience'] = re.sub("年经验","",ex)
        x['jobexperience'] = re.sub("无", "0", ex)
        x['jobexperience'] = re.sub("年以上经验", "", ex)
    print("【工作经验格式转换完毕】")

# 需求人数格式转换【若干换成""】
def peoplenumFormat(list):
    for x in list:
        num = x['peoplepnumber']
        x['peoplepnumber'] = re.sub("若干","",num)
    print("【需求人数格式转换完毕】")

# 读取城市字典  发现其中竟然有【异地招聘】和【国外】加入字典
def toLoadCity():
    with open("city.txt", encoding="utf-8") as f:
        str = f.readlines()
        cityDict = {}
        for line in str:
            line = line.strip()  # 去掉/n
            aList = line.split(":")  # 将省和城市分开
            cityDict[aList[0]] = aList[1].split(" ")  # 存储在字典里
    return cityDict

# 统计所有标签的格式情况进行下一步的数据清洗格式转换操作
def statisticalFormat(list):
    jobNameSet=set()
    companynameSet=set()
    jobAddSet=set()
    jobSalarySet=set()
    jobContentSet=set()
    jobExperienceSet=set()
    educationSet=set()
    peoplepnumberSet=set()
    for x in list:
        jobNameSet.add(x['jobname'])
        companynameSet.add(x['companyname'])
        jobAddSet.add(x['jobadd'])
        jobSalarySet.add(x['jobsalary'])
        jobContentSet.add(x['jobcontent'])
        jobExperienceSet.add(x['jobexperience'])
        educationSet.add(x['education'])
        peoplepnumberSet.add(x['peoplepnumber'])
        # x['jobname'],x['companyname'],x['jobadd'],x['jobsalary'],x['jobcontent'],x['jobexperience'],x['education'],x['peoplepnumber']
    print("【打印样例招聘信息1】",list[0])
    #统计格式情况
    print("【总信息条数】：",len(list))#总信息条数（含重复的）
    print("【名称】：",len(jobNameSet))#名称
    print("【公司】：",len(companynameSet))#公司
    print("【地点】：",len(jobAddSet))#地点
    # for x in jobAddSet:
    #     if re.search("-",x) is not None:
    #         add = re.findall("(.*)-(.*)", x)
    #         bigCitySet.add(add[0][0])
    #         citySet.add(add[0][1])
    #     else:
    #         bigCitySet.add(x)
    # print(bigCitySet)
    # print(len(bigCitySet))
    # print(citySet)
    # print(len(citySet))
    print("【工资】：",len(jobSalarySet))#工资{'', '-万/月', '千以下/月', '元/小时', '-千/月', '万以下/年', '元/天', '万以上/年', '-万/年', '万以上/月'
    print("【职责描述】：",len(jobContentSet))#职责描述
    print("【工作经验】：",len(jobExperienceSet))#工作经验{'8-9年经验', '无工作经验', '1年经验', '5-7年经验', '3-4年经验', '10年以上经验', '2年经验'}
    print(jobExperienceSet)
    print("【学历】：",len(educationSet))#学历{'本科', '初中及以下', '中技', '博士', '高中', '硕士', '大专', '中专'}
    print(educationSet)
    print("【用人个数】：",len(peoplepnumberSet))#用人个数{'若干'}
    print(peoplepnumberSet)
    return jobAddSet

# statisticalFormat(toLoad())
dataList=toLoad()
change(dataList)

# 连接shujuk
# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "51job")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
a=0
for x in dataList:
    a=a+1
    jobName = str(x['jobname'])
    companyName = str(x['companyname'])
    jobAddProvince = ""
    jobAddCity = ""
    jobAddDistrict = ""
    addstr = str(x['jobadd'])
    if x['jobadd'] == "异地招聘" or x['jobadd'] == "国外":
        jobAddProvince = addstr
    else:
        add = str(x['jobadd']).split("-")
        if len(add) == 2:
            jobAddProvince = add[0]
            jobAddCity = add[1]
        else:
            jobAddProvince = add[0]
            jobAddCity = add[1]
            jobAddDistrict = add[2]
    jobSalaryMin = ""
    jobSalaryAvg = ""
    jobSalaryMax = ""
    moneystr = str(x['jobsalary'])
    if re.search("-", moneystr) is None and moneystr != "":
        jobSalaryAvg = moneystr
    if re.search("-", moneystr) is not None:
        add = str(moneystr).split("-")
        if add[0] != "":
            jobSalaryMin = add[0]
        if add[1] != "":
            jobSalaryMax = add[1]
        if add[0] != "" and add[1] != "":
            jobSalaryAvg = str(round((float(jobSalaryMin) + float(jobSalaryMax)) / 2, 2))
    jobContent = str(x['jobcontent'])
    jobWord = ""
    jobexperience = str(x['jobexperience'])
    education =  str(x['education'])
    peoplepNumber = ""
    peoplenum=str(x['peoplepnumber'])
    if peoplenum != "":
        peopleNumber = peoplenum
    print(a,type(jobName), type(companyName), type(jobAddProvince), type(jobAddCity), type(jobAddDistrict), type(jobSalaryMin), type(jobSalaryAvg), type(jobSalaryMax), type(jobContent), type(jobWord), type(jobexperience), type(education), type(peopleNumber))

    sql = "INSERT INTO 51jobData (jobName, companyName, \
      jobAddProvince, jobAddCity, jobAddDistrict, \
      jobSalaryMin, jobSalaryAvg, jobSalaryMax, \
      jobContent, jobWord, \
      jobexperience, education, peopleNumber) \
      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
        (jobName,companyName, \
        jobAddProvince,jobAddCity,jobAddDistrict, \
        jobSalaryMin,jobSalaryAvg,jobSalaryMax, \
        jobContent,jobWord, \
        jobexperience,education,peopleNumber)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
# 关闭数据库连接
db.close()
