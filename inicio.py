from flask import Flask, render_template, request, redirect, url_for, Response, session, flash
from flask_mysqldb import MySQL 

app=Flask(__name__)
app.secret_key = 'mysql' #Clave secreta para sesiones
mysql = MySQL() #Inicializar la ext MySQL

# conexion de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    user={ # Dicionario de contacto
        'nombre': '',
        'email': '',
        'mensaje': ''
    }
    if request.method == 'GET':
        user['nombre'] = request.args.get('nombre', '')
        user['email'] = request.args.get('email', '')
        user['mensaje'] = request.args.get('mensaje', '')
    return render_template('contacto.html', usuario=user)

@app.route('/contactopost', methods=['GET', 'POST'])
def contactopost():
    user={ # Dicionario de contacto
        'nombre': '',
        'email': '',
        'mensaje': ''
    }
    if request.method == 'POST':
        user['nombre'] = request.form.get('nombre', '')
        user['email'] = request.form.get('email', '')
        user['mensaje'] = request.form.get('mensaje', '')
    return render_template('contactopost.html', usuario=user)

@app.route('/datousuarioget', methods=['GET', 'POST'])
def datousuarioget():
    user={
        'nombres': '',
        'apellidos': '',
        'cedula': '',
        'direccion': '',
        'mensaje': ''
    }
    if request.method == 'GET':
        user['nombres'] = request.args.get('nombres', '')
        user['apellidos'] = request.args.get('apellidos', '')
        user['cedula'] = request.args.get('cedula', '')
        user['direccion'] = request.args.get('direccion', '')
        user['mensaje'] = request.args.get('mensaje', '')
    return render_template('datousuarioget.html', usuario=user)

@app.route('/datousuariopost', methods=['GET', 'POST'])
def datousuariopost():
    user={
        'nombres': '',
        'apellidos': '',
        'cedula': '',
        'direccion': '',
        'mensaje': ''
    }
    if request.method == 'POST':
        user['nombres'] = request.form.get('nombres', '')
        user['apellidos'] = request.form.get('apellidos', '')
        user['cedula'] = request.form.get('cedula', '')
        user['direccion'] = request.form.get('direccion', '')
        user['mensaje'] = request.form.get('mensaje', '')
    return render_template('datousuariopost.html', usuario=user)

@app.route('/usuario')
def usuario():
    if 'usuarios' in session:
        return render_template("usuario.html", usuario=session['usuarios'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/accesologin', methods=['GET', 'POST'])
def accesologin():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['id_rol'] = user['id_rol']
            if user['id_rol'] == 1:
                flash('¡Has iniciado sesión como administrador!', 'success')
                return render_template('admin.html', user=user)
            elif user['id_rol'] == 2:
                return render_template('index.html')
            else:
                flash('Rol de usuario no reconocido.', 'danger')
                return render_template('login.html', error='Credenciales incorrectas')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

@app.route('/Registro', methods=['GET', 'POST'])
def Registro():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        id_rol = 2  # Rol usuario por defecto

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (email, password, id_rol) VALUES (%s, %s, %s)",
                    (email, password, id_rol))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('inicio'))

    return render_template("Registro.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
