function alertSuccess(message, duration) {
    $("#alert-success .alert-message").text(message);
    $("#alert-success").css("display", "block").css("opacity", "1");

    setTimeout(function() {
        $("#alert-success").css("opacity", "0");
        setTimeout(function() {
            $("#alert-success").css("display", "none");
        }, 600); // Время должно совпадать с transition из CSS
    }, duration);
}

function alertDanger(message, duration) {
    $("#alert-danger .alert-message").text(message);
    $("#alert-danger").css("display", "block").css("opacity", "1");

    setTimeout(function() {
        $("#alert-danger").css("opacity", "0");
        setTimeout(function() {
            $("#alert-danger").css("display", "none");
        }, 600); // Время должно совпадать с transition из CSS
    }, duration);
}