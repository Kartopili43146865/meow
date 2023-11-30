from werkzeug.utils import secure_filename
from form import addPost, editPost
import os
from models import Product
from extensions import app, render_template, db, redirect


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
            filename = secure_filename(form.img.data.filename)
            new_product = Product(title=form.title.data, img=f'./static/images/{filename}')
            form.img.data.save(os.path.join(app.root_path, './static/images', filename))
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')

    return render_template('addpost.html', form=form)

# edit page
@app.route('/edit<int:product_id>', methods=["GET","POST"])
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
def delete(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')