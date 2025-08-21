from flask import Flask, render_template, request

app=Flask(__name__)

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


@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)