
var fps = 50, fondo, bolaroja, bolaazul, canvas, ctx, ancho = 1080, largo = 608;//Variables
var nbolas =9;
var posiciones =[];
//Inicio del juego.
var bola = function () {//Objeto bola
    
    this.dibujarBolita = function(){
        for(var i =0; i<nbolas;i++){
            this.color = colorAleatorio();
            if(this.color == 1){
                dibujarRoja();
            }else{
                dibujarAzul();
            }
            posiciones.push([objBola.x, objBola.y,this.color]);
            aleatorio();
        }       
    }
}
var bola1 = new bola();//Objeto bola1

function colorAleatorio(){//Color aleatorio, 1=rojo 0=azul
    var colors = Math.floor(Math.random() * (1 - 0 + 1) + 0);
    return colors;
}
var objBola = {x: 100 , y: 100};

function ini_canvas(){//Inicializo el canvas
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    cargarImagenes();
}

function cargarImagenes() {//Cargo la imagenes del aimbot
    bolaazul = new Image();
    bolaroja = new Image();
    fondo = new Image();
    bolaazul.src = "bolaazul.png";
    bolaroja.src = "bolaroja.png";
    fondo.src = "fondo.jpg";
    fondo.onload = function(){
        dibujarFondo();
        bola1.dibujarBolita();
        logicaBola();
    }
}
function borrarCanvas() {
    canvas.width = ancho;
    canvas.height = largo;
    dibujarFondo();
}

function dibujarFondo() {
    ctx.drawImage(fondo,0,0,1080,608,0,0,1080,608);
}

function logicaBola() {
    canvas.addEventListener('click',function(evento){
        var posMouse = getMouse(evento);
        verificacion(posMouse);
        console.log(posMouse.posx + " " + posMouse.posy);
    });
}

function getMouse(evento) {
    return {
        posx: evento.clientX, posy: evento.clientY
    };    
}
var puntaje_html= document.getElementById("puntajeprototipo");
var puntos=0;
function verificacion(posMouse) {
    //console.log("Hola");
    var bool = false;
    for(var i =0; i< nbolas;i++){
        if(posMouse.posx >= posiciones[i][0] && posMouse.posy >= posiciones[i][1]){
            if(posMouse.posx <= posiciones[i][0] + 48 && posMouse.posy <= posiciones[i][1] + 48){
                //Borrar la bola que fue clickeada
                //1.  Borrar canvas
                borrarCanvas();
                //2. Las bolitas que ya fueron seleccionadadas se las guarda con -1
                posiciones[i][0] = -1;
                posiciones[i][1] = -1;
                //3. Imprimir las bolitas que no han sido seleccionadas
                reaparecer();
                puntos+=1;
                bool=true;
                puntaje_html.innerHTML = puntos;
                break;
            }
        }
    }
    if(bool==false){
        puntos-=1;
        puntaje_html.innerHTML = puntos;
    }



}

function aleatorio(){
    objBola.x =  Math.floor(Math.random() * (980 - 100 + 1) + 100);
    objBola.y = Math.floor( Math.random() * (508 - 100 + 1) + 100);
    //console.log (objBola.x + " x  " + objBola.y);
}

function dibujarRoja(){
    ctx.drawImage(bolaroja,0,0,30,30,objBola.x,objBola.y,50,50);
}
function dibujarAzul(){
    ctx.drawImage(bolaazul,0,0,30,30,objBola.x,objBola.y,50,50);  
}

function reaparecer(){
    for(var i =0; i < nbolas;i++){
        if(posiciones[i][0] != -1){
            objBola.x = posiciones[i][0];
            objBola.y = posiciones[i][1];
            if(posiciones[i][2] == 1){
                dibujarRoja();
            }
            else{
                dibujarAzul();
            }
        }
    }
}
