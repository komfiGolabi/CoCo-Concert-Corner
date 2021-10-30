$(document).ready(function(){
    $(".dropdown-trigger").dropdown({ hover: false });
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    
});


// Manually make all DOM with .collapsible collapsible 
function initialCollaps (){
  $('.collapsible').collapsible();
}
initialCollaps();
      