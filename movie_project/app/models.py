from datetime import datetime
from app import db


class User(db.Model):
	''' 会员信息 '''
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)   #编号
	name = db.Column(db.String(100), unique=True)   # 昵称
	pwd = db.Column(db.String(100))  # 密码
	email = db.Column(db.String(100), unique=True)  # 邮件
	phone = db.Column(db.String(11), unique=True)  # 电话
	info = db.Column(db.Text)  # 个性简介
	face = db.Column(db.String(255), unique=True)  # 头像
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  #注册时间
	uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
	userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
	comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
	moviecols = db.relationship('Moviecol', backref='user')  # 电影收藏外键关系关联

	def __repr__(self):
		return '<User %r>' % self.name

	def check_pwd(self, pwd):
		from werkzeug.security import check_password_hash
		return check_password_hash(self.pwd, pwd)

class Userlog(db.Model):
	''' 会员登陆日志 '''
	__tablename__ = 'uselog'
	id = db.Column(db.Integer, primary_key=True)  #编号
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
	ip = db.Column(db.String(100))   # 登陆ip
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

	def __repr__(self):
		return '<Userlog %r>' %self.id

class Tag(db.Model):
	''' 电影标签 '''
	__tablename__ = 'tag'
	id = db.Column(db.Integer, primary_key=True)  #编号
	name = db.Column(db.String(100), unique=True)   # 标题
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
	movies = db.relationship('Movie', backref='tag')  # 电影外键关系关联

	def __repr__(self):
		return '<Tag %r>' %self.name

class Movie(db.Model):
	''' 电影 '''
	__tablename__ = 'movie'
	id = db.Column(db.Integer, primary_key=True)  #编号
	title = db.Column(db.String(255), unique=True)   # 标题
	url = db.Column(db.String(255), unique=True)   # 地址
	info = db.Column(db.Text)   # 简介
	logo = db.Column(db.String(255))   # 封面	
	star = db.Column(db.SmallInteger)   # 星级
	playnum = db.Column(db.BigInteger)   # 播放次数
	commentnum = db.Column(db.BigInteger)   # 评论次数
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  #标签id
	area = db.Column(db.String(255))   # 地区
	release_time = db.Column(db.Date)   # 上映日期
	length = db.Column(db.String(100))   # 片长
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
	comments = db.relationship('Comment', backref='movie')  # 评论外键关系关联
	moviecols = db.relationship('Moviecol', backref='movie')  # 电影收藏外键关系关联

	def __repr__(self):
		return '<Movie %s>' % self.title

class Preview(db.Model):
	''' 上映预告 '''
	__tablename__ = 'preview'
	id = db.Column(db.Integer, primary_key=True)  #编号
	title = db.Column(db.String(255), unique=True)   # 标题
	logo = db.Column(db.String(255))   # 封面	
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

	def __repr__(self):
		return '<Preview %s>' % self.title

class Comment(db.Model):
	''' 评论 '''
	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True)  #编号
	content = db.Column(db.Text)  #内容
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) #所属电影
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #所属用户
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

	def __repr__(self):
		return '<Comment %s>' % self.id

class Moviecol(db.Model):
	''' 电影收藏 '''
	__tablename__ = 'moviecol'
	id = db.Column(db.Integer, primary_key=True)  # 编号
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))# 所属用户
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

	def __repr__(self):
		return '<Moviecol %s>' % self.id

class Auth(db.Model):
	''' 权限 '''
	__tablename__ = 'auth'
	id = db.Column(db.Integer, primary_key=True) # 编号
	name = db.Column(db.String(100), unique=True)   # 名称
	url = db.Column(db.String(255), unique=True)   # 地址
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

	def __repr__(self):
		return '<Auth %s>' % self.name

class Role(db.Model):
	''' 角色 '''
	__tablename__ = 'role'
	id = db.Column(db.Integer, primary_key=True) # 编号
	name = db.Column(db.String(100), unique=True)   # 名称
	auths = db.Column(db.String(600))  #权限列表
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
	roles = db.relationship('Admin', backref='role')  # 管理员外键关系关联

	def __repr__(self):
		return '<Role %s>' % self.name

class Admin(db.Model):
	''' 管理员 '''
	__tablename__ = 'admin'
	id = db.Column(db.Integer, primary_key=True)   # 编号
	name = db.Column(db.String(100), unique=True)   # 管理员账号
	pwd = db.Column(db.String(100))  # 密码
	is_super = db.Column(db.SmallInteger)  # 是否为超级管理员
	role_id = db.Column(db.Integer, db.ForeignKey('role.id')) # 所属角色
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
	adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员日志外键关系关联
	oplogs = db.relationship('Oplog', backref='admin')  # 管理员操作日志外键关系关联

	def __repr__(self):
		return '<Admin %s>' % self.name

	def check_pwd(self, pwd):
		''' 验证密码 '''
		from werkzeug.security import check_password_hash
		return check_password_hash(self.pwd, pwd)           

class Adminlog(db.Model):
	''' 管理员登陆日志 '''
	__tablename__ = 'adminlog'
	id = db.Column(db.Integer, primary_key=True)  #编号
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
	ip = db.Column(db.String(100))   # 登陆ip
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

	def __repr__(self):
		return '<Adminlog %r>' %self.id

class Oplog(db.Model):
	''' 管理员操作日志 '''
	__tablename__ = 'oplog'
	id = db.Column(db.Integer, primary_key=True)  #编号
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
	ip = db.Column(db.String(100))   # 登陆ip
	reason = db.Column(db.String(600))   # 操作原因
	addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

	def __repr__(self):
		return '<Oplog %r>' %self.id

'''
if __name__ == '__main__':
	# db.create_all()  #新建所有表
	
	role = Role(name='超级管理员', auths='')  #role表新增一条数据
	db.session.add(role)
	db.session.commit()
	

	from werkzeug.security import generate_password_hash
	admin = Admin(name='admin',
		pwd=generate_password_hash('admin'),
		is_super=0,
		role_id=1)
	db.session.add(admin)
	db.session.commit()
'''