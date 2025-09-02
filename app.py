from flask import Flask, render_template, url_for

app=Flask(__name__)

@app.route('/')
def index(): # Funcion para la ruta principal
    return render_template('index.html')

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
    app.run(debug=True, port=8000)  # Ejecucion la aplicacion en modo de depuracion