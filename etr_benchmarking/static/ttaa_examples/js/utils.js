// Put your custom javascript functions here

// Function that returns an array of EY colors
function getEyColors() {
    var c = {
        yellow:'#ffe600',
        yellow50: '#fff27f',  
        greyDark: '#333333',
        grey: '#646464',
        greyAlt: '#808080',
        grey1: '#999999',
        grey2: '#c0c0c0',
        grey3: '#f0f0f0',
        blue: '#336699',
        red: '#f04c3e',
        blueSpecial: '#00a3ae',
        purpleSpecial: '#91278f',
        greenSpecial: '#2c973e',
        lilacSpecial: '#ac98db',
        blueSpecial50: '#7fd1d6',
        purpleSpecial50: '#c893c7',
        greenSpecial50: '#95cb89',
        lilacSpecial50: '#d8d2e0'
    };
    return c;
}





$(document).ready(function() {
    $('.gotoA').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#A').offset().top - 60
		}, 'slow');
	});
	$('.gotoB').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#B').offset().top - 60
		}, 'slow');
	});
	$('.gotoC').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#C').offset().top - 60
		}, 'slow');
	});
	$('.gotoD').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#D').offset().top - 60
		}, 'slow');
	});
	$('.gotoE').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#E').offset().top - 60
		}, 'slow');
	});
	$('.gotoF').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#F').offset().top - 60
		}, 'slow');
	});
		$('.gotoG').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#G').offset().top - 60
		}, 'slow');
	});
		$('.gotoH').on("click", function(){
		$('html, body').animate({
			scrollTop: $('#H').offset().top - 60
		}, 'slow');
	});
(function () {

   //////////////////////
	// Utils
  //////////////////////
    function throttle(fn, delay, scope) {
        // Default delay
        delay = delay || 250;
        var last, defer;
        return function () {
            var context = scope || this,
                now = +new Date(),
                args = arguments;
            if (last && now < last + delay) {
                clearTimeout(defer);
                defer = setTimeout(function () {
                    last = now;
                    fn.apply(context, args);
                }, delay);
            } else {
                last = now;
                fn.apply(context, args);
            }
        }
    }

    function extend(destination, source) {
        for (var k in source) {
            if (source.hasOwnProperty(k)) {
                destination[k] = source[k];
            }
        }
        return destination;
    }

   //////////////////////
	// END Utils
  //////////////////////

   //////////////////////
   // Scroll Module
   //////////////////////

    var ScrollManager = (function () {

        var defaults = {

                steps: null,
                navigationContainer: null,
                links: null,
                scrollToTopBtn: null,

                navigationElementClass: '.Quick-navigation',
                currentStepClass: 'current',
                smoothScrollEnabled: true,
                stepsCheckEnabled: true,

                // Callbacks
                onScroll: null,

                onStepChange: function (step) {
                    var self = this;
                    var relativeLink = [].filter.call(options.links, function (link) {
                        link.classList.remove(self.currentStepClass);
                        return link.hash === '#' + step.id;
                    });
                    relativeLink[0].classList.add(self.currentStepClass);
                    // alert(typeof relativeLink);
                    
                    
                    var test= String(relativeLink).slice(-2);
                    console.log(test);
                    $("a.Quick-navigation-item").each(function() {
                        if ($(this).attr("href") == test) {
                            $(this).css('background-color', '#646464').css('opacity', '1');
                        } else {
                            $(this).css('background-color', '#c0c0c0').css('opacity', '1');
                        }
                    })
                },

                // Provide a default scroll animation
                smoothScrollAnimation: function (target) {
                    $('html, body').animate({
                        scrollTop: target
                    }, 'slow');
                }
            },

            options = {};

        // Privates
        var _animation = null,
            currentStep = null,
            throttledGetScrollPosition = null;

        return {

            scrollPosition: 0,

            init: function (opts) {

                options = extend(defaults, opts);

                if (options.steps === null) {
                    console.warn('Smooth scrolling require some sections or steps to scroll to :)');
                    return false;
                }

                // Allow to customize the animation engine ( jQuery / GSAP / velocity / ... )
                _animation = function (target) {
                    target = typeof target === 'number' ? target : $(target).offset().top -60;
                    return options.smoothScrollAnimation(target);
                };

                // Activate smooth scrolling
                if (options.smoothScrollEnabled)  this.smoothScroll();

                // Scroll to top handling
                if (options.scrollToTopBtn) {
                    options.scrollToTopBtn.addEventListener('click', function () {
                        options.smoothScrollAnimation(0);
                    });
                }

                // Throttle for performances gain
                throttledGetScrollPosition = throttle(this.getScrollPosition).bind(this);
                window.addEventListener('scroll', throttledGetScrollPosition);
                window.addEventListener('resize', throttledGetScrollPosition);

                this.getScrollPosition();
            },

            getScrollPosition: function () {
                this.scrollPosition = window.pageYOffset || window.scrollY;
                if (options.stepsCheckEnabled) this.checkActiveStep();
                if (typeof  options.onScroll === 'function') options.onScroll(this.scrollPosition);
            },

            scrollPercentage: function () {
                var body = document.body,
                    html = document.documentElement,
                    documentHeight = Math.max(body.scrollHeight, body.offsetHeight,
                        html.clientHeight, html.scrollHeight, html.offsetHeight);

                var percentage = Math.round(this.scrollPosition / (documentHeight - window.innerHeight) * 100);
                if (percentage < 0)  percentage = 0;
                if (percentage > 100)  percentage = 100;
                return percentage;
            },

            doSmoothScroll: function (e) {
                if (e.target.nodeName === 'A') {
                    e.preventDefault();
                    if (location.pathname.replace(/^\//, '') === e.target.pathname.replace(/^\//, '') && location.hostname === e.target.hostname) {
                        var targetStep = document.querySelector(e.target.hash);
                        targetStep ? _animation(targetStep) : console.warn('Hi! You should give an animation callback function to the Scroller module! :)');
                    }
                }
            },

            smoothScroll: function () {
                if (options.navigationContainer !== null) options.navigationContainer.addEventListener('click', this.doSmoothScroll);
            },

            checkActiveStep: function () {
                var scrollPosition = this.scrollPosition;

                [].forEach.call(options.steps, function (step) {
                    var bBox = step.getBoundingClientRect(),
                        position = step.offsetTop,
                        height = position + bBox.height;

                    if (scrollPosition >= position && scrollPosition < height && currentStep !== step) {
                        currentStep = step;
                        step.classList.add(self.currentStepClass);
                        if (typeof options.onStepChange === 'function') options.onStepChange(step);
                    }
                    step.classList.remove(options.currentStepClass);
                });
            },

            destroy: function () {
                window.removeEventListener('scroll', throttledGetScrollPosition);
                window.removeEventListener('resize', throttledGetScrollPosition);
                options.navigationContainer.removeEventListener('click', this.doSmoothScroll);
            }
        }
    })();
     //////////////////////
     // END scroll Module
     //////////////////////


    //////////////////////
    // APP init
    //////////////////////

    var scrollToTopBtn = document.querySelector('.Scroll-to-top'),
        steps = document.querySelectorAll('.js-scroll-step'),
        navigationContainer = document.querySelector('.Quick-navigation'),
        links = navigationContainer.querySelectorAll('a'),
        progressIndicator = document.querySelector('.Scroll-progress-indicator');

    ScrollManager.init({
        steps: steps,
        scrollToTopBtn: scrollToTopBtn,
        navigationContainer: navigationContainer,
        links: links,

        // Customize onScroll behavior
        /*onScroll: function () {
            var percentage = ScrollManager.scrollPercentage();
            percentage >= 90 ? scrollToTopBtn.classList.add('visible') : scrollToTopBtn.classList.remove('visible');

            if (percentage >= 10) {
                progressIndicator.innerHTML = percentage + "%";
                progressIndicator.classList.add('visible');
            } else {
                progressIndicator.classList.remove('visible');
            }
        },*/

		// Behavior when a step changes
		// default : highlight links

		// onStepChange: function (step) {},

		// Customize the animation with jQuery, GSAP or velocity
     // default : jQuery animate()
     // Eg with GSAP scrollTo plugin

		//smoothScrollAnimation: function (target) {
		//		TweenLite.to(window, 2, {scrollTo:{y:target}, ease:Power2.easeOut});
  	 //}

    });

    //////////////////////
    // END APP init
    //////////////////////

})();
});

