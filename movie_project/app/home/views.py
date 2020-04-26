from . import home
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PwdForm, CommentForm
from app.models import User, Userlog, Preview, Tag, Movie, Comment, Moviecol
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid
from app import db, app
from functools import wraps
import os, datetime


#登陆装饰器
def user_login_req(f):     #定义装饰器，验证登陆时，session中用户是否已验证通过
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'user' not in session:
			return redirect(url_for('home.login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function


#修改文件名称
def change_filename(filename):
	fileinfo = os.path.splitext(filename)  #将文件名分割成后缀名和文件名
	ch_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
	return ch_filename

#会员登陆
@home.route('/login/',methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=data['name']).first()
		if not user.check_pwd(data['pwd']):
			flash('密码错误！')
			return redirect(url_for('home.login'))
		else:
			session['user'] = user.name
			session['user_id'] = user.id
			userlog = Userlog(
				user_id=user.id,
				ip=request.remote_addr,
				)
			db.session.add(userlog)
			db.session.commit()		
			return redirect(request.args.get('next') or url_for('home.user'))

	return render_template('home/login.html', form=form)

@home.route('/logout/')
def logout():
	session.pop('user', None)
	session.pop('user_id', None)
	return redirect(url_for('home.login'))

#会员注册
@home.route('/regist/',methods=['GET','POST'])
def regist():
	form = RegistForm()
	if form.validate_on_submit():
		data = form.data
		user = User(
			name = data['name'],
			pwd = generate_password_hash(data['pwd']),
			phone = data['phone'],
			email = data['email'],
			uuid = uuid.uuid4().hex
			)
		db.session.add(user)
		db.session.commit()
		flash('注册成功！','ok')
	return render_template('home/regist.html', form=form)

#会员中心

@home.route('/user/', methods=['POST','GET'])
@user_login_req
def user():
	form = UserdetailForm()
	user = User.query.get(int(session['user_id']))
	form.face.validators = []
	if request.method == 'GET':
		form.name.data = user.name
		form.phone.data = user.phone
		form.email.data = user.email
		form.info.data = user.info
	if form.validate_on_submit():
		data = form.data
		
		if not os.path.exists(app.config['FC_DIR']):
			os.makedirs(app.config['FC_DIR'])
			os.chmod(app.config['FC_DIR'],'rw')
		if form.face.data != '':
			file_face = secure_filename(form.face.data.filename)
			user.face = change_filename(file_face)
			form.face.data.save(app.config['FC_DIR']+user.face)

		name_count = User.query.filter_by(name=data['name']).count()
		if user.name != data['name'] and name_count != 0:
			flash('昵称已存在','err')
			return redirect(url_for("home.user"))

		phone_count = User.query.filter_by(phone=data['phone']).count()
		if user.phone != data['phone'] and phone_count != 0:
			flash('手机已存在','err')
			return redirect(url_for("home.user"))

		email_count = User.query.filter_by(email=data['email']).count()
		if user.email != data['email'] and email_count != 0:
			flash('邮箱已存在','err')
			return redirect(url_for("home.user"))

		user.name = data['name']
		user.phone = data['phone']
		user.email = data['email']
		user.info = data['info']
		db.session.commit()
		flash('会员信息修改成功','ok')
		return redirect(url_for("home.user"))
	return render_template('home/user.html', form=form,user=user)

@home.route('/pwd/', methods=['GET','POST'])
@user_login_req
def pwd():
	form = PwdForm()
	if form.validate_on_submit():
		data = form.data
		user = User.query.filter_by(name=session["user"]).first()
		from werkzeug.security import generate_password_hash
		user.pwd = generate_password_hash(data['new_pwd'])
		db.session.commit()
		flash("修改密码成功，请重新登录！", "ok")
		return redirect(url_for('home.logout'))
	return render_template('home/pwd.html', form=form)


@home.route('/comments/<int:page>/')
@user_login_req
def comments(page=1):
	page_data = Comment.query.join(
			User
		).join(
			Movie
		).filter(
			Comment.movie_id == Movie.id,
			Comment.user_id == session['user_id'],
		).order_by(
			Comment.addtime.desc()
		).paginate(
			page=page, per_page=5
		)

	return render_template('home/comments.html', page_data=page_data)


#会员登陆日志
@home.route('/loginlog/<int:page>', methods=['GET'])
@user_login_req
def loginlog(page=1):
	page_data = Userlog.query.filter_by(
			user_id = int(session['user_id'])
		).order_by(
			Userlog.addtime.desc()
		).paginate(page=page, per_page=10)

	return render_template('home/loginlog.html', page_data=page_data)

#添加收藏
@home.route("/moviecol/add/", methods=['GET'])
@user_login_req
def moviecol_add():
	uid = request.args.get("uid","")
	mid = request.args.get("mid","")
	moviecol = Moviecol.query.filter_by(
			user_id = int(uid),
			movie_id = int(mid),
		).count()
	if moviecol==1:
		data = dict(ok=0)
	else:
		moviecol = Moviecol(
			user_id = int(uid),
			movie_id = int(mid),
			)
		db.session.add(moviecol)
		db.session.commit()
		data = dict(ok=1)
	import json
	return json.dumps(data)


@home.route('/moviecol/<int:page>/',methods=['GET'])
@user_login_req
def moviecol(page=1):
	page_data = Moviecol.query.join(Movie).join(User).filter(
			Movie.id == Moviecol.movie_id,
			User.id == int(session['user_id']),
		).order_by(
			Moviecol.addtime.desc()
		).paginate(page=page, per_page=10)

	return render_template('home/moviecol.html', page_data=page_data)

@home.route('/<int:page>/', methods=['GET'])
@home.route("/", methods=["GET"])
def index(page=1):
	tags = Tag.query.all()
	page_data = Movie.query

	tid = request.args.get("tid", 0)
	#print(tid, flush=True)
	if int(tid) != 0:
		page_data = page_data.filter_by(tag_id=int(tid))

	
	star = request.args.get("star", 0)
	if int(star) != 0:
		page_data = page_data.filter_by(star=int(star))

	time = request.args.get("time", 0)
	if int(time) != 0:
		if int(time) == 1:
			page_data = page_data.order_by(Movie.addtime.desc())
		else:
			page_data = page_data.order_by(Movie.addtime.asc())

	pm = request.args.get("pm", 0)
	if int(pm) != 0:
		if int(pm) == 1:
			page_data = page_data.order_by(Movie.playnum.desc())
		else:
			page_data = page_data.order_by(Movie.playnum.asc())

	cm = request.args.get("cm", 0)
	if int(cm) != 0:
		if int(cm) == 1:
			page_data = page_data.order_by(Movie.commentnum.desc())
		else:
			page_data = page_data.order_by(Movie.commentnum.asc())

	page_data = page_data.paginate(page=page, per_page=10)

	p = dict(
		tid=tid,
		star=star,
		time=time,
		pm=pm,
		cm=cm,
		)
	return render_template('home/index.html', tags=tags,p=p, page_data=page_data)

@home.route('/animation/',methods=['GET'])
def animation():
	data = Preview.query.all()
	return render_template('home/animation.html', data=data)

@home.route('/search/<int:page>/',methods=['GET','POST'])
def search(page=1):
	key = request.args.get('key','')
	movie_count =  Movie.query.filter(
		Movie.title.ilike('%'+key+'%')
		).count()
	page_data = Movie.query.filter(
		Movie.title.ilike('%'+key+'%')
		).order_by(
		Movie.addtime.desc()
		).paginate(
		page=page, per_page=10)
	return render_template('home/search.html',key=key,page_data=page_data, movie_count=movie_count)

@home.route('/play/<int:id>/<int:page>/',methods=['GET','POST'])
def play(id=None,page=1):
	movie = Movie.query.join(Tag).filter(
		Movie.tag_id == Tag.id,
		Movie.id == int(id),
		).first_or_404()
	movie.playnum = Movie.playnum+1
	db.session.add(movie)
	db.session.commit()

	page_data = Comment.query.join(
			User
		).join(
			Movie
		).filter(
			Comment.user_id == User.id,
			Comment.movie_id == movie.id,
		).order_by(
			Comment.addtime.desc()
		).paginate(
			page=page, per_page=5
		)
	comment_count = Comment.query.join(
			User
		).join(
			Movie
		).filter(
			Comment.user_id == User.id,
			Comment.movie_id == movie.id,
		).count()

	form = CommentForm()
	if "user" in session and form.validate_on_submit():
		data = form.data
		comment = Comment(
			content=data['content'],
			user_id = session['user_id'],
			movie_id = movie.id,

			)
		db.session.add(comment)
		db.session.commit()
		movie.commentnum = Movie.commentnum+1
		db.session.add(movie)
		db.session.commit()
		flash('评论提交成功','ok')
		return redirect(url_for('home.play',id=movie.id, page=1))

	return render_template('home/play.html',movie=movie,form=form,page_data=page_data,comment_count=comment_count)

