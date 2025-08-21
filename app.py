from flask import Flask

app=Flask(__name__)

@app.route('/')
def home(): # Funcion para la ruta principal
    return "Hola mundo"

@app.route('/contacto')
def contacto(): # Funcion para la ruta de contacto
    return "Esta es la pagina de contacto"

@app.route('/about')
def about(): # Funcion para la ruta de acerca de
    return "Esta es la pagina de acerca de"

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