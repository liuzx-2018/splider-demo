import pymysql
conn = pymysql.connect(host='192.168.1.69', user='noah', passwd="noah", db='competition')
cur = conn.cursor()
cur.execute("SELECT * FROM tab_user")
for r in cur:
  print(r)
cur.close()
conn.close()