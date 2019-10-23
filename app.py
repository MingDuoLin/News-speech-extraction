from flask import Flask

from views.main import main as main_view

app = Flask(__name__)

app.secret_key = 'test for good'

app.register_blueprint(main_view, url_prefix='/')


# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=6060,
    )
    app.run(**config)
