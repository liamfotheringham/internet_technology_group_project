/**
 * 
 * 
 * Custom AJAX to check if Username already exists in backend
 * 
 * 
 */
$(document).ready(function(){
    //Whenever user types in Username input
    $("#registerUsername").on('keyup',function(){
        var query;
        query = $(this).val(); //Attach input value to query variable
    
        //Send get request to /rango/check_username
        $.get('/rango/check_username/',
        {'username': query},
        function(data){
            //If the username already exists - inform user
            if(data == 'True'){
                $('#username-exists-span').text('This username already exists')
            }
            //Otheriwse, tell user it is available
            else{
                $('#username-exists-span').text('This username is not taken')
            }
        });
    });
});