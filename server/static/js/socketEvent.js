var socket = io();

socket.on("connect", function() {
    console.log('Connected to server');
//    socket.send('Hello, server!');
});

socket.on("sync_map", function(data) {
//    if (debug || true) {
//        console.log("map_sync: " + data);
//    }
    radar.map.update(data["map_name"]);
});

socket.on("player_dot", function(data) {
//    radarWindow.config.rotation = Math.cos((new Date().getTime()) / 1000 * .4) * 360;
//    radarWindow.config.scale = 0.5 + Math.sin((new Date().getTime()) / 1000 * 1.2) * 0.5;
    radar.players = data["players"];


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