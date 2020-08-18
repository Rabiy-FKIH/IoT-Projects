from flask import Flask , render_template
app = Flask(__name__)
import mysql.connector as mariadb



def getData():
	conn=mariadb.connect(user='rabiy',password='tel27652322',database='Weather')
	curs=conn.cursor()
	curs.execute("select * from DHT11 order by Timestamp desc limit 1")
	record=curs.fetchone()
	time=str(record[0])
	temp=record[1]
	hum=record[2]
	conn.close()
	return time , temp , hum


@app.route("/")
def index():
	time,temp,hum=getData()
	template={
		'time' : time,
		'temp' : temp,
		'hum' :hum }
	return render_template('index.html' ,**template )


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=False)
