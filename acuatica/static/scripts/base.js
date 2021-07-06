// Toggle Animation by Class
$(window).scroll(function(){
    if($(document).scrollTop() > 100){
      $('nav').addClass('animate');
    }else{
      $('nav').removeClass('animate');
    }
  })

  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  })

