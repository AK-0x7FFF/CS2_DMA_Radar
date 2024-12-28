function world2Map(pos) {
    x = (pos["x"] - targetMapData["x"]) / targetMapData["scale"];
    y = (targetMapData["y"] - pos["y"]) / targetMapData["scale"];

    return [x, y]
}

function makeDraggable(element) {
    element.onmousedown = function(mouseEventDown) {
        let elementStartX = mouseEventDown.clientX - element.offsetLeft;
        let elementStartY = mouseEventDown.clientY - element.offsetTop;

        onmousemove = function(mouseEventMove) {
            let targetX = mouseEventMove.clientX - elementStartX;
            let targetY = mouseEventMove.clientY - elementStartY;

            if (targetX < 0) {
                targetX = 0;
            }
            if ((targetX + element.offsetWidth) > window.innerWidth) {
                targetX = window.innerWidth - element.offsetWidth;
            }
            if (targetY < 0) {
                targetY = 0;
            }
            if ((targetY + element.offsetHeight) > window.innerHeight) {
                targetY = window.innerHeight - element.offsetHeight;
            }

            element.style.left = targetX + 'px';
            element.style.top = targetY + 'px';
        };

        element.onmouseup = function(mouseEventUp) {
            onmousemove = null;
            element.ontouchmove = null;
        };
    };
};


function rotate(x, y) {
    radianRotation = (radar.state.rotation + 180) * Math.PI / -180;

    oppoX = (x - radar.state.x) * radar.state.scale;
    oppoY = (y - radar.state.y) * radar.state.scale;

    x = 512 - oppoX * Math.cos(radianRotation) - oppoY * Math.sin(radianRotation);
    y = 512 + oppoX * Math.sin(radianRotation) - oppoY * Math.cos(radianRotation);
    x *= (radar.element.offsetWidth / 1024)
    y *= (radar.element.offsetHeight / 1024)

    return [x, y]
}