from flask import flash

def politica_password(password):

        validar=False 
        long=len(password) 
        espacio=False  
        mayuscula=False 
        minuscula=False 
        numeros=False 
        y=password.isalnum()
        correcto=True 
        
        for carac in password: 

            if carac.isspace()==True: 
                espacio=True 

            if carac.isupper()== True: 
                mayuscula=True
                
            if carac.islower()== True:
                minuscula=True 
                
            if carac.isdigit()== True:
                numeros=True 
  
        if espacio==True: 
                flash("La contraseña no puede contener espacios")
        else:
            validar=True
                       
        if long <8 and validar==True:
            flash("La contraseña debe tener mínimo 8 caracteres")
            validar=False 

        if mayuscula == True and minuscula ==True and numeros == True and y== False and validar ==True:
           validar = True
        else:
           correcto=False 
           
        if validar == True and correcto==False:
           flash("La contraseña elegida no es segura:")
           flash("debe contener mínimo una minúscula, una mayúscula")
           flash("un número y al menos 1 carácter no alfanumérico o simbolo")

        if validar == True and correcto ==True:
           return True
    