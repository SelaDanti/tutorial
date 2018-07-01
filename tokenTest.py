from flask import Flask, jsonify,request,make_response
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecetkey'

def token_required(f):
	@wraps(f)
	def decorated(*args,**kwargs):
		token = request.args.get('token')# get token
		if not token:
			return(jsonify({'result':'token is missing'}))
		try:
			data = jwt.decode(token,app.config['SECRET_KEY'])#decode token if false throw error
		except:
			return(jsonify({'result':'Token is invalid'}))

		return(f(*args,**kwargs))

	return decorated


@app.route('/unprotected')
def uprotected():
	return(jsonify({'result':'unprotected'}))

@app.route('/protected')
@token_required
def protected():
	return(jsonify({'result':'protected'}))

@app.route('/login')
def login():
	auth = request.authorization
	if auth and auth.password == 'passwords':
		token = jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=35)},
			app.config['SECRET_KEY'])#create token
		return jsonify({'token':token.decode('UTF-8')})
		
	return(make_response('could not varify',401,{'www-Authenticate':'Basic realm="Login-Required"'}))

if __name__ == '__main__':
	app.run(debug = True)