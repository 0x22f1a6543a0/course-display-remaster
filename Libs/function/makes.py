# -*- coding: UTF-8 -*-
import os
import time
import xlrd
import json
import datetime
from tkinter import filedialog

try:
    data = xlrd.open_workbook(filedialog.askopenfilename())
except:
    print("没有选择文件")
    exit(0)

class make:
    def __init__(self):
        self.week = ""
        self._class = {}
        self.subject = []

    def result(self):
        for i, day in enumerate(self.week):
            self._class[day] = {}
            for item in self.subject[i]:
                subject_id, subject_name, starttime, endtime = item
                self._class[day][str(subject_id)] = {
                    "subject": subject_name,
                    "starttime": starttime,
                    "endtime": endtime,
                    "enable": True
                }
        #return self._class
        return json.dumps(self._class,indent=3,ensure_ascii=False)

    def get_subject(self):
        # 声明一些奇怪の变量
        for i in data.sheet_names():
            endtime = []
            starttime = []
            data.sheet_names()
            worksheet = data.sheet_by_name(i)
            try:
                kinds = worksheet.row_values(0)
                ID = kinds.index("序号");subjects = kinds.index("课程")
                start = kinds.index("开始时间");end = kinds.index("结束时间")

                # 计算开始时间
                for s in range(len(worksheet.col_values(start))-1):
                    time_value = datetime.datetime.fromordinal(
                        datetime.datetime(1900, 1, 1).toordinal() + int(
                            worksheet.col_values(start)[1:][s]) - 2) + datetime.timedelta(
                        days=float(worksheet.col_values(start)[1:][s]) % 1)
                    truly_time = time_value.strftime('%H:%M:%S')
                    starttime.append(truly_time)
                # 计算结束时间
                for e in range(len(worksheet.col_values(end))-1):
                    time_value = datetime.datetime.fromordinal(
                        datetime.datetime(1900, 1, 1).toordinal() + int(
                            worksheet.col_values(end)[1:][e]) - 2) + datetime.timedelta(
                        days=float(worksheet.col_values(end)[1:][e]) % 1)
                    truly_time = time_value.strftime('%H:%M:%S')
                    endtime.append(truly_time)
                print(f"已经成功制作了一个标题格：{i}")
            except Exception as e:
                print(f"程序执行在标题格：{i} 时发生报错！ 指向 {type(e)} -> {e}\n")
                break
            # 封装结果
            self.subject.append(list(zip(map(int, worksheet.col_values(ID)[1:]),worksheet.col_values(subjects)[1:]
                           ,starttime,endtime)))
        return self.subject

    def get_week(self):
        print(data.sheet_names())
        if "星期一" in data.sheet_names():self.week = self.week+"Monday "
        if "星期二" in data.sheet_names():self.week = self.week+"Tuesday "
        if "星期三" in data.sheet_names():self.week = self.week+"Wednesday "
        if "星期四" in data.sheet_names():self.week = self.week+"Thursday "
        if "星期五" in data.sheet_names():self.week = self.week+"Friday "
        if "星期六" in data.sheet_names():self.week = self.week+"Saturday "
        if "星期日" in data.sheet_names():self.week = self.week+"Sunday "
        self.week = self.week.split()
        for w in self.week:
            self._class.update({w: {}})
        return json.dumps(self._class,indent=3,ensure_ascii=False)


speed = str(input("1、蜗牛解析\t2、极速解析"))
print("[*] 开始制作\n")
print("[*] 开始制作日期数据")
# 制作日期
make = make()
data1 = make.get_week()
if speed == "1":
    for i in range(len(str(data1))):
        print(str(data1)[i],flush=True,end="")
        time.sleep(0.011)
else:
    print(data1)
print("\n[+] 已经成功制作了日期数据\n")

print("[*] 开始制作简易列表\n")
# 制作初步课程
data2 = make.get_subject()
print(data2)
print(f"\n\n[+] 已经制作了简易版\n")

print("[*] 开始汇总")
# 制作最终数据
data3 = json.loads(make.result())
data4 = json.dumps(data3,indent=3,ensure_ascii=False)
if speed == "1":
    for i in range(len(str(data4))):
        print(str(data4)[i], flush=True, end="")
        time.sleep(0.001)
else:
    print(data4)

print("\n[*] 完成制作\n")

print("\n[*] 开始写入json文件……\n")
with open('../resource/class.json', 'w') as f:
    json.dump(data3,f,indent=3,ensure_ascii=False)
print("[+++] 完成！")

os.system("pause")
