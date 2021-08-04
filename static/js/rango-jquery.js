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

    //When user types in confirm password box
    $('#registerConfirmPassword').on('keyup', function(){
        //If the confirmation password matches the intitial password - inform user
        if($(this).val() == $('#registerPassword').val()){
            PasswordsMatch();
        }

        //Otherwise - inform user they do not match
        else{
            PasswordsDoNotMatch();
        }
    });

    //When user types in password box
    $('#registerPassword').on('keyup', function(){
        //If the initial password matches the confirmation password - inform user
        if($(this).val() == $('#registerConfirmPassword').val()){
            PasswordsMatch();
        }

        //Otherwise - inform user they do not match
        else{
            PasswordsDoNotMatch();
        }
    });

    //When user switches from an input
    $('input').blur(function(){
    
        //if passwords match and username does not exist - enable Register button
        if($('#matching-password-span').text()=='Passwords Match' && $('#username-exists-span').text() == 'This username is not taken'){
            $('#register-submit-button').prop('disabled', false);
        }

        //Otherwise - disable Register button
        else{
            $('#register-submit-button').prop('disabled', true);
        }
    });
});

//Update values if passwords match
function PasswordsMatch(){
    $('#matching-password-span').removeClass("not-matching-passwords");
    $('#matching-password-span').addClass("matching-passwords");
    $('#matching-password-span').text("Passwords Match");
}

//Update values if passwords do not match
function PasswordsDoNotMatch(){
    $('#matching-password-span').removeClass("matching-passwords");
    $('#matching-password-span').addClass("not-matching-passwords");
    $('#matching-password-span').text("Passwords Do Not Match");
}