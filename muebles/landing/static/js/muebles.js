
const images = document.querySelectorAll('.foto');
let span = "";

let currentIndex = 0;

$('.zoom').each(function() {
	$(this).wrap('<span style="display:inline-block;justify-self:center" class="span-wrapper"></span>')
		.css('display', 'block')
		.parent()
		.zoom({url: $(this).attr('src')
		});
	if($(this).width() < 500){
		$(this).parent().css({
			'width': $(this).width() * 2,
			'padding-left': $(this).width(),
		}); 
	}
	setTimeout(setup(), 100);
});

function setup() {
	span = document.querySelectorAll('.span-wrapper');

	span[currentIndex].style.opacity = '1'; // show the first image initially
	span[currentIndex].style.zIndex = '1';
}

function changeImage(value) {
	span[currentIndex].style.opacity = '0';
	span[currentIndex].style.zIndex = '-1';
	currentIndex = (currentIndex + value) 
	if(currentIndex < 0){
		currentIndex = images.length - 1;
	}
	currentIndex %= images.length;

	span[currentIndex].style.opacity = '1';
	span[currentIndex].style.zIndex = '1';
}

const leftArrow = document.querySelector('.left');
const rightArrow = document.querySelector('.right');

leftArrow.addEventListener('click', () => {
	changeImage(-1);
});
rightArrow.addEventListener('click', () => {
	changeImage(1);
});

