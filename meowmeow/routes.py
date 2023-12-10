from werkzeug.utils import secure_filename
from form import addPost, editPost, like, signUp, loginForm
import os
from models import Product, User
from extensions import app, render_template, db, redirect, request
from flask_login import current_user, login_required, login_user, logout_user


# posts = [
#     {
#         'title': 'mewo meow emosje',
#         'img': 'https://img.flawlessfiles.com/_r/1366x768/100/04/56/0456cafffaea918e8ea0d0ca74e2d71c/0456cafffaea918e8ea0d0ca74e2d71c.jpg',
#     }
# ]
# home page
@app.route('/')
def home():
    posts = Product.query.all()
    return render_template('index.html', posts=posts)

# add_post page
@app.route('/add_post', methods=["GET","POST"])
def inner():
    form = addPost()
    if form.validate_on_submit():
        if form.img.data:
            if current_user.is_authenticated:
                filename = secure_filename(form.img.data.filename)
                new_product = Product(
                    title=form.title.data,
                    img=f'./static/images/{filename}', 
                    like = 0,
                    username=current_user.name
                    )
                form.img.data.save(os.path.join(app.root_path, './static/images', filename))
                db.session.add(new_product)
                db.session.commit()
                return redirect('/')
            else: return redirect('/signup')

    return render_template('addpost.html', form=form)

# edit page
@app.route('/edit<int:product_id>', methods=["GET","POST"])
@login_required
def edit(product_id):
    product = Product.query.get(product_id)
    form = editPost(title=product.title)
    if form.validate_on_submit():
        product.title = form.title.data
        if form.img.data:
            filename = secure_filename(form.img.data.filename)
            form.img.data.save(os.path.join(app.root_path, './static/images', filename))
            product.img = f'./static/images/{filename}'
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form)

# delete
@app.route('/delete<int:product_id>', methods=["GET","POST"])
@login_required
def delete(product_id):
    product = Product.query.get(product_id)
    os.remove(os.path.join(app.root_path, product.img)) 
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

@app.route('/process_data', methods=['POST'])
@login_required
def process_data():
    post_id = request.form.get('post_id')
    product = Product.query.get(post_id)
    product.like += 1
    db.session.commit()
    return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = signUp()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.name == form.name.data).first()
        if existing_user:
            return 'sdda'
        else:
            new_user = User(name=form.name.data,password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/')
    return render_template('signup.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.name.data == User.name).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect('/')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')