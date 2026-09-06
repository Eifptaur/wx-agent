# -*- coding: utf-8 -*-
import io

c = io.open('agent/console_html.py', encoding='utf-8').read()
if 'api.minimaxi.com/v1' not in c:
    old = "minimax:{label:'MiniMax', base:'https://api.minimax.chat/v1'"
    new = "minimax:{label:'MiniMax', base:'https://api.minimaxi.com/v1'"
    assert old in c
    c = c.replace(old, new)
    io.open('agent/console_html.py', 'w', encoding='utf-8').write(c)
    print('console minimax endpoint fixed')
else:
    print('console already ok')

p = '价目表.md'
t = io.open(p, encoding='utf-8').read()
if 'minimaxi' not in t:
    target = '| MiniMax · M2（新） | 1.0 | 8.0 | ¥0.072 | 139 |'
    assert target in t
    t = t.replace(target, target + '\n（MiniMax 端点：国内 api.minimaxi.com/v1、国际 api.minimax.io/v1；控制台预设已用国内官方地址）')
    io.open(p, 'w', encoding='utf-8').write(t)
    print('pricing note added')
else:
    print('pricing already ok')
