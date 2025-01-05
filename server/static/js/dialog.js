function setBindPlayer() {
    dialog = $("<div></div>", {
        "class": "dialog",
        "click": () => {
            dialog.remove();
            $("#mainContent").removeClass("blur")
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
            $("#mainContent").removeClass("blur")
        }
    }));
    radar.players.forEach((player) => {
        if (player["steam_id"] == 0) {return;};

        button = $('<button/>', {
            text: player["name"] + " (" + player["steam_id"] + ")",
            click: () => {
                radar.player_binding = player["steam_id"];
                dialog.remove();
                $("#mainContent").removeClass("blur")
            }
        })
        content.append(button);

    });

    $("#mainContent").addClass("blur")
    dialog.append(content)
    $("body").append(dialog)
}


function openSettingDialog() {
    function closeDialog() {
        dialog.remove();
        $("#mainContent").removeClass("blur");
    };

    dialog = $("<div></div>", {
        "class": "dialogBackground",
        "click": closeDialog
    });
    $("#mainContent").addClass("blur")
    $("body").append(dialog)

    settingWindow = $("<div></div>", {
        "class": "dialogContent",
        "click": (event) => {
            event.stopPropagation();
        }
    });
    dialog.append(settingWindow)

    settingWindow.append($("<h4>", {
        "text": "已绑定: null",
        "class" : "settingText",
        "style" : "margin-top: 20px;",
    }));
    settingWindow.append($("<button>", {
        "text": "玩家绑定",
        "style" : "font-size: 24px; font-family: 'HYWenHei-85W'; margin-bottom: 20px;",
        "click": () => {

        }
    }));


//    settingWindow.append($('<h4 style="color: rgb(0, 0, 0); font-family: 'HYWenHei-85W';">玩家点大小</h4>'))
    row1 = $("<div>", {
        "style": "display: flex; flex-direction: row; justify-content: space-between; gap: 20px;"
    });
    row2 = $("<div>", {
        "style": "display: flex; flex-direction: row; justify-content: space-between; gap: 20px;"
    });
    row3 = $("<div>", {
        "style": "display: flex; flex-direction: row; justify-content: space-between; gap: 20px;"
    });


    row1.append($("<h4>", {
        "text": "玩家点大小",
        "class" : "settingText"
    }));
    playerDotInput = $("<input>", {
        "type": "range",
        "min": 24,
        "max": 128,
        "value": radar.playerDot.dotSize,
        "class" : "settingRangeBar"
    });
    playerDotInput.change(() => {
        radar.playerDot.dotSize = parseFloat(playerDotInput.val());
    })
    row1.append(playerDotInput)




    row2.append($("<h4>", {
        "text": "手动地图旋转",
        "class" : "settingText"
    }));
    mapRotationInput = $("<input>", {
        "type": "range",
        "min": 0,
        "max": 270,
        "step": 45,
        "value": radar.state.rotation,
        "class" : "settingRangeBar"
    });
    mapRotationInput.change(() => {
        radar.state.rotation = parseFloat(mapRotationInput.val());
    })
    row2.append(mapRotationInput)



    row3.append($("<h4>", {
        "text": "手动地图缩放",
        "class" : "settingText"
    }));
    mapScaleInput = $("<input>", {
        "type": "range",
        "min": 0.5,
        "max": 3,
        "step": 0.1,
        "value": radar.state.scale,
        "class" : "settingRangeBar"
    });
    mapScaleInput.change(() => {
        radar.state.scale = parseFloat(mapScaleInput.val());
    });
    row3.append(mapScaleInput);

    settingWindow.append(row1);
    settingWindow.append(row2);
    settingWindow.append(row3);






}