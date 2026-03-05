// Lógica de las pestañas principales de perfil (mis artículos y mis solicitudes)

// 1. evt: recibe a información del evento (el click que hacemos)
// 2. tabName: el id del bloque que queremos mostrar (el de mis artículos o mis solicitudes) 
function openTab(evt,tabName){

    //Para esconder todos los bloques del contenido
    let tabcontent = document.getElementsByClassName("tab-content") //Obtenemos las tuplas
    for(let i=0; i<tabcontent.length; i++){

        tabcontent[i].style.display = "none";   //Los hacemos invisibles para que no se muestren
    }

    //Para quitarle el resaltado visual a los botones
    let tablinks = document.getElementsByClassName("tab-link") //Obtenemos las tuplas de los botones
    for(let i = 0; i<tablinks.length; i++){

        tablinks[i].className = tablinks[i].className.replace(" active",""); //Le quitamos la plalabra active del nombre de su clase
    }

    //Mostramos la información
    document.getElementById(tabName).style.display = "block";   //Muestra el contenido que hayamos especificado
    evt.currentTarget.className += " active";   //Activamos el elemento que acabe de ser clicado
}

// estadoBuscado = 'Publicado', 'Reservado', etc.
// claseTarjetas = 'mueble-container' o 'solicitud-card'
// claseBotones = 'filtro-articulos' o 'filtro-solicitudes'
function filtrar(evt, estadoBuscado, claseTarjetas, claseBotones){
    
    // Para actualizar el color de los botones
    let botones = document.getElementsByClassName(claseBotones);
    for (let i = 0; i < botones.length; i++) {
        botones[i].classList.remove("active");
    }

    //Activamos el botón que hemos pulsado
    evt.currentTarget.classList.add("active");

    //Filtramos las tarjetas
    let tarjetas = document.getElementsByClassName(claseTarjetas);
    for (let i = 0; i < tarjetas.length; i++){

        let estadoTarjeta = tarjetas[i].getAttribute("data-estado");
        
        if(estadoBuscado == 'Todos' || estadoTarjeta == estadoBuscado){

            tarjetas[i].style.display = "flex"; 
        }else{

            tarjetas[i].style.display = "none";
        }
    }
}