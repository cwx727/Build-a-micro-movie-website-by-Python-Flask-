from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import User

class RegistForm(FlaskForm):
	name = StringField(
		label = '昵称',
		validators = [                          #验证器
			DataRequired("请输入昵称！")          #不能为空     
		],
		description = '昵称',                    #描述
		render_kw = {                           #属性
			"class" : "form-control input-lg",
			"placeholder" : "请输入昵称！",
			}
		)

	email = StringField(
		label = '邮箱',
		validators = [                          #验证器
			DataRequired("请输入邮箱！"),         #不能为空 
			Email("邮箱格式不正确！")  
		],
		description = '邮箱',                    #描述
		render_kw = {                           #属性
			"class" : "form-control input-lg",
			"placeholder" : "请输入邮箱！",

			}
		)

	phone = StringField(
		label = '手机',
		validators = [                          #验证器
			DataRequired("请输入手机！"),        #不能为空 
			Regexp("1[3458]\\d{9}",message="手机号码不正确！")  
		],
		description = '手机',                    #描述
		render_kw = {                           #属性
			"class" : "form-control input-lg",
			"placeholder" : "请输入手机！",

			}
		)

	pwd = PasswordField(
		label = '密码',
		validators = [
			DataRequired("请输入密码！")
		],
		description = '密码',
		render_kw = {
			"class" : "form-control input-lg",
			"placeholder" : "请输入密码！",
           
			}
		)

	repwd = PasswordField(
		label = '确认密码',
		validators = [
			DataRequired("请输入确认密码！"),
			EqualTo('pwd', message='两次密码不一致！')
		],
		description = '确认密码',
		render_kw = {
			"class" : "form-control input-lg",
			"placeholder" : "请输入确认密码！",
          
			}
		)


	submit = SubmitField(
		render_kw = {
			"class":"btn btn-lg btn-success btn-block"
			}
		)

	def validate_name(self, field):
		name = field.data
		user = User.query.filter_by(name=name).count()
		if user == 1:
			raise ValidationError("昵称已存在！")

	def validate_email(self, field):
		email = field.data
		user = User.query.filter_by(email=email).count()
		if user == 1:
			raise ValidationError("邮箱已存在！")

	def validate_phone(self, field):
		phone = field.data
		user = User.query.filter_by(phone=phone).count()
		if user == 1:
			raise ValidationError("手机已存在！")


class LoginForm(FlaskForm):
	name = StringField(
		label = '账号',
		validators = [                          #验证器
			DataRequired("请输入账号！")          #不能为空     
		],
		description = '账号',                    #描述
		render_kw = {                           #属性
			"class" : "form-control input-lg",
			"placeholder" : "请输入账号！",
			}
		)

	pwd = PasswordField(
		label = '密码',
		validators = [
			DataRequired("请输入密码！")
		],
		description = '密码',
		render_kw = {
			"class" : "form-control input-lg",
			"placeholder" : "请输入密码！",
           
			}
		)	

	submit = SubmitField(
		render_kw = {
			"class":"btn btn-lg btn-success btn-block"
			}
		)

	def validate_name(self, field):
		name = field.data
		user = User.query.filter_by(name=name).count()
		if user == 0:
			raise ValidationError('账号不存在！')


class UserdetailForm(FlaskForm):
	name = StringField(
		label = '昵称',
		validators = [                          #验证器
			DataRequired("请输入昵称！")          #不能为空     
		],
		description = '昵称',                    #描述
		render_kw = {                           #属性
			"class" : "form-control",
			"placeholder" : "请输入昵称！",
			}
		)

	email = StringField(
		label = '邮箱',
		validators = [                          #验证器
			DataRequired("请输入邮箱！"),         #不能为空 
			Email("邮箱格式不正确！")  
		],
		description = '邮箱',                    #描述
		render_kw = {                           #属性
			"class" : "form-control",
			"placeholder" : "请输入邮箱！",

			}
		)

	phone = StringField(
		label = '手机',
		validators = [                          #验证器
			DataRequired("请输入手机！"),        #不能为空 
			Regexp("1[3458]\\d{9}",message="手机号码不正确！")  
		],
		description = '手机',                    #描述
		render_kw = {                           #属性
			"class" : "form-control",
			"placeholder" : "请输入手机！",

			}
		)
	
	face = FileField(
		label = '头像',
		description = '头像', 
		render_kw = {                           
			"id" : "input_face",
			}    
		)

	info = TextAreaField(
		label = '简介',
		validators = [                         
			DataRequired("请输入简介！")               
		],
		description = '简介',                   
		render_kw = {                           
			"class" : "form-control",
			"id" : "input_info",			
			"rows" : 10,
			}
		)

	submit = SubmitField(
		'保存修改',
		render_kw = {
			"class":"btn btn-success"
			}
		)


class PwdForm(FlaskForm):
	old_pwd = PasswordField(
		label = '旧密码',
		validators = [
			DataRequired("请输入旧密码！")
		],
		description = '旧密码',
		render_kw = {
			"class" : "form-control",
			"placeholder" : "请输入旧密码！",       
			}
		)

	new_pwd = PasswordField(
		label = '新密码',
		validators = [
			DataRequired("请输入新密码！")
		],
		description = '新密码',
		render_kw = {
			"class" : "form-control",
			"placeholder" : "请输入新密码！",       
			}
		)

	submit = SubmitField(
		'提交',
		render_kw = {
			"class":"btn btn-success"
			}
		)

	def validate_old_pwd(self, field):
		from flask import session
		pwd = field.data
		user = User.query.filter_by(name=session['user']).first()
		if not user.check_pwd(pwd):
			raise ValidationError('旧密码错误')

class CommentForm(FlaskForm):
	content = TextAreaField(
		label = '内容',
		validators = [
			DataRequired("请输入评论内容！")
		],
		description = '内容',
		render_kw = {
			"id" : "input_content",       
			}
		)

	submit = SubmitField(
		'提交评论',
		render_kw = {
			"class":"btn btn-success",
			"id":"btn-sub",
			}
		)