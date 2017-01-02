py -3 manage.py shell
db.create_all()
user=User(username='yoyo4')
user1=User(username='yoyo')
user2=User(username='yoyo')
user3=User(username='yoyo')
user4=User(username='yoyo')
user5=User(username='yoyo21')
user6=User(username='yoyo21')
user7=User(username='yoyo1')
user8=User(username='yoyo121')
user9=User(username='yoyo1')
user10=User(username='yoy121')
user11=User(username='yoy12121')
user12=User(username='yoy2121')
user13=User(username='yoy2121')
user14=User(username='yoy2121')
user15=User(username='yoy21')

db.session.add(user)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(user6)
db.session.add(user7)
db.session.add(user8)
db.session.add(user9)
db.session.add(user10)
db.session.add(user11)
db.session.add(user12)
db.session.add(user13)
db.session.add(user14)
db.session.add(user15)
db.session.commit()
User.query.all()

User.query.filter(
    User.id>3
).all()

#修改
User.query.filter_by(username='yoyo42').update({'password':'test'})
#删除
user=User.query.filter_by(username='yoyo42').first()
db.session.delete(user)
db.session.commit()

user=User.query.get(1)
new_post=Post('post title')
new_post.user_id=user.id
db.session.add(new_post)
db.session.commit()
user.posts

third_post=Post('third Title')
user.posts.append(third_post)
db.session.add(third_post)
db.session.commit()
user.posts

post_one=Post.query.filter_by(title='post title').first()
post_two=Post.query.filter_by(title='third Title').first()
tag_one=Tag('Python')
tag_two=Tag('SQLALchemy')
tag_three=Tag('Flask')
post_one.tags=[tag_two]
post_two.tags=[tag_one,tag_two,tag_three]
tag_two.posts
db.session.add(post_one)
db.session.add(post_two)
db.session.commit()

# 新建一个user
user=User('yao631029659')
db.session.add(user)
db.session.commit()
# 选中它
userk=User.query.filter_by(username='yao631029659').first()
# 新建一个post
new_post=Post('is well hanson')
# 在new_post的列里面新增 user.posts也可以查到
new_post.user_id=userk.id
db.session.add(new_post)
db.session.commit()