function disableAccept(topParent,shownElement)
{
	var attr = shownElement.attr('acceptDisabled');
  	var acceptButton = $( topParent ).parent().find('#acceptButton')
	if (typeof attr !== typeof undefined && attr !== false) {
    	if(attr == 1)
    	{
    		
    		acceptButton.prop('disabled', true);
    	}
    	else
    	{
    		acceptButton.prop('disabled', false);
    	}
	}
	else
	{
		acceptButton.prop('disabled', false);
	}
}
var inSubStep = false
$(document).on('click','#activateButton',function(){
	inSubStep = true
	var parent = $( this ).parent( ".subControl" )
	var numberOfInstructions = $('.subText',parent).length
	parent.attr("index",1)
	parent.attr("numberOfInstructions",numberOfInstructions)
   $("#wellText",parent).show()

  $(this).hide()
  $("#backFowardCancel",parent).show()
  var currentIndex =parseInt(parent.attr("index"))
  var txtToShow = 'subText' +currentIndex 
  var shownElement = $("#"+txtToShow,parent)

  disableAccept(this,shownElement)

  changeProgressBar(0, parent)
  parent.find('#completedCheck').hide()
});

$(document).on('click',"#cancelButton",function(){
	var parent = $( this ).parents( ".subControl" )
	reset(parent)
});

$(document).on('click',"#fowardButton",function(){	

    var parent = $(this).parents(".subControl")

	var currentIndex =parseInt(parent.attr("index")) 

	var txtToHide = 'subText' +currentIndex
	currentIndex = currentIndex+1
	parent.attr("index",currentIndex)
	var txtToShow = 'subText' +currentIndex

	var hiddenElement = $("#"+txtToHide,parent)
	var shownElement = $("#"+txtToShow,parent)
	shownElement.show()
	hiddenElement.hide()

	var attr = shownElement.attr('apiFuncStart');
	if (typeof attr !== typeof undefined && attr !== false) {
    	eval(attr)
	}
	disableAccept(this,shownElement)
	
	checkControlValid(parent)
	changeProgressBar((currentIndex - 1) / (parent.attr("numberOfInstructions") - 1), parent)
	var completedattr = $(shownElement).attr('completed');
	if (typeof completedattr !== typeof undefined && completedattr !== false) {
	    $(parent).find('#completedCheck').show()
	}
	else
	{
	    $(parent).find('#completedCheck').hide()
	}

});

$(document).on('click',"#acceptButton",function(){	
	var parent = $( this ).parents( ".subControl" )

	var currentIndex =parseInt(parent.attr("index")) 
	var txtToShow = 'subText' +currentIndex

	var shownElement = $("#"+txtToShow,parent)

	
	var attr = shownElement.attr('apiFunc');
	if (typeof attr !== typeof undefined && attr !== false) {
    	eval(attr)
	}
	$(shownElement).attr('completed', true)
	$(parent).find('#completedCheck').show()
	
});

$(document).on('click',"#backButton",function(){
	var parent = $( this ).parents( ".subControl" )

	var currentIndex =parseInt(parent.attr("index")) 

	var txtToHide = 'subText' +currentIndex
	currentIndex = currentIndex-1
	parent.attr("index",currentIndex)
	var txtToShow = 'subText' +currentIndex

	var hiddenElement = $("#"+txtToHide,parent)
	var shownElement = $("#"+txtToShow,parent)
	shownElement.show()
	hiddenElement.hide()
	var attr = shownElement.attr('apiFuncStart');
	if (typeof attr !== typeof undefined && attr !== false) {
    	eval(attr)
	}

	disableAccept(this,shownElement)


	checkControlValid(parent)
	changeProgressBar((currentIndex - 1) / (parent.attr("numberOfInstructions") - 1), parent)

	var completedattr = $(shownElement).attr('completed');
	if (typeof completedattr !== typeof undefined && completedattr !== false) {
	    $(parent).find('#completedCheck').show()
	}
	else {
	    $(parent).find('#completedCheck').hide()
	}
		
});

function reset(parent)
{
	inSubStep = false
	$("#wellText",parent).hide('fast')
	$("#activateButton",parent).show('fast')
	$("#backFowardCancel",parent).hide('fast')
	$(".subText",parent).hide('fast')
	$("#subText1",parent).show('fast')
	parent.attr("index",1)
	checkControlValid(parent)
	changeProgressBar(0, parent)
	parent.find('.subText').each(function (index,subtext) {
	    var completedattr = $(subtext).attr('completed');
	    if (typeof completedattr !== typeof undefined && completedattr !== false) {
	        subtext.removeAttribute('completed')
	    }
	    
	})
}
function changeProgressBar(newPercentage,parent)
{
	newPercentage = newPercentage*100
	var $pb = $('.progress .progress-bar',parent);
	$pb.attr('data-transitiongoal', newPercentage).progressbar({display_text: 'center',use_percentage: false,
		amount_format: function(p, t) {return parent.attr("index") + ' of ' + parent.attr("numberOfInstructions");}});
}

function checkControlValid(parent) {
    var numberOfInstructions = parseInt(parent.attr("numberOfInstructions"))
    var currentIndex = parseInt(parent.attr("index")) 
    if(currentIndex==numberOfInstructions)
    {
    	$('#fowardButton',parent).attr("disabled", true);
    	$("#cancelButton",parent).hide('slow')
    	$('#backButton',parent).attr("disabled", true);
    	setTimeout(reset,2000,parent)
    	return
    }
    else
    {
    	$('#fowardButton',parent).attr("disabled", false);
    	$("#cancelButton",parent).show();
    }

    if(currentIndex==1)
    {
    	$('#backButton',parent).attr("disabled", true);
    }
    else
    {
    	$('#backButton',parent).attr("disabled", false);
    }
}

var subControlTemplate = "<h5 > {{mainStep}} <span id='completedCheck'> - <b>Completed</b></span></h5>\
                   	<div class='row' >\
                   		<div class='col-xs-8'>\
							<div class='progress progress-striped'>\
								<div id= 'step3ProgressBar' class='progress-bar' role='progressbar' data-transitiongoal='0'></div>\
							</div>\
						</div>\
						<div class='col-xs-4'>\
							<div id = 'backFowardCancel' class='btn-group' style='display: none;'' >\
								<button type='button' id='backButton' class='btn btn-default btn-sm'><span class='glyphicon glyphicon-chevron-left'></span></button>\
								<button type='button' id='acceptButton' class='btn btn-default btn-sm'>Accept</button>\
								<button type='button' id='fowardButton' class='btn btn-default btn-sm'><span class='glyphicon glyphicon-chevron-right'></span></button>\
								<!--<button type='button' id='cancelButton' class='btn btn-default btn-sm'>Cancel</button>-->\
							</div>\
						</div>\
					</div>"
var subControlValuesPage2 = {mainStep: "Step 2, Part 1 Progress"};
var subControlValuesPage3 = {mainStep: "Step 2, Part 2 Progress"};
var subControlValuesPage4 = { mainStep: "Step 4 Part 2 Progress" };
var subControlValuesPage5 = { mainStep: "Step 3 Part 1 Progress" };
var subControlValuesPage32 = { mainStep: "Step 4 Part 1 Progress" }
var subControlValuesPage61 = {mainStep: "Step 5 part 1 Progress"};
var subControlValuesPage62 = {mainStep: "Step 5 part 2 Progress"};
var subControlValuesPage63 = {mainStep: "Step 5 part 3 Progress"};
var subControlValuesPage7 = { mainStep: "Step 6 part 1 Progress" };
var subControlValuesPage72 = { mainStep: "Step 6 part 2 Progress" };
var subControlValuesPage8 = { mainStep: "Step 7 Progress" };


// 
