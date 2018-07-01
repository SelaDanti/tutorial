import psycopg2 #needed to configure a database
from  werkzeug.security import generate_password_hash , check_password_hash #needed for password encryption

con = psycopg2.connect(dbname='database name', user='user', host='host', password='password')# connect to database

"""
quering data to database
"""
try:
	cur = con.cursor()
	sql = "an sql statement"
	cur.execute(sql);
	con.commit()
except psycopg2.Error as e:
	con.rollback()
	return({e.pgcode:e.pgerror},500)
