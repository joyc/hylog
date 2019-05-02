# -*- coding: utf-8 -*-
"""
虚拟测试数据生成函数
"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from hylog.extensions import db
from hylog.models import Admin, Category, Post, Comment, Link


fake = Faker('zh_CN')


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='嗨森博客',
        blog_sub_title="就是个测试博客",
        name='嗨森',
        about='白天是个邮递员，晚上是个码农，养了条叫斯坦森的狗...'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):

    category = Category(name='默认')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            content=fake.text(300),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=300):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            content=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)  # 10%的未审核评论
    for i in range(salt):
        # 未审核评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            content=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
        # 管理员发表的评论
        comment = Comment(
            author='嗨森',
            email='hython@hython.com',
            site='hython.com',
            content=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            # from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            content=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='https://twitter.com/')
    facebook = Link(name='Facebook', url='https://www.facebook.com/')
    linkedin = Link(name='Linkedin', url='https://www.linkedin.com/')
    weibo = Link(name='微博', url='https://www.weibo.com/')
    db.session.add_all([twitter, facebook, linkedin, weibo])
    db.session.commit()
