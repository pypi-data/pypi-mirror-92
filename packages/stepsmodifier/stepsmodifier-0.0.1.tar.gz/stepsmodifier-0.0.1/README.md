(1) Call function:

    from stepsmodifier.xiaomi import *
    Xiaomiyundong().run(account, password, steps, proxies)
    
(2) Parameter description:

    account --> must be a xiaomiyundong account, not a xiaomi account
    password --> password of xiaomiyundong account
    steps --> steps you want to modify, it's better not to exceed 100000
    proxies --> if you want to modify a large number of accounts, you'd better use proxy IP
    
    
(3) Parameters returned:
    
    {'code': code, 'msg': msg}
    code: 200 or -1 (200: success / -1: failed)
    msg: tips of status