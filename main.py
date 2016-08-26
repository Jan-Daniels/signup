# Get the username, password, and email address
# Upon validation, display Welcome page
#
import webapp2
import re

signup_form = """

<!DOCTYPE html>
<html>
<head>
	<title>Caesar</title>
    <style type="text/css">
        form {
                background-color: #0080FF;
                padding: 10px;
                margin: 0 auto;
                width: 500px;
                font-family: "Times New Roman", Times, serif;
                font: 30px;
                border-radius: 20px;
            }
    </style>
</head>
<body>
<h1>SignUp</h1> 
    <form method="POST">
        <h2>Username : 
        	<input type="text" name="user_name" value="%(user_name)s" />%(error_username)s</h2>
        <h2>Password :
        	<input type="password" name="pass_word" value="" /> %(error_password)s</h2>
        <h2>Verify Password :
        	<input type="password" name="verify_password" value="" />%(error_verify)s</h2>
        <h2>Email (Optional) :
        	<input type="text" name="email_address" value="%(email_address)s"/>%(error_mail)s</h2>                
        <input type="submit">
    </form>
</body>
</html>
"""

welcome_form = """
<!DOCTYPE html>
<html>

<head>
	<title>Welcome</title>
</head>

<body>
	<h2>Welcome, %(new_user_name)s</h2>
</body>

</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
	return user_name and USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(pass_word):
	return pass_word and PASS_RE.match(pass_word)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email_address):
	return not email_address or EMAIL_RE.match(email_address)

class Signup(webapp2.RequestHandler):
	def write_signup_form ( self, user_name = "", pass_word = "", verify_password = "", email_address = "", error_username = "", error_password = "", error_verify = "", error_mail = "" ):
		self.response.out.write ( signup_form % { "user_name": user_name, 
											    "pass_word": pass_word,
											    "verify_password": verify_password,
											    "email_address": email_address,
											    "error_username": error_username,
											    "error_password": error_password,
											    "error_verify": error_verify,
											    "error_mail": error_mail } )

	def get(self):
		self.write_signup_form()

	def post(self):
		have_error = False
		user_name = self.request.get("user_name")
		pass_word = self.request.get("pass_word")
		verify_password = self.request.get("verify_password")
		email_address = self.request.get("email_address")

		if not valid_username(user_name):
			error_username = "That wasn't a valid username." 
			have_error = True
		else:
			error_username = ""

		if not valid_password(pass_word):
			error_password = "That wasn't a valid password."
			have_error = True
		else:
			error_password = ""
		
		if pass_word != verify_password:
			error_verify = "Your passwords didn't match."
			have_error = True
		else:
			error_verify = ""

		if not valid_email(email_address):
			error_mail = "That's not a valid email."
			have_error = True
		else:
			error_mail = ""

		if have_error:
			self.write_signup_form(user_name, pass_word, verify_password, email_address, 
				error_username, error_password, error_verify, error_mail)
		else:
			self.redirect('/welcome_form?user_name=' + user_name)

class Welcome(webapp2.RequestHandler):
	def write_welcome_form ( self, new_user_name = ""):
		self.response.out.write ( welcome_form % { "new_user_name": new_user_name } )
		
	def get(self):
		new_user_name = self.request.get("user_name")
		self.write_welcome_form ( new_user_name )

app = webapp2.WSGIApplication([('/', Signup),
							   ('/welcome_form', Welcome)], debug=True)