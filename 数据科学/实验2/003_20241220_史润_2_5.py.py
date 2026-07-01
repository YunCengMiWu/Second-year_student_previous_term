# 建立个人信息字典
my_info = {
    "姓名": "张三",
    "年龄": 20,
    "学号": "20241220",
    "年级": "大一",
    "班级": "01班",
}
my_info["性别"] = "男"  # 字典中加入性别信息
age_str = str(my_info["年龄"])
print(
    f"年龄（字符串类型）: {age_str}, 类型: {type(age_str)}"
)  # 从字典中输出年龄（字符串类型）

student_id = my_info.pop("学号")
print(f"被删除的学号: {student_id}")  # 从字典中输出学号，并从字典中删除

keys = list(my_info.keys())
third_key = keys[2]
print(f"第三个key: {third_key}")  # 从字典中输出第三个key

my_info["班级"] = "数据科学04班"  # 更新班级信息，"01班" 改为 "数据科学04班"
print("操作后的字典:", my_info)  # 打印最终的字典
