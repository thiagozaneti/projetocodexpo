// JQUERY
$('#card-number').mask("9999");
$('#card-number').mouseover(function(){$(this).attr('placeholder','9999')});
$('#card-number').mouseout(function(){$(this).attr('placeholder','Ultimos 4 numeros')});


$('#expiration-date').mask("9999")
$('#expiration-date').mouseover(function(){$(this).attr('placeholder','0000')});
$('#expiration-date').mouseout(function(){$(this).attr('placeholder','Cartão expira em')});


$('#cvv').mask("999")
$('#cvv').mouseover(function(){$(this).attr('placeholder','999')});
$('#cvv').mouseout(function(){$(this).attr('placeholder','Cvv')});