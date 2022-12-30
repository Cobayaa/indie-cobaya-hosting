from config.db_login import db

def email_no_repetido(email):
    cursor = db.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM login_users WHERE email = %s",(
        email,
    ))
    email = cursor.fetchall()
    return email


def datos_de_login(email, password):
    cursor = db.cursor(buffered=True)
    
    cursor.execute("SELECT * FROM login_users WHERE email = %s and password = %s and status='1'",(
        email,
        password,
    ))
    vae = cursor.fetchone()
    cursor.close()  
    variabl = False
    if vae != None:
        variabl=True
    return variabl

def session_user(email, password):
    cursor = db.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM login_users WHERE email = %s and password = %s and status='1'",(
        email,
        password,
    ))
    vae = cursor.fetchone()
    cursor.close()  
    return vae


def insertar_registro_a_db(username, email, password, status, phone, description, address, image):
    cursor = db.cursor(buffered=True)
    cursor.execute("INSERT INTO login_users (username, email, password, status , phone, description, address, image) values (%s,%s,%s,%s,%s,%s,%s,%s)",(
    username, 
    email, 
    password,
    status, 
    phone, 
    description, 
    address, 
    image,
    ))
    cursor.close()


def cambiar_estado_de_status(email):
    cursor = db.cursor(buffered=True)
    cursor.execute("UPDATE login_users SET status='1' WHERE email='"+email+"'"),(
    email,
    )
    cursor.close()

def eliminar_estado_de_status(email):
    cursor = db.cursor(buffered=True)
    cursor.execute("DELETE FROM login_users WHERE email='"+email+"' AND status='0'"),(
    email,
    )
    cursor.close()    


def guardar_datos_de_crud(nombre, descripción, precio, estado, imagen, id_user):
    cursor = db.cursor(dictionary=True)
    cursor.execute("INSERT INTO productos (nombre,descripción,precio,estado,imagen, id_user) VALUES (%s,%s,%s,%s,%s,%s)",(
    nombre, 
    descripción, 
    precio, 
    estado, 
    imagen,
    id_user,
    ))
    cursor.close()


def change_password(email):  
    cursor = db.cursor(buffered=True)
    cursor.execute(" SELECT * FROM login_users WHERE email = '"+email+"' AND status='1' "),(
    email,
    )
    vas = cursor.fetchone()
    cursor.close()  
    validar = False
    if vas != None:
        validar=True
    return validar 
    
def update_password(email, password_verified):
    cursor = db.cursor(buffered=True)
    cursor.execute("UPDATE login_users SET password='"+ password_verified +"' where email='"+ email +"'")
    cursor.close()

   
def editar_productos(id):
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s",(
        id,
    ))
    datos = cursor.fetchone()
    cursor.close()  
    return datos

def actualizar_productos(producto, descripción,precio,estado,imagen, id):
    cursor = db.cursor(buffered=True)
    cursor.execute("UPDATE productos SET nombre = %s, descripción = %s, precio = %s, estado = %s,imagen = %s WHERE id = %s",(
        producto,
        descripción,
        precio,
        estado,
        imagen,
        id,
    ))
    cursor.close()

def mostrar_productos_usuario(id_user):
    cursor = db.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_user = %s",(id_user,))
    products = cursor.fetchall()
    cursor.close()
    return products


def updating_company(username, password, email, phone, description, address, image, id):
    cursor=db.cursor(buffered=True)
    cursor.execute("UPDATE login_users SET username=%s,password=%s, email=%s, phone=%s, description=%s, address=%s, image=%s WHERE id=%s",(
        username,
        password, 
        email, 
        phone, 
        description, 
        address, 
        image, 
        id
    ))
    cursor.close()










