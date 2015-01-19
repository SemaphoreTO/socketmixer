$('.questionMarkPlaceHolder').each(function( ) {
  //$(this).append("<span  class='glyphicon glyphicon-question-sign' style='horizontal-align:right'></span>")
});

$(document).on("click",".questionMarkPlaceHolder",function() {
	var attr = $(this).attr('helpPage');

	// For some browsers, `attr` is undefined; for others,
	// `attr` is false.  Check for both.
	var location =''
	if (typeof attr !== typeof undefined && attr !== false && attr) {
		debugger;
		location  = 'html/modeling/helpPages/'+attr
	}
	else
	{
		location = 'html/modeling/helpPages/noHelpText.html'
	}

	var width = screen.width
	var height = screen.height
	var args = "width=" + width / 5 + ", height=" + height * 0.5 + "top=0,left=0"
	window.open(location, "", args);

});