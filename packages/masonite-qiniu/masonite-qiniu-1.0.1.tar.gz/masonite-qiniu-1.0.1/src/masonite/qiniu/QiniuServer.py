from qiniu import Auth, BucketManager, CdnManager


# https://developer.qiniu.com/kodo/sdk/python

class QiniuServer:
    secret_key = None
    access_key = None
    bucket_name = None
    domain = None

    def __init__(self, access_key, secret_key, bucket_name, domain):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.domain = domain

    def q(self):
        return Auth(self.access_key, self.secret_key)

    # 获取上传token
    def upload_token(self, key, time=3600, policy=None):
        return self.q().upload_token(self.bucket_name, key, time, policy)

    # 空间资源管理
    def bucket(self):
        return BucketManager(self.q())

    # CDN相关
    def cdn(self):
        return CdnManager(self.q())
