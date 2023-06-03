$(document).ready(main);
 
var contador = 1;
 
function main(){
	$('.menu').click(function(){
		// $('nav').toggle(); 
 
		if(contador == 1){
			$('.ulMovilIndex').animate({
				left: '0'
			});
			contador = 0;
		} else {
			contador = 1;
			$('.ulMovilIndex').animate({
				left: '-100%'
			});
		}
 
	});

}