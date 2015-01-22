$(document).on("change",".fineNumber",function() {
  $(this).closest(".row").find('.rangeSlider').val($(this).val())
});

$(document).on("change",".rangeSlider",function() {
  $(this).closest(".row").find('.fineNumber').val($(this).val()).change()
});


function callAccept() {
    $(event.target).parent().closest('.subControl').find('.subText').filter(':visible').find('button').click()
}

function RemeshAcceptButton(id) {
    var Remesh = $(id).parent().find('#Remesh').val()
    var Smooth = $(id).parent().find('#Smooth').val()
    $.post('api/remesh(1,' + Remesh + ')', function (data) {
        if(apiReturnParser(data) ==false)
        {
            return;
        }

        $.post('api/remesh(2,' + Smooth + ')', function (data) {
            if (apiReturnParser(data) == false) {
                return;
            }
            $.post('api/accept()', apiReturnParser)
        })
    })
}

function SmoothAcceptButton(id) {
    var Smooth = $(id).parent().find('#Smooth').val()
    $.post('api/deformSmooth(' + Smooth + ')', function (data) {
        if (apiReturnParser(data) == false) {
            return;
        }

        $.post('api/accept()', apiReturnParser)
    })
   
}

function SmoothScaleAcceptButton(id) {
    var SmoothScale = $(id).parent().find('#Scale').val()
    $.post('api/deformSmoothScale(' + SmoothScale + ')', function (data) {
        if (apiReturnParser(data) == false) {
            return;
        }

        $.post('api/accept()', apiReturnParser)
    })
}


function offsetAcceptButton(id,connected) {
    var distance = $(id).parent().find('#Distance').val()
    var softTrans = $(id).parent().find('#SoftTransition').val()
    var condition = ''
    if (connected)
    {
        condition = 'True'
    }
    else
    {
        condition = 'False'
    }
    $.post('api/offsetDistance(' + distance + ',' + condition + ')', function (data) {
        if (apiReturnParser(data) == false) {
            return;
        }
        if (softTrans == undefined)
        {
            softTrans = 0
        }
        $.post('api/softTransition(' + softTrans + ')', function (data) {
            if (apiReturnParser(data) == false) {
                return;
            }
            $.post('api/accept()', apiReturnParser)
        })
        
    })
    $(id).parent().find('#Distance')
}


var template = "<div class='row' style='margin-left:3px;margin-right:3px;'>\
                        <button style='display: none;' id='hiddenAcceptButton' type='button' onclick={{acceptFunction}}>You should not able to see me</button>\
					  	{{#sliders}}\
						    <h5> {{sectionName}}</h5>\
							<div  class='row' style='margin-left:3px;margin-right:3px;'>\
								<div class='col-xs-9'>\
									<input class='rangeSlider' value={{value}} step = '{{step}}' min='{{min}}' max='{{max}}' type='range'>\
								</div>\
								<div class='col-xs-2' >\
									<input id = {{idName}} class='fineNumber' onchange={{onchange}} value={{value}} step = '{{step}}' name='quantity' min='{{min}}' max='{{max}}' type='number'>\
								</div>\
								<div class='col-xs-1'>\
									<p align='left'>{{units}} </p>\
								</div>\
							</div>\
						{{/sliders}} \
					</div>";
//----------------------------------------------------------------------------------------------------------------------
	var OffsetValuesAllowNegative = {
 	mainControlName:"Offset",
 	sliders:[{
 		value:4.0,
 		sectionName: "Distance",
 		idName: "Distance",
 		max: 20,
		min: -20,
		step:0.05,
        units:'mm',
		onchange: "$.post('api/offsetDistance('+$(this).val()+',True)',apiReturnParser)"
 	},
 	{
 		value:31,
 		sectionName: "Soft Transition",
 		idName: "SoftTransition",
 		max: 50,
		min: 0,
		step:0.05,
        units:'mm',
		onchange: "$.post('api/softTransition('+$(this).val()+')',apiReturnParser)"
 	}],
 	acceptFunction: "offsetAcceptButton(this,true)"
	};


 var OffsetValues = {
 	mainControlName:"Offset",
 	sliders:[{
 		value:4.0,
 		sectionName: "Distance",
 		idName: "Distance",
 		max: 10,
		min: 0,
		step:0.05,
        units:'mm',
		onchange: "$.post('api/offsetDistance('+$(this).val()+',True)',apiReturnParser)"
 	},
 	{
 		value:31,
 		sectionName: "Soft Transition",
 		idName: "SoftTransition",
 		max: 50,
		min: 0,
		step:0.05,
        units:'mm',
		onchange: "$.post('api/softTransition('+$(this).val()+')',apiReturnParser)"
 	}]
     , acceptFunction: "offsetAcceptButton(this,true)"
	};

 var OffsetValues2 = {
	mainControlName:"Offset",
	sliders:[{
		value:4.0,
		sectionName: "Distance",
		idName: "Distance",
		max: 10,
	    min: 0,
	    step:0.05,
        units:'mm',
	onchange: "$.post('api/offsetDistance('+$(this).val()+',False)',apiReturnParser)"
	}]
     , acceptFunction: "offsetAcceptButton(this,false)"
 };
 var OffsetValues3 = {
     mainControlName: "Offset",
     sliders: [{
         value: 4.0,
         sectionName: "Distance",
         idName: "Distance",
         max: 10,
         min: 0,
         step: 0.05,
         units: 'mm',
         onchange: "$.post('api/offsetDistance('+$(this).val()+',False)',apiReturnParser)"
     }]
     , acceptFunction: "offsetAcceptButton(this,true)"
 };

//----------------------------------------------------------------------------------------------------------------------
 var SmoothValues = {
 	mainControlName:"Smooth",
 	sliders:[{
 		value:0.5,
 		sectionName: "Select Size",
 		idName: "Smooth",
 		max: 1.0,
		min: 0,
		step:0.05,
        units:'',
		onchange: "$.post('api/deformSmooth('+$(this).val()+')',apiReturnParser)"
 	}]
     , acceptFunction: "SmoothAcceptButton(this)"
 };
 var SmoothValuesScale = {
     mainControlName: "SmoothScale",
     sliders: [{
         value: 4.0,
         sectionName: "Select Size",
         idName: "Scale",
         max: 200.0,
         min: 0,
         step: 1.0,
         units: '',
         onchange: "$.post('api/deformSmoothScale('+$(this).val()+')',apiReturnParser)"
     }]
      , acceptFunction: "SmoothScaleAcceptButton(this)"
 };
//----------------------------------------------------------------------------------------------------------------------
 var SelectValues = {
 	mainControlName:"Select Size",
 	sliders:[{
 		value:7,
 		sectionName: "Select Size",
 		idName: "Select",
 		max: 100,
		min: 0,
		step:1.0,
        units:'',
		onchange: "$.post('api/selectTool('+$(this).val()+')',apiReturnParser)"
 	}]
     , acceptFunction: "SelectAcceptButton(this)"
 };
 var SelectValuesTrimLine = {
     mainControlName: "Select Size",
     sliders: [{
         value: 5,
         sectionName: "Select Size",
         idName: "Select",
         max: 100,
         min: 0,
         step: 1.0,
         units: '',
         onchange: "$.post('api/selectTool('+$(this).val()+')',apiReturnParser)"
     }]
      , acceptFunction: "SelectAcceptButton(this)"
 };

//----------------------------------------------------------------------------------------------------------------------
 var RemeshValues = {
 	mainControlName:"Remesh",
 	sliders:[{
 		value:0.4,
 		sectionName: "Remesh",
 		idName:"Remesh",
 		max: 1,
		min: 0,
		step:0.05,
        units:'',
		onchange: "$.post('api/remesh(1,'+$(this).val()+')',apiReturnParser)"
 	},
 	{
 		value:0.5,
 		sectionName: "Smooth",
 		idName: "Smooth",
 		max: 1,
		min: 0,
		step:0.05,
        units:'',
		onchange: "$.post('api/remesh(2,'+$(this).val()+')',apiReturnParser)"
 	}
 	]
     , acceptFunction: "RemeshAcceptButton(this)"
	};




