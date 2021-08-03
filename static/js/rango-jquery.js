/**
 * 
 * 
 * 
 * Custom jQuery to check if passwords supplied in register page match
 * 
 * 
 * 
 **/
$(document).ready(function () {
    $('#registerConfirmPassword').on('keyup', function(){
        if($(this).val() == $('#registerPassword').val()){
            $('#matching-password-span').removeClass("not-matching-passwords");
            $('#matching-password-span').addClass("matching-passwords");
            $('#matching-password-span').text("Passwords Match");
            $('#register-submit-button').prop('disabled', false);
        }
        else{
            $('#matching-password-span').removeClass("matching-passwords");
            $('#matching-password-span').addClass("not-matching-passwords");
            $('#matching-password-span').text("Passwords Do Not Match");
            $('#register-submit-button').prop('disabled', true);
        }
    });

    $('#registerPassword').on('keyup', function(){
        if($(this).val() == $('#registerConfirmPassword').val()){
            $('#matching-password-span').removeClass("not-matching-passwords");
            $('#matching-password-span').addClass("matching-passwords");
            $('#matching-password-span').text("Passwords Match");
            $('#register-submit-button').prop('disabled', false);
        }
        else{
            $('#matching-password-span').removeClass("matching-passwords");
            $('#matching-password-span').addClass("not-matching-passwords");
            $('#matching-password-span').text("Passwords Do Not Match");
            $('#register-submit-button').prop('disabled', true);
        }
    });
});