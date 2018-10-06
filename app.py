from config import query
from flask import Flask, request, session, redirect, render_template, url_for
from flask_socketio import SocketIO, send
import json
import os
import copy
app = Flask(__name__)
socket = SocketIO(app)

@app.route('/chat', methods=['GET'])
def chat():
    
	return render_template('chat.html', hospt_id=session["hospital_id"])


@socket.on("message")
def message(msg):
    req = json.loads(msg)
    print("message : " + msg)
    result = dict()
    if req["type"] == "connect":
        print(req["id"])
        result['message'] = 'New User'
        result['type'] = 'connect'
    else:
        result['message'] = msg
        result['type'] = 'normal'
    send(result, broadcast=True)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('username')
    user_pw = request.form.get('password')
    q = "SELECT * FROM `hospital` WHERE `HOSPITAL_USER_ID` = %s AND `HOSPITAL_USER_PW` = %s"
    data = query(q, True, True, False, user_id, user_pw)
    if data:
        session['hospital_id'] = data["HOSPITAL_ID"]
        return "true";
    else:
        return "false";


@app.route('/load_diagnosis', methods=['POST'])
def diagnosis():
    pet_id = request.form.get('pet_id')
    hospt_id = request.form.get('hospt_id')
    q = "SELECT * FROM `diagnosis` WHERE `PET_ID` = %s AND `HOSPITAL_ID` = %s"

    return query(q, True, False, True, pet_id, hospt_id)

@app.route('/load_personal', methods=['POST'])
def personal():
    pet_id = request.form.get('pet_id');
    q = "SELECT * FROM `pet` WHERE `PET_ID` = %s";

    return query(q, True, True, True, pet_id);

@app.route('/allPerson', methods=['POST'])
def allPerson():
    hospt_id = request.form.get('hospt_id')
    page = request.form.get('page')
    if page is None:
        page = 0
    elif type(page) != type(1):
        page = int(page) - 1
    page = page * 12
    q = "SELECT * FROM `diagnosis` a, `pet` b WHERE a.`HOSPITAL_ID` = %s AND b.`HOSPITAL_ID` = %s AND b.`PET_ID` = a.`PET_ID` ORDER BY `DIAGN_DATE` DESC LIMIT  %s, 12"
    diags = query(q, True, False, False, hospt_id, hospt_id, page)
    if diags:

        # if request.form.get('num'):
        #     size = len(query("SELECT * FROM `diagnosis` WHERE `HOSPITAL_ID` = %s", True, False, False, hospt_id))
        #     contents.append(size)
        return json.dumps(diags)
    return json.dumps([])
@app.route('/join', methods=['GET'])
def join():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        return render_template("join.html", hospt_id=hospt_id)

    return redirect('/')

@app.route('/main', methods=['GET'])
def main():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        q = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = %s";
        data = query(q, True, True, False, hospt_id)

        if data:
            hospt_name = data["HOSPITAL_NAME"]
            pet_id = request.args.get('pet')
            return render_template("main.html", hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)

    return redirect('/')

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/insert_pet', methods=['POST'])
def insertPet():
    ks = []
    vs = []
    for k in request.form:
        ks.append("`"+k+"`")
        vs.append(request.form.get(k))
    ks = ",".join(ks)
    q = "INSERT INTO `pet`({}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(ks)
    pet_id = query(q, False, False, False, vs[0], vs[1], vs[2], vs[3], vs[4], vs[5], vs[6], vs[7], vs[8], vs[9])

    q = "INSERT INTO `chat_room`(`HOSPITAL_ID`, `PET_ID`) VALUES (%s, %s)"
    chat_room = query(q, False, False, False, vs[9], pet_id)
    return "success"
<<<<<<< HEAD
@app.route('/load_medicine_category', methods=['POST'])
def medicineCategory():
    s = set()
    words1 = request.form.getlist('word1[]')
    if len(words1) > 0:
        for word in words1:
            result = query("SELECT * FROM disease_medicine_category WHERE `DISEASE_ID` = %s", True, False, False, word)
            if result:
                if len(s) > 0:
                    s = s.union({r["CATEGORY_ID"] for r in result})
                else:
                    s = {r["CATEGORY_ID"] for r in result}
            else:
                continue
        result = query("SELECT * FROM medicine_category WHERE CATEGORY_ID = %s" + " OR CATEGORY_ID = %s" * (len(s) - 1), True, False, True, *tuple(s))
        if result:
            return result
        else:
            return ""

    return ""

@app.route('/load_medicine', methods=['POST'])
def medicine():
    iid = request.form.getlist('id')
    result = query("SELECT * FROM medicine WHERE CATEGORY_ID = %s", True, False, True, iid)
    if result:
        return result
    else:
        return ""

    return ""

@app.route('/search_disease', methods=['POST'])
def search():
    word = request.form.get('search')
    result = query("SELECT * FROM disease WHERE `DISEASE_NAME` LIKE %s", True, False, True,
                   "%{}%".format(word))
    if result:
        return result
    return ""

=======
@app.route('/load_medicine', methods=['POST'])
def medicine():
    words1 = request.form.getlist('word1[]')
    words2 = request.form.getlist('word2[]')
    return json.dumps({"server" : words1+words2})
>>>>>>> 69fe84c62f79bda4d6097797813082b6b946da64
@app.route('/load_disease', methods=['POST'])
def disease():
    s = set()
    words2 = request.form.getlist('word2[]')
    if len(words2) > 0:
        for word in words2:
            result = query("SELECT * FROM disease_symptom WHERE `SYMPTOME_NAME` LIKE %s", True, False, False, "%{}%".format(word))
            if result:
                if len(s) > 0:
                    s = s.intersection({r["DISEASE_ID"] for r in result})
                else:
                    s = {r["DISEASE_ID"] for r in result}
            else:
                continue
<<<<<<< HEAD
        result = query("SELECT * FROM disease WHERE DISEASE_ID = %s" + " OR DISEASE_ID = %s" * (len(s) - 1), True, False, True, *tuple(s))
        if result:
            return result
        else:
            return ""
=======
        return query("SELECT * FROM disease WHERE DISEASE_ID = %s" + " OR DISEASE_ID = %s" * (len(s) - 1), True, False, True, *tuple(s))
>>>>>>> 69fe84c62f79bda4d6097797813082b6b946da64
    return ""

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)





@app.route('/diag', methods=['GET'])
def diag():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        q = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = %s";
        data = query(q, True, True, False, hospt_id)

        if data:
            hospt_name = data["HOSPITAL_NAME"]
            pet_id = request.args.get('pet')
            return render_template('diag.html', hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)

    return redirect('/')

@app.route('/person')
def person():
    return render_template('person.html', hospt_id=session["hospital_id"])

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #app.run(host="0.0.0.0", port=5000)
    # socket.run(app, port=5000, host='0.0.0.0')
    socket.run(app)
