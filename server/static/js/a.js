function setBindPlayer() {
    dialog = $("<div></div>", {
        "class": "dialog",
        "click": () => {
            dialog.remove();
        }
    })
    content = $("<div></div>", {
        "class": "dialogContent",
    })

    content.append($('<button>', {
        text: "关闭",
        click: () => {
            radar.player_binding = null;
            dialog.remove();
        }
    }));
    radar.players.forEach((player) => {
        if (player["steam_id"] == 0) {return;};

        button = $('<button/>', {
            text: player["name"] + " (" + player["steam_id"] + ")",
            click: () => {
                radar.player_binding = player["steam_id"];
                dialog.remove();
            }
        })
        content.append(button);

    });


    dialog.append(content)
    $("body").append(dialog)
}