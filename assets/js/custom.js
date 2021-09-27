$(document).ready(function(){

	// Set the splides
	try{
		var splide = new Splide( '.splide', {
			type   : 'loop',
			drag: false,
			pagination: false,
			arrows: false,
		} ).mount();

		$('#splide_prev').on('click', function() {
			splide.go( '<' );
		})
		$('#splide_next').on('click', function() {
			splide.go( '>' );
		})

	} catch(e){
		console.log(e)
	}

	// Helper functions
	// This helps to set multiple attributes at once
	function setAttributes(el, attrs) {
		for(var key in attrs) {
			el.setAttribute(key, attrs[key]);
		}
	}

	$(".et-preloader").fadeOut("slow");
	//-------------------------------
	// Mobile Nav Menu
	//-------------------------------
	if($("#et-mobile-nav").length) {
		$('#et-mobile-nav').hcOffcanvasNav({
			maxWidth: 768
		});
	}

	// Ajax settings
	// Adding the format attr to strings
	String.prototype.format = function () {
	    var i = 0, args = arguments;
	    return this.replace(/{}/g, function () {
	      return typeof args[i] != 'undefined' ? args[i++] : '';
	    });
	  };


	// Code to select only one captain in line up options
	if ($('.line_up_captain').length){
		$('.line_up_captain').on('click', function(e){
			let line_up_captain = document.querySelectorAll('.line_up_captain')

			line_up_captain.forEach(i=>{
				if (i != this){
					i.checked = false
				}
			})
		})
	}


	// Code to generate time list
	let time_list = []
	let lhour = 12
	let lmin = 0
	let meridian = 'PM'

	for (var i=0; i < 96; i++){
		

		if (lmin == 60){
			lhour ++;
			lmin = 0;

			if (lhour == 13){
				lhour = 1
			}
		}

		if ((meridian == 'AM') && (lhour == 12) && (lmin == 0)){
			meridian = 'PM'
		} else if ((meridian == 'PM') && (lhour == 12) && (lmin == 0)){
			meridian = 'AM'
		}

		// Save time
		// Zero padd the lmin
		let lminz = lmin
		if (lmin == 0){
			lminz = '00'
		}
		time_list.push('{}:{} {}'.format(lhour, lminz, meridian))

		lmin += 15
	}

	// Setting the list times
	let list_times = document.querySelectorAll('.list_times')

	if ($('.list_times').length){
		let time_list_html = ''

		time_list.forEach(i=>{
			time_list_html += '<option>{}</option>'.format(i)
		})

		list_times.forEach(i=>{
			i.innerHTML = time_list_html
		})
	}

	function convert_to_24(val){
		let sp = val.split(' ')

		let main = sp[0]
		let meridian = sp[1]

		let sp2 = main.split(':')
		let hour = sp2[0]
		let min = sp2[1]

		if (meridian == 'PM'){
			if (hour != '12'){
				hour = parseInt(hour) + 12
			}

		} else if (meridian == 'AM'){
			if (hour == '12'){
				hour = 0
			}
		}

		return '{}:{}'.format(hour, min)
	}


	// Setting the dynamic options for select els
	let dy_selects = document.querySelectorAll('.dy_select')
	dy_selects.forEach(i=>{
		let text = i.getAttribute('select_text')

		// Get the select el
		let select_el = i.querySelector('select')

		if (select_el){
			select_el.firstElementChild.innerText = text
		}
	})


	// Codes for ajax setup for get and post requests to backend
	function getCookie(name) {
	    let cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        let cookies = document.cookie.split(';');
	        for (let i = 0; i < cookies.length; i++) {
	            let cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}


	let csrftoken = getCookie('csrftoken');


	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}



	try{
		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});
	} catch(e){
		console.log(e)
	}

	function load_news_carousel(){
		if($('#et-latest-news .owl-carousel').length){
			$('#et-latest-news .owl-carousel').owlCarousel({
				loop:true,
				nav:true,
				dots:false,
				margin:20,
				center: true,
				autoplay: false,
				autoplaySpeed: 1000,
				navSpeed: 1000,
				items:5,
				responsive:{
					0 : {
						items:1
					},
					// breakpoint from 480 up
					575 : {
						items:2
					},
					// breakpoint from 768 up
					768 : {
						items:3
					},
					// breakpoint from 1200 up
					1200 : {
						items:4
					}
				}
			})
		}
	}

	// Get facebook news
	if ($('#news_carousel').length){
	    let thisURL = $('#news_carousel').attr('news')

	    $.ajax({
	        method: "GET",
	        url: thisURL,
	        success: function (data){
	            let results = data['results']


	            // console.log(results)

	            // load results in dom
	            html = ''

	            author_img = $('#news_carousel').attr('author_img')
	            results.forEach(obj=>{
	            	// Posted 2 days ago

	            	var $owl = $('#news_carousel');
	            	$owl.trigger('destroy.owl.carousel');
	            	
	            	text = obj['text'].substring(0, 30) + '...'
	            	html += `
						<div class="item">
							<div class="blog-grid boxhover transition w-100 mt-4 rounded shadow">
								<div class="image-wrap img-overlay position-relative">
									<span class="badge badge-primary photocount pointer position-absolute"><i class="icon-eye"></i> 25</span>
									<span class="author-avatar overflow-hidden position-absolute shadow"><img src="{}" alt="Author"></span>
									<img src="{}" alt="img" class="img-fluid rounded-top" style="height: 300px;object-fit: cover;">
								</div>
								<div class="content p-4">

									<p class="text-muted">{}</p>
									<h4 class="mb-3"><a href="{}" class="text-decoration-none text-reset">Facebook News</a></h4>
									<p class="description">
										{}
									</p>
									<hr>
									<div class="d-flex align-items-center">
										<a href="#" class="text-decoration-none text-primary">Bonspiels Updates</a>
										<a target="_blank" href="{}" class="bg-primary text-white readmore rounded text-decoration-none d-inline-flex align-items-center justify-content-center border-0 ml-auto"><i class="icon-download"></i></a>
									</div>
								</div>
							</div>
						</div>
	            	`.format(author_img, obj['image'], obj['created'], obj['link'], text, obj['link'])

	            	$('#news_carousel').html(html)
	            	load_news_carousel()
	            })
	        },
	        error: function (jqXHR) {
	            console.log(jqxHR)
	        },
	    })
	}

	// Autocomplete for title suggestions
	$('#search-tcd').on('keyup', function(event){
		// Get the value for the input
		let input = document.querySelector('#search-tcd')
		let value = input.value

		// Create a string in serializable format and send with ajax
	    let serverLink = 'search-tcd={}'.format(value)

	    let thisURL = window.location.href // or set your own url

	    $.ajax({
	        method: "GET",
	        url: thisURL,
	        data: serverLink,
	        success: function (data){
	            let results = data['results']

	            // Change the datalist
	            let inHtml = ''
	            results.forEach(i=>{
	            	inHtml += '<option>{}</option>'.format(i)
	            })
	            $('#title_list').html(inHtml)
	        },
	        error: function (jqXHR) {
	            console.log(jqxHR)
	        },
	    })
	})

	//-------------------------------
	// Google Maps Initialization
	//-------------------------------
	if ($('#loadmaps').length) {
		var singleMap   =   false;
		if($('#loadmaps').hasClass('single-map')) {
			singleMap   =   true;
		}
		try{
			loadMap(singleMap);
		} catch(e){

		}
	}


	//-------------------------------
	// Lightbox
	//-------------------------------
	if($("a.lightbox").length) {
	$("a.lightbox").fancybox();
}
	//-------------------------------
	// jQuery Nice Select
	//-------------------------------
	if($("select").length) {
		$('select').niceSelect();
	}


	function setDateRel(input_el, this_el){
		// Update the start date rel input
		let el = document.querySelector("input[name='{}']".format(input_el))

		if (el){
			let sdate = this_el.value

			let parent = this_el.parentElement.parentElement

			let stime = parent.querySelector('.option.selected').innerText

			// Convert the stime into 24 hours time
			stime = convert_to_24(stime)

			el.value = '{} {}'.format(sdate, stime)
		}
	}



	if ($('#start_date_picker').length){
		$('#start_date_picker').on('change', function(e){
			if ($('#end_date_picker').length){
				$('#end_date_picker')[0].value = $('#start_date_picker')[0].value
			}

			setDateRel('start_date', this)
		})
	}

	if ($('#end_date_picker').length){
		$('#end_date_picker').on('change', function(e){
			setDateRel('end_date', this)
		})
	}



	// Updating anytime list times changes
	function setListTimeEvent(){
		list_times = document.querySelectorAll('.list_times')
		list_times.forEach(i=>{
			i.addEventListener('click', function(e){
				let target = e.target

				if ($(target).hasClass('option')){
					let input = target.parentElement.parentElement.parentElement.querySelector('input.form_datetime')
					// let picker = document.querySelector("input[list_times_id='#{}']".format())
					
					setTimeout(function(){
						$(input).change();
						
					}, 1000)
				}
			})
		})
	}
	setListTimeEvent()

	// Function to convert 24 hour time to 12 hour
	function tConvert (time) {
	  // Check correct time format and split into components
	  time = time.toString ().match (/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];

	  if (time.length > 1) { // If time format correct
	    time = time.slice (1);  // Remove full string match value
	    time[5] = +time[0] < 12 ? ' AM' : ' PM'; // Set AM/PM
	    time[0] = +time[0] % 12 || 12; // Adjust hours
	  }
	  return time.join (''); // return adjusted time or original string
	}



	// Code to update the start date when default data is added
	if ($('.default_time_data').length){
		let default_time_data = document.querySelectorAll('.default_time_data')

		default_time_data.forEach(i=>{
			let val = i.value

			if (val){
				let sp = val.split(' ')
				let input = i.parentElement.querySelector('.form_datetime')
				input.value = sp[0]

				let reTime = sp[1]
				if (reTime.length == 4){
					reTime = '0' + reTime
				}

				let lh = tConvert(reTime)
				let time_select = i.parentElement.querySelector('.list_times')

				console.log(lh)

				time_select.childNodes.forEach(i=>{
					if (i.innerText == lh){
						console.log('Found')
						i.setAttribute('selected', true)
						$(i).siblings().removeAttr('selected')
					}
				})

				$('select').niceSelect('update');
				setListTimeEvent()
			}
		})


	}



	//-------------------------------
	// Custom Scrollbar
	//-------------------------------
	if($(".scrollbar-inner").length) {
		jQuery('.scrollbar-inner').scrollbar();
	}


	//-------------------------------
	// Toggle Events list/grid view
	//-------------------------------
	if($(".event-results").length) {
		$(".list-view").hide();
		$('#event-grid-view').on("click", function(){
			$(".grid-view").show();
			$(".list-view").hide();
		})
		$('#event-list-view').on("click", function(){
			$(".list-view").show();
			$(".grid-view").hide();
		})
	}

	//-------------------------------
	// Gallery Images Upload
	//-------------------------------
	$('.image_bringer').change(function(event){
		var imageHTML = '';

		$(event.target.files).each(function(index){
			var tmppath = URL.createObjectURL(event.target.files[index]);
			imageHTML += '<div class="image-box no-hover position-relative"><img src="'+tmppath+'" alt="img"><span class="badge badge-primary ml-auto mt-3 pointer border-0 font-weight-normal remove-image position-absolute" data-targetimg="'+ index +'"><i class="fas fa-trash"></i></span></div>';
		});

		let image_view = this.getAttribute('image_view')

		if (image_view == '#multiple_images'){
			$(image_view).html($(image_view).html() + imageHTML);
		} else {
			$(image_view).html(imageHTML);
		}

		$('.remove-image').on('click', function(e){
			this.parentElement.remove()
		})

		
		event.preventDefault();

	});

	// Submits form on change sort_selector
	$('#sort_selector').on('change', function(event){
		$('#filterFormSubmit').click()
	})

	//-------------------------------
	// Gallery Images Upload
	//-------------------------------
	function listenRemoveSchedules() {
		$('.remove-schedule').on("click", function() {
			let num = $("#event-schedules").children().length;
			if (num > 1){
				this.parentElement.parentElement.remove()
			} else {
				alert('You are required to add at least a schedule')
			}
			// Update form-TOTAL_FORMS
			let tot_form = $("input[name='form-TOTAL_FORMS']")
			tot_form[0].value = num - 1
		})
	}

	//-------------------------------
	// Toggle Event Filter
	//-------------------------------
	if($(".search-filter").length) {
		$('#toggle-filter').on("click", function(){
			$( ".search-filter" ).slideToggle("slow");
		});
	}


	//-------------------------------
	// Calendar
	//-------------------------------
	if($(".event-calendar").length) {
		$(".event-calendar .calendar:not(.month)").hide();
		$(".calendar-nav button.show-days").on("click", function(){
			$(this).addClass("btn-primary text-white").siblings("button").removeClass("btn-primary text-white");
			$(".event-calendar .calendar.day").show().siblings(".calendar").hide();
		})
		$(".calendar-nav button.show-week").on("click", function(){
			$(this).addClass("btn-primary text-white").siblings("button").removeClass("btn-primary text-white");
			$(".event-calendar .calendar.week").show().siblings(".calendar").hide();
		})
		$(".calendar-nav button.show-month").on("click", function(){
			$(this).addClass("btn-primary text-white").siblings("button").removeClass("btn-primary text-white");
			$(".event-calendar .calendar.month").show().siblings(".calendar").hide();
		})
	}

	//-------------------------------
	// Scrolldown
	//-------------------------------
	if($(".scrolldown").length) {
		$('.scrolldown').on('click', function(){
			$("html, body").animate({
				scrollTop: $('#et-popular-events').offset().top
			}, 1000);
		});
	}

	//-------------------------------
	// Fix Tabs
	//-------------------------------
	if($(".scroll-tabs").length) {
		$(window).bind('scroll', function() {
			var navHeight = $( window ).height() - 70;
			if ($(window).scrollTop() > navHeight) {
				$('.scroll-tabs').addClass('fixed shadow');
			}
			else {
				$('.scroll-tabs').removeClass('fixed shadow');
			}
		});
	}

	//-------------------------------
	// Generic Smooth Scroll on Anchor
	//-------------------------------
	try{
		$(document).on('click', 'a[href^="#"]', function (event) {
			event.preventDefault();
			$(this).addClass("active").siblings().removeClass("active");
			$('html, body').animate({
				scrollTop: $($.attr(this, 'href')).offset().top-75
			}, 500);
		});
	} catch(e){

	}

	//-------------------------------
	// Switch Galleries
	//-------------------------------
	if($("#et-big-gallery").length){
		$('.big-gallery > div[class^="gallery-1"]').show();
		$(document).on('click', 'div[id^="gallery-"]', function (event) {
			event.preventDefault();
			var ID = $(this).attr("id");
			var gallery = $("div." + ID);
			$(gallery).show().siblings('div[class^="gallery-"]').hide();
		});
	}
	
	//-------------------------------
	// Switch Galleries
	//-------------------------------
	if($("#et-big-gallery-2").length){
		$('.big-gallery > div[class^="gallery-1"]').show();
		$(document).on('click', 'div[id^="gallery-"]', function (event) {
			event.preventDefault();
			var ID = $(this).attr("id");
			var gallery = $("div." + ID);
			$(gallery).show().siblings('div[class^="gallery-"]').hide();
		});
	}

	//-------------------------------
	// Switch Galleries
	//-------------------------------
	if($("#et-big-gallery-2").length){
		$('.big-gallery > div[class^="gallery-1"]').show();
		$(document).on('click', 'div[id^="gallery-"]', function (event) {
			event.preventDefault();
			var ID = $(this).attr("id");
			var gallery = $(".big-gallery > div").attr("class") == ID;
			console.log($(".big-gallery > div").attr("class") == ID);
			$(gallery).show();
		});
	}

	//-------------------------------
	// Range Slider
	//-------------------------------
	if($(".js-range-slider").length) {
		$(".js-range-slider").ionRangeSlider({
			skin: "big"
		});
	}

	//-------------------------------
	// Featured Events
	//-------------------------------
	if($('.featured-events .owl-carousel').length){
		$('.featured-events .owl-carousel').owlCarousel({
			loop:true,
			nav:true,
			dots:false,
			autoplay: false,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:1
		})
	}


	//-------------------------------
	// Big gallery
	//-------------------------------
	if($('.big-gallery').length){
		$('.big-gallery .owl-carousel').owlCarousel({
			loop:true,
			nav:true,
			dots:false,
			autoplay: true,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:1
		})
	}


	//-------------------------------
	// Testimonial
	//-------------------------------
	if($('#et-testimonial .owl-carousel').length){
		$('#et-testimonial .owl-carousel').owlCarousel({
			loop:true,
			nav:true,
			dots:false,
			autoplay: true,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:2,
			responsive:{
				0 : {
					items:1
				},
				768 : {
					items:2
				}
			}
		})
	}

	//-------------------------------
	// Latest News
	//-------------------------------
	load_news_carousel()

	//-------------------------------
	// Testimonial (About)
	//-------------------------------
	if($('#et-testimonial2 .owl-carousel').length){
		$('#et-testimonial2 .owl-carousel').owlCarousel({
			loop:true,
			nav:true,
			dots:false,
			autoplay: true,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:2,
			responsive:{
				0 : {
					items:1
				},
				// breakpoint from 480 up
				575 : {
					items:1
				},
				// breakpoint from 768 up
				768 : {
					items:2
				},
				// breakpoint from 1200 up
				1200 : {
					items:2
				}
			}
		})
	}

	//-------------------------------
	// Upcoming Events
	//-------------------------------
	if($('#et-upcoming-events .owl-carousel').length){
		$('#et-upcoming-events .owl-carousel').owlCarousel({
			loop:true,
			nav:true,
			dots:false,
			autoplay: true,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:5,
			center: true,
			responsive:{
				0 : {
					items:1
				},
				// breakpoint from 480 up
				575 : {
					items:2
				},
				// breakpoint from 768 up
				768 : {
					items:3
				},
				// breakpoint from 1200 up
				1200 : {
					items:5
				}
			}
		})
	}

	//-------------------------------
	// Related Events
	//-------------------------------
	if($('#et-related-events .owl-carousel').length){
		$('#et-related-events .owl-carousel').owlCarousel({
			loop:true,
			// nav:true,
			dots:false,
			autoplay: true,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:5,
			margin: 20,
			center: true,
			responsive:{
				0 : {
					items:1
				},
				// breakpoint from 480 up
				575 : {
					items:2
				},
				// breakpoint from 768 up
				768 : {
					items:3
				},
				// breakpoint from 1200 up
				1200 : {
					items:5
				}
			}
		})
	}

	//-------------------------------
	// Content Slides
	//-------------------------------
	if($('.content-slides .owl-carousel').length){
		$('.content-slides .owl-carousel').owlCarousel({
			loop:true,
			dots:false,
			nav: true,
			autoplay: false,
			autoplaySpeed: 1000,
			navSpeed: 1000,
			items:1,
			center: true
		})
	}

	/*
	==============================================================
	Project Detail Slider
	==============================================================
	*/
	if($('#et-project_slider .owl-carousel').length){
		$("#et-project_slider .owl-carousel").owlCarousel({
			loop:true,
			margin:20,
			nav:true,
			items:1
		});
	};

	//-------------------------------
	// Countdown
	//-------------------------------

	if($('.time-left').length){
		// Get all the timers on screen to get their enddates
		let timers = document.querySelectorAll('.time-left')

		timers.forEach(i=>{
			function makeTimer() {
				//		var endTime = new Date("29 July 2018 9:56:00 GMT+01:00");
				var endTime = new Date(i.getAttribute('end_date'));
				endTime = (Date.parse(endTime) / 1000);
	
				var now = new Date();
				now = (Date.parse(now) / 1000);
	
				var timeLeft = endTime - now;

				if (timeLeft < 0 ){
					$(i.querySelector('.days')).html(0 + "<span>Days</span>");
					$(i.querySelector('.hours')).html(0 + "<span>Hr</span>");
					$(i.querySelector('.minutes')).html(0 + "<span>Min</span>");
					$(i.querySelector('.seconds')).html(0 + "<span>Sec</span>");
				} else {
	
					var days = Math.floor(timeLeft / 86400);
					var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
					var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
					var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
		
					if (hours < "10") { hours = "0" + hours; }
					if (minutes < "10") { minutes = "0" + minutes; }
					if (seconds < "10") { seconds = "0" + seconds; }

					$(i.querySelector('.days')).html(days + "<span>Days</span>");
					$(i.querySelector('.hours')).html(hours + "<span>Hr</span>");
					$(i.querySelector('.minutes')).html(minutes + "<span>Min</span>");
					$(i.querySelector('.seconds')).html(seconds + "<span>Sec</span>");

				}
			}
			setInterval(function() { makeTimer(); }, 1000);
		})
	}

	//-------------------------------
	// Star Rating
	//-------------------------------

	if($('#stars').length){

		/* 1. Visualizing things on Hover - See next part for action on click */
		$('#stars li').on('mouseover', function(){
			var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on

			// Now highlight all the stars that's not after the current hovered star
			$(this).parent().children('li.star').each(function(e){
				if (e < onStar) {
					$(this).addClass('hover');
				}
				else {
					$(this).removeClass('hover');
				}
			});

		}).on('mouseout', function(){
			$(this).parent().children('li.star').each(function(e){
				$(this).removeClass('hover');
			});
		});

		/* 2. Action to perform on click */
		$('#stars li').on('click', function(){
			var onStar = parseInt($(this).data('value'), 10); // The star currently selected
			var stars = $(this).parent().children('li.star');

			for (i = 0; i < stars.length; i++) {
				$(stars[i]).removeClass('selected');
			}

			for (i = 0; i < onStar; i++) {
				$(stars[i]).addClass('selected');
			}

			// JUST RESPONSE (Not needed)
			var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
			var msg = "";
			if (ratingValue > 1) {
				msg = "You rated " + ratingValue + " stars.";
			}
			else {
				msg = "You rated " + ratingValue + " stars.";
			}
			responseMessage(msg);

		});
		function responseMessage(msg) {
			$('.rate-result').fadeIn(200);
			$('.rate-result').text(msg);
		}
	}


	//-------------------------------
	// Event Gallery
	//-------------------------------

	if($('.gallery-mason').length){
		const divs = document.querySelectorAll('.gallery-mason .image-box');
		const body = document.body;
		const prev = document.querySelector('.gallery-mason .prev');
		const next = document.querySelector('.gallery-mason .next');


		Array.prototype.slice.call(divs).forEach(function (el) {
			el.addEventListener('click', function () {
				this.classList.toggle('show');
				body.classList.toggle('gallery-active');
				checkNext();
				checkPrev();
			});
		});

		prev.addEventListener('click', function() {
			const show = document.querySelector('.gallery-mason .image-box.show');
			const event = document.createEvent('HTMLEvents');
			event.initEvent('click', true, false);

			show.previousElementSibling.dispatchEvent(event);
			show.classList.remove('show');
			body.classList.toggle('gallery-active');
			checkNext();
		});

		next.addEventListener('click', function() {
			const show = document.querySelector('.gallery-mason .image-box.show');
			const event = document.createEvent('HTMLEvents');
			event.initEvent('click', true, false);

			show.nextElementSibling.dispatchEvent(event);
			show.classList.remove('show');
			body.classList.toggle('gallery-active');
			checkPrev();
		});

		// Remove Image
		$(".image-box .remove-image").on("click", function(){
			$(this).parent(".image-box").remove();
		})
	}
	//-------------------------------
	// Bootstrap DateTimePicker
	//-------------------------------
	function refreshDatepickers(){
		// $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii'});
		$(".form_datetime").datetimepicker({
			format: 'yyyy-mm-dd',
			minView:'month'
		});
	}
	if($(".form_datetime").length) {
		refreshDatepickers()
	}

	//-------------------------------
	// Initiliaze Tooltip
	//-------------------------------
	if($('[data-toggle="tooltip"]').length) {
		$(function () {
			$('[data-toggle="tooltip"]').tooltip({
				// Pass options here
			})
		})
	}


	//-----------------------------------------
	// Variable content info for Add Event Form
	//-----------------------------------------

	if($("#et-add-event").length) {
		var infoBoxTop  =   $('.info-box').offset().top+50;
		$(".getcontent").each(function() {
			$(this).find(".form-control").focus(function() {
				console.log('focused');
				var infoBoxNewTop   =   $(this).offset().top-infoBoxTop;
				var title = $(this).attr("placeholder");
				var description = $(this).attr("title");

				$(".info-box").css('margin-top', infoBoxNewTop+'px');

				$(".info-box h5").text(title);
				$(".info-box p").text(description);
			});
		});
	}

	

	// --------------https://github.com/devvspaces/----------------
	// Agree sign up checkbox
	// ------------------------------------------------------------
	let signupcheck = document.getElementById('signupcheck')
	let signupbtn = document.getElementById('signupbtn')

	function setSignupbtn(e) {
		if (signupcheck.checked){
			signupbtn.removeAttribute('disabled')
			console.log(signupbtn)
		} else {
			signupbtn.removeAttribute('disabled', '')
			console.log(signupbtn)
		}
		
	}

	try{
		signupcheck.addEventListener('click', setSignupbtn)
	} catch(e){
		console.log(e)
	}
	


	// Review submission
	$('#review_submit').on('click', function(){
		// Count selected starts
		let stars_count = document.querySelectorAll('#review_ratings .star.selected').length

		// Set the input value of the stars
		$("#review_form input[name='stars'")[0].value = stars_count

		$("#review_form").submit()
	})


	// Code for information tools
	let included_tool_box = document.querySelectorAll('.included_tool_box')
	
	$('.included_tool_box').on('change', function(event){
		let req_el = document.getElementById(this.getAttribute('req_id'))
		if (this.checked){
			req_el.removeAttribute('disabled')
		} else {
			req_el.setAttribute('disabled', true)
			req_el.checked = false
		}
	})

	included_tool_box.forEach(i=>{
		let req_el = document.getElementById(i.getAttribute('req_id'))
		if (i.checked){
			req_el.removeAttribute('disabled')
		} else {
			req_el.setAttribute('disabled', true)
			req_el.checked = false
		}
	})

	// Code to submit event form
	$('#addEventForm').on('submit', function(event){
		event.preventDefault()
		swal({
		  title: "Save and Publish Event?",
		  text: "Are you ready to save and publish this event?",
		  icon: "success",
		  buttons: true,
		  dangerMode: false,
		})
		.then((willDelete) => {
		  if (willDelete) {
		    swal($('#addEventForm').attr('message'), {
		      icon: "success",
		      button: false
		    });

		    document.querySelector('#addEventForm').submit()
		  }
		});

	});


	// Code to report event form
	$('#reportEvent').on('click', function(event){
		event.preventDefault()
		swal({
		  title: "Report event?",
		  text: "Are you sure you want to report this event?",
		  icon: "error",
		  buttons: true,
		  dangerMode: true,
		})
		.then((willDelete) => {
		  if (willDelete) {
		    swal("Reporting event ...", {
		      icon: "error",
		      button: false
		    });
		    window.location.href = $('#reportEvent').attr('href')
		  }
		});

	});
});

//-------------------------------
// Google Maps
//-------------------------------
function loadMap(singleMap) {
	var docWidth    =   $(document).width();
	let loadmaps = document.getElementById('loadmaps')

	featured_image = loadmaps.getAttribute('featured_image')
	title = loadmaps.getAttribute('title')
	description = loadmaps.getAttribute('description')
	status = loadmaps.getAttribute('status')
	// detail_link = loadmaps.getAttribute('detail_link')
	detail_link = window.location.href

	if(singleMap) {
		var mapZoom     =   25,
		mapCenter   =   [loadmaps.getAttribute('lat'), loadmaps.getAttribute('lon')]
		var lsitingLocations = [
			['Maroubra Beach', loadmaps.getAttribute('lat'), loadmaps.getAttribute('lon'), 1]
		];

		var listingContents =   [
			`<div class="listing-map-window">
				<img width='30px' class='rounded-circle' src="{}" class="mb-3" alt="{}">
				<div class="pl-1">
					<h6>{}</h6>
					<p>{}</p>
					<span class="badge badge-primary mr-3">{}</span>
					<a class="w-100 text-primary" href="{}">View Details <i class="fas fa-angle-double-right"></i></a>
				</div>
			</div>`.format(featured_image, title, title, description, status, detail_link),
		]
	} else {

		var mapZoom     =   16;
		if($('.sidebar-map-fixed').length && docWidth > 980){
			var footerHeight    =   $('.et-copyright-bar').height(),
			windowHeight    =   $(window).height(),
			mapTop          =   $('.sidebar-map-fixed').offset().top,
			mapHeight       =   parseInt(windowHeight-(mapTop+footerHeight));


			$('.sidebar-map-fixed').css('height', mapHeight+'px');
			mapZoom     =   14;
		}
		if(jQuery('section.et-maps-banner-wrapper').length) {
			mapZoom	=	15;
		}


		if(docWidth > 319 && docWidth < 980) {
			mapZoom =   14
		}
		var mapCenter   =   [-33.91722, 110.23064];
		var lsitingLocations = [
			['Bondi Beach', -33.9148339, 110.2404048, 4],
			['new beach', -33.9169667, 110.2345321, 3],
			['new beach', -33.9158827, 110.2314457, 2],
			['new beach', -33.9175679, 110.2255712, 1],
		];

		var listingContents =   [
			`<div class="listing-map-window">
				<img src="{}" class="mb-3 w-100" alt="{}">
				<div class="pl-1">
					<h6>{}</h6>
					<p>{}</p>
					<span class="badge badge-primary mr-3">{}</span>
					<a class="w-100 text-primary" href="{}">View Details <i class="fas fa-angle-double-right"></i></a>
				</div>
			</div>`.format(featured_image, title, description, status, detail_link),
		]
	}


	var icons = ['hotel', 'shopping', 'auto', 'hospital'];
	var map = new google.maps.Map(loadmaps, {
		zoom: mapZoom,
		center: new google.maps.LatLng(mapCenter[0], mapCenter[1]),
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});

	var infowindow = new google.maps.InfoWindow();

	var marker, i;

	for (i = 0; i < lsitingLocations.length; i++) {
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(lsitingLocations[i][1], lsitingLocations[i][2]),
			map: map,
			icon: 'img/'+icons[i]+'-marker.png'
		});
		if(docWidth > 767) {
			google.maps.event.addListener(marker, 'click', (function(marker, i) {
				return function() {
					infowindow.setContent(listingContents[0]);
					infowindow.open(map, marker);
				}
			})(marker, i));
		}
	}
}


function initMap() {
	var map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: -33.8688, lng: 151.2195},
	  zoom: 13
	});
	var input = document.getElementById('searchInput');
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

	var autocomplete = new google.maps.places.Autocomplete(input);
	autocomplete.bindTo('bounds', map);

	var infowindow = new google.maps.InfoWindow();
	var marker = new google.maps.Marker({
		map: map,
		anchorPoint: new google.maps.Point(0, -29)
	});

	autocomplete.addListener('place_changed', function() {
		infowindow.close();
		marker.setVisible(false);
		var place = autocomplete.getPlace();
		if (!place.geometry) {
			// window.alert("Autocomplete's returned place contains no geometry");
			return;
		}
  
		// If the place has a geometry, then present it on a map.
		if (place.geometry.viewport) {
			map.fitBounds(place.geometry.viewport);
		} else {
			map.setCenter(place.geometry.location);
			map.setZoom(17);
		}
		marker.setIcon(({
			url: place.icon,
			size: new google.maps.Size(71, 71),
			origin: new google.maps.Point(0, 0),
			anchor: new google.maps.Point(17, 34),
			scaledSize: new google.maps.Size(35, 35)
		}));
		marker.setPosition(place.geometry.location);
		marker.setVisible(true);
	
		var address = '';
		if (place.address_components) {
			address = [
			  (place.address_components[0] && place.address_components[0].short_name || ''),
			  (place.address_components[1] && place.address_components[1].short_name || ''),
			  (place.address_components[2] && place.address_components[2].short_name || '')
			].join(' ');
		}
	
		infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
		infowindow.open(map, marker);
	  
		// Location details
		// for (var i = 0; i < place.address_components.length; i++) {
		// 	if(place.address_components[i].types[0] == 'postal_code'){
		// 		document.getElementById('postal_code').innerHTML = place.address_components[i].long_name;
		// 	}
		// 	if(place.address_components[i].types[0] == 'country'){
		// 		document.getElementById('country').innerHTML = place.address_components[i].long_name;
		// 	}
		// }
		// document.getElementById('location').innerHTML = place.formatted_address;
		
		document.getElementById('lat').value = place.geometry.location.lat();
		document.getElementById('lon').value = place.geometry.location.lng();
	});
}