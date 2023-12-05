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


// Função para definir um cookie com um determinado nome, valor e tempo de expiração em minutos
function setCookie(name, value, minutes) {
  var d = new Date();
  d.setTime(d.getTime() + (minutes * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Função para obter o valor de um cookie com base no nome
function getCookie(name) {
  var cname = name + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
          c = c.substring(1);
      }
      if (c.indexOf(cname) == 0) {
          return c.substring(cname.length, c.length);
      }
  }
  return "";
}

// Função principal para verificar se o botão deve ser bloqueado
function verificarBotao() {
  var botao = document.getElementById("seuBotao"); // Substitua "seuBotao" pelo ID do seu botão

  // Verificar se o cookie existe e está dentro do prazo de uma hora
  var ultimoClique = getCookie("ultimoClique");
  if (ultimoClique != "" && (new Date().getTime() - ultimoClique) < 60 * 60 * 1000) {
      // Bloquear o botão
      botao.disabled = true;
  } else {
      // Liberar o botão
      botao.disabled = false;

      // Atualizar o cookie com o novo tempo
      setCookie("ultimoClique", new Date().getTime(), 60);
  }
}

// Chamar a função de verificação ao carregar a página
verificarBotao();
