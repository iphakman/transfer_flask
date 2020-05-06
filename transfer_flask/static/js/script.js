$(document).ready(function(){

    $('#btnSend').click(function(){
        var errores = '';

        // Validando Correo ==============================
        if($('#email').val() == ''){
            errores += '<p>Necesita un email valido</p>'
            $('#email').css('border-bottom-color', '#F14B4B')
        } else {
            $('#email').css('border-bottom-color', '#d1d1d1')
        }

        // Validando Password ==============================
        if($('#password').val() == ''){
            errores += '<p>Password vacio!</p>'
            $('#password').css('border-bottom-color', '#F14B4B')
        } else {
            $('#password').css('border-bottom-color', '#d1d1d1')
        }

        // ENVIANDO MENSAJE ==============================
        if(errores == '' == false){
            var mensajeModal = '<div class="modal_wrap">' +
                                    '<div class="mensaje_modal">'+
                                        '<h3>Errores encontrados</h3>'+
                                        errores+
                                        '<span id="btnClose">Close</span>'
                                    '</div>'+
                                '</div>'

            $('body').append(mensajeModal);
        }

        // CERRANDO MODAL ==============================
        $('#btnClose').click(function(){
            $('.modal_wrap').remove();
        });
    });

});

$(document).ready(function(){

    $('#btnAddUser').click(function(){

        var errores = '';

        // Validando Campos de formulario ==============================
        if($('#name').val() == ''){
            errores += '<p>Nombre esta vacio.</p>'
            $('#name').css('border-bottom-color', '#F14B4B')
        } else {
            $('#name').css('border-bottom-color', '#d1d1d1')
        }

        if($('#last_name').val() == ''){
            errores += '<p>Necesita un last name.</p>'
            $('#last_name').css('border-bottom-color', '#F14B4B')
        } else {
            $('#last_name').css('border-bottom-color', '#d1d1d1')
        }

        if($('#email').val() == ''){
            errores += '<p>Necesita un email valido</p>'
            $('#email').css('border-bottom-color', '#F14B4B')
        } else {
            $('#email').css('border-bottom-color', '#d1d1d1')
        }

        if($('#phone_number').val() == ''){
            errores += '<p>Necesita un telefono valido</p>'
            $('#phone_number').css('border-bottom-color', '#F14B4B')
        } else {
            $('#phone_number').css('border-bottom-color', '#d1d1d1')
        }

        if($('#msdi').val() == ''){
            errores += '<p>Necesita ingresar el MSDI</p>'
            $('#msdi').css('border-bottom-color', '#F14B4B')
        } else {
            $('#msdi').css('border-bottom-color', '#d1d1d1')
        }

        if($('#password').val() == ''){
            errores += '<p>Password vacio!</p>'
            $('#password').css('border-bottom-color', '#F14B4B')
        } else {
            $('#password').css('border-bottom-color', '#d1d1d1')
        }

        // ENVIANDO MENSAJE ==============================
        if(errores !== ''){
            var mensajeModal = '<div class="modal_wrap">' +
                                    '<div class="mensaje_modal">'+
                                        '<h3>Errores encontrados</h3>'+
                                        errores+
                                        '<span id="btnClose">Close</span>'
                                    '</div>'+
                                '</div>'

            $('body').append(mensajeModal);
        }

        // CERRANDO MODAL ==============================
        $('#btnClose').click(function(){
            $('.modal_wrap').remove();
        });
    });

});

$(document).ready(function(){
    $('#btnRenew').click(function(){
        var errores = '';

        if($('#filename').val() == ''){
            errores += '<p>Nombre de archivo requerido</p>'
            $('#filename').css('border-bottom-color', '#F14B4B')
        } else {
            $('#filename').css('border-bottom-color', '#D1D1D1')
        }

        if(errores !== ''){
            var mensajeModal = '<div class="modal_wrap">' +
                                    '<div class="mensaje_modal">'+
                                        '<h3>Errores encontrados</h3>'+
                                        errores+
                                        '<span id="btnClose">Close</span>'
                                    '</div>'+
                                '</div>'

            $('body').append(mensajeModal);
        }

        $('#btnClose').click(function(){
            $('.modal_wrap').remove()
        });
    });
});

$(document).ready(function(){

    $('#btnTran').click(function(){
        var errores = '';

        // Validando Formulario ==============================
        if($('#origin').val() == ''){
            errores += '<p>Necesita un origin id valido</p>'
            $('#origin').css('border-bottom-color', '#F14B4B')
        } else {
            $('#origin').css('border-bottom-color', '#d1d1d1')
        }

        if($('#destination').val() == ''){
            errores += '<p>Necesita un destination email.</p>'
            $('#destination').css('border-bottom-color', '#F14B4B')
        } else {
            $('#destination').css('border-bottom-color', '#d1d1d1')
        }

        if($('#amount').val() == ''){
            errores += '<p>Necesita un destination email.</p>'
            $('#amount').css('border-bottom-color', '#F14B4B')
        } else {
            $('#amount').css('border-bottom-color', '#d1d1d1')
        }

        // ENVIANDO MENSAJE ==============================
        if(errores == '' == false){
            var mensajeModal = '<div class="modal_wrap">' +
                                    '<div class="mensaje_modal">'+
                                        '<h3>Errores encontrados</h3>'+
                                        errores+
                                        '<span id="btnClose">Close</span>'
                                    '</div>'+
                                '</div>'

            $('body').append(mensajeModal);
        }

        // CERRANDO MODAL ==============================
        $('#btnClose').click(function(){
            $('.modal_wrap').remove();
        });
    });

});
