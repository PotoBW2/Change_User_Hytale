import configparser
import os
from Funciones import png_to_ico, auxiliar, obt_all_users, verificar_no_nick_repetidos, instertar_usuarios, \
    obtener_nombre_inicial, obtener_id, editar_datos
from tkinter import *
from tkinter import ttk, messagebox

ventana = Tk()
ventana.title("Change User Hytale - v1.00")
icono = png_to_ico("Icon-256.png")
ventana.iconphoto(True, icono)

"""Centra la ventana en la pantalla"""
ventana.update_idletasks()
ancho = ventana.winfo_width()
alto = ventana.winfo_height()
x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
y = (ventana.winfo_screenheight() // 2) - (alto // 2)
ventana.geometry(f'+{x}+{y}')
ventana.resizable(False, False)
ventana._icono = icono

ventana.principal = ttk.Frame(ventana, padding=(3, 3, 12, 12))
ventana.principal.grid(column=0, row=0, sticky=(N, W, E, S))

ventana.var_usuario = StringVar()
ventana.sel_usuario = ttk.Combobox(ventana.principal, textvariable=ventana.var_usuario, state='readonly', )
ventana.sel_usuario.grid(column=0, row=0)

if os.path.exists('OnlineFix.ini'):
    config = configparser.ConfigParser()
    config.read('OnlineFix.ini', encoding='utf-8-sig')
    ventana.opc_usuario = []
    for elemento in obt_all_users():
        ventana.opc_usuario.append(elemento[0])
    ventana.sel_usuario['values'] = ventana.opc_usuario
    ventana.sel_usuario.set(obtener_nombre_inicial())
else:
    messagebox.showinfo(message='No se pudo encontrar el archivo OnlineFix.ini.', icon='error', title='ERROR')
    ventana.quit()
    ventana.destroy()

ventana.bt_new_user = ttk.Button(ventana.principal, text='Nuevo Usuario',
                                 command=lambda: abrir_ventana_add_user(ventana))
ventana.bt_new_user.grid(column=1, row=0)

ventana.bt_aceptar_user = ttk.Button(ventana.principal, text='Aceptar', command=lambda: editar_init(ventana))
ventana.bt_aceptar_user.grid(column=1, row=1)


def abrir_ventana_add_user(ventana):
    ventana.tl_add_user = Toplevel(ventana)
    ventana.tl_add_user.title("Crear Usuario")
    ventana.tl_add_user.update_idletasks()

    parent_x = ventana.winfo_x()
    parent_y = ventana.winfo_y()
    parent_ancho = ventana.winfo_width()
    parent_alto = ventana.winfo_height()
    x = parent_x + (parent_ancho // 2)
    y = parent_y + (parent_alto // 2)
    ventana.tl_add_user.geometry(f'+{x}+{y}')
    ventana.tl_add_user.resizable(False, False)
    ventana.tl_add_user.transient(ventana)  # Mantener sobre la principal
    ventana.tl_add_user.grab_set()  # Hacerla modal

    ventana.tl_add_user.f_add = ttk.Frame(ventana.tl_add_user, padding=(3, 3, 12, 12))
    ventana.tl_add_user.f_add.grid(column=0, row=0, sticky=(N, W, E, S))

    ventana.tl_add_user.var_nick = StringVar()
    ventana.tl_add_user.e_name = ttk.Entry(ventana.tl_add_user.f_add, textvariable=ventana.tl_add_user.var_nick)
    ventana.tl_add_user.e_name.grid(column=0, row=0, sticky=(N, W, E, S))

    ventana.tl_add_user.bt_add_user = ttk.Button(ventana.tl_add_user.f_add, text='Crear',
                                                 command=lambda: agregar_user_to_bd(ventana))
    ventana.tl_add_user.bt_add_user.grid(column=1, row=0)

def agregar_user_to_bd(ventana):
    if not verificar_no_nick_repetidos(ventana.tl_add_user.var_nick.get()):
        instertar_usuarios(ventana.tl_add_user.var_nick.get())
        ventana.opc_usuario = []
        for elemento in obt_all_users():
            ventana.opc_usuario.append(elemento[0])
        ventana.sel_usuario['values'] = ventana.opc_usuario
        ventana.sel_usuario.set(ventana.tl_add_user.var_nick.get())
        ventana.tl_add_user.destroy()
    else:
        print("nombre repetido")


def editar_init(ventana):
    nick = ventana.var_usuario.get()
    id = obtener_id(nick)
    editar_datos(id, nick)
    ventana.quit()
    ventana.destroy()

ventana.mainloop()
