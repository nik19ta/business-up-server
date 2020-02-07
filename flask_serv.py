from flask import Flask, render_template, request, redirect, url_for, make_response
import mysql.connector

connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '123',
        database='bisup'
)
mycursor = connection.cursor(buffered=True)

app = Flask(__name__)
#
#
#
#
# Александр Яблонский
@app.route('/Vasiliy', methods=['GET'])
def Alexander():
    response = make_response({'id': 'Vasiliy','login': 'Nichiporov','sity': 'Moscow' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/arthur', methods=['GET'])
def arthur():
    response = make_response({'id': 'Arthur','login': 'Khorshikyan','sity': 'Moscow' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/Amir', methods=['GET'])
def Amir():
    response = make_response({'id': 'Amir','login': 'Omarov','sity': 'Moscow' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/Dmitry', methods=['GET'])
def Dmitry():
    response = make_response({'id': 'Dmitry','login': 'Kuzmin','sity': 'Moscow','district': 'Yuzhnoye Tushino district' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/anton', methods=['GET'])
def antom():
    response = make_response({'id': 'Anthony','login': 'Morato','sity': 'Moscow' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/data', methods=['GET'])
def data():
    response = make_response({'id': '1','login': 'test data','sity': 'moskows' }, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#
#
#
#
#

@app.route('/users', methods=['POST'])
def users():
    raw_data = request.form['users_id']
    print(raw_data)
    ids = raw_data.split(',')
    all=[]
    for id in ids:
        mycursor.execute(f'SELECT * FROM users WHERE id = {id}')
        acc = mycursor.fetchall()
        all.append(acc)
    ok = {'all': all}

    response = make_response(ok, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/usersinchampionat', methods=['POST'])
def usersinchampionat():
    raw_data = request.form['users_id']
    championat_id = request.form['championat_id']
    ids = raw_data.split(',')


    mycursor.execute(f'select users_id from teams where championat_id = {championat_id}')
    accounts = mycursor.fetchall()

    all=[]
    counts=[]

    for id in ids:
        mycursor.execute(f'SELECT * FROM users WHERE id = {id}')
        acc1 = mycursor.fetchall()


        list = True
        for i in accounts: # кортеж

            for acc in i: # кортеж в кортеже

                for acc2 in acc.split(','): # 2

                    if id == acc2:
                        list = False
                        all.append({'data':acc1, 'team': False})
                        print(id + ' ' + acc2)

                    if list == False:
                        print('break')
                        break
                if list == False:
                    print('break')
                    break
            if list == False:
                print('break')
                break
        if list == True:
            print('nik')
            all.append({'data':acc1, 'team': True})

    ok = {'all': all}

    response = make_response(ok, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/deluser', methods=['POST'])
def deluser():
    user_id = request.form['userid']
    team_id = request.form['teamid']
    mycursor.execute('SELECT users_id FROM teams WHERE team_name = %s', (team_id,))
    raw_users_id = mycursor.fetchone()
    users_id = raw_users_id[0].split(',')
    users_id.remove(user_id)
    ids = ','.join(users_id)

    mycursor.execute('UPDATE teams SET users_id = %s WHERE team_name = %s', (ids, team_id))
    connection.commit()

    response = make_response('ok',200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/testteam', methods=['POST'])
def testteam():
    id = str(request.form['id'])
    mycursor.execute('SELECT team_name FROM teams WHERE captain = %s', (id,))
    user = mycursor.fetchone()
    print(user)
    response = make_response({'arg':user},200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/exitFromChampionat', methods=['POST'])
def exitFromChampionat():
    championat_id = request.form['championat_id']
    user_id = request.form['user_id']
    team_id = request.form['teamid']
    print(championat_id, user_id, team_id)
    if team_id != 'false':
        mycursor.execute('SELECT captain FROM teams WHERE id = %s', (team_id,))
        captain = mycursor.fetchone()
        captain_id = captain[0]
        if user_id == captain_id:
            print(team_id)
            mycursor.execute('DELETE FROM teams WHERE id = %s', (team_id,))
            connection.commit()

            # mycursor.execute('SELECT teams_id FROM championats WHERE id = %s', (championat_id,))
            # raw_teams_id = mycursor.fetchone()
            # teams_id = raw_teams_id[0].split(',')
            # teams_id.remove(team_id)
            # teams_ids = ','.join(teams_id)
            # mycursor.execute('UPDATE championats SET teams_id = %s WHERE id = %s', (teams_ids, championat_id))


            mycursor.execute('SELECT users_id FROM championats WHERE id = %s', (championat_id,))
            raw_users_ids = mycursor.fetchone()
            users_ids = raw_users_ids[0].split(',')
            users_ids.remove(user_id)
            users_id = ','.join(users_ids)
            mycursor.execute('UPDATE championats SET users_id = %s WHERE id = %s', (users_id, championat_id))




            response = make_response('участник был капитаном, поэтому и команда удалена!', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            mycursor.execute('SELECT users_id FROM teams WHERE id = %s', (team_id,))
            raw_users_ids = mycursor.fetchone()
            users_ids = raw_users_ids[0].split(',')
            users_ids.remove(user_id)
            users_id = ','.join(users_ids)
            mycursor.execute('UPDATE teams SET users_id = %s WHERE id = %s', (users_id, team_id))

            mycursor.execute('SELECT users_id FROM championats WHERE id = %s', (championat_id,))
            rawUsersIds = mycursor.fetchone()
            usersIds = rawUsersIds[0].split(',')
            usersIds.remove(user_id)
            usersId = ','.join(usersIds)
            mycursor.execute('UPDATE championats SET users_id = %s WHERE id = %s', (usersId, championat_id))

            response = make_response('Пользователь удален из чемпионата и команды!', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    else:
            mycursor.execute('SELECT users_id FROM championats WHERE id = %s', (championat_id,))
            rawUsersIds = mycursor.fetchone()
            usersIds = rawUsersIds[0].split(',')
            usersIds.remove(user_id)
            usersId = ','.join(usersIds)
            mycursor.execute('UPDATE championats SET users_id = %s WHERE id = %s', (usersId, championat_id))

            response = make_response('Пользователь удален из чемпионата!', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


@app.route('/allusers',methods= ['POST'])
def allusers():
    status = 'ok'
    mycursor.execute('SELECT * FROM users')
    account = mycursor.fetchall()
    acc = {'all': account}
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/server',methods= ['POST'])
def server():
    response = make_response('all work', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/championats',methods= ['POST'])
def championats():
    status = 'ok'
    mycursor.execute('SELECT * FROM championats')
    championats_name = mycursor.fetchall()
    acc = {'all': championats_name}
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/addteamUser',methods= ['POST'])
def addteamUser():
    user_id = request.form['id']
    championat_id = request.form['championat_id']
    mycursor.execute('SELECT users_id FROM championats where id = %s', (championat_id,))
    users_id = mycursor.fetchone()
    users = list(users_id)
    users1 = users[0] + ',' + str(user_id)
    mycursor.execute('UPDATE championats SET Users_id = %s WHERE (id = %s);', (users1, championat_id))
    connection.commit()
    mycursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = mycursor.fetchone()
    info = {'all': user}
    response = make_response(info, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/changepass',methods= ['POST'])
def chmore():
    status = 'ok'
    passw = request.form['passw']
    passw2 = request.form['passw2']
    id = request.form['id']
    mycursor.execute("UPDATE users SET password = %s WHERE id = %s and password = %s",(passw2,id,passw))
    response = make_response('otl', 200)
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
    mycursor.execute("UPDATE users SET date_of_birth = %s WHERE id = %s and login = %s",(dataof, id, login ))
    # connection.commit()
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


@app.route('/teamsall',methods= ['POST'])
def teamsall():
    status = 'ok'
    championat_id = request.form['championat_id']
    mycursor.execute('SELECT * FROM teams where championat_id = %s',(championat_id,))
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
    response = make_response(infoacc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/addacc', methods=['POST'])
def addacc():
    accid = request.form['accid']
    id = request.form['id']
    login = request.form['login']
    password = request.form['password']
    mycursor.execute("UPDATE users SET account = %s WHERE ID = %s and LOGIN = %s and password = %s",(accid, id, login, password ))
    connection.commit()
    response = make_response(f'id аккаунта виртомоники изменён на {accid}', 200)
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
    # mycursor.execute('SELECT captain FROM teams WHERE captain =%s', (nameteam,))
    # captain = mycursor.fetchall()
    if nameuser == '' or nameteam == '' or nomination == '' or coverletter == '':
        response = make_response('заполенены не все поля', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        if acc:
            response = make_response('Приглашение уже отправленно', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            # if captain:
            #     response = make_response('Вы не можете отправить приглашение себе', 200)
            #     response.headers['Access-Control-Allow-Origin'] = '*'
            #     return response
            # else:
            mycursor.execute('INSERT INTO invitation (nameuser, nameteam, nomination, coverletter) VALUES (%s, %s, %s, %s)', (nameuser, nameteam, nomination, coverletter))
            connection.commit()
            response = make_response('Приглашение отправленно', 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

@app.route('/AddToTeam', methods= ['POST'])
def AddToTeam():
    team_name = request.form['team_name']
    team_nomination = request.form['team_nomination']
    team_discribtion = request.form['team_discribtion']
    championat_id = request.form['championat_id']
    captain_id = request.form['captain_id']
    # данные для проверки названия команды
    mycursor.execute("SELECT team_name FROM teams WHERE team_name = %s", (team_name,))
    # mycursor.execute(f'SELECT team_name FROM teams WHERE team_name = {team_name}')

    acc = mycursor.fetchone()
    print(acc)
    # данные для проверки капитана команды в чемпионате
    mycursor.execute('SELECT captain FROM teams WHERE championat_id = %s AND captain = %s', (championat_id, captain_id))
    acc1 = mycursor.fetchone()
    print(acc1)

    if acc1 == None:
        if acc == None:
            if team_name == '' or team_nomination == '' or team_discribtion == '' or championat_id == '' or captain_id ==   '':
                response = make_response('Заполнены не все поля', 200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            else:
                mycursor.execute('INSERT INTO teams (team_name, users_id,championat_id, team_describtion, captain) values(%s,%s, %s, %s, %s)', (team_name, captain_id, championat_id, team_discribtion, captain_id))
                connection.commit()
                mycursor.execute("SELECT id from teams where team_name = %s",(team_name,))
                team_id = mycursor.fetchone()
                team_elem = team_id[0]
                # mycursor.execute('SELECT teams_id FROM championats where id = %s', (championat_id,))
                # teams_id = mycursor.fetchone()
                # teams = list(teams_id)
                # teams1 = teams[0] + ',' + str(team_elem)
                # tuple(teams1)
                # mycursor.execute('UPDATE championats SET teams_id = %s WHERE id = %s', (teams1, championat_id))
                response = make_response('Команда создана!', 200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        else:
            response = make_response("Имя команды занято", 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    else:
        response = make_response('Копитанам команд нельзя создавать команды', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/addUserToTeam', methods=['POST'])
def addUserToTeam():
    userId = request.form['userId']
    teamname = request.form['teamname']

    mycursor.execute('SELECT users_id FROM teams WHERE team_name = %s', (teamname,))
    raw_usersid = mycursor.fetchone()
    usersid = raw_usersid[0].split(',')

    if userId not in usersid:
        mycursor.execute('SELECT users_id FROM teams WHERE team_name=%s', (teamname,))
        usersId = mycursor.fetchone()
        users_id = list(usersId)
        users_id.append(userId)
        users_str = ','.join(users_id)
        mycursor.execute('UPDATE teams SET users_id = %s WHERE team_name = %s', (users_str, teamname))
        connection.commit()
        mycursor.execute('DELETE FROM invitation WHERE nameuser = %s', (userId,))
        users1_id = {'all': users_str}
        response = make_response('Вы вступили в команду', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response('Вы уже состоите в данной команде', 200)
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
    response = make_response(acc, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/testin', methods=['POST'])
def testin():
    user = request.form['user']
    mycursor.execute('SELECT team_name FROM teams where captain = %s',(user,))
    users = mycursor.fetchall()
    list = {'list': users,}
    response = make_response(list, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/login',methods= ['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    mycursor.execute('SELECT * FROM users WHERE Login = %s AND Password = %s', (login, password))
    account = mycursor.fetchone()
    status = 'error'
    def acc():
        if account:
            print('ok')
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
		'city':account[7],
		'img':account[8],
		'account':account[9],
        }
        status = {'info':databaseinfo, 'status': 'ok'}
    response = make_response(status, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/reg', methods=['POST'])
def register():
    login = request.form['login']
    email = request.form['email']
    password = request.form['password']
    mycursor.execute('SELECT * FROM users WHERE login=%s', (login,))
    acc = mycursor.fetchone()
    if not acc:
        mycursor.execute('INSERT INTO users (login, email, password) VALUES (%s, %s, %s)', (login, email, password))
        connection.commit()
        response = make_response('ok', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response('login isssss', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response



##########################################
#                                        #
#                 Chat                   #
#                                        #
##########################################

# +----+------------+--------+-----------+--------------+---------------------+
# | id | message_id | sender | recipient | message      | data                |
# +----+------------+--------+-----------+--------------+---------------------+

@app.route('/getusers',methods= ['POST'])
def getusers():
    sender = request.form['sender']
    # print(sender)
    # print(sender)
    # print(sender)
    # print(sender)
    mycursor.execute(f'SELECT if(sender = {sender},recipient,sender) as "RESULT" FROM chat WHERE (sender = {sender}) or (recipient = {sender})')
    chat = mycursor.fetchall()
    chatsers = []
    print(chat)

    for i in set(chat):
        mycursor.execute(f'SELECT fio,img FROM users WHERE id = {i[0]}')
        chat = mycursor.fetchone()
        chatsers.append(chat + i)

    print(chatsers)

    ChatUsersList = {'users': chatsers}

    response = make_response(ChatUsersList, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getchat',methods= ['POST'])
def getchat():
    sender = request.form['sender']
    recipient = request.form['recipient']
    print(sender)
    print(recipient)
    mycursor.execute(f'SELECT message_id,message,id,sender,recipient FROM chat WHERE (sender = {sender} and recipient = {recipient}) or (sender = {recipient} and recipient = {sender})')
    datachat = mycursor.fetchall()
    print(datachat)

    chat = {'chat': datachat}

    response = make_response(chat, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/sendchat',methods= ['POST'])
def sendchat():
    sender = request.form['sender']
    recipient = request.form['recipient']
    message = request.form['message'];
    print(sender)
    print(recipient)
    print(message)
    mycursor.execute(f'insert into chat (sender, recipient, message) VALUES (%s, %s, %s)', (sender, recipient, message))
    connection.commit()
    mycursor.execute(f'SELECT message_id,message,id,sender,recipient FROM chat WHERE (sender = {sender} and recipient = {recipient}) or (sender = {recipient} and recipient = {sender})')

    datachat = mycursor.fetchall()
    print(datachat)

    chat = {'chat': datachat}

    response = make_response(chat, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/search',methods= ['POST'])
def search():
    content = request.form['content']
    print(content)
    mycursor.execute(f'SELECT id FROM users WHERE login = {content}')
    datachat = mycursor.fetchall()

    chat = {'chat': datachat}

    response = make_response(chat, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response






if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
