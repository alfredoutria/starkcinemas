from fileinput import close
from re import template
from string import punctuation
from flask import Flask, render_template,  request, flash, redirect, url_for
from db import init_db
from db import conexion
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
from os import remove

app = Flask(__name__)

app.debug = True #para poder actualizar las paginas con solo refrescar las paginas web
app.secret_key = 'c0v1-d1sp4p3l3s#2022' #os.urandom(24)  #'Hola mundo'




def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData



#/////////////////////////////////////////////////////////////////////////////////////
                            #INDEX
#////////////////////////////////////////////////////////////////////////////////////

@app.route('/')
def index():
    strsql = "SELECT* FROM peliculas"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    data = cursorObj.fetchall()
    peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],nombre_imagen=row[10],imagen=row[11]) for row in data]
    return render_template('index.html', peliculas=peliculas)

#/////////////////////////////////////////////////////////////////////////////////////
                            #SUPERADMINISTRADOR
#////////////////////////////////////////////////////////////////////////////////////


@app.route('/agregar', methods=('GET','POST'))
def insertar():
  if(request.method == 'POST' and 'guardar' in request.form):
    titulo = request.form['titulo']
    fecha1 = request.form['fecha1']
    fecha2 = request.form['fecha2']
    fecha3 = request.form['fecha3']
    fecha_total = fecha3 + "-" + fecha2 + "-" + fecha1
    f1 = request.form['fecha1']
    f2 = request.form['fecha2']
    f3 = request.form['fecha3']
    genero = request.form['genero']
    publico = request.form['publico']
    descripcion = request.form['descripcion']
    reparto = request.form['reparto']
    director = request.form['director']
    cantidad_tiquetes = request.form['cantidad_tiquetes']
    precio = request.form['precio_tiquete']
    p= request.form['precio_tiquete']
    precio_tiquete = '$'+ format(int(precio),",")
    imagen_archivo = request.files['seleccionArchivos']
    

    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
    MEDIA_DIR = os.path.join(BASE_DIR, 'app/static')
    POSTS_IMAGES_DIR = os.path.join(MEDIA_DIR, 'imagenes')

    if imagen_archivo.filename:
        nombre = secure_filename(imagen_archivo.filename)
        num = random.randint(1, 5) 
        aleatorio = str(num)
        image_name = aleatorio  + nombre 
        images_dir = POSTS_IMAGES_DIR
        os.makedirs(images_dir, exist_ok=True)
        file_path = os.path.join(images_dir, image_name)
        imagen_archivo.save(file_path)
     
    ruta = os.path.join(POSTS_IMAGES_DIR, image_name)
    nombre_imagen = image_name
    imagen = convertToBinaryData(ruta)

 
    strsql = "INSERT INTO peliculas (titulo, fecha, genero, publico, descripcion, reparto, director, cantidad_tiquetes, precio_tiquete,nombre_imagen, imagen,f1,f2,f3,p) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,(titulo, fecha_total, genero, publico,descripcion,reparto, director,cantidad_tiquetes,precio_tiquete,nombre_imagen,imagen,f1,f2,f3,p)).fetchone()
    con.commit()
    con.close()
    Directorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
    carpeta1 = os.path.join(Directorio, 'app/static')
    carpeta2 = os.path.join(carpeta1, 'temporal/')
    carpeta_archivo =  os.path.join(carpeta2,nombre_imagen )
    return render_template('guardado.html')
 

  return render_template('administrador_agregar.html')

@app.route('/guardado')
def guardado():
    return render_template('guardado.html')

def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
     


@app.route('/consultar')
def consultar():
    strsql = "SELECT* FROM peliculas"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    data = cursorObj.fetchall()
    peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],nombre_imagen=row[10],imagen=row[11]) for row in data]
    return render_template('cartelera.html', peliculas=peliculas)



@app.route('/crud', methods=('GET','POST'))
def consultar_id():
   if request.method == 'POST' and 'texto' in request.form:
      strsql = "SELECT* FROM peliculas WHERE id LIKE '%" + request.form['texto'] + "%' OR titulo LIKE '%" + request.form['texto'] + "%'"
   else:
     strsql = "SELECT* FROM peliculas"

   con = conexion()
   cursorObj = con.cursor()
   cursorObj.execute(strsql)
   peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],descripcion=row[5],reparto=row[6],director=row[7],cantidad_tiquetes=row[8],precio_tiquete=row[9],nombre_imagen=row[10],imagen=row[11],f1=row[12],f2=row[13],f3=row[14],p=row[15]) for row in cursorObj.fetchall()]
   con.close()

   if 'editar_eliminar' in request.form:
     return render_template('administrador_editar_eliminar.html', peliculas=peliculas)
   return render_template('crud.html', peliculas=peliculas)


@app.route('/editar_eliminar',methods=('GET','POST'))
def editar_eliminar():
  
  id = request.args.get('id')
  strsql = "SELECT * FROM peliculas WHERE id=" + id
  con = conexion()
  cursorObj = con.cursor()
  cursorObj.execute(strsql)
  peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],descripcion=row[5],reparto=row[6],director=row[7],cantidad_tiquetes=row[8],precio_tiquete=row[9],nombre_imagen=row[10],imagen=row[11],f1=row[12],f2=row[13],f3=row[14],p=row[15]) for row in cursorObj.fetchall()]
  con.close()
  


  if(request.method == 'POST' and 'actualizar' in request.form):
    id_actualizar = request.args.get('id')
    imagen_actualizar = request.args.get('nombre_imagen')
    
    titulo = request.form['titulo']
    fecha1 = request.form['fecha1']
    fecha2 = request.form['fecha2']
    fecha3 = request.form['fecha3']
    fecha_total = fecha3 + "-" + fecha2 + "-" + fecha1
    f1 = request.form['fecha1']
    f2 = request.form['fecha2']
    f3 = request.form['fecha3']
    genero = request.form['genero']
    publico = request.form['publico']
    descripcion = request.form['descripcion']
    reparto = request.form['reparto']
    director = request.form['director']
    cantidad_tiquetes = request.form['cantidad_tiquetes']
    precio = request.form['precio_tiquete']
    precio_tiquete = '$'+ format(int(precio),",") 
    imagen_archivo = request.files['seleccionArchivos']

  
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  
    MEDIA_DIR = os.path.join(BASE_DIR, 'app/static')
    POSTS_IMAGES_DIR = os.path.join(MEDIA_DIR, 'imagenes')
    imagenEliminar = os.path.join(POSTS_IMAGES_DIR, imagen_actualizar)
    if imagen_archivo:
         nombre = secure_filename(imagen_archivo.filename)
         num = random.randint(1, 5) 
         aleatorio = str(num)
         image_name = aleatorio  + nombre 
         images_dir = POSTS_IMAGES_DIR
         os.makedirs(images_dir, exist_ok=True)
         file_path = os.path.join(images_dir, image_name)
         imagen_archivo.save(file_path)

         ruta = os.path.join(POSTS_IMAGES_DIR, image_name)
         nombre_imagen = image_name
         imagen = convertToBinaryData(ruta)

         imagenEliminar = os.path.join(POSTS_IMAGES_DIR, imagen_actualizar)
         remove(imagenEliminar)
         strsql = "UPDATE peliculas SET titulo=?, fecha=?, genero=?, publico=?, descripcion=?, reparto=?, director=?, cantidad_tiquetes=?, precio_tiquete=?, nombre_imagen=?, imagen=?, f1=?, f2=?, f3=? WHERE id = " +  id_actualizar +""
         con = conexion()
         cursorObj = con.cursor()
         cursorObj.execute(strsql,(titulo, fecha_total, genero, publico, descripcion, reparto, director, cantidad_tiquetes, precio_tiquete, nombre_imagen, imagen, f1,f2,f3))
         con.commit()
         con.close()
         return render_template('actualizado.html')

    
    else:
     strsql = "UPDATE peliculas SET titulo=?, fecha=?, genero=?, publico=?, descripcion=?, reparto=?, director=?, cantidad_tiquetes=?, precio_tiquete=?, f1=?, f2=?, f3=? WHERE id = " +  id_actualizar +""
     con = conexion()
     cursorObj = con.cursor()
     cursorObj.execute(strsql,(titulo, fecha_total, genero, publico, descripcion, reparto, director, cantidad_tiquetes, precio_tiquete, f1,f2,f3))
     con.commit()
     con.close()
     return render_template('actualizado.html')
  
  if (request.method == 'POST' and 'eliminar' in request.form):
      id_eliminar = request.args.get('id')
      imagen_eliminar = request.args.get('nombre_imagen')
   
      strsql = "DELETE FROM peliculas WHERE id = " + id_eliminar 
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      con.commit()
      con.close()
       
      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

      MEDIA_DIR = os.path.join(BASE_DIR, 'app/static')
      POSTS_IMAGES_DIR = os.path.join(MEDIA_DIR, 'imagenes')

      Ruta_imagen = os.path.join(POSTS_IMAGES_DIR, imagen_eliminar)
      remove(Ruta_imagen)

      return render_template('eliminado.html')

  return render_template('administrador_editar_eliminar.html',peliculas=peliculas)

@app.route('/panel_super')
def panel_super():
  return render_template('superadministrador.html')



#/////////////////////////////////////////////////////////////////////////////////////
                            # ADMINISTRADOR
#////////////////////////////////////////////////////////////////////////////////////

@app.route('/registrarAdministrador',methods=('GET','POST'))
def registrarAdminstrador():
   if(request.method == 'POST' and 'registrar_admin' in request.form):
    nombres = request.form['nombres']
    genero = request.form['genero']
    usuario = request.form['usuario']
    tipo_cedula = request.form['tipo_cedula']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']
    f1 = request.form['f1']
    f2 = request.form['f2']
    f3 = request.form['f3']
    clave = generate_password_hash(request.form['clave'])
    
 
    strsql = "INSERT INTO admin (usuario, clave, nombres,genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,(usuario, clave, nombres,genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3)).fetchone()
    con.commit()
    con.close()

    strsql = "SELECT* FROM peliculas"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    data = cursorObj.fetchall()
    peliculas= [dict(titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],nombre_imagen=row[10],imagen=row[11]) for row in data]
    return render_template('admin.html',usuario=usuario, peliculas=peliculas)
 

   return render_template('admin_registrar.html')


@app.route('/crudAdministrador', methods=('GET','POST'))
def crudAdministrador():
   if request.method == 'POST' and 'texto' in request.form:
      strsql = "SELECT* FROM admin WHERE id LIKE '%" + request.form['texto'] + "%' OR usuario LIKE '%" + request.form['texto'] + "%'"
   else:
     strsql = "SELECT* FROM admin"

   con = conexion()
   cursorObj = con.cursor()
   cursorObj.execute(strsql)
   administrador= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
   con.close()
   if 'usuario_editar_eliminar' in request.form:
     return render_template('admin_editar_eliminar.html',administrador=administrador)
   return render_template('crud_admin.html', administrador=administrador)



@app.route('/admin_editar_eliminar',methods=('GET','POST'))
def admin_editar_eliminar():
  
  id = request.args.get('id')
  strsql = "SELECT * FROM admin WHERE id=" + id
  con = conexion()
  cursorObj = con.cursor()
  cursorObj.execute(strsql)
  administrador= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
  con.close()
  


  if(request.method == 'POST' and 'admin_actualizar' in request.form):
    id_actualizar = request.args.get('id')
    
    nombres = request.form['nombres']
    usuario = request.form['usuario']
    genero = request.form['genero']
    tipo_cedula = request.form['tipo_cedula']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']
    f1 = request.form['f1']
    f2 = request.form['f2']
    f3 = request.form['f3']

  
  
    strsql = "UPDATE admin SET usuario=?, nombres=?, genero=?, correo=?, tipo_cedula=?, cedula=?, telefono=?,f1=?,f2=?,f3=? WHERE id = " +  id_actualizar +""
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,(usuario, nombres, genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3))
    con.commit()
    con.close()
     
    id = request.args.get('id')
    strsql = "SELECT * FROM admin"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    administrador= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
    con.close()

    return render_template('crud_admin.html', administrador=administrador)
    



  if (request.method == 'POST' and 'admin_eliminar' in request.form):
      id_eliminar = request.args.get('id')

   
      strsql = "DELETE FROM admin WHERE id = " + id_eliminar 
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      con.commit()
      con.close()

      id = request.args.get('id')
      strsql = "SELECT * FROM admin"
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      administrador= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
      con.close()
      return render_template('crud_admin.html', administrador=administrador)

  return render_template('admin_editar_eliminar.html', administrador=administrador)

@app.route('/panel_admin')
def panel_admin():
  return render_template('admin.html')



#/////////////////////////////////////////////////////////////////////////////////////
                            #USUARIO
#////////////////////////////////////////////////////////////////////////////////////

@app.route('/registrar',methods=('GET','POST'))
def registrarUsuario():
   if(request.method == 'POST' and 'registrar' in request.form):
    nombres = request.form['nombres']
    genero = request.form['genero']
    usuario = request.form['usuario']
    tipo_cedula = request.form['tipo_cedula']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']
    f1 = request.form['f1']
    f2 = request.form['f2']
    f3 = request.form['f3']
    clave = generate_password_hash(request.form['clave'])
    
 
    strsql = "INSERT INTO usuarios (usuario, clave, nombres,genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,(usuario, clave, nombres,genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3)).fetchone()
    con.commit()
    con.close()

    strsql = "SELECT* FROM peliculas"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    data = cursorObj.fetchall()
    peliculas= [dict(titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],nombre_imagen=row[10],imagen=row[11]) for row in data]
    cerrarSesion = "Cerrar Sesión"
    return render_template('cartelera.html',usuario=usuario, peliculas=peliculas, cerrarSesion=cerrarSesion)
 

   return render_template('registrate.html')


@app.route('/pelicula',methods=('GET','POST'))
def pelicula():

    id = request.args.get('id')
    usuario = request.args.get('usuario')
    cerrarSesion = request.args.get('cerrarSesion')
    strsql = "SELECT * FROM peliculas WHERE id=" + id
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],descripcion=row[5],reparto=row[6],director=row[7],cantidad_tiquetes=row[8],precio_tiquete=row[9],nombre_imagen=row[10],imagen=row[11],f1=row[12],f2=row[13],f3=row[14],p=row[15]) for row in cursorObj.fetchall()]
    con.close()

    strsql = "SELECT* FROM comentarios"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    data = cursorObj.fetchall()
    comentarios= [dict(pelicula=row[1], usuario=row[2],comentario=row[3],puntuacion=row[4]) for row in data]
    #<input type="submit" name="boton_eliminar_co" id="boton_eliminar_co"  style="color: white; cursor: pointer; border: none; border-radius: 10px; background: rgb(199, 11, 11); width: 150px; height: 30px; font-size: 15px;" value="Eliminar comentario">

    if(request.method == 'POST' and 'boton_comentarios' in request.form):
      nombre_usuario = request.form['usuario']
      pelicula = request.form['pelicula']
      comentario = request.form['comentario']
      puntuacion = request.form['puntuacion']


      if len(nombre_usuario)>0: 
       strsql = "INSERT INTO comentarios (pelicula,usuario, comentario, puntuacion) VALUES (?,?,?,?)"
       con = conexion()
       cursorObj = con.cursor()
       cursorObj.execute(strsql,(pelicula,nombre_usuario, comentario, puntuacion)).fetchone()
       con.commit()
       con.close()
    
       strsql = "SELECT* FROM comentarios"
       con = conexion()
       cursorObj = con.cursor()
       cursorObj.execute(strsql)
       data = cursorObj.fetchall()
       comentarios= [dict(id=row[0],pelicula=row[1], usuario=row[2],comentario=row[3],puntuacion=row[4]) for row in data]
       return render_template('pelicula.html',usuario=usuario, peliculas=peliculas,comentarios=comentarios)
      
      else:
       flash('Para hacer comentarios debes Inciar Sesion')
   
    return render_template('pelicula.html',usuario=usuario, peliculas=peliculas,comentarios=comentarios,cerrarSesion=cerrarSesion)



@app.route('/crudUsuario', methods=('GET','POST'))
def crudUsuario():
   if request.method == 'POST' and 'texto' in request.form:
      strsql = "SELECT* FROM usuarios WHERE id LIKE '%" + request.form['texto'] + "%' OR usuario LIKE '%" + request.form['texto'] + "%'"
   else:
     strsql = "SELECT* FROM usuarios"

   con = conexion()
   cursorObj = con.cursor()
   cursorObj.execute(strsql)
   usuarios= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
   con.close()
   if 'usuario_editar_eliminar' in request.form:
     return render_template('usuario_editar_eliminar.html',usuarios=usuarios)
   return render_template('crud_usuario.html', usuarios=usuarios)



@app.route('/usuario_editar_eliminar',methods=('GET','POST'))
def usuario_editar_eliminar():
  
  id = request.args.get('id')
  strsql = "SELECT * FROM usuarios WHERE id=" + id
  con = conexion()
  cursorObj = con.cursor()
  cursorObj.execute(strsql)
  usuarios= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
  con.close()
  


  if(request.method == 'POST' and 'usuario_actualizar' in request.form):
    id_actualizar = request.args.get('id')
    
    nombres = request.form['nombres']
    usuario = request.form['usuario']
    genero = request.form['genero']
    tipo_cedula = request.form['tipo_cedula']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']
    f1 = request.form['f1']
    f2 = request.form['f2']
    f3 = request.form['f3']

  
  
    strsql = "UPDATE usuarios SET usuario=?, nombres=?, genero=?, correo=?, tipo_cedula=?, cedula=?, telefono=?,f1=?,f2=?,f3=? WHERE id = " +  id_actualizar +""
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,(usuario, nombres, genero, correo, tipo_cedula, cedula, telefono,f1,f2,f3))
    con.commit()
    con.close()

    id = request.args.get('id')
    strsql = "SELECT * FROM usuarios"
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
    con.close()
    return render_template('crud_usuario.html', usuarios=usuarios)

    



  if (request.method == 'POST' and 'usuario_eliminar' in request.form):
      id_eliminar = request.args.get('id')

   
      strsql = "DELETE FROM usuarios WHERE id = " + id_eliminar 
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      con.commit()
      con.close()

      id = request.args.get('id')
      strsql = "SELECT * FROM usuarios"
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      usuarios= [dict(id=row[0],usuario=row[1],nombres=row[3],genero=row[4],correo=row[5],tipo_cedula=row[6],cedula=row[7],telefono=row[8],f1=row[9],f2=row[10],f3=row[11]) for row in cursorObj.fetchall()]
      con.close()
      return render_template('crud_usuario.html', usuarios=usuarios)



  return render_template('usuario_editar_eliminar.html', usuarios=usuarios)


@app.route('/sesion',methods=('GET','POST'))
def sesion():

  if (request.method == 'POST'):

    tipo_usuario = request.form['tipo_usuario']
    usuario = request.form['usuario']
    clave = request.form['clave']

    if tipo_usuario == 'USUARIO' and 'ingresar' in request.form:
      strsql = "SELECT* FROM usuarios"

      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      datos = cursorObj.fetchall()


      strsql = "SELECT * FROM usuarios WHERE usuario= '"+ usuario +"'" 
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      datos = cursorObj.fetchall()
      con.close()
      if len(datos)>0:
        for fila in datos:
         usuario_bd = fila[1]
         clave_bd = fila[2]
        comparacion = check_password_hash(clave_bd, clave)
        con.close()

        if(comparacion and usuario == usuario_bd):
         strsql = "SELECT* FROM peliculas"
         con = conexion()
         cursorObj = con.cursor()
         cursorObj.execute(strsql)
         data = cursorObj.fetchall()
         peliculas= [dict(id=row[0],titulo=row[1], fecha=row[2],genero=row[3],publico=row[4],nombre_imagen=row[10],imagen=row[11]) for row in data]
         cerrarSesion= 'Cerrar Sesión'
         return render_template('cartelera.html',usuario=usuario, peliculas=peliculas, cerrarSesion=cerrarSesion)
    
        else:
          flash("Los datos son incorrectos")
 
  
    if tipo_usuario == 'ADMINISTRADOR' and 'ingresar' in request.form:
     strsql = "SELECT* FROM admin WHERE usuario= '"+ usuario +"'" 

     con = conexion()
     cursorObj = con.cursor()
     cursorObj.execute(strsql)
     datos = cursorObj.fetchall()

     if len(datos)>0:
       for fila in datos:
        clave_bd = fila[2]
       comparacion = check_password_hash(clave_bd, clave)
       con.close()

       if(comparacion):
        return render_template('admin.html')
    
       else:
        flash("Los datos son incorrectos")

 
    if tipo_usuario == 'SUPERADMINISTRADOR' and 'ingresar' in request.form:
    
     strsql = "SELECT* FROM superadmin WHERE usuario= '"+ usuario +"'" 
     con = conexion()
     cursorObj = con.cursor()
     cursorObj.execute(strsql)
     datos = cursorObj.fetchall()
     con.close()

     if len(datos)>0:
       for fila in datos:
        clave_bd = fila[2]
       comparacion = check_password_hash(clave_bd, clave)
       con.close()

       if(comparacion):
        return render_template('superadministrador.html')
    
       else:
        flash("Los datos son incorrectos")


  return render_template('iniciarSesion.html')



@app.route('/recuperacion', methods=('GET','POST'))
def recuperacion():
   
   if request.method == 'POST' and 'boton_recuperar' in request.form:
     nombre_usuario = request.form['usuario']
     cedula = request.form['cedula']
     telefono = request.form['telefono'] 
     f1 = request.form['f1']
     f2= request.form['f2']
     f3 = request.form['f3']  


        
     strsql = "SELECT * FROM usuarios WHERE usuario= '"+ nombre_usuario +"'" 
     con = conexion()
     cursorObj = con.cursor()
     cursorObj.execute(strsql)
     datos = cursorObj.fetchall()
     con.close()
     for fila in datos:
      id_bd=fila[0]
      usuario_bd=fila[1]
      cedula_bd=fila[7]
      telefono_bd=fila[8]
      f1_bd=fila[9]
      f2_bd=fila[10]
      f3_bd=fila[11]
  
     if nombre_usuario == usuario_bd and cedula == cedula_bd and telefono == telefono_bd and f1 == f1_bd and f2 == f2_bd and f3 == f3_bd:
        return redirect(url_for('nueva_contraseña',id_usuario=id_bd))
     else:
       flash('Datos Incorrectos o no existe el usuario')
       return render_template('recuperar_contraseña.html') 

   return render_template('recuperar_contraseña.html')


   
@app.route('/nueva_contraseña', methods=('GET','POST'))
def nueva_contraseña():

    if request.method == 'POST' and 'boton_nueva_contraseña' in request.form:
      id = request.args.get('id_usuario')
      nuevaContraseña = request.form['nuevaContraseña']

      clave = generate_password_hash(nuevaContraseña)

      strsql = "UPDATE usuarios SET clave='"+ clave +"' WHERE id= '"+ id +"'"
      con = conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      con.commit()
      con.close()
      return redirect(url_for('sesion'))

    else:
     return render_template('nueva_contraseña.html')  




@app.route('/nosotros')
def nosotros():
  return render_template('nosotros.html')


@app.route('/terminos')
def terminos():
  return render_template('terminos.html')

@app.route('/habeasData')
def heabeas():
  return render_template('habeasData.html')


#/////////////////////////////////////////////////////////////////////////////
                      # CONTACTENOS
#/////////////////////////////////////////////////////////////////////////////


@app.route('/contactos',methods=('GET','POST'))
def contactos():
   if(request.method == 'POST' and 'boton_enviar_contacto' in request.form):
     nombres = request.form['nombres']
     cedula = request.form['cedula']
     correo = request.form['correo']
     telefono = request.form['telefono']
     motivo = request.form['motivo']
    
 
     strsql = "INSERT INTO contactos (nombres, cedula, correo,telefono, motivo) VALUES (?,?,?,?,?)"
     con = conexion()
     cursorObj = con.cursor()
     cursorObj.execute(strsql,(nombres, cedula, correo,telefono, motivo)).fetchone()
     con.commit()
     con.close()
     return render_template('contactenos.html')
   return render_template('contactenos.html')



@app.route('/crudContactos', methods=('GET','POST'))
def crudContactos():
   if request.method == 'POST' and 'texto' in request.form:
      strsql = "SELECT* FROM contactos WHERE id LIKE '%" + request.form['texto'] + "%' OR usuario LIKE '%" + request.form['texto'] + "%'"
   else:
     strsql = "SELECT* FROM contactos"

   con = conexion()
   cursorObj = con.cursor()
   cursorObj.execute(strsql)
   usuarios= [dict(id=row[0],nombres=row[1],cedula=row[2],correo=row[3],telefono=row[4],motivo=row[5]) for row in cursorObj.fetchall()]
   con.close()
   if 'contacto_editar_eliminar' in request.form:
     return render_template('contactos_editar_eliminar.html',usuarios=usuarios)
   return render_template('crud_contactos.html', usuarios=usuarios)



@app.route('/contactos_editar_eliminar',methods=('GET','POST'))
def contactos_editar_eliminar():
  
    id = request.args.get('id')
    strsql = "SELECT * FROM contactos WHERE id=" + id
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios= [dict(id=row[0],nombres=row[1],cedula=row[2],correo=row[3],telefono=row[4],motivo=row[5]) for row in cursorObj.fetchall()]
    con.close()
  
    if (request.method == 'POST' and 'contacto_eliminar' in request.form):
       id_eliminar = request.args.get('id')

   
       strsql = "DELETE FROM contactos WHERE id = " + id_eliminar 
       con = conexion()
       cursorObj = con.cursor()
       cursorObj.execute(strsql)
       con.commit()
       con.close()
        
       id = request.args.get('id')
       strsql = "SELECT * FROM contactos"
       con = conexion()
       cursorObj = con.cursor()
       cursorObj.execute(strsql)
       usuarios= [dict(id=row[0],nombres=row[1],cedula=row[2],correo=row[3],telefono=row[4],motivo=row[5]) for row in cursorObj.fetchall()]
       con.close()
       return render_template('crud_contactos.html', usuarios=usuarios)
    return render_template('contactos_editar_eliminar.html', usuarios=usuarios)



    #/////////////////////////////////////////////////////////////////////////////
                      # COMENTARIOS
#/////////////////////////////////////////////////////////////////////////////

@app.route('/crudComentarios', methods=('GET','POST'))
def crudComentarios():
   if request.method == 'POST' and 'texto' in request.form:
      strsql = "SELECT* FROM comentarios WHERE id LIKE '%" + request.form['texto'] + "%' OR usuario LIKE '%" + request.form['texto'] + "%'"
   else:
     strsql = "SELECT* FROM comentarios"

   con = conexion()
   cursorObj = con.cursor()
   cursorObj.execute(strsql)
   usuarios= [dict(id=row[0],pelicula=row[1],nombre_usuario=row[2],comentario=row[3],punctuation=row[4]) for row in cursorObj.fetchall()]
   con.close()
   if 'comentario_editar_eliminar' in request.form:
     return render_template('comentarios_editar_eliminar.html',usuarios=usuarios)
   return render_template('crud_comentarios.html', usuarios=usuarios)



@app.route('/comentarios_editar_eliminar',methods=('GET','POST'))
def comentarios_editar_eliminar():
  
    id = request.args.get('id')
    strsql = "SELECT * FROM comentarios WHERE id=" + id
    con = conexion()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    usuarios= [dict(id=row[0],pelicula=row[1],nombre_usuario=row[2],comentario=row[3],punctuation=row[4]) for row in cursorObj.fetchall()]
    con.close()
  
    if (request.method == 'POST' and 'comentario_eliminar' in request.form):
       id_eliminar = request.args.get('id')

   
       strsql = "DELETE FROM comentarios WHERE id = " + id_eliminar 
       con = conexion()
       cursorObj = con.cursor()
       cursorObj.execute(strsql)
       con.commit()
       con.close()
       return render_template('crud_comentarios.html', usuarios=usuarios)
    return render_template('comentarios_editar_eliminar.html', usuarios=usuarios)

if __name__ =='__main__': #para que pueda funcionar el app.debug = true

   app.run(debug=True)