from flask import Flask, render_template, request, redirect, url_for, make_response
import mysql.connector

connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '123',
        database='bisup'
)
mycursor = connection.cursor()

app = Flask(__name__)


@app.route('/allusers',methods= ['POST'])
def allusers():
    status = 'ok'
    mycursor.execute('SELECT * FROM users')
    account = mycursor.fetchall()
    acc = {'all': account}
    print(acc)
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



@app.route('/championats',methods= ['POST'])
def championats():
    status = 'ok'
    mycursor.execute('SELECT * FROM championats')
    championats_name = mycursor.fetchall()
    print(championats_name)
    acc = {'all': championats_name}
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/addteamUser',methods= ['POST'])
def addteamUser():
    user_id = request.form['id']
    championat_id = request.form['championat_id']
    print(championat_id)
    print(user_id)
    mycursor.execute('SELECT users_id FROM championats where id = %s', (championat_id,))
    users_id = mycursor.fetchone()
    print(user_id)
    users = list(users_id)
    print(users)
    users1 = users[0] + ',' + str(user_id)
    print(users1)
    mycursor.execute('UPDATE championats SET Users_id = %s WHERE (id = %s);', (users1, championat_id))
    response = make_response('users1', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/changepass',methods= ['POST'])
def chmore():
    status = 'ok'
    passw = request.form['passw']
    passw1 = request.form['passw1']
    passw2 = request.form['passw2']
    id = request.form['id']
    print(passw)
    print(passw1)
    print(passw2)
    print(id)
    if passw1 == passw2:
        mycursor.execute("UPDATE users SET password = %s WHERE id = %s and password = %s",(passw2,id,passw))
        response = make_response('otl', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response('no otl', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/chengedata',methods= ['POST'])
def chmore1():
    status = 'ok'
    id = request.form['id']
    login = request.form['login']
    fio = request.form['fio']
    dataof = request.form['dataof']
    city = request.form['city']
    mycursor.execute("UPDATE users SET FIO = %s WHERE id = %s and login = %s",(fio, id, login ))
    mycursor.execute("UPDATE users SET city = %s WHERE id = %s and login = %s",(city, id, login ))
    mycursor.execute("UPDATE users SET birthday = %s WHERE id = %s and login = %s",(dataof, id, login ))
    response = make_response('accounts', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/teams',methods= ['POST'])
def teams():
    status = 'ok'
    id = request.form['id']
    mycursor.execute('SELECT * FROM teams where id = %s',(id,))
    teams = mycursor.fetchall()
    acc = {'all': teams}
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/usersid',methods= ['POST'])
def usersid():
    mycursor.execute('SELECT users_id FROM teams')
    users_id = mycursor.fetchall()
    users = users_id[0][0].split(',')
    acc = {'all': users}
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/invate', methods=['POST'])
def invate():
    user_id = request.form['id']
    mycursor.execute('SELECT * FROM invitation where nameuser = %s',(user_id,))
    info = mycursor.fetchall()
    infoacc = {'inform': info,}
    # print(acc.all)
    response = make_response(infoacc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/invatetoadd', methods=['POST'])
def invatetoadd():
    nameuser = request.form['nameuser']
    nameteam = request.form['nameteam']
    nomination = request.form['nomination']
    coverletter = request.form['coverletter']
    mycursor.execute('SELECT nameuser, nameteam FROM invitation WHERE nameteam=%s and nameuser=%s', (nameteam, nameuser))
    acc = mycursor.fetchall()
    if nameuser == '' or nameteam == '' or nomination == '' or coverletter == '':
        response = make_response('oops', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        if acc:
            response = make_response('teem is', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            mycursor.execute('INSERT INTO invitation (nameuser, nameteam, nomination, coverletter) VALUES (%s, %s, %s, %s)', (nameuser, nameteam, nomination, coverletter))
            connection.commit()
            response = make_response('ok', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


@app.route('/AddToTeam', methods= ['POST'])
def AddToTeam():
    team_name = request.form['team_name']
    team_nomination = request.form['team_nomination']
    team_discribtion = request.form['team_discribtion']
    championat_id = request.form['championat_id']
    captain_id = request.form['captain_id']
    if team_name == '' or team_nomination == '' or team_discribtion == '' or championat_id == '' or captain_id == '':
        response = make_response('nuul inp', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        mycursor.execute('INSERT INTO teams (team_name, users_id, team_describtion, captain) values(%s, %s, %s, %s)', (team_name, captain_id, team_discribtion, captain_id))
        connection.commit()
        mycursor.execute("Select id from teams where team_name = %s",(team_name,))
        team_id = mycursor.fetchone()
        team_elem = team_id[0]
        mycursor.execute('SELECT teams_id FROM championats where id = %s', (championat_id,))
        teams_id = mycursor.fetchone()
        teams = list(teams_id)
        teams1 = teams[0] + ',' + str(team_elem)
        # teams1 = teams[0] + ',' + str(team_id)
        tuple(teams1)
        mycursor.execute('UPDATE championats SET teams_id = %s WHERE id = %s', (teams1, championat_id))
        response = make_response('teams1', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/addUserToTeam', methods=['POST'])
def addUserToTeam():
    userId = request.form['userId']
    # championatId = request.form['championatId']
    teamname = request.form['teamname']
    mycursor.execute('SELECT users_id FROM teams WHERE team_name=%s', (teamname,))
    usersId = mycursor.fetchone()
    users_id = list(usersId)
    users_id.append(userId)
    users_str = ','.join(users_id)
    mycursor.execute('UPDATE teams SET users_id = %s WHERE team_name = %s', (users_str, teamname))
    connection.commit()
    mycursor.execute('DELETE FROM invitation WHERE nameuser = %s', (userId,))
    users1_id = {'all': users_str}
    response = make_response(users_str, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/noAddToTeam', methods=['POST'])
def noAddToTeam():
    userId = request.form['userId']
    # championatId = request.form['championatId']
    teamname = request.form['teamname']
    mycursor.execute('DELETE FROM invitation WHERE nameuser = %s and nameteam = %s', (userId, teamname))
    response = make_response('ok', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/user', methods=['POST'])
def user():
    user_id = request.form['id']
    mycursor.execute('SELECT * FROM users where id = %s',(user_id,))
    users = mycursor.fetchall()
    acc = {'all': users,}
    print(acc)
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/login',methods= ['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    print(login)
    mycursor.execute('SELECT * FROM users WHERE Login = %s AND Password = %s', (login, password))
    account = mycursor.fetchone()
    print(account)
    status = 'error'
    def acc():
        if account:
            print('ok')
            print(account[0])
        else:
            print('error password')
    acc()
    if account:
        databaseinfo = {
		'id':account[0],
		'login':account[1],
		'email': account[2],
		'password':account[3],
		'fio':account[4],
		'date_of_birth':account[5],
		'gender':account[6],
		'sity':account[7],
		'img':account[8]
        }
        status = {'info':databaseinfo, 'status': 'ok'}
    response = make_response(status, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/register', methods=['POST'])
def register():
    login = request.form['login']
    email = request.form['email']
    passw = request.form['password']
    passw1 = request.form['passw1']
    print(login)
    print(passw)
    print(email)
    mycursor.execute('SELECT * FROM users WHERE login=%s', (login,))
    acc = mycursor.fetchone()
    if not acc:
        if passw != passw1:
            response = make_response('passw incorect', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            mycursor.execute('INSERT INTO users (login, email, password) VALUES (%s, %s, %s)', (login, email, passw))
            connection.commit()
            response = make_response('ok', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    else:
        response = make_response('login isssss', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
