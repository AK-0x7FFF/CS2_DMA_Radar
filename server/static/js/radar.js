


var radarWindow = new Radar();
radarWindow.mapCanvas.update(null);
fetch(location.href + "static/map_data.json")
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    response.json().then(json_data => {
        radarWindow.map_data = json_data
    });

  })

$(document).ready(() => {
    let radarElement = document.querySelector("#radar");
    makeDraggable(radarElement);

    radarElement.style.left = (window.innerWidth / 2 - (radarElement.offsetWidth / 2)) + "px";
    radarElement.style.top = (window.innerHeight / 2 - (radarElement.offsetHeight / 2)) + "px";
    radarElement.classList.add("fade-in");

//    setInterval(() => {
//        radarWindow.rotation = Math.sin((new Date().getTime()) / 1000 * 0.6) * 360;
//        radarWindow.mapCanvas.draw();
//    }, 1 / 64)

    console.log("loaded");
});


function Radar() {
    this.config = {
        x: 512,
        y: 512,
        scale: 1,
        rotation: 0
    };
    this.getRotatePos = function(x, y) {
        radianRotation = (this.config.rotation + 180) * Math.PI / -180;

        oppoX = (x - this.config.x) * this.config.scale;
        oppoY = (y - this.config.y) * this.config.scale;

        x = 512 - oppoX * Math.cos(radianRotation) - oppoY * Math.sin(radianRotation);
        y = 512 + oppoX * Math.sin(radianRotation) - oppoY * Math.cos(radianRotation);

        return [x, y];
    }

    this.players = {};

    this.boundPlayerId = 0;
    this.bindPlayer = function(steamId) {
//        this.players["t"].concat(this.players["ct"]).forEach((playerEntity) => {
//        });
        this.boundPlayerId = steamId;
    };

    this.map_data = {};

    this.updateConfig = function() {
        if (this.boundPlayerId == 0) {
            this.config.x = 512;
            this.config.y = 512;
            this.config.rotation = 0;

            this.playersDot.tColor = this.playersDot.T_COLOR;
            this.playersDot.ctColor = this.playersDot.CT_COLOR;
        } else {
            this.players.forEach((playerEntity) => {
                if (playerEntity["id"] == this.boundPlayerId) {
                    this.config.x = playerEntity["x"];
                    this.config.y = playerEntity["y"];
                    this.config.rotation = playerEntity["d"] - 90;

                    this.playersDot.tColor = playerEntity["team"] == "t" ? this.playersDot.TEAMMATE_COLOR : this.playersDot.ENEMY_COLOR;
                    this.playersDot.ctColor = playerEntity["team"] == "ct" ? this.playersDot.TEAMMATE_COLOR : this.playersDot.ENEMY_COLOR;
                };
            });
        };
    };
//    setInterval(this.aaa, 1);

    this.mapCanvas = new (function(parent) {
        this.radar = parent
        this.canvas = document.querySelector("#mapCanvas");
        this.ctx = this.canvas.getContext('2d');

        this.mapName = "";
        this.mapImage = new Image();
        this.loadedImage = false;

        this.update = function(mapName) {
            this.loadedImage = false;
//            this.mapImage.src = (mapLocation == null) ? "static/img/no_map.png" : (location.href + mapLocation);
            this.mapName = mapName;
            this.mapData = this.radar.map_data[mapName]
            this.mapImage.src = (mapName == null) ? "static/img/no_map.png" : "static/img/maps/" + mapName + ".png";
            this.mapImage.onload = () => {
                this.loadedImage = true;
                this.draw();
            };
        };

        this.draw = function() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            if (this.loadedImage == false) {return;}

            this.ctx.save();
            this.ctx.translate(this.canvas.width /2, this.canvas.height / 2);
            this.ctx.rotate(this.radar.config.rotation * Math.PI / 180);

            this.ctx.drawImage(
                this.mapImage,
                -this.radar.config.x * this.radar.config.scale,
                -this.radar.config.y * this.radar.config.scale,
                this.canvas.width * this.radar.config.scale,
                this.canvas.height * this.radar.config.scale
            );

            this.ctx.restore();
        }
    })(this);

    this.playersDot = new (function(parent) {
        this.T_COLOR = "#EAD28B";
        this.CT_COLOR = "#B6D4EE";
        this.TEAMMATE_COLOR = "#FFFFFF";
        this.ENEMY_COLOR = "#FF0000";

        this.radar = parent;
        this.canvas = document.querySelector("#playersDot");
        this.ctx = this.canvas.getContext('2d');

        this.tColor = this.T_COLOR;
        this.ctColor = this.CT_COLOR;

        this.drawPlayersDot = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            this.radar.players.forEach((playerEntity) => {
                this.drawDot(
                    playerEntity["x"], playerEntity["y"], playerEntity["d"],
                    (playerEntity["team"] == "t") ? this.tColor : (playerEntity["team"] == "ct" ? this.ctColor : "#808080")
                );
            });
        };

        this.drawDot = (x, y, direction, color) => {
            [x, y] = this.radar.getRotatePos(x, y);

            this.ctx.beginPath();
            this.ctx.arc(x, y, 8, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        };
    })(this);
};


function showInfoPop() {
    infoPop = document.getElementById("info_pop");

    infoPop.classList.remove("fade-out");
    infoPop.classList.add("fade-in");
};

function hideInfoPop() {
    infoPop = document.getElementById("info_pop");

    infoPop.classList.remove("fade-in");
    infoPop.classList.add("fade-out");

    document.querySelector("#radar").classList.add("fade-in");
//    document.querySelector("#player_status").classList.add("fade-in");
//    document.querySelector("#bomb_status").classList.add("fade-in");
};
setTimeout(function() {showInfoPop()}, 0);








//    (() => {
//        let playerStatusElement = document.querySelector("#player_status");
//        makeDraggable(playerStatusElement);
//
//        playerStatusElement.style.left = (window.innerWidth / 1.3 - (playerStatusElement.offsetWidth / 2)) + "px";
//        playerStatusElement.style.top = (window.innerHeight / 2 - (playerStatusElement.offsetHeight / 2)) + "px";
//    })();
//
//    (() => {
//        let bombStatusElement = document.querySelector("#bomb_status");
//        makeDraggable(bombStatusElement);
//
//        bombStatusElement.style.left = (window.innerWidth / 2 - (bombStatusElement.offsetWidth / 2)) + "px";
//    })();


//window.ontouchstart = function(event){
//        alert("This is from the touch event");
//    }


