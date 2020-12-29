import sqlite3,os

db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
    os.remove(db_file)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user1 (id varchar(20) primary key, name varchar(20))')
cursor.execute('insert into user1 (id, name) values (\'1\', \'Michael\')')
cursor.rowcount
cursor.close()
conn.commit()
conn.close()


conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('select * from user1 where id=?', ('1',))
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()

db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
    os.remove(db_file)

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
cursor.close()
conn.commit()
conn.close()

def get_score_in(low, high):

    conn=sqlite3.connect(db_file)

    cursor=conn.cursor()

    try:

        cursor.execute('select * from user where score between ? and ? order by score', (low,high))

        return list(map(lambda x:x[1], cursor.fetchall()))

    finally:

        cursor.close()

        conn.close()
# 测试:
#get_score_in(80, 95)
assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)

print('Pass')