import os

from masonite.provider import ServiceProvider
from masonite.helpers import config

from .. import QiniuServer


class QiniuProvider(ServiceProvider):
    wsgi = False

    def register(self):
        config_path = os.path.join(os.path.dirname(__file__), '../configs')

        self.publishes({
            os.path.join(config_path, 'qiniu.py'): 'config/qiniu.py'
        }, tag="config")

        server = QiniuServer(config('qiniu.access_key'),
                             config('qiniu.secret_key'),
                             config('qiniu.bucket_name'),
                             config('qiniu.domain'))

        self.app.bind('QiniuServer', server)

    def boot(self, qiniu: QiniuServer):
        self.app.bind('Qiniu', qiniu)
