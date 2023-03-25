#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tkinter as tk
import json
import datetime
import webbrowser
import pandas as pd

def calculate_gift_difference():
    # 获取包裹礼物变化前、后状态和查询的礼物 ID 的内容
    before_content = before_input.get("1.0", 'end-1c')
    after_content = after_input.get("1.0", 'end-1c')
    giftids_content = giftids_input.get("1.0", 'end-1c')
    # 将内容解码为 JSON 对象
    before = json.loads(before_content)
    after = json.loads(after_content)
    # 将礼物 ID 转换为整数列表
    giftids = [int(giftid) for giftid in giftids_content.strip().split("\n")]
    # 从 JSON 对象中提取礼物 ID 和数量，存储在字典中
    
    before_dict = {item.get("giftid") or item.get("id", 0): item.get("count", 0) for item in before["packageList"]}
    after_dict = {item.get("giftid") or item.get("id", 0): item.get("count", 0) for item in after["packageList"]}
    # 初始化结果字符串
    result_str = "当前查询时间：" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n"
    # 遍历查询的礼物 ID
    for giftid in giftids:
        # 获取礼物数量的变化情况
        before_count = before_dict.get(giftid, 0)
        after_count = after_dict.get(giftid, 0)
        count_difference = after_count - before_count
        expired_time = 0
        # 在 after 字典中查找该礼物对应的 mapExtra 字典
        for item in after["packageList"]:
            if item["giftid"] == giftid:
                map_extra = item.get("mapExtra", {})
                # 获取该礼物的 expired_time
                expired_time = int(map_extra.get("expire_time", 0))
                break
        # 根据礼物数量的变化情况生成结果字符串
        if count_difference >= 0:
            result_str += "礼物ID：{:<10} 原来{}个，现在{}个，相比增加{}个".format(giftid, before_count,after_count, count_difference)
            if expired_time > 0:
                result_str += " 剩余有效期：{}s".format(expired_time)
            result_str += "\n"
        else:
            result_str += "礼物ID：{:<10} 原来{}个，现在{}个，相比减少{}个".format(giftid, before_count,after_count, abs(count_difference))
            if expired_time > 0:
                result_str += " 剩余有效期：{}s".format(expired_time)
            result_str += "\n"

    result_text.config(state="normal")
    result_text.insert("end", result_str + "\n")
    result_text.see('end')
    result_text.config(state="disabled")

def clear_input():
    before_input.delete("1.0", "end")
    after_input.delete("1.0", "end")
    giftids_input.delete("1.0", "end")

root = tk.Tk()
root.title("包裹礼物数量变化计算")

frame1 = tk.Frame(root)
frame1.pack(padx=10, pady=10, fill="both", expand=True)
before_label = tk.Label(frame1, text="输入包裹礼物变化前的json：", font=("Arial", 10), padx=4, pady=4)
before_label.pack(side="top", anchor="w")
before_input = tk.Text(frame1, height=8, font=("Arial", 10))
scrollbar = tk.Scrollbar(frame1, orient="vertical", command=before_input.yview)
scrollbar.pack(side="right", fill="y")
before_input.pack(side="right", fill="x", expand=True)
before_input.config(yscrollcommand=scrollbar.set, wrap="word")
scrollbar.config(command=before_input.yview)

frame2 = tk.Frame(root)
frame2.pack(padx=10, fill="x", pady=8)
after_label = tk.Label(frame2, text="输入包裹礼物变化后的json：", font=("Arial", 10))
after_label.pack(side="top", anchor="w")
after_input = tk.Text(frame2, height=8, width=50, font=("Arial", 10))
scrollbar = tk.Scrollbar(frame2, orient="vertical", command=before_input.yview)
scrollbar.pack(side="right", fill="y")
after_input.pack(side="right", fill="x", expand=True)
after_input.config(yscrollcommand=scrollbar.set, wrap="word")
scrollbar.config(command=after_input.yview)
frame3 = tk.Frame(root)
frame3.pack(padx=10, fill="x", pady=8)

frame3 = tk.Frame(root)
frame3.pack(padx=10, fill="x", pady=8)
giftids_label = tk.Label(frame3, text="输入查询的礼物id(单行单个id)：", font=("Arial", 10))
giftids_label.pack(side="top", anchor="w")
giftids_input = tk.Text(frame3, height=8, width=50, font=("Arial", 10))
scrollbar = tk.Scrollbar(frame3, orient="vertical", command=before_input.yview)
scrollbar.pack(side="right", fill="y")
giftids_input.pack(side="right", fill="x", expand=True)
giftids_input.config(yscrollcommand=scrollbar.set, wrap="word")
scrollbar.config(command=giftids_input.yview)

frame5 = tk.Frame(root)
frame5.pack(pady=4, anchor="center")
calculate_button = tk.Button(frame5, text="计算差值", command=calculate_gift_difference, font=("Arial", 10))
calculate_button.pack(side="left", padx=4)
clear_button = tk.Button(frame5, text="清除输入", command=clear_input, font=("Arial", 10))
clear_button.pack(side="right", padx=12)

frame4 = tk.Frame(root)
frame4.pack(padx=10, fill="both", expand=True, pady=8)
result_label = tk.Label(frame4, text="礼物数量变化结果：", font=("Arial", 10))
result_label.pack(side="top", anchor="w")
result_text = tk.Text(frame4, height=16, width=50, wrap="word", font=("Arial", 10))
scrollbar = tk.Scrollbar(frame4, orient="vertical", command=before_input.yview)
scrollbar.pack(side="right", fill="y")
result_text.pack(side="right", fill="both", expand=True)
result_text.config(yscrollcommand=scrollbar.set, wrap="word")
scrollbar.config(command=result_text.yview)

root.mainloop()
