#Cryptography
from cryptography.fernet import Fernet

texto = "x?1_p-M.4!eM"

# Generar una clave y guardarla en un archivo

clave = Fernet.generate_key()
objecto = Fernet(clave)
# Encriptar el texto
texto_encriptado = objecto.encrypt(texto.encode())
print(f"Texto encriptado: {texto_encriptado}")

# Desencriptar el texto
texto_desencriptado = objecto.decrypt(texto_encriptado).decode()
print(f"Texto desencriptado: {texto_desencriptado}")