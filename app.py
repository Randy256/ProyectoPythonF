from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL 

mysql = MySQL()
app=Flask(__name__)
app.secret_key = 'mysql' #Clave secreta para sesiones


# conexion de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index(): # Enviando mensajes flash de atipo success a la plantilla index.html
    flash('Mensaje de prueba', 'success')
    flash('Mensaje de Success con Flash', 'success')
    flash('Mensaje de Info con Flash', 'info')
    flash('Mensaje de Warning con Flash', 'warning')
    flash('Mensaje de Error con Flash', 'error')
    return render_template('index.html')

@app.route('/demo-flash', methods=['GET'])
def demo_flash():
    flash('Mensaje de Success con Flash', 'success')
    flash('Mensaje de Info con Flash', 'info')
    flash('Mensaje de Warning con Flash', 'warning')
    flash('Mensaje de Error con Flash', 'error')
    return redirect(url_for('index'))

@app.route('/contacto')
def contacto(): # Funcion para la ruta de contacto
    return render_template('contacto.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/acercade')
def about(): # Funcion para la ruta de acerca de
    return render_template('acercade.html')

@app.route('/login')
def login(): # Funcion para la ruta de login
    return render_template('login.html')

@app.route('/mensajes')
def mensajes():
    return render_template('mensajes.html')

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

@app.route('/registros')
def registros(): # Funcion para la ruta de registros
    return render_template('registros.html')

@app.route('/productos')
def productos(): # Funcion para la ruta de productos
    return render_template('productos.html')

@app.route('/servicios/<nombre>')
def servicios(nombre): # Funcion para la ruta de servicios
    return 'El nombre del servicio es: %s' % nombre

@app.route('/edad/<edad>')
def edad(edad): # Funcion para la ruta de edad
    return 'La edad es: {} años'.format(edad)

@app.route('/suma/<int:num1>/<int:num2>')
def suma(num1, num2):
    resultado=num1+num2
    return 'La suma de {} y {} es: {}'.format(num1,num2,resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecucion la aplicacion en modo de depuracion