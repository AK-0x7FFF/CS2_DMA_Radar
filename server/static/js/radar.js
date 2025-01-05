var radar = new (function() {
    this.element = document.getElementById("radar")

    $(document).ready(() => {
        makeDraggable(this.element);

        this.element.style.left = (window.innerWidth / 2 - (this.element.offsetWidth / 2)) + "px";
        this.element.style.top = (window.innerHeight / 2 - (this.element.offsetHeight / 2)) + "px";
        socket.emit("sync_map_request");

        fetch(location.href + "static/map_data.json").then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            response.json().then(json_data => {
                this.map_data = json_data
            });
        })

        setInterval(() => {
            socket.emit("sync_map_request");
        }, 3000)

//        setInterval(() => {
//            this.state.rotation = Math.sin((new Date().getTime()) / 1000 * 0.6) * 360;
//            this.map.draw();
//        }, 1 / 64)

        console.log("loaded");
    });

    this.state = {
        x: 512,
        y: 512,
        scale: 1,
        rotation: 0
    };
    this.map_data = null;

    this.players = [];
    this.player_binding = null;

    setInterval(() => {
//        this.state.x = 512;
//        this.state.y = 512;
//        this.state.rotation = 0;

        if (this.player_binding != null && this.player_binding != 0) {
            this.players.forEach((player) => {
                if (this.player_binding != player["steam_id"]) {return;};

                targetMapData = this.map_data[this.map.mapName];
                if (targetMapData == null) {return;};

                [x, y] = world2Map(player["pos"])
                this.state.x = x;
                this.state.y = y;
                this.state.rotation = player["direction"]["y"] - 90;
            });
        }

        this.map.draw();
        this.playerDot.draw();
        this.bombDot.draw();
    }, 1 / tick);

    this.map = new (function(parent) {
        this.parent = parent;
        this.mapName = null;

        this.update = function(mapName) {
            this.mapName = mapName;
//            $("#map").attr("src", (mapName == null || mapName == "<empty>") ? "static/img/no_map.png" : "static/img/maps/" + mapName + ".png");
            $("#map").css({
                "background-image": "url(\"/static/img/" + ((this.mapName == null || this.mapName == "<empty>") ? "no_map.png" : "maps/" + this.mapName + ".png") + "\")"
            });
        };

        this.draw = function() {
            x = -(this.parent.state.x - 512) + this.parent.state.x;
            y = -(this.parent.state.y - 512) + this.parent.state.y;
            [x, y] = rotate(x, y)

            $("#map").css({
                "transform": "translate(-50%, -50%) rotate(" + this.parent.state.rotation + "deg)",
                "left": x + "px",
                "top": y + "px",
                "width": this.parent.state.scale * this.parent.element.offsetWidth + "px",
                "height": this.parent.state.scale * this.parent.element.offsetHeight + "px",
            });

        };
    })(this);

    this.playerDot = new (function(parent) {
        this.parent = parent;

        this.dotSize = 40;

        this.draw = function() {
            if ($("#playerDot").children().length != this.parent.players.length) {
                $("#playerDot").empty();

                for (let i = 0; i < this.parent.players.length; i++) {
                    dot = $("<div>", {
                        "class": "playerDot",
                        "style": {
                            "left": (this.parent.element.offsetWidth / 2) + "px",
                            "top": (this.parent.element.offsetHeight / 2) + "px",
                        }
                    });
                    $("#playerDot").append(dot);
                }
            }
            dots = $("#playerDot div")

            this.parent.players.forEach((player, index) => {
                targetMapData = this.parent.map_data[this.parent.map.mapName];
                if (targetMapData == null) {return;};

                [x, y] = world2Map(player["pos"])
                [x, y] = rotate(x, y)

                d = -player["direction"]["y"] + 90 + this.parent.state.rotation;

                dot = dots.eq(index)
//                dot.attr("src",  );
                imageUrl = "/static/img/" + (player["team_num"] == 2 ? "player_dot_t.png" : player["team_num"] == 3 ? "player_dot_ct.png" : "player_dot.png")
                dot.css({
                    "transform": "translate(-50%, -50%) rotate(" + d + "deg)",
//                    "left": x + "px",
//                    "top": y + "px",
                    "background-image": "url(\"" + imageUrl + "\")",
                    "width": this.dotSize * this.parent.state.scale + "px",
                    "height": this.dotSize * this.parent.state.scale + "px",
                });

                lastLeft = parseFloat(dot.css("left"))
                lastTop = parseFloat(dot.css("top"))
                dot.css({
                    "left": (lastLeft + ((x - lastLeft) / 16)) + "px",
                    "top": (lastTop + ((y - lastTop) / 16)) + "px",
                })
            });
        };
    })(this)

    this.bombDot = new (function(parent) {
        this.parent = parent;

        this.planted = false;
        this.bomb = null;

        this.update = function(data) {
            this.planted = data["planted"];
            this.bomb = data["bomb"];
        };

        this.draw = function() {
            bomb = $("#bombDot")

            if (!this.planted) {
                bomb.hide()
            } else {
                [x, y] = world2Map(this.bomb.pos)
                [x, y] = rotate(x, y)

                bomb.css({
                    "left": x,
                    "top": y,
                    "width": 33 * this.parent.state.scale + "px",
                    "height": 24 * this.parent.state.scale + "px"
                })
                bomb.show()
            }
        };
    })(this);

})();