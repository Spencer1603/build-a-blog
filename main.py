from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:BlogTime@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
       
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email
'''

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
       
    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<%r \n %r>' % (self.title, self.body)

@app.route('/blog', methods=['GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id is not None:
        blog = Blog.query(id=blog_id)
        return render_template('dynamic_blog.html', site_title=Blog.title, 
            blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', site_title="Blog Listings", 
            blogs=blogs)


@app.route('/newpost', methods=['GET'])
def newpost():
    
    return render_template('newpost.html', site_title="Create a Blog Post")

@app.route('/newpost', methods=['POST'])
def validate_newpost():
    blog_title = request.form['blog_title']
    blog_body = request.form['blog_body']

    title_error = ""
    body_error = ""

    if blog_title == "":
        title_error = "Please enter a title"
    if blog_body == "":
        body_error = "Please enter a body"

    if blog_title == "" or blog_body == "":
        return render_template('newpost.html', site_title="Create a Blog Post", 
        blog_title=blog_title, title_error=title_error, 
        blog_body=blog_body, body_error=body_error)

    new_blog = Blog(blog_title, blog_body)
    db.session.add(new_blog)
    db.session.commit()
    
    return redirect('/blog')


if __name__ == '__main__':
    app.run()