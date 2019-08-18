from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
    current_app,
    jsonify,
)

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """
    Index.
    """
    result = []

    return render_template('index.html', result=result)


@main.route("content", methods=('POST',))
def content():
    """
    文本解析请求.
    """
    news = request.form['content']
    print(news)

    result = [['我', '说', '你'], ['他', '说', '你']]
    return jsonify(success=True, message='Extraction Completed.', data=result)

