import uuid
from queue import Queue, Empty
from flask import g, request
from fluent import sender
from elasticapm.contrib.flask import ElasticAPM
from mark_fluent_log.object_2_log import object_to_log


class MarkFluentLog(object):
    """基于fluent的logger插件,和Flask的请求绑定"""

    def __init__(self, app, tag, host, apm_token, port=24224):
        self.app = app
        self.init_app(app)
        # Unbounded queue for sent events
        self.queue = Queue()

        self.tag = tag
        self.host = host
        self.port = port
        verbose = False
        self._sender = sender.FluentSender(
            tag, host=host, port=port, verbose=verbose)

        # ---------APM代理-----------------
        app.config['ELASTIC_APM'] = {
            # 设置所需的服务名称。允许使用的字符：
            # a-z、A-Z、0-9、-、_ 以及空格
            'SERVICE_NAME': 'iwrs_api',
            # # APM Server 需要令牌时使用
            'SECRET_TOKEN': apm_token,
            # # 设置定制 APM Server URL（默认值：http://localhost:8200）
            'SERVER_URL': 'http://127.0.0.1:8200',
        }
        apm = ElasticAPM(app)
        # ---------APM代理-----------------

    def error(self, args):
        self._sender.emit("error",
                          object_to_log(args, request_id=g.request_id, log_type=g.log_type, request_url=request.url))
        # self.queue.put(("error", object_to_log(args, request_id=g.request_id, log_type=g.log_type)))

    def info(self, args):
        # 打印Bug
        # self.queue.put(("info", object_to_log(args, request_id=g.request_id, log_type=g.log_type)))
        self._sender.emit("info",
                          object_to_log(args, request_id=g.request_id, log_type=g.log_type, request_url=request.url))

    def init_app(self, app):
        app.before_request(self.register_before_request)
        # after_request: 每一个请求之后绑定一个函数，如果请求没有异常。
        # app.after_request(self.send_events)
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.send_events)
        else:
            # teardown_request: 每一个请求之后绑定一个函数，即使遇到了异常
            app.teardown_request(self.send_events)

    def register_before_request(self):
        g.request_id = str(uuid.uuid4()).replace('-', '')
        g.logger = self
        g.log_type = "API默认TYPE"
        path = request.path
        if path.startswith('/api/v1.0/ert'):
            g.log_type = "ert"
        elif path.startswith('/api/v1.0/epro'):
            g.log_type = "epro"
        elif path.startswith('/api/v1.0/luck_draw'):
            g.log_type = "luck_draw"
        elif path.startswith('/api/v1.0/edc'):
            g.log_type = "edc"

    def send_events(self, exception):
        """
        请求结束后推送所有的该请求的数据,有可能会丢失某个请求的所有事件
        """
        pumping = True
        while pumping:
            try:
                tag, evt = self.queue.get_nowait()
                self._sender.emit(tag, evt)
                self.queue.task_done()
            except Empty:
                pumping = False
            except Exception as e:
                # 这样处理不是很优雅，但更糟糕的是由于日志问题而破坏了请求。
                # print(e)
                self.queue.task_done()
        return exception
