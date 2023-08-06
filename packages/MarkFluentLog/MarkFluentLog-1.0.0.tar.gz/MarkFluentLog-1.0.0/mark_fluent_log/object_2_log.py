import datetime
import time
import traceback


def exception_to_string(excp):
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
    pretty = traceback.format_list(stack)
    return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)


def object_to_log(args, request_id=None, log_type="默认TYPE", request_url=""):
    if isinstance(args, int) or isinstance(args, str) or isinstance(args, float):
        args = {
            'msg': args,
        }
    elif isinstance(args, dict):
        pass
    elif isinstance(args, Exception):
        args = {
            'msg': exception_to_string(args)
        }
    else:
        args = {
            'msg': '日志不支持该{}类型,请传递字符串或者可以json序列化的dict.'.format(type(args))
        }
    args.update({
        'type': log_type,
        "response_start_time": time.time(),
        'request_id': request_id,
        "request_url": request_url,
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    })
    return args
