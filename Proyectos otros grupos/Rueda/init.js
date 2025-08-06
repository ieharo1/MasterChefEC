// the game itself
let game;

// global object with configuration options
let gameOptions = {

    // radius of the big circle, in pixels
    bigCircleRadius: 300,

    // thickness of the big circle, in pixels
    bigCircleThickness: 20,

    // radius of the player, in pixels
    playerRadius: 25,

    // player speed, in degrees per frame
    playerSpeed: 0.6,

    // world gravity
    worldGravity: 0.5,

    // jump force of the single and double jump
    jumpForce: [10, 8]
}

window.onload = function () {
    let gameConfig = {
        type: Phaser.CANVAS,
        backgroundColor: 0x444444,
        scale: {
            mode: Phaser.Scale.FIT,
            autoCenter: Phaser.Scale.CENTER_BOTH,
            parent: "contenedor",
            width: 800,
            height: 800
        },
        scene: {
            preload: preload,
            create: create,
            update: update
        },
        physics: {
            default: "arcade",
            arcade: {
                gravity: {
                    //y: 400
                }
            }
        }
    }
    var text;
    var textoPuntos;
    var timedEvent;


    game = new Phaser.Game(gameConfig);
    window.focus();
}
var gameOver = false;
var puntos = 0;

function preload() {
    //this.load.image("player", "player.png");

}
function create() {

    text = this.add.text(32, 32);
    textoPuntos = this.add.text(340, 300, puntos, { fontSize: "100px", fill: "#000" });
    this.add.text(230, 390, "puntos", { fontSize: "100px", fill: "#000" });

    // calculate the distance from the center of the canvas and the big circle
    this.distanceFromCenter = gameOptions.bigCircleRadius - gameOptions.playerRadius - gameOptions.bigCircleThickness / 2;

    // draw the big circle
    this.bigCircle = this.add.graphics();
    this.bigCircle.lineStyle(gameOptions.bigCircleThickness, 0xffffff);
    this.bigCircle.strokeCircle(game.config.width / 2, game.config.height / 2, gameOptions.bigCircleRadius);

    // add player sprite
    this.player = this.physics.add.sprite(game.config.width / 2, game.config.height / 2 - this.distanceFromCenter, "player");
    this.player.setScale(1.2);


    // player current angle, on top of the big circle
    this.player.currentAngle = -90;

    // player previous angle, at the moment same value of current angle
    this.player.previousAngle = this.player.currentAngle;

    // jump offset, the distance from the ground and player position during jumps
    this.player.jumpOffset = 0;

    // counter to keep track of player jumps
    this.player.jumps = 0;

    // current jump force
    this.player.jumpForce = 0;

    // input listener
    this.input.on("pointerdown", function () {

        // if the player jumped less than 2 times...
        if (this.player.jumps < 2) {

            // one more jump
            this.player.jumps++;

            // add to player jump force the proper force according to the number of jumps performed
            this.player.jumpForce = gameOptions.jumpForce[this.player.jumps - 1];
        }
        if (gameOver) {
            this.scene.restart();
            puntos = 0;
            gameOver = false;
            gameOptions.playerSpeed = 0.6;
        }
    }, this);

    timedEvent = this.time.delayedCall(9000, onEvent, [], this);

    this.obstaculo = this.physics.add.sprite(game.config.width / 2, game.config.height / 2 + this.distanceFromCenter, "obstaculo");
    this.obstaculo.setScale(1);

    this.physics.add.overlap(this.player, this.obstaculo, function () {
        gameOver = true;
    });
}

// method to be executed at each frame
function update(time, delta) {

    if (!gameOver) {
        texto = text.setText('Siguiente movimiento: ' + (10 - (timedEvent.getProgress().toString().substr(0, 4) * 10)).toPrecision(2));
        textoPuntos = textoPuntos.setText(puntos);

        // if the player is jumping...
        if (this.player.jumps > 0) {

            // increase player jump offset according to jump force
            this.player.jumpOffset += this.player.jumpForce;

            // decrease jump force ti simulate gravity
            this.player.jumpForce -= gameOptions.worldGravity;

            // if jump offset is zero or less than zero, that is the player is on the ground...
            if (this.player.jumpOffset < 0) {

                // set jump offset to zero
                this.player.jumpOffset = 0;

                // player is not jumping
                this.player.jumps = 0;

                // player has no jump force
                this.player.jumpForce = 0;
            }
        }

        // update current angle adding player speed
        this.player.currentAngle = Phaser.Math.Angle.WrapDegrees(this.player.currentAngle + gameOptions.playerSpeed);

        // transform degrees to radians
        let radians = Phaser.Math.DegToRad(this.player.currentAngle);

        // determine distance from center according to jump offset
        let distanceFromCenter = this.distanceFromCenter - this.player.jumpOffset;

        // position player using trigonometry
        this.player.x = game.config.width / 2 + distanceFromCenter * Math.cos(radians);
        this.player.y = game.config.height / 2 + distanceFromCenter * Math.sin(radians);

        // rotate player using trigonometry
        this.player.angle = -this.player.currentAngle * 10;
    }

    if (gameOver) {
        this.gameOverText = this.add.text(240, 200, "Game Over", { fontSize: "60px", fill: "#000" });
        this.gameOverText = this.add.text(168, 490, "Click para volver a jugar", { fontSize: "32px", fill: "#000" });
    }
}


function onEvent() {

    if (!gameOver) {
        this.positionX = Phaser.Math.FloatBetween(-3.14, 3.14);
        this.obstaculo.setPosition(game.config.height / 2 + (gameOptions.bigCircleRadius - gameOptions.playerRadius - gameOptions.bigCircleThickness / 2) * Math.cos(this.positionX), game.config.height / 2 + (gameOptions.bigCircleRadius - gameOptions.playerRadius - gameOptions.bigCircleThickness / 2) * Math.sin(this.positionX));

        console.log(this.obstaculo);
        if (this.obstaculo.scale < 1.8) {
            this.obstaculo.setScale(this.obstaculo.scale + 0.1);
        }

        if(gameOptions.playerSpeed < 1.7)
        {
            gameOptions.playerSpeed += 0.1
        }

        puntos += 10;
        timedEvent = this.time.delayedCall(6000, onEvent, [], this);
    }
}

function rotation() {
    return this.realInRange(-3.1415926, 3.1415926);
}
