$(document).ready(function(){
//    alert('funciono')

    $('#btnSend').click(function(){

        var errores = '';

        // Validando Correo ==============================
        if($('#email').val() == ''){
            errores += '<p>Necesita un email valido</p>'
            $('#email').css("border-bottom-color", "#F14B4B")
        } else {
            $('#email').css("border-bottom-color", "#d1d1d1")
        }

        // Validando Password ==============================
        if($('#password').val() == ''){
            errores += '<p>Password vacio!</p>'
            $('#password').css("border-bottom-color", "#F14B4B")
        } else {
            $('#password').css("border-bottom-color", "#d1d1d1")
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

})