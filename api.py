from flask import Flask,render_template,request,redirect,url_for,session
from model.model import user_exists,save_user,product_exists,add_product,products_list,remove_from_db,add_to_cart,cart_info,remove_from_cart
from wtforms import Form,StringField,PasswordField,TextAreaField,RadioField,validators
from wtforms.fields.html5 import EmailField
app=Flask(__name__)
app.secret_key='hello'
class RegistrationForm(Form):

	
	name = StringField('Name',[validators.Length(min=4,max=25)])
	username = StringField('Username',[validators.Length(min=4,max=25)])
	email =EmailField('Email address', [validators.DataRequired(), validators.Email()])
	password = PasswordField('Password',[
		validators.Length(min=4,max=25),
		validators.DataRequired(),
		validators.EqualTo('confirm',message="Passwords don't match!")
		])
	confirm = PasswordField('Confirm Password')
	account_type = RadioField('Account Type',choices=[('buyer','Buyer'),('seller','Seller')])
	#message has been initialized in _messages.

@app.route("/signup",methods=['GET','POST'])

def register():

	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user_info={}

		user_info["name"] = form.name.data
		user_info["username"] = form.username.data
		user_info["email"] = form.email.data
		user_info["account_type"]=form.account_type.data
		user_info["password"] = sha256_crypt.encrypt(str(form.password.data))

		session["username"]=user_info["name"]
		session["account_type"]=user_info["account_type"]


@app.route('/')
def home():
	return render_template('home.html',title='home')
@app.route('/about')
def about():
	
	return render_template('about.html',title='about')
@app.route('/contact')
def contact():
	
	return render_template('contact.html',title='contact')
@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		users={'user1':'123',
		'user2':'1234',
		'user3':'12345'
		}
		username=request.form['username']
		password=request.form['password']
		result=user_exists(username)
		if result:
			if result['password']!=password:
				return "password dint match go back and reenter password"
			session['username']=username
			session['c_type']=result['c_type']
			return redirect(url_for('home'))
		return "username doesnt exist"
	return redirect(url_for('home'))
@app.route('/signup',methods=['GET','POST'])

def signup():
	if request.method == 'POST':
		user_info={}
		user_info['username'] = request.form['username']
		user_info['password'] = request.form['password1']
		password2 = request.form['password2']
		user_info['c_type'] = request.form['type']
		if user_info['c_type']=='buyer':
			user_info['cart']={}
			#user_info['cart']['quantity']=request.form['quantity']

		if user_exists(user_info['username']):
			return "user already exists. Enter another username"
		if user_info['password']!=password2:
			return "passwords don't match. Try again"
		save_user(user_info)
		#ession['username']=username
		#ession['c_type']=c_type
		return redirect(url_for('home'))
	return redirect(url_for('home'))

@app.route('/products',methods=['GET','POST'])
def products():
	if request.method=='POST':
		product_info={}
		product_info['name']=request.form['name']
		product_info['price']=int(request.form['price'])
		product_info['description']=request.form['description']
		product_info['seller']=session['username']

		if product_exists(product_info['name']):
			return "product exists"
		add_product(product_info)
		return redirect(url_for('products'))
	return render_template('products.html',products=products_list())

@app.route('/remove_products',methods=['GET','POST'])
def remove_products():
	if request.method=='POST':
		name=request.form['name']
		remove_from_db(name)
		return redirect(url_for('products'))
	return redirect(url_for('products'))

@app.route('/cart',methods=['GET','POST'])
def cart():
	if request.method=='POST':
		name=request.form['name']
		add_to_cart(name)
		return redirect(url_for('products'))
	products=cart_info()
	return render_template('cart.html',products=products)
	return redirect(url_for('products'))

@app.route('/remove_cart',methods=['GET','POST'])
def remove_cart():
	if request.method=='POST':
		name=request.form['name']
		remove_from_cart(name)
		return redirect(url_for('cart'))
	return redirect(url_for('products'))


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))
@app.route('/search',methods = ['POST'])
def search():
	word = request.form['word']
	matches = search_prod(word)
	return render_template('products.html',products=matches)

	
app.run(debug=True)
