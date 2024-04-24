
const images = document.querySelectorAll('.foto');
let span = "";

let currentIndex = 0;

function createSpan(){
	$('.zoom').each(function() {
		var $zoomedImg = $(this);
		$zoomedImg.wrap('<span style="display:inline-block;justify-self:center" class="span-wrapper"></span>')
			.css('display', 'block')
			.parent()
			.zoom({url: $zoomedImg.attr('src'),
				callback: function() {
					setupSpan($zoomedImg);
				}
			});
	});
	setup();
}
function setupSpan($image){
	if($image.width() < 500){
		$image.parent().css({
			'width': $image.width() * 2,
			'padding-left': $image.width(),
		}); 
	}
}

function setup() {
	span = document.querySelectorAll('.span-wrapper');

	span[currentIndex].style.opacity = '1'; // show the first image initially
	span[currentIndex].style.zIndex = '1';
}

createSpan();

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

