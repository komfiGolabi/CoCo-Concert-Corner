$(document).ready(function(){
    $(".dropdown-trigger").dropdown({ hover: false });
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker({
      format: "dd mmmm, yyyy",
      yearRange: 5,
      showClearBtn: true,
      i18n: {
          done: "Select"
      }
    });
    
});


// Manually make all DOM with .collapsible collapsible 
function initialCollaps (){
  $('.collapsible').collapsible();
}
initialCollaps();

function eventDate(){
  $('.datepicker').datepicker();
}

eventDate();
      