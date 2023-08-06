# masonite-qiniu

# 安装

## pip

```shell
pip install masonite-qiniu
```

## 增加服务提供者

`config/providers.py`

```python
from masonite.qiniu.providers import QiniuProvider

PROVIDERS = [
    # Application Providers
    QiniuProvider,
]
```

## 推送`config/qiniu.py`文件 (可选)

```shell
craft publish QiniuProvider
```

## `.evn` 增加配置

`.env`

```.dotenv
QINIU_DOMAIN=
QINIU_ACCESS_KEY=
QINIU_SECRET_KEY=
QINIU_BUCKET=
```

# 使用

```python
from masonite.qiniu import Qiniu


def start(self, qiniu: Qiniu):
    # 或使用容器
    # qiniu = container().make('Qiniu')

    # 获取配置信息
    secret_key = qiniu.secret_key
    access_key = qiniu.access_key
    bucket_name = qiniu.bucket_name
    domain = qiniu.domain
    
    q = qiniu.q()

    # 获取上传token
    token = qiniu.upload_token('key')

    # 空间资源管理
    bucket = qiniu.bucket()

    # CDN相关
    cdn = qiniu.cdn()
```

# todo
- [x] 第一个版本
- [ ] 让其更人性化一点
- [ ] 重写部分需要单独传递 `bucket_name` 的接口