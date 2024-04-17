# 从 http.server 模块导入 SimpleHTTPRequestHandler 和 HTTPServer。
from http.server import SimpleHTTPRequestHandler, HTTPServer

# 定义一个名为 CORSRequestHandler 的类，它继承 SimpleHTTPRequestHandler 的类。
class CORSRequestHandler(SimpleHTTPRequestHandler):
    # 重写 end_headers 方法，这是在发送 HTTP 头部数据后调用的方法。
    def end_headers(self):
        # 添加一个 HTTP 头，允许所有的域名进行跨域请求。
        self.send_header('Access-Control-Allow-Origin', '*')
        # 调用基类的 end_headers 方法，以确保其他头部也被正常发送。
        super().end_headers()

# 定义一个名为 run 的函数，它接受三个参数：server_class、handler_class 和 port。
# 默认使用 HTTPServer 作为服务器类，CORSRequestHandler 作为处理类，端口号为 8081。
def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8081):
    # 设置服务器地址，空字符串 '' 表示服务器将监听所有可用的地址。
    server_address = ('', port)
    # 创建一个 HTTP 服务器实例，传入服务器地址和处理请求的类。
    httpd = server_class(server_address, handler_class)
    # 在控制台打印启动服务器的端口信息。
    print(f'在端口上启动服务器 {port}...')
    # 输出服务器启动成功的消息。
    print('服务器启动成功！')
    # 启动服务器，使其永久运行，直到手动停止。
    httpd.serve_forever()

# 如果这个脚本作为主程序运行，那么调用 run 函数。
if __name__ == "__main__":
    run()

