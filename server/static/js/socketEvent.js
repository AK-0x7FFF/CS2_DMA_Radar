var socket = io();

socket.on("connect", function() {
    console.log('Connected to server');
});

socket.on("sync_map", function(data) {
    radar.map.update(data["map_name"]);
});

socket.on("player_dot", function(data) {
    radar.players = data["players"];
});

socket.on("bomb_dot", function(data) {
    radar.bombDot.update(data);
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