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


$(document).ready(function() {

    function openModal(modalId) {
        $('body').addClass('no-scroll');
        $(modalId).addClass('show');
    }

    function closeModal(modalId) {
        $('body').removeClass('no-scroll');
        $(modalId).removeClass('show');
    }


    $( "#burger-toggler" ).on( "click", function() {
        $('#body-overlay').show();
        $('#navbar-right').show();
    });

    $( "#close-right" ).on( "click", function() {
        $('#body-overlay').hide()
        $('#navbar-right').hide()
    });

    $( "#navbar-right .menu-item" ).on( "click", function() {
        setTimeout(function() {
            $('#body-overlay').hide()
            $('#navbar-right').hide()
        }, 50);
        
    });


    $( "#body-overlay" ).on( "click", function() {
        $('#body-overlay').hide()
        $('#navbar-right').hide()
    });




    $('.education-element').on('click', function() {
        const diplomaSrc = $(this).data('diploma');
        $('#diplomaImage').attr('src', diplomaSrc);
        openModal('#diplomaModal');
    });

    $('.service-main-button').on('click', function(e) {
        e.preventDefault();
        openModal('#formModal');
    });

    $('#get-help-button').on('click', function(e) {
        e.preventDefault();
        openModal('#formModal');
    });

    $('.modal-close').on('click', function() {
        const modal = $(this).closest('.modal');
        closeModal(modal);
    });

    $('.modal').on('click', function(e) {
        if ($(e.target).hasClass('modal')) {
            closeModal($(this));
        }
    });

    $(document).on('keydown', function(e) {
        if (e.key === 'Escape') {
            $('.modal.show').each(function() {
                closeModal($(this));
            });
        }
    });
});