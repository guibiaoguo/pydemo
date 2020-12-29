# 导入:
from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    books = relationship('Book')
    
    def __repr__(self):
        return self.name
            
class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('user.id'))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='10', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()

session = DBSession()

new_book = Book(id='8', name='book9', user_id='1')

session.add(new_book)

new_book = Book(id='9', name='book9', user_id='1')

session.add(new_book)
new_book = Book(id='10', name='book9', user_id='1')

session.add(new_book)
session.commit()

session.close()

# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='1').one()
# 打印类型和对象的name属性:
print('type:', type(user))
print('name:', user.name)
print(user.books)
# 关闭Session:
session.close()