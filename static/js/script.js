function updateUianimated() {
    var uianimateds = document.querySelectorAll('.uianimated');
    var windowheight = window.innerHeight;
    var uianimatedpoint = 40;
  
    uianimateds.forEach(function (element) {
      var uianimatedtop = element.getBoundingClientRect().top;
      if (uianimatedtop < windowheight - uianimatedpoint) {
        element.classList.add('active');
      } else {
        element.classList.remove('active');
      }
    });
  }
  window.addEventListener('load', updateUianimated);
  window.addEventListener('scroll', updateUianimated);
  



  function uianimated() {
    var uianimateds = document.querySelectorAll('.uianimated');
  
    for (var i = 0; i < uianimateds.length; i++) {
      var windowheight = window.innerHeight;
      var uianimatedtop = uianimateds[i].getBoundingClientRect().top;
      var uianimatedpoint = 40;
  
      if (uianimatedtop < windowheight - uianimatedpoint) {
        uianimateds[i].classList.add('active');
      } else {
        uianimateds[i].classList.remove('active');
      }
    }
  }
  
  function onPageload() {
    uianimated();
    window.addEventListener('scroll', uianimated);
  }
