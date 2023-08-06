""" Qiniu Settings """

from masonite import env

access_key = env('QINIU_ACCESS_KEY')
secret_key = env('QINIU_SECRET_KEY')
bucket_name = env('QINIU_BUCKET')
domain = env('QINIU_DOMAIN')
