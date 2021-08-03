/**
 * 
 * 
 * 
 * Custom jQuery to check if passwords supplied in register page match
 * Enable "Register" button is username isnt taken and passwords match
 * 
 * 
 **/
$(document).ready(function () {
    $('#registerConfirmPassword').on('keyup', function(){
        if($(this).val() == $('#registerPassword').val()){
            $('#matching-password-span').removeClass("not-matching-passwords");
            $('#matching-password-span').addClass("matching-passwords");
            $('#matching-password-span').text("Passwords Match");
        }
        else{
            $('#matching-password-span').removeClass("matching-passwords");
            $('#matching-password-span').addClass("not-matching-passwords");
            $('#matching-password-span').text("Passwords Do Not Match");
        }
    });

    $('#registerPassword').on('keyup', function(){
        if($(this).val() == $('#registerConfirmPassword').val()){
            $('#matching-password-span').removeClass("not-matching-passwords");
            $('#matching-password-span').addClass("matching-passwords");
            $('#matching-password-span').text("Passwords Match");
        }
        else{
            $('#matching-password-span').removeClass("matching-passwords");
            $('#matching-password-span').addClass("not-matching-passwords");
            $('#matching-password-span').text("Passwords Do Not Match");
        }
    });

    $('input').blur(function(){
    
        if($('#matching-password-span').text()=='Passwords Match' && $('#username-exists-span').text() == 'This username is not taken'){
            $('#register-submit-button').prop('disabled', false);
        }
        else{
            $('#register-submit-button').prop('disabled', true);
        }
    });
});