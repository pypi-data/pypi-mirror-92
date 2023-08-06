#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: main_demo.py
# @time: 2019/12/10 11:39
# @Software: PyCharm

from base64 import b64decode
from pysmx.SM2._SM2 import Verify, Sign, generate_keypair
import chardet

pk = b'BDD2bV50fogKfCTQvj253OZTEPbopv0o6hxh+2L1e16Ph2Fuon16X7Paak43ScBFrSYcgNt1wIhtW0CGyRAjkOk='
pb_bytes = b64decode(pk)
print(pb_bytes)
data = b'eyJ5c3RJRCI6IjA2MDY3MSIsImludXNlSUQiOiIwNjA2NzEiLCJvcmdJRCI6IjEwMTU4OSIsInRpbWUiOiIyMDE5LTEyLTA5VDA4OjUwOjI3IiwiaXAiOiI5OS4xNzAuMjYuNDkiLCJzYXBJRCI6IjAxMDIwMDk3IiwiZW1haWwiOiJheWluZ0BjbWJjaGluYS5jb20iLCJuYW1lIjoi5p%2bP6aKWIiwiYnIxIjoxMDE1MTMsInBhdGhOYW1lIjoi6YeN5bqG5YiG6KGML%2bS%2foeaBr%2baKgOacr%2bmDqC%2fova%2fku7blvIDlj5HlrqQiLCJncElEIjoiMDIwMjM0NTExMCIsInN5c0lEIjoxMzAzLCJvc1ZlcnNpb24iOiIiLCJwdWJWZXJzaW9uIjoiIiwicGxhdGZvcm0iOiJwYyIsInBhdGhJRCI6IjEwMTUxMy8xMDE1ODgvMTAxNTg5IiwiZGV2aWNlSUQiOiIiLCJvcmdOYW1lIjoi6L2v5Lu25byA5Y%2bR5a6kIiwiZ2VuZGVyIjoiTSJ9'
# b'eyJ5c3RJRCI6IuS4gOS6i+mAmuWPtyIsInRpbWUiOiIyMDE1LTEyLTI4VDE2OjU5OjQxIiwib3NWZXJzaW9uIjoiOS4wLjIiLCJwdWJWZXJzaW9uIjoiMTIyNDAxIiwicGxhdGZvcm0iOiJpcGFkIiwic2FwSUQiOiLlkZjlt6Xlj7ciLCJvcmdJRCI6IuacuuaehOe8luWPtyIsInBhdGhJRCI6Ii8xMDAwMDMvMDAwMDAwIiwiZGV2aWNlSUQiOiI5MzM2NjRERi03OUZBLTQxREYtODk5Qi00QTFFMjExNzcwQUMiLCJvcmdOYW1lIjoi5py65p6E5ZCN56ewIiwicGF0aE5hbWUiOiLmnLrmnoTot6/lvoTvvJov5oC76KGML1hYWOmDqC9YWFjlrqQiLCJuYW1lIjoi5aeT5ZCNIn0='

data_dict = b64decode(data)
data_str = str(data_dict)
print(data_dict)
print(chardet.detect(data_dict))
# print(data_dict.decode('utf-8'))

# data_sign = '8c0e0529ceba5eecfcd7086edd616906cf281e2526f8b827e954a500c221284a0fd51758d7bdec2041e2a1f08835208e5072cdc84c27fbdf3b5bc60950bd0265'
data_sign = 'dd5acc8d9663c8107fd8e5ef2fe7951166c79349a218747ac1867d0336ac0e92ae67985a4fecca90a0ccf1020ab66005a328465dd009c29da5c9ca97f25d2485'

pk, sk = generate_keypair()
flag = Verify(data_sign, data_str, pb_bytes)
print(flag)
