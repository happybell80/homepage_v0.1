from flask import Flask, send_from_directory, render_template, url_for
import os

app = Flask(__name__, template_folder='html', static_folder='html')
# app = Flask(__name__)
# 임시 포스트 데이터 (실제로는 데이터베이스에서 가져와야 함)
posts = {
    1: {
        'title': "투자는 자산을 늘리는 모든 행위",
        'subtitle': "좋은 투자란 자산의 가치를 평가하고 싼 가격에 사서 현금흐름을 일으키며 보유하는 것.",
        'author': "JT",
        'date': "231002",
        'content': "<p>여기에 포스트 내용이 들어갑니다...</p>"
    }
}

@app.route("/hello")  #127.0.0.1
def hello_world():
    return "<p> Hello World</p>"

@app.route('/')  #127.0.0.1/css/b.css
def index():
    return "<p> Index</p>"
    # return send_from_directory('html', 'index.html') #127.0.0.1/index.html

# @app.route('/post/1')  #127.0.0.1/post/1
# def post():
#     return render_template('index.html') #127.0.0.1/index.html

# def post(post_id):
#     post_data = posts.get(post_id)
#     if post_data:
#         return render_template('post.html', post=post_data)
#     else:
#         return "Post not found", 404

@app.route('/<path:filename>')  
def serve_static(filename):
    return send_from_directory(app.static_folder, filename) #127.0.0.1/html/css/b.css

if __name__ == '__main__':
    app.run(debug=True)
