import sqlite3
import os
# 连接到SQLite数据库
# 如果文件不存在，会自动在当前目录创建:
# 创建一个Cursor:
#想导入制定文件须在外部定义一个全局变量，否则在sqlite.connect括号定义则认为在当前项目路径下
db = r"D:\competition.db"
conn = sqlite3.connect(db)
cursor=conn.cursor()
#查询语句
cursor.execute('select * from tab_demo where id=?', ('1',))
values=cursor.fetchall()
print(values)
cursor.close()
conn.close()