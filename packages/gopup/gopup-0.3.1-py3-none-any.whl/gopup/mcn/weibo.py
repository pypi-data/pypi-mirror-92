#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/23 0023
# @Author  : justin.郑 3907721@qq.com
# @File    : weibo.py
# @Desc    : 微博

from crawler_weibo import Weibo


def weibo_user(user_id):
    # 微博账户数据
    return Weibo().get_weibo_user_info(user_id=user_id)


def weibo_list(user_id):
    # 微博数据
    return Weibo().get_weibo(user_id=user_id)


if __name__ == "__main__":
    tmp = weibo_list(user_id="2609084213")
    print(tmp)

