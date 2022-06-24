
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

var_comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('main_page.html', comments=var_comments)

    else:
        var_comments.append(request.form['harrie'])
        return redirect(url_for('index'))


