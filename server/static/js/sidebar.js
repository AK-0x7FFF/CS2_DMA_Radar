function sidebarToggle() {
    if ($("#sidebar").css("left") == "0px") {
        $("#sidebar").css("left", "-50vmin");
        $("#mainContent").off("click");

    } else {
        $("#sidebar").css("left", "0px");
        $("#mainContent").click(() => {
            sidebarToggle()
        })
    }

}