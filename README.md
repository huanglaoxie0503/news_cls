爬虫数据写入到 ElasticSearch

1、使用 ElasticSearch 5.1.1 中文发行版，针对中文集成了相关插件，方便学习测试.

2、ElasticSearch-head

3、kibana-5.1.1

----
破解财联社sign标签加密
```python
import time
from hashlib import sha1
from hashlib import md5

dt = int(time.time())

a = "app=CailianpressWeb&hasFirstVipArticle=1&last_time={0}&os=web&refresh_type=0&rn=20&subscribedColumnIds=&sv=6.8.0".format(dt)


def get_sign(keywords):
    # 首先sha1加密
    psw = sha1()
    psw.update(keywords.encode('utf8'))
    s_pwd_sha1 = psw.hexdigest()
    # sha1加密结果再次md5加密
    hash_md5 = md5(s_pwd_sha1.encode('utf8'))
    psw = hash_md5.hexdigest()
    return psw


if __name__ == '__main__':
    sign = get_sign(a)
    print(sign)

```