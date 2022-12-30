from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from models.encriptar_contraseña import hash_password
from config import settings
from config.db_login import db
from smtplib import SMTP
from email.message import EmailMessage
from models import consultas, condicionales
app = Flask(__name__)

app.secret_key = "secretkey"
s=URLSafeTimedSerializer("elpepe")


@app.route("/")
def simple_function():
    return render_template("pre_home.html")

@app.get("/login")
def renderlogin():

    return render_template("login.html")


@app.route("/login", methods=['GET','POST'])
def login():
   
    if request.method == 'POST':
        email = request.form['email']
        passwor = request.form['password']
        password = hash_password(password=passwor)
        
        if consultas.datos_de_login(email=email, password=password) == True:
            user = consultas.session_user(email=email, password=password)
            
            session['id'] = user['id']
            
            return redirect(url_for('render_home'))
        else:
            flash("Algo salió mal, revisa tus credenciales")
        return render_template("login.html")
    return render_template("login.html")


@app.route('/registro', methods=['GET','POST'])
def registro():
    
    if request.method=='POST':
        password = request.form['password']
        status=0
        if password == "":
            flash("ingrese la contraseña")
            return render_template("registro.html")
        if condicionales.politica_password(password=password)==True:
            password=hash_password(password=password)
            username = request.form['username']
            if username == "":
                flash("ingrese el nombre de usuario")
                return redirect(url_for('registro'))
            email = request.form['email']
            original_email = consultas.email_no_repetido(email)
            flag = True       
            phone = request.form['phone']
            if phone == "":
                flash("ingrese el número telefónico ")
                return redirect(url_for('registro'))
            description = request.form['description']
            if description == "":
                flash("ingrese una descripción")
                return redirect(url_for('registro'))
            address = request.form['address']
            if address == "":
                flash("ingrese una dirección")
                return redirect(url_for('registro'))
            image = request.files['image']
            if image == "":
                flash("ingrese una imágen")
                return redirect(url_for('registro'))
            if (len(original_email)>0):
                flash("El correo ingresado para registrar su empresa, se encuentra en uso, no olvide cargar su logo ")
                flag = False
            if flag == False:
                return render_template("registro.html", username=username,phone=phone,description=description, address=address,image=image)
        #---------------consultar sobre marca de tiempo------------------------
            nombre_imagen = image.filename
            image.save("./static/cambiar_avatar/"+nombre_imagen)
            consultas.insertar_registro_a_db(username=username, email=email, password=password, status=status ,phone=phone, description=description, address=address, image="/static/cambiar_avatar/"+nombre_imagen)  
            
            token=s.dumps(email, salt="email-confirm")
            link = url_for("confirmaremail", token=token, _external=True) 

            msg = EmailMessage()
            msg.set_content("Token de validación: {}".format(link))
            msg["Subject"] = "Registro de confirmación"    
            msg["From"] = settings.SMTP_EMAIL
            msg["To"]  = email
            username = settings.SMTP_EMAIL
            password = settings.SMTP_PASSWORD
            server = SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            flash("Te hemos enviado a tu email un correo de confirmación. Esto es lo último para crear tu cuenta")
            return redirect(url_for('login'))

        else:
            return render_template("registro.html")

    return render_template("registro.html") 
    

@app.route("/login/confirmaremail/<token>")    
def confirmaremail(token):
    try:
        email=s.loads(token, salt="email-confirm", max_age=60)
        consultas.cambiar_estado_de_status(email=email)        
    except SignatureExpired:
        return "<h1> timeout </h1>"
    return "<h1>"+ email + " Registro terminado, a hora puedes iniciar sesión <a href='"+url_for('login')+"'>Iniciar Sesión</a></h1>"

#-----------------------------------------------------------------------------------------------------------


@app.route("/login/cambiar_contraseña/<token>")
def recuperar_contraseña(token):
    try:
        email=s.loads(token, salt='cambiar', max_age=60)
    except SignatureExpired:
        return render_template("recuperar_contraseña.html")

    return redirect(url_for('cambiarP', email=email, _external=True))


@app.route("/login/recuperar_contraseña", methods=["GET","POST"])
def rec_password():
    if request.method=="POST":
        email = request.form["email"]

        if consultas.change_password(email=email) == True:
            flash("Se ha enviado un correo de acceso para restaurar su contraseña")
            token=s.dumps(email, salt='cambiar')
            link=url_for('recuperar_contraseña', token=token, _external=True)
        
            msg = EmailMessage()
            msg.set_content("Link de acceso para cambiar contraseña: {} ".format(link))
            msg["Subject"] = "Modificar Contraseña"
            msg["From"] = settings.SMTP_EMAIL
            msg["To"] = email
            username = settings.SMTP_EMAIL
            password = settings.SMTP_PASSWORD 
            server = SMTP("smtp.gmail.com:587")
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            flash("Verifica tu correo")
            return render_template("login.html")
        else:
            flash("Algo salió mal")
            return render_template("recuperar_contraseña.html")
    return render_template("recuperar_contraseña.html")

#---------------------------------------------------------------------------------------
@app.route("/login/cambiar_contraseña/actualizada/<email>", methods=["GET", "POST"])
def cambiarP(email):
    if request.method == "POST":
        password = request.form["password"]
        password_confirm = request.form["password-confirm"]
        
        if password == "" or password_confirm == "":
            flash("Los campos de las credenciales son obligatorios")
            return render_template("recuperar_contraseña2.html")
        if password == password_confirm:
            if condicionales.politica_password(password_confirm=password_confirm)==True:
                password_verified = condicionales.politica_password(password_confirm)
                if (password_verified==True):
                    password = hash_password(password=password)
                    consultas.update_password(email=email, password_verified=password_verified)
                    flash("Contraseña actualizada")
                    return render_template("login.html")        
        flash("Las contraseñas no son iguales >:(")
        return ("recuperar_contraseña2.html")

#------------------------------------------------------------------------------------------------------------

@app.get("/user_home")
def render_home(): 
    products = consultas.mostrar_productos_usuario(session['id'])
     
    return render_template("user_home.html",id_user=session['id'], products=products)

@app.route("/user_home",methods=["POST"])
def agregar():
    if request.method=="POST":

        nombre = request.form["nombre"]
        descripción = request.form["descripción"]
        precio = request.form["precio"]
        estado = request.form["estado"]
        imagen = request.files["imagen"]
        es_valido = True
        if nombre == "":
            es_valido = False
            flash("pon el nombre")
        if descripción == "":
            es_valido = False
            flash("pon la descripción")
        if precio == "":
            es_valido = False
            flash("pon el precio")
        if not precio.isdigit():
            es_valido = False
        if estado == "":
            es_valido = False
            flash("pon el estado")
        if imagen == "":
            es_valido = False
            flash("pon la imagen")
        if es_valido == False:
            return render_template("user_home.html", nombre=nombre, descripción=descripción, precio=precio, estado=estado, imagen=imagen)

        nombre_imagen = imagen.filename
        imagen.save('./static/cambiar_avatar/'+'/' + nombre_imagen)
     
        consultas.guardar_datos_de_crud(nombre=nombre, descripción=descripción, precio=precio, estado=estado,imagen='/static/cambiar_avatar/' + nombre_imagen, id_user=session['id'])
        flash("Nuevo Producto Agregado a la Lista")
        return redirect(url_for("agregar")) 
        
    else:
        flash("no tiene permiso")
        

#----------------------------------------------------------------------------------------------------------------

@app.route("/updating_company_document/<int:id>")
def select_register_company_data(id):

    cursor=db.cursor()
    cursor.execute("SELECT * FROM login_users WHERE id =%s",(
        id,
    ))
    poc=cursor.fetchall()
    cursor.close()
    return render_template("data_updating_company.html", usuario=poc[0])

@app.route("/nameusers/<int:id>")
def name_users(id):

    cursor = db.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT login_users.`username` FROM login_users WHERE id_user = %s",(id,))
    users = cursor.fetchone()
    cursor.close()
    
    return render_template("user_home.html",usuario=users[0])


@app.route("/data_company_company/<int:id>", methods=["GET","POST"])
def updating_data_company(id):

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if password == " ":
            flash("Llene éste campo")
            return render_template("data_updating_company.html")
        if condicionales.politica_password(password=password) == True:
            password=hash_password(password=password)
            email = request.form["email"]
            phone = request.form['phone']
            description = request.form['description']
            address = request.form['address']
            image = request.files['image']
            nombre_imagen = image.filename
            image.save("./static/cambiar_avatar/"+nombre_imagen)
            consultas.updating_company(username=username, password=password, email=email,phone=phone, description=description, address=address, image='/static/cambiar_avatar/' + nombre_imagen, id=id)
            flash("Cambio de datos exitoso")
            return redirect(url_for('render_home'))
        else:
            return render_template("data_updating_company.html",username=username, password=password, email=email,phone=phone, description=description, address=address, image='/static/cambiar_avatar/' + nombre_imagen, id=id)

#-----------------------------------------------------------------------------------------------------
@app.route("/editar/<id>")
def editar(id):
        datos = consultas.editar_productos(id=id)

        return render_template('actualizar_crud.html', productos = datos)

@app.route('/actualizar/<int:id>', methods=["GET","POST"])
def actualizar(id):
    if request.method == 'POST':
        producto = request.form['producto']
        descripción = request.form['descripción']
        precio = request.form['precio']
        estado = request.form['estado']
        imagen = request.files['imagen']

        nombre_imagen = imagen.filename
        imagen.save('./static/cambiar_avatar/'+'/'+nombre_imagen)
        consultas.actualizar_productos(producto=producto, descripción=descripción, precio=precio, estado=estado, imagen='/static/cambiar_avatar/'+nombre_imagen, id=id)
        
        flash('productos actualizados')
        return redirect(url_for("agregar")) 


@app.route("/eliminar/<int:id>")
def eliminar(id):

    cursor=db.cursor()
    cursor.execute("DELETE FROM productos WHERE id = {0}".format(id))
    cursor.close()
    flash('producto eliminado')
    return redirect(url_for('render_home'))

#-----------------------------------------------------------------------------------------------------

@app.get("/productos_empresa")
def company_products():
    products = consultas.mostrar_productos_usuario(session['id'])
    
    return render_template("menu_empresa.html", id_user=session['id'], products=products)

@app.route("/productos_empresa/<string:id_user>", methods=['GET','POST'])
def productos_empresa(id_user):
    
    products = consultas.mostrar_productos_usuario(id_user)

    return render_template("menu_empresa.html", products=products)

#------------------------------------------------------------------------------------------
@app.route('/layout', methods=["GET","POST"])
def layout():
    session.clear()
    return redirect(url_for('login'))

#------------------------------------------------------------------------------------------        



if __name__ == '__main__':
    app.run(debug=True)     