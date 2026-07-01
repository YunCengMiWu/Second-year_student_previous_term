current_rating = {
    "照明灯具": "1-5 安培",
    "插座": "10-16 安培",
    "空调": "15-32 安培",
    "电热水器": "20-40 安培",
    "电磁炉": "15-30 安培",
}  # 创建电气设备-额定电流范围字典
print("可用的设备类型：", list(current_rating.keys()))

print("\n查询结果：")
print(f"空调的额定电流范围：{current_rating['空调']}")  # 示例查询
print(f"电热水器的额定电流范围：{current_rating['电热水器']}")
# 交互式查询功能
print("\n----- 交互式查询 -----")
print("提示：输入'退出'可以结束查询\n")
while True:  # 循环查询功能
    device = input("请输入要查询的设备类型：")  # 获取用户输入
    if device == "退出":
        print("查询结束，谢谢使用！")  # 判断是否退出
        break

    rating = current_rating.get(device, "未找到")  # 使用get()方法安全查询，避免KeyError
    if rating != "未找到":  # get()方法第二个参数为默认值，当键不存在时返回该值
        print(f"{device}的额定电流范围是：{rating}\n")
    else:
        print(f"抱歉，未找到该设备\n")
