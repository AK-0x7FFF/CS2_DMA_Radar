var socket = io();

socket.on("connect", function() {
    console.log('Connected to server');
});

socket.on("sync_map", function(data) {
    radar.map.update(data["map_name"]);
});

socket.on("player_dot", function(data) {
    radar.players = data["players"];
    if (debug) {
        $("#debugWindow h3").eq(0).text("player_dot: " + Math.round(((new Date().getTime() / 1000) - data["t"]) * 1000) + "ms")
    }

});

socket.on("bomb_dot", function(data) {
    radar.bombDot.update(data);
    if (debug) {
        $("#debugWindow h3").eq(1).text("bomb_dot: " + Math.round(((new Date().getTime() / 1000) - data["t"]) * 1000) + "ms")
    }

});



//socket.on("bomb_status", function(data) {
//    if (debug) {
//        console.log("[bomb_status] bomb_planted: " + data["planted"] + ", time_left: " + data["time_left"] + ", defusing: " + data["defusing"] + ", defuse_time_left: " + data["defuse_time_left"]);
//    };
//});
//
//socket.on("bomb_beep", function(data) {
//    if (debug) {
//        console.log("[bomb_beep] Beep: " + data["beep_span"]);
//    };
//});