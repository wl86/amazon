# -*- coding: utf-8 -*-
# import random
#
#
# def GBK2312():
#     password = ''
#     while True:
#         head = random.randint(0xb0, 0xf7)
#         body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
#         val = f'{head:x}{body:x}'
#         str = bytes.fromhex(val).decode('gb2312')
#         if str:
#             password = str
#         else:
#
#
#         return str
#
#
# for i in range(10):
#     g = GBK2312()
#     print(g)

import codecs

from twisted.python.compat import unichr

start,end = (0x4E00, 0x9FA5)

with codecs.open("chinese.txt", "wb", encoding="utf-8") as f:
 for codepoint in range(int(start),int(end)):
  f.write(unichr(codepoint))  #写出汉字
