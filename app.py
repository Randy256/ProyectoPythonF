from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL 

mysql = MySQL()
app=Flask(__name__)
app.secret_key = 'mysql' #Clave secreta para sesiones


# conexion de la base de datos
app.config['MYSQL_HOST'] = 'bnt3twhorvgn2whhbuhn-mysql.services.clever-cloud.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'umdcsdsolhwqdwxx'
app.config['MYSQL_PASSWORD'] = '27b7wmzWyoHny5bfz8gr'
app.config['MYSQL_DB'] = 'bnt3twhorvgn2whhbuhn'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

@app.route('/') # Decorador para la ruta principal
def index(): # Funcion para la ruta principal
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

usuarios = []

# ...existing code...

usuarios = []  # Lista en memoria

@app.route('/listar')
def listar():
    # Mostrar usuarios de la lista en memoria, no de la base de datos
    return render_template("listar.html", usuarios=usuarios)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    if nombre and email and password:
        # Generar un ID simple para el usuario
        new_id = len(usuarios) + 1
        usuarios.append({'id': new_id, 'nombre': nombre, 'email': email, 'password': password})
        flash('Usuario agregado en memoria.', 'success')
        # Redirigir a la página de usuario después del registro
        return redirect(url_for('usuario'))
    else:
        flash('Faltan datos.', 'danger')
        return redirect(url_for('registros'))
## ...existing code...

@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    id = int(request.form['id'])
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    # Buscar y actualizar el usuario en la lista en memoria
    for usuario in usuarios:
        if usuario['id'] == id:
            usuario['nombre'] = nombre
            usuario['email'] = email
            usuario['password'] = password
            flash('Usuario actualizado en memoria.', 'success')
            break
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('listar'))

@app.route('/borrarUser/<int:id>', methods=['GET'])
def borrarUser(id):
    global usuarios
    # Eliminar el usuario de la lista en memoria
    usuarios = [u for u in usuarios if u['id'] != id]
    flash('Usuario eliminado en memoria.', 'success')
    return redirect(url_for('listar'))

# ...existing code...

@app.route('/ventas')
def ventas(): # Funcion para la ruta de ventas
    return render_template('ventas.html')

@app.route('/carrito')
def carrito(): # Funcion para la ruta de carrito
    return render_template('carrito.html')

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
                flash('¡Has iniciado sesión como usuario!', 'success')
                return render_template('usuario.html', user=user)
            else:
                flash('Rol de usuario no reconocido.', 'danger')
                return render_template('login.html')
        else:
            flash('Credenciales incorrectas.', 'danger')
            return render_template('login.html')
    # Si la petición no es POST o faltan datos, mostrar login
    return render_template('login.html')

# ...existing code...
@app.route('/productos/agregar')
def listar_productos_agregados():
    # Aquí puedes poner la lógica que necesites
    productos = session.get('productos', [])
    return render_template('agregar_producto.html', productos=productos)
# ...existing code...

@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregarProducto():
    if request.method == 'POST':
        productos = session.get('productos', [])
        nuevo = {
            'id': len(productos) + 1,
            'nombre': request.form['nombre'],
            'precio': request.form['precio'],
            'cantidad': request.form['cantidad'],
            'descripcion': request.form['descripcion']
        }
        productos.append(nuevo)
        session['productos'] = productos
        session.modified = True  # para que Flask guarde los cambios
        return redirect(url_for('agregarProducto'))

    # Si es GET, solo muestra la página con los productos actuales
    productos = session.get('productos', [])
    return render_template('agregar_producto.html', productos=productos)


# ...existing code...
@app.route('/productos/listar')
def listar_productos():
    productos = session.get('productos', [])
    return render_template('listar_productos.html', productos=productos)

# -----------------------------------------------------------
# EDITAR PRODUCTO
# -----------------------------------------------------------
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)

    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['precio'] = request.form['precio']
        producto['descripcion'] = request.form['descripcion']
        session['productos'] = productos
        session.modified = True
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto)


# -----------------------------------------------------------
# BORRAR PRODUCTO
# -----------------------------------------------------------
@app.route('/productos/borrar/<int:id>')
def borrar_producto(id):
    productos = session.get('productos', [])
    nuevos = [p for p in productos if p['id'] != id]
    session['productos'] = nuevos
    session.modified = True
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('listar_productos'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('index'))

@app.route('/registros')
def registros(): # Funcion para la ruta de registros
    return render_template('registros.html')

@app.route('/productos')
def productos(): # Funcion para la ruta de productos
    return render_template('productos.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

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