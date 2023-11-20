from flask import Flask, render_template, flash
from werkzeug.utils import secure_filename
from form import addPost
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsahsfgafisdsdf'

posts = [
    {
        'title': 'mewo meow emosje',
        'img': 'https://img.flawlessfiles.com/_r/1366x768/100/04/56/0456cafffaea918e8ea0d0ca74e2d71c/0456cafffaea918e8ea0d0ca74e2d71c.jpg',
    }
]
# home page
@app.route('/')
def home():
    return render_template('index.html', posts=posts)

# add_post page
@app.route('/add_post', methods=["GET","POST"])
def inner():
    form = addPost()
    print(form.validate_on_submit == True)
    if form.validate_on_submit:
        flash('fill imagesss')
        if form.img.data:
            filename = secure_filename(form.img.data.filename)
            new_product = {
                "title": form.title.data,
                "img": f'./static/{filename}'
            }
            form.img.data.save(os.path.join(app.root_path, 'static', filename))
            posts.append(new_product)
            return render_template('index.html', posts=posts)

    return render_template('addpost.html', form=form)

# # carts page
# @app.route('/carts')
# def carts():
#     return render_template('carts.html')

app.run(debug=True)