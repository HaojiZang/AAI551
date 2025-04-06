# Author: Linpeng Mao
# Date: 04/03/2025
# Description:
# 1. 登录、注册、身份验证
# 2. Tkinter 的界面交互，以及用户凭证的读写逻辑

def login_screen(root):
# 构建登录页面 UI，连接验证逻辑
# tk.Label 放提示文字：“用户名”、“密码”
# tk.Entry 输入框
# tk.Button 按钮：一个“登录”、一个“注册”
# 登录按钮：调用 validate_user() 检查账号密码
# 注册按钮：调用 register_user() 把新用户写入文件
    pass

def register_user(username, password):
# 打开 users.csv（如果不存在就创建）
# 把用户名和密码保存进去，格式如下：
#    alice,123456
#    bob,abc123
    pass

def validate_user(username, password):
# 打开 users.csv
# 逐行读取，找到和输入相符的用户名+密码
# 匹配成功则返回 True，否则 False
    pass

# 登录界面布局
# +-----------------------------+
# |    登录 / 注册 界面        |
# +-----------------------------+
# | 用户名：[___________]       |
# | 密 码：[___________]        |
# | [ 登录 ]  [ 注册 ]          |
# +-----------------------------+