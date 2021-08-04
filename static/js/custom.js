/**
 * 
 * 
 * 
 * Custom JavaScript script to check if the back to top button is within the viewport on load
 * 
 * If True - then make sure it can't be seen
 * 
 * Else - Make it visible
 * 
 */

window.onload = hideBackToTopButton; //Call Function when window loads on browser

function hideBackToTopButton(){
    var bttb = document.getElementById('back-to-top-button') //Get back to top button by its Id
    var bounding = bttb.getBoundingClientRect(); //Find where it is in the ViewPort

    //Check if it is within the visible window on browser
    if(bounding.top >= 0 &&
        bounding.left >= 0 &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth) &&
        bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)){
        bttb.style.visibility='hidden'; //Hide
    }
    else{
        bttb.style.visibility='visible'; //Show
    }
}