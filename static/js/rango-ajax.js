/**
 * 
 * 
 * Custom AJAX to check if Username already exists in backend
 * 
 * 
 */
$(document).ready(function(){
    $("#registerUsername").on('keyup',function(){
        var query;
        query = $(this).val();
    
        $.get('/rango/check_username/',
        {'username': query},
        function(data){
            if(data == 'True'){
                $('#username-exists-span').text('This username already exists')
            }
            else{
                $('#username-exists-span').text('This username is not taken')
            }
        });
    });
});