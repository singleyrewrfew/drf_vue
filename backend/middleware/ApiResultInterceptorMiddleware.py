import json
import logging

logger = logging.getLogger('django')


class ResponseLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 可选：只监控特定路径（留空则监控所有）
        # self.monitored_paths = ['/api/articles/', '/api/comments/']
        self.monitored_paths = []  # 空列表表示监控所有 JSON 响应

    def __call__(self, request):
        # 1. 请求先经过这里
        response = self.get_response(request)

        # 2. 视图执行完，返回结果在这里拦截
        try:
            # 只处理 JSON 格式的返回
            if "application/json" in response.get("Content-Type", ""):
                # 如果设置了监控路径，则只打印匹配的路径
                if self.monitored_paths and not any(request.path.startswith(path) for path in self.monitored_paths):
                    return response
                
                # 读取返回内容
                response_data = response.content.decode("utf-8")

                # 格式化打印（漂亮格式）
                print("=" * 80)
                print(f"📥 接口返回结果 [{request.method}] {request.path}")
                print(f"   状态码: {response.status_code}")
                try:
                    # 尝试格式化 JSON，更好看
                    json_data = json.loads(response_data)
                    print(json.dumps(json_data, ensure_ascii=False, indent=2))
                except:
                    # 不是标准 JSON 就直接打印
                    print(response_data)
                print("=" * 80)

        except Exception as e:
            print(f"中间件打印出错: {e}")

        return response
