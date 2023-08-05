import json
import logging
from flask import abort, Response

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class Parameter():
    def __init__(self, request):
        self.method = request.method  # 请求方法
        self.headers = dict(request.headers)  # 请求头
        # GET方法的取参
        self.param_url = request.args
        # 非GET方法取值
        try:
            self.param_json = json.loads(
                request.get_data(as_text=True)
            )
        except json.decoder.JSONDecodeError:
            self.param_json = {}
        # 表单提交取值
        self.param_form = request.form

    def get_content(self) -> dict:
        return {
            'method': self.method,
            'headers': self.headers,
            'param_url': self.param_url,
            'param_json': self.param_json,
            'param_form': self.param_form
        }

    def verification(self, checking: dict, verify: dict, optional: dict = {}) -> bool:
        for opt_k, opt_v in optional.items():
            # 没有选填参数时，填充预设的默认值
            if not checking.__contains__(opt_k):
                checking[opt_k] = opt_v
        if not set(verify.keys()).issubset(set(checking.keys())):
            json_data = {'All Parameters': {}, 'Optional': optional}
            for k, v in verify.items():
                json_data['All Parameters'][k] = str(v)
            logging.warning('请求参数不完整: {0}'.format(json.dumps(json_data)))
            abort(Response(json.dumps(json_data), 400, {}))
        for _k, _v in checking.items():
            try:
                if type(_v) != verify[_k]:
                    str_data = f'参数 {_k} 应该是 {verify[_k]} 类型'
                    logging.warning('请求参数类型校验失败: {0}'.format(str_data))
                    abort(Response(str_data, 400, {}))
            except KeyError as err:
                str_data = f'有多余的参数 {err}'
                logging.warning('多余的请求参数: {0}'.format(str_data))
                abort(Response(str_data, 400, {}))
        return True
