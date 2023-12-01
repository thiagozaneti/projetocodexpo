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
  
//js para parallax

//js de driver 
const driver = window.driver.js.driver;

const driverObj = driver();

driverObj.highlight({
  element: "#homeadm",
  popover: {
    title: "Seja bem vindo",
    description: "Description"
  }
});