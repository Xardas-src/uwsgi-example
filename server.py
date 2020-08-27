from http.client import responses
import json


class Application:
    redirect_if_no_trailing_slash = True

    def __init__(self):
        self.handlers_map = {}

    def add_handler(self, path, handler_callable):
        self.handlers_map[path] = handler_callable

    def __call__(self, env, start_response):
        # def application(env, start_response):
        print(env)
        path = env['PATH_INFO']
        #status_code = 200

        if not path.endswith("/") and self.redirect_if_no_trailing_slash:
            handler = self.redirect_trailing_slash_handler
        else:
            handler = self.handlers_map.get(path, self.not_found_handler)

        response = handler(env)
        response_body = ''
        response_headers = {'Content-Type': 'text/html'}
        if 'text' in response:
            response_body = response['text']
        elif 'json' in response:
            response_body = json.dumps(response['json'])
            response_headers = {'Content-Type': 'text/json'}

        status_code = response.get('status_code', 200)
        extra_header = response.get('extra_header', {})

        response_headers.update(extra_header)

        start_response(
            '{} {}'.format(
                status_code,
                responses[status_code]
            ),
            list(response_headers.items()),
        )
        return [response_body.encode('utf-8')]

    @staticmethod
    def not_found_handler(env):
        return {
            'text': 'Not found',
            'status_code': 404,
        }

    @staticmethod
    def redirect_trailing_slash_handler(env):
        path = env['PATH_INFO'] + "/"
        return {
            'extra_header': {'Location': path},
            'status_code': 301,
        }
