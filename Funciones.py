import os
import sqlite3
import configparser
from PIL import Image, ImageTk
import random
import string


def exist_db():
    if not os.path.exists('users.db'):
        conexion = sqlite3.connect('users.db')
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE "usuario"
                          (
                              "id_usuario" varchar(36) NOT NULL,
                              "nick"       varchar(18) NOT NULL,
                              PRIMARY KEY ("id_usuario"),
                              UNIQUE ("nick" ASC)
                          );
                       ''')
        id, nick = obtener_datos_iniciales()
        cursor.execute("INSERT INTO usuario(id_usuario, nick) VALUES ('" + id + "', '" + nick + "');")
        conexion.commit()
        conexion.close()


def obtener_bd():
    exist_db()
    return sqlite3.connect('users.db')


def obtener_datos_iniciales():
    config = configparser.ConfigParser()
    config.read('OnlineFix.ini', encoding='utf-8-sig')
    try:
        if 'User' in config:
            id = config['User']['UUID']
            nick = config['User']['Name']
            return id, nick
    except configparser.NoSectionError:
        print("Error: Sección no encontrada.")
    except configparser.NoOptionError:
        print("Error: Opción no encontrada.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def obtener_nombre_inicial():
    config = configparser.ConfigParser()
    config.read('OnlineFix.ini', encoding='utf-8-sig')
    try:
        if 'User' in config:
            nick = config['User']['Name']
            return nick
    except configparser.NoSectionError:
        print("Error: Sección no encontrada.")
    except configparser.NoOptionError:
        print("Error: Opción no encontrada.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def png_to_ico(org):
    imagen = Image.open(org)
    return ImageTk.PhotoImage(imagen)


def auxiliar():
    print("funciono")


def obt_all_users():
    conexion = obtener_bd()
    cursor = conexion.cursor()
    cursor.execute('''SELECT nick
                      FROM usuario
                      ORDER BY nick''')
    resp = cursor.fetchall()
    conexion.close()
    return resp


def verificar_no_nick_repetidos(new_nick):
    conexion = obtener_bd()
    cursor = conexion.cursor()
    cursor.execute('''SELECT nick
                      FROM usuario''')
    resp = cursor.fetchall()
    conexion.close()
    filt_res = []
    for elem in resp:
        filt_res.append(elem[0])
    if new_nick in filt_res:
        return True
    else:
        return False

def verificar_no_id_repetidos(new_id):
    conexion = obtener_bd()
    cursor = conexion.cursor()
    cursor.execute('''SELECT id_usuario
                      FROM usuario''')
    resp = cursor.fetchall()
    conexion.close()
    filt_res = []
    for elem in resp:
        filt_res.append(elem[0])
    if new_id in filt_res:
        return True
    else:
        return False


def instertar_usuarios(nick):
    conexion = obtener_bd()
    cursor = conexion.cursor()
    id =elaborar_id()
    cursor.execute("INSERT INTO usuario(id_usuario, nick) VALUES ('" + id + "', '" + nick + "');")
    conexion.commit()
    conexion.close()


def elaborar_id():
    while True:
        new_id = str(random.randint(1, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + "-"
        new_id = new_id + str(random.randint(1, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + "-"
        new_id = new_id + str(random.randint(1, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + "-"
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + "-"
        new_id = new_id + str(random.randint(1, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))
        new_id = new_id + random.choice(string.ascii_lowercase)
        new_id = new_id + str(random.randint(0, 9))

        if not verificar_no_id_repetidos(new_id):
            return new_id

def editar_datos(id, nick):
    config = configparser.ConfigParser()
    config.read('OnlineFix.ini', encoding='utf-8-sig')
    try:
        if 'User' in config:
            config['User']['UUID'] = id
            config['User']['Name'] = nick
    except configparser.NoSectionError:
        print("Error: Sección no encontrada.")
    except configparser.NoOptionError:
        print("Error: Opción no encontrada.")
    except Exception as e:
        print(f"Error inesperado: {e}")

    with open('OnlineFix.ini', 'w', encoding='utf-8-sig') as configfile:
        config.write(configfile)


def obtener_id(nick):
    conexion = obtener_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario FROM usuario WHERE nick = '"+nick+"'")
    resp = cursor.fetchall()
    conexion.close()
    return resp[0][0]