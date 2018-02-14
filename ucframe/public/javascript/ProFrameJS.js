var cpu = [], cpuCore = [], disk = [];
var dataset;
var totalPoints = 100;
var updateInterval = 5000;
var now = new Date().getTime();

var options = {
    series: {
        lines: {
            lineWidth: 1.2
        },
        bars: {
            align: "center",
            fillColor: { colors: [{ opacity: 1 }, { opacity: 1}] },
            barWidth: 500,
            lineWidth: 1
        }
    },
    xaxis: {
        mode: "time",
        tickSize: [60, "second"],
        tickFormatter: function (v, axis) {
            var date = new Date(v);

            if (date.getSeconds() % 20 == 0) {
                var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
                var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

                return hours + ":" + minutes + ":" + seconds;
            } else {
                return "";
            }
        },
        axisLabel: "Time",
        axisLabelUseCanvas: true,
        axisLabelFontSizePixels: 12,
        axisLabelFontFamily: 'Verdana, Arial',
        axisLabelPadding: 10
    },
    yaxes: [
        {
            min: 0,
            max: 100,
            tickSize: 5,
            tickFormatter: function (v, axis) {
                if (v % 10 == 0) {
                    return v + "%";
                } else {
                    return "";
                }
            },
            axisLabel: "CPU loading",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }, {
            max: 5120,
            position: "right",
            axisLabel: "Disk",
            axisLabelUseCanvas: true,
            axisLabelFontSizePixels: 12,
            axisLabelFontFamily: 'Verdana, Arial',
            axisLabelPadding: 6
        }
    ],
    legend: {
        noColumns: 0,
        position:"nw"
    },
    grid: {      
        backgroundColor: { colors: ["#ffffff", "#EDF5FF"] }
    }
};

function initData() {
    for (var i = 0; i < totalPoints; i++) {
        var temp = [now += updateInterval, 0];

        cpu.push(temp);
        cpuCore.push(temp);
        disk.push(temp);
    }
}

function GetData() {
    $.ajaxSetup({ cache: false });

    $.ajax({
        url: "http://www.jqueryflottutorial.com/AjaxUpdateChart.aspx",
        dataType: 'json',
        success: update,
        error: function () {
            setTimeout(GetData, updateInterval);
        }
    });
}

var temp;

function update(_data) {
    cpu.shift();
    cpuCore.shift();
    disk.shift();

    now += updateInterval

    temp = [now, _data.cpu];
    cpu.push(temp);

    temp = [now, _data.core];
    cpuCore.push(temp);

    temp = [now, _data.disk];
    disk.push(temp);

    dataset = [
        { label: "CPU:" + _data.cpu + "%", data: cpu, lines: { fill: true, lineWidth: 1.2 }, color: "#00FF00" },
        { label: "Disk:" + _data.disk + "KB", data: disk, color: "#0044FF", bars: { show: true }, yaxis: 2 },
        { label: "CPU Core:" + _data.core + "%", data: cpuCore, lines: { lineWidth: 1.2}, color: "#FF0000" }        
    ];

    $.plot($("#flot-placeholder1"), dataset, options);
    setTimeout(GetData, updateInterval);
}

function sketchProc(processing){
  // Override draw function, by default it will be called 60 times per second
  processing.draw = function() {
    // determine center and max clock arm length
	var itemSize = 20;
	var textSize = 200;
	processing.size(800, 600);
	processing.noLoop();
    // erase background
    processing.background(0);
	processing.textSize(itemSize);
	
	var mydata = JSON.parse(data);
	
	for (var key in mydata){
		var i = 0;
		if (key == "People"){
			for (position = 0; position < mydata[key].length; position++){
				processing.rect((0), (i), (itemSize), (itemSize));
				processing.text(mydata[key][position], itemSize,i+itemSize);
				i = i + itemSize;
			}
		}
		i = 0;
		if (key == "Tool"){
			for (position = 0; position < mydata[key].length; position++){
				processing.ellipse((itemSize*2+itemSize/2 + textSize), (i+itemSize/2), (itemSize), (itemSize));
				processing.text(mydata[key][position], (itemSize*2+itemSize/2 + textSize + itemSize),(i+itemSize));
				i = i + itemSize;
			}
		}
		i = 0;
		if (key == "Material"){
			for (position = 0; position < mydata[key].length; position++){
				processing.triangle((itemSize*4 + textSize*2), (i), (itemSize*5 + textSize*2), (i), (itemSize*4 + itemSize/2 + textSize*2), (i+itemSize*3/4));
				processing.text(mydata[key][position], (itemSize*5 + textSize*2),i+itemSize);
				i = i + itemSize;
			}
		}
		
	}
  };  
}



function TaskComparisonView(processing){
	  // Override draw function, by default it will be called 60 times per second
	  processing.draw = function() {
	    // determine center and max clock arm length
		var itemSize = 40;
		var textSize = 300;
		processing.size(1500, 1000);
		processing.stroke(125);
		processing.strokeWeight(2);
		processing.noLoop();
	    // erase background
	    processing.background(0);
		processing.textSize(itemSize/2);
		
		var mydata = JSON.parse(data);

		var rectX, rectY, circleX, circleY, textX, textY, triangleX1, triangleX2, triangleX3, triangleY1, triangleY2, triangleY3, lineX1, lineY1, lineX2, lineY2;
		var PeopleTypeNumber = 0;
		var MaterialTypeNumber = 2;
		var ToolTypeNumber = 4;
		
		function countRectPosition(number, typeNumber) {      
				rectX = (textSize) * typeNumber;
				rectY = number * itemSize;
		    };
		function countCirclePosition(number, typeNumber) {      
			circleX = (textSize) * typeNumber + itemSize/2;
			circleY = number * itemSize + itemSize/2;
	    };
		function countTrianglePosition(number, typeNumber) {      
			triangleX1 = (textSize) * typeNumber;
			triangleY1 = number * itemSize; 
			triangleX2 = (textSize) * typeNumber + itemSize;
			triangleY2 = number * itemSize;
			triangleX3 = (textSize) * typeNumber + itemSize/2;
			triangleY3 = number * itemSize + itemSize*3/4;
	    };
		function countTextPosition(number, typeNumber) { 
			textX = itemSize + (textSize) * typeNumber;
			textY = (number+3/4) * itemSize;
	    };
		function countLinePosition(number, typeNumber, number2, typeNumber2) { 
			lineX1 = itemSize + (textSize) * typeNumber;
			lineY1 = (number+1/2) * itemSize;
			lineX2 = (textSize) * typeNumber2;
			lineY2 = (number2+1/2) * itemSize;
	    };
		
		for (var key in mydata){
			if (key == "People"){
				for (var tag in mydata[key]){
					
					for (position = 0; position < mydata['TagInOriginalTaskCase']['People'].length; position++){
						//alert(tag + "---- " + mydata['sameMaterial'][position]);
						if(tag == mydata['TagInOriginalTaskCase']['People'][position]){
							processing.fill(102, 204,0);	
							//alert("TEMP");
						}
					}
					
					countCirclePosition(mydata[key][tag],PeopleTypeNumber+0.5);
					processing.ellipse(circleX, circleY, (itemSize), (itemSize));
					countTextPosition(mydata[key][tag],PeopleTypeNumber+0.5);
					processing.text(tag, textX,textY);		
					countCirclePosition(mydata[key][tag],PeopleTypeNumber+1);
					processing.ellipse(circleX, circleY, (itemSize), (itemSize));
				}
				processing.fill(255);
			}
			if (key == "Material"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata['TagInOriginalTaskCase']['Material'].length; position++){
						//alert(tag + "---- " + mydata['sameMaterial'][position]);
						if(tag == mydata['TagInOriginalTaskCase']['Material'][position]){
							processing.fill(102, 204,0);	
							//alert("TEMP");
						}
					}
					countRectPosition(mydata[key][tag],MaterialTypeNumber);
					processing.rect(rectX, rectY, (itemSize*3/4), (itemSize*3/4));
					countTextPosition(mydata[key][tag],MaterialTypeNumber);
					processing.text(tag, textX,textY);
					countRectPosition(mydata[key][tag],MaterialTypeNumber+1);
					processing.rect(rectX, rectY, (itemSize*3/4), (itemSize*3/4));
					
					
					processing.fill(255);
				}
			}
			if (key == "Tool"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata['TagInOriginalTaskCase']['Tool'].length; position++){
						//alert(tag + "---- " + mydata['sameMaterial'][position]);
						if(tag == mydata['TagInOriginalTaskCase']['Tool'][position]){
							processing.fill(102, 204,0);	
							//alert("TEMP");
						}
					}
					countTrianglePosition(mydata[key][tag],ToolTypeNumber);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					countTextPosition(mydata[key][tag],ToolTypeNumber);
					processing.text(tag, textX,textY);	
					countTrianglePosition(mydata[key][tag],ToolTypeNumber+0.8);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					
					
					
					processing.fill(255);
				}
			}
			if (key == "PeopleLink"){
				processing.strokeWeight(4);
				processing.stroke(102, 204,0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["People"][tag], PeopleTypeNumber+1, mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber);
						processing.line(lineX1, lineY1-5, lineX2, lineY2-5);
					}			
				}
				processing.strokeWeight(2);
			}
			if (key == "ToolLink"){
				processing.strokeWeight(4);
				processing.stroke(102, 204,0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1-5, lineX2, lineY2-5);
					}			
				}
				processing.strokeWeight(2);
			}
			if (key == "PeopleLink1"){
				processing.stroke(0, 102, 204);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["People"][tag], PeopleTypeNumber+1, mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber);
						processing.line(lineX1, lineY1, lineX2, lineY2);
					}			
				}
			}
			if (key == "ToolLink1"){
				processing.stroke(0, 102, 204);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+0.1, lineX2, lineY2+0.1);
					}			
				}
			}
			if (key == "PeopleLink2"){
				processing.stroke(255, 0, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["People"][tag], PeopleTypeNumber+1, mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber);
						processing.line(lineX1, lineY1+5, lineX2, lineY2+5);
					}			
				}
			}
			if (key == "ToolLink2"){
				processing.stroke(255, 0, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+5, lineX2, lineY2+5);
					}			
				}
			}
			if (key == "PeopleLink3"){
				processing.stroke(255, 255, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["People"][tag], PeopleTypeNumber+1, mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber);
						processing.line(lineX1, lineY1+10, lineX2, lineY2+10);
					}			
				}
			}
			if (key == "ToolLink3"){
				processing.stroke(255, 255, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+10, lineX2, lineY2+10);
					}			
				}
			}
		}	

	};
}


function ToolChainView(processing){
	// Override draw function, by default it will be called 60 times per second
	  processing.draw = function() {
	    // determine center and max clock arm length
		var itemSize = 40;
		var textSize = 300;
		processing.size(1800, 1000);
		processing.stroke(125);
		processing.strokeWeight(2);
		processing.noLoop();
	    // erase background
	    processing.background(0);
		processing.textSize(itemSize/2);
		
		var mydata = JSON.parse(data);

		var rectX, rectY, circleX, circleY, textX, textY, triangleX1, triangleX2, triangleX3, triangleY1, triangleY2, triangleY3, lineX1, lineY1, lineX2, lineY2;
		var PeopleTypeNumber = 0;
		var MaterialTypeNumber = 2;
		var ToolTypeNumber = 4;
		
		function countRectPosition(number, typeNumber) {      
				rectX = (textSize) * typeNumber;
				rectY = number * itemSize;
		    };
		function countCirclePosition(number, typeNumber) {      
			circleX = (textSize) * typeNumber + itemSize/2;
			circleY = number * itemSize + itemSize/2;
	    };
		function countTrianglePosition(number, typeNumber) {      
			triangleX1 = (textSize) * typeNumber;
			triangleY1 = number * itemSize; 
			triangleX2 = (textSize) * typeNumber + itemSize;
			triangleY2 = number * itemSize;
			triangleX3 = (textSize) * typeNumber + itemSize/2;
			triangleY3 = number * itemSize + itemSize*3/4;
	    };
		function countTextPosition(number, typeNumber) { 
			textX = itemSize + (textSize) * typeNumber;
			textY = (number+3/4) * itemSize;
	    };
		function countLinePosition(number, typeNumber, number2, typeNumber2) { 
			lineX1 = itemSize + (textSize) * typeNumber;
			lineY1 = (number+1/2) * itemSize;
			lineX2 = (textSize) * typeNumber2;
			lineY2 = (number2+1/2) * itemSize;
	    };
		
		for (var key in mydata){
			if (key == "Material"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata['TagInOriginalTaskCase']['Material'].length; position++){
						//alert(tag + "---- " + mydata['sameMaterial'][position]);
						if(tag == mydata['TagInOriginalTaskCase']['Material'][position]){
							processing.fill(102, 204, 0);	
							//alert("TEMP");
						}
					}
					countRectPosition(mydata[key][tag],MaterialTypeNumber-1);
					processing.rect(rectX, rectY, (itemSize*3/4), (itemSize*3/4));
					countTextPosition(mydata[key][tag],MaterialTypeNumber-1);
					processing.text(tag, textX,textY);
					countRectPosition(mydata[key][tag],MaterialTypeNumber+1);
					processing.rect(rectX, rectY, (itemSize*3/4), (itemSize*3/4));
					
					
					processing.fill(255);
				}
			}
			if (key == "Tool"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata['TagInOriginalTaskCase']['Tool'].length; position++){
						//alert(tag + "---- " + mydata['sameMaterial'][position]);
						if(tag == mydata['TagInOriginalTaskCase']['Tool'][position]){
							processing.fill(102, 204, 0);	
							//alert("TEMP");
						}
					}
					countTrianglePosition(mydata[key][tag],ToolTypeNumber);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					countTextPosition(mydata[key][tag],ToolTypeNumber);
					processing.text(tag, textX,textY);	
					countTrianglePosition(mydata[key][tag],ToolTypeNumber+1);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					
					
					
					processing.fill(255);
				}
			}
			if (key == "ToolLink"){
				processing.strokeWeight(4);
				processing.stroke(102, 204, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1-5, lineX2, lineY2-5);
					}			
				}
				processing.strokeWeight(2);
			}
			if (key == "ToolLink1"){
				processing.stroke(0, 102, 204);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+0.1, lineX2, lineY2+0.1);
					}			
				}
			}
			if (key == "ToolLink2"){
				processing.stroke(255, 0, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+5, lineX2, lineY2+5);
					}			
				}
			}
			if (key == "ToolLink3"){
				processing.stroke(255, 255, 0);
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber+1, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1+10, lineX2, lineY2+10);
					}			
				}
			}
		}	

	};
}



function TaskDetailView(processing){
	  // Override draw function, by default it will be called 60 times per second
	  processing.draw = function() {
	    // determine center and max clock arm length
		var itemSize = 40;
		var textSize = 300;
		processing.size(1000, 1000);
		processing.stroke(255);
		processing.noLoop();
	    // erase background
	    processing.background(0);
		processing.textSize(itemSize/2);
		
		var mydata = JSON.parse(data);

		var rectX, rectY, circleX, circleY, textX, textY, triangleX1, triangleX2, triangleX3, triangleY1, triangleY2, triangleY3, lineX1, lineY1, lineX2, lineY2;
		var PeopleTypeNumber = 0;
		var MaterialTypeNumber = 1;
		var ToolTypeNumber = 2;
		
		function countRectPosition(number, typeNumber) {      
				rectX = (itemSize/2 + textSize) * typeNumber;
				rectY = number * itemSize;
		    };
		function countCirclePosition(number, typeNumber) {      
			circleX = (itemSize/2 + textSize) * typeNumber + itemSize/2;
			circleY = number * itemSize + itemSize/2;
	    };
		function countTrianglePosition(number, typeNumber) {      
			triangleX1 = (itemSize/2 + textSize) * typeNumber;
			triangleY1 = number * itemSize; 
			triangleX2 = (itemSize/2 + textSize) * typeNumber + itemSize;
			triangleY2 = number * itemSize;
			triangleX3 = (itemSize/2 + textSize) * typeNumber + itemSize/2;
			triangleY3 = number * itemSize + itemSize*3/4;
	    };
		function countTextPosition(number, typeNumber) { 
			textX = itemSize + (itemSize/2 + textSize) * typeNumber;
			textY = (number+3/4) * itemSize;
	    };
		function countLinePosition(number, typeNumber, number2, typeNumber2) { 
			lineX1 = itemSize + (itemSize/2 + textSize) * typeNumber;
			lineY1 = (number+1/2) * itemSize;
			lineX2 = (itemSize/2 + textSize) * typeNumber2;
			lineY2 = (number2+1/2) * itemSize;
	    };
		
		for (var key in mydata){
			if (key == "People"){
				for (var tag in mydata[key]){
					countCirclePosition(mydata[key][tag],PeopleTypeNumber);
					processing.ellipse(circleX, circleY, (itemSize), (itemSize));
					countTextPosition(mydata[key][tag],PeopleTypeNumber);
					processing.text(tag, textX,textY);					
				}
			}
			if (key == "Material"){
				for (var tag in mydata[key]){
					countRectPosition(mydata[key][tag],MaterialTypeNumber);
					processing.rect(rectX, rectY, (itemSize*3/4), (itemSize*3/4));
					countTextPosition(mydata[key][tag],MaterialTypeNumber);
					//processing.text(tag, textX,textY);
				}
			}
			if (key == "Tool"){
				for (var tag in mydata[key]){
					countTrianglePosition(mydata[key][tag],ToolTypeNumber);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					countTextPosition(mydata[key][tag],ToolTypeNumber);
					processing.text(tag, textX,textY);				
				}
			}
			if (key == "PeopleLink"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["People"][tag], PeopleTypeNumber+1, mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber);
						processing.line(lineX1, lineY1, lineX2, lineY2);					
					}			
				}
			}
			if (key == "ToolLink"){
				for (var tag in mydata[key]){
					for (position = 0; position < mydata[key][tag].length; position++){
						countLinePosition(mydata["Material"][mydata[key][tag][position]] , MaterialTypeNumber, mydata["Tool"][tag], ToolTypeNumber);
						processing.line(lineX1, lineY1, lineX2, lineY2);					
					}			
				}
			}
			
		}
	  };
}

function AllTagItemView(processing){
	  // Override draw function, by default it will be called 60 times per second
	  processing.draw = function() {
	    // determine center and max clock arm length
		var itemSize = 40;
		var textSize = 300;
		processing.size(1000, 1000);
		processing.noLoop();
	    // erase background
	    processing.background(0);
		processing.textSize(itemSize/2);
		
		var mydata = JSON.parse(data);
		
		var rectX, rectY, circleX, circleY, textX, textY, triangleX1, triangleX2, triangleX3, triangleY1, triangleY2, triangleY3;
		
		function countRectPosition(number, typeNumber) {      
				rectX = (itemSize/2 + textSize) * typeNumber;
				rectY = number * itemSize;
		    };
		function countCirclePosition(number, typeNumber) {      
			circleX = (itemSize/2 + textSize) * typeNumber + itemSize/2;
			circleY = number * itemSize + itemSize/2;
	    };
		function countTrianglePosition(number, typeNumber) {      
			triangleX1 = (itemSize/2 + textSize) * typeNumber;
			triangleY1 = number * itemSize; 
			triangleX2 = (itemSize/2 + textSize) * typeNumber + itemSize;
			triangleY2 = number * itemSize;
			triangleX3 = (itemSize/2 + textSize) * typeNumber + itemSize/2;
			triangleY3 = number * itemSize + itemSize*3/4;
	    };
		function countTextPosition(number, typeNumber) { 
			textX = itemSize + (itemSize/2 + textSize) * typeNumber;
			textY = (number+3/4) * itemSize;
	    };
		
		for (var key in mydata){
			var i = 0;
			if (key == "People"){
				for (position = 0; position < mydata[key].length; position++){
					countCirclePosition(i,0);
					processing.ellipse(circleX, circleY, (itemSize), (itemSize));
					countTextPosition(i,0);
					processing.text(mydata[key][position], textX,textY);
					i = i + 1;
				}
			}
			i = 0;
			if (key == "Material"){
				for (position = 0; position < mydata[key].length; position++){
					countRectPosition(i,1);
					processing.rect(rectX, rectY, (itemSize), (itemSize));
					countTextPosition(i,1);
					processing.text(mydata[key][position], textX,textY);
					i = i + 1;
				}
			}
			i = 0;
			if (key == "Tool"){
				for (position = 0; position < mydata[key].length; position++){
					countTrianglePosition(i,2);
					processing.triangle(triangleX1, triangleY1, triangleX2, triangleY2,triangleX3, triangleY3);
					countTextPosition(i,2);
					processing.text(mydata[key][position], textX,textY);
					i = i + 1;
				}
			}
			
		}
	  };
}


