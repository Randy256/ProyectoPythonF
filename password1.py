#Bcrypt
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

password_plano = "mi_contraseña_secreta"
hash_contraseña = bcrypt.generate_password_hash(password_plano).decode('utf-8')
print(f"Contraseña encriptada: {hash_contraseña}")

# Para verificar la contraseña
Contraseña_interna = "mi_contraseña_secreta"
Contraseña_interna = bcrypt.check_password_hash(hash_contraseña, Contraseña_interna)
print(f"¿La contraseña es válida? {Contraseña_interna}")