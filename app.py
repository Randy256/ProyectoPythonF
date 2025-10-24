from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL 

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'mysql'  # Clave secreta para sesiones


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
    user = session.get('user')  # tomar datos del usuario en sesión si existen
    return render_template('usuario.html', user=user)


@app.route('/listar')
def listar():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, nombre, email, password FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template("listar.html", usuarios=usuarios)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    # Obtener el valor del campo oculto. Si no existe (registro público), será None.
    origen = request.form.get('origen_formulario') # NUEVA LÍNEA
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    if nombre and email and password:
        cursor = mysql.connection.cursor()
        # insertar con id_rol = 2 (usuario)
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, password, id_rol) VALUES (%s, %s, %s, %s)',
            (nombre, email, password, 2)
        )
        mysql.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()
        # guardar en session y marcar rol
        session['user'] = {'id': last_id, 'nombre': nombre, 'email': email, 'id_rol': 2}
        session['id_rol'] = 2
        flash('Usuario agregado correctamente.', 'success')

        if origen == 'admin_list':
            # Si viene de listar.html, redirigir a la misma lista (listar.html)
            return redirect(url_for('listar'))
        else:
            # Si viene de registros.html (registro público), redirigir al panel de usuario (usuario.html)
            return redirect(url_for('usuario'))
    else:
        flash('Faltan datos.', 'danger')
        return redirect(url_for('registros'))

@app.route('/updateUsuario', methods=['POST'])
def updateUsuario():
    id = int(request.form['id'])
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE usuarios SET nombre = %s, email = %s, password = %s WHERE id = %s',
        (nombre, email, password, id)
    )
    mysql.connection.commit()
    cursor.close()
    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('listar'))

@app.route('/borrarUser/<int:id>', methods=['GET'])
def borrarUser(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('listar'))

# ...existing code...

@app.route('/ventas')
def ventas(): # Funcion para la ruta de ventas
    return render_template('ventas.html')

@app.route('/carrito')
def carrito(): # Funcion para la ruta de carrito
    return render_template('carrito.html')

# -----------------------------------------------------------
# RUTA CHECKOUT (PAGO)
# -----------------------------------------------------------
@app.route('/checkout')
def checkout():
    # En una aplicación real, esta función manejaría la lógica de pago
    # como validar el carrito, procesar la transacción y registrar la venta.
    
    # Por ahora, solo renderizaremos una plantilla simple de confirmación
    # o de formulario de pago.
    
    # NOTA: Debes crear un archivo llamado 'checkout.html' en la carpeta 'templates'
    
    return render_template('checkout.html')

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

# -----------------------------------------------------------
# AGREGAR PRODUCTO Y MOSTRAR LISTA (EN LA MISMA PÁGINA)
# -----------------------------------------------------------
@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregarProducto():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        marca = request.form['marca']
        caducidad_str = request.form.get('caducidad')
        descripcion = request.form['descripcion']

        # LÓGICA PARA MANEJAR CADUCIDAD: Si está vacío, se envía 'None' (que MySQL interpreta como NULL)
        caducidad_db = caducidad_str if caducidad_str else None

        # Insertar el nuevo producto en la base de datos
        cursor.execute(
            "INSERT INTO productos (nombre, precio, cantidad, marca, caducidad, descripcion) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, precio, cantidad, marca, caducidad_db, descripcion)
        )
        mysql.connection.commit()
        flash('Producto agregado correctamente.', 'success')

    # Obtener la lista actualizada de productos
    cursor.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cursor.fetchall()
    cursor.close()

    # Mostrar la página con el formulario y la tabla de productos
    return render_template('agregar_producto.html', productos=productos)


# -----------------------------------------------------------
# LISTAR PRODUCTOS DESDE MYSQL
# -----------------------------------------------------------
@app.route('/productos/listar')
def listar_productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('listar_productos.html', productos=productos)


# -----------------------------------------------------------
# EDITAR PRODUCTO
# -----------------------------------------------------------
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        marca = request.form['marca']
        caducidad_str = request.form.get('caducidad')
        descripcion = request.form['descripcion']

        # LÓGICA PARA MANEJAR CADUCIDAD: Si está vacío, se envía 'None' (que MySQL interpreta como NULL)
        caducidad_db = caducidad_str if caducidad_str else None

        cursor.execute("""
            UPDATE productos 
            SET nombre = %s, precio = %s, cantidad = %s, marca = %s, caducidad = %s, descripcion = %s
            WHERE id = %s
        """, (nombre, precio, cantidad, marca, caducidad_db, descripcion, id))
        mysql.connection.commit()
        cursor.close()

        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('listar_productos'))

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()

    return render_template('editar_producto.html', producto=producto)


# -----------------------------------------------------------
# ELIMINAR PRODUCTO
# -----------------------------------------------------------
@app.route('/productos/borrar/<int:id>')
def borrar_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

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