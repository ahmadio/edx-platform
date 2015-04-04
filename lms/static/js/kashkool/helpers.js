// Kashkool helpers 

var kashkool = kashkool || {};

(function($, _) {
	'use strict';

	kashkool.filterCourses = function(filter) {
		preventDefault();
        if (!(filter in ['current', 'past', 'comming'])){
          return false;
        }
        $('course-item').removeClass('shown');
        $('course-item'+'.'+filter).addClass('shown');
	};

	$(".filter-toggle").click(function(event){
		event.preventDefault();
		event.stopPropagation();
		console.log($(this).data('filter'));
		// if (!(filter in ['current', 'past', 'comming'])){
  //         return false;
  //       }

  		$('.course-item').removeClass('shown');
        $('.course-item'+'.'+$(this).data('filter')).addClass('shown');
        $('.filter-toggle').removeClass('active');
        $(this).addClass('active');
	});

}).call(this, $, _);