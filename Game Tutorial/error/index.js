const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');
canvas.width = innerWidth;
canvas.height = innerHeight;

//Create a player
class Player{
    constructor(x, y, radius, color){
        this.x=x;
        this.y=y;
        this.radius=radius;
        this.color=color;
    }
    draw(){
        c.beginPath();
        //Dibujamos el circulo
        c.arc(this.x, this.y, this.radius, 0, Math.PI*2, false);
        c.fillStyle = this.color;
        c.fill();
    }
}

//SHOOT PROJECTILES
class Projectiles{
    constructor(x, y, radius, color, velocity){
        this.x=x;
        this.y=y;
        this.radius=radius;
        this.color=color;
        this.velocity=velocity;
    }
    draw(){
        c.beginPath();
        c.arc(this.x, this.y, this.radius, 0, Math.PI*2, false);
        c.fillStyle= this.color;
        c.fill();
    }
    update(){
        this.draw();
        this.x= this.x+this.velocity.x;
        this.y=this.y+this.velocity.y;
    }
}
//Enemies
class Enemy{
    constructor(x,y,radius,color,velocity){
        this.x=x;
        this.y=y;
        this.radius=radius;
        this.color=color;
        this.velocity=velocity;
    }
    draw(){
        c.beginPath;
        c.arc(this.x, this.y, this.radius, 0, Math.PI*2,false);
        c.fillStyle=this.color;
        c.fill();
    }
    update(){
        this.draw();
        this.x=this.x+this.velocity.x;
        this.y=this.y+this.velocity.y;
    }
}
//GAME WORK
const x = canvas.width/2, y =canvas.height/2;
const player = new Player(x,y,30,'blue');
const projectiles2=[];
const enemies=[];
//Spawn Enemy
function spawnEnemies(){
    setInterval(()=>{
        const x=100, y=100, radius=20, color='green';
        const velocity={
            x:1,
            y:1
        };
        enemies.push(new Enemy(x,y,radius,color,velocity));
        console.log(enemies);
    }, 1000);
}

//Animate the shooter
function animate(){
    requestAnimationFrame(animate);
    //Borra el canvas
    c.clearRect(0,0,canvas.width,canvas.height);
    player.draw();
    projectiles2.forEach(projectile =>{
        projectile.update();
    });
    enemies.forEach(enemy =>{
        enemy.update();
    });

}
window.addEventListener('click', (event)=>{
    //Angle at the same moment when we click
    const angle = Math.atan2(event.clientY-canvas.height/2, event.clientX-canvas.width/2)
    //Velocity x aumenta o dismuniye y en y aumenta o disminuye
    const velocity = {x: Math.cos(angle), y: Math.sin(angle)};
    projectiles2.push(new Projectiles(canvas.width/2, canvas.height/2, 5, 'blue',velocity))
});

animate();
spawnEnemies();