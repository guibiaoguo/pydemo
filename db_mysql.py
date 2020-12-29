import mysql.connector

conn = mysql.connector.connect(user='root', password='root', database='test')
# cursor = conn.cursor()
# # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

# cursor.execute('insert into user (id, name) values (%s, %s)', ['41', 'Michael'])
# print(cursor.rowcount)
# conn.commit()
# cursor.close()

cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('101',))
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()

def test():
    conn = mysql.connector.connect(user='root', password='root', database='test')
    cursor = conn.cursor()
    cursor.execute('insert into media (name,url,country) values (%s, %s, %s)', ['test', 'https://sexhd.co/f/mnj50i5xww0773x','Korea'])
    print(cursor.rowcount)
    conn.commit()
    cursor.close()
    conn.close()
test()