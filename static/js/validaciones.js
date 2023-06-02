function soloLetras(e){
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = "8-37-39-46";

    tecla_especial = false
    for(var i in especiales){
         if(key == especiales[i]){
             tecla_especial = true;
             break;
         }
     }

     if(letras.indexOf(tecla)==-1 && !tecla_especial){
         return false;
     }
 }


 function soloNumeros(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras =  letras = "0123456789";
    especiales = [8, 37, 39, 46];

    tecla_especial = false
    for(var i in especiales) {
        if(key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla) == -1 && !tecla_especial)
        return false;

    }


   


      var checkbox = document.getElementById('ischecked ');
      checkbox.addEventListener("change", validaCheckbox, false);
      function validaCheckbox(){
      var checked = checkbox.checked;
      if(checked){
          alert('checkbox esta seleccionado');
      }
      }



      


      function validaVacio(valor) {
        valor = valor.replace("&nbsp;", "");
        valor = valor == undefined ? "" : valor;
        if (!valor || 0 === valor.trim().length) {
            return true;
            }
        else {
            return false;
            }
        }


      function validarfor(){
    
        var correo = document.getElementById("correo").value; 
        var nombres = document.getElementById("nombres").value;
        var usuario = document.getElementById("usuario").value;
        var cedula = document.getElementById("cedula").value;
        var clave = document.getElementById("clave").value;
        var telefono = document.getElementById("telefono").value;
        var comentarios = document.getElementById("comentarios").value;
     
        var nombre = document.getElementById("nombre").value;
        var descripcion = document.getElementById("descripcion").value; 
        var cantidad = document.getElementById("cantidad").value;
        var precio = document.getElementById("precio").value;  
    
        if ( validaVacio(correo.value) || validaVacio(nombres.value) || validaVacio(usuario.value) || validaVacio(telefono.value) || validaVacio(cedula.value) || validaVacio(comentarios.value )|| validaVacio(clave.value )|| validaVacio(nombre.value ) || validaVacio(descripcion.value )|| validaVacio(cantidad.value )|| validaVacio(precio.value )) {  //COMPRUEBA CAMPOS VACIOS
            alert("Los campos no pueden quedar vacios");
            return false;
        }
        return true;

        }