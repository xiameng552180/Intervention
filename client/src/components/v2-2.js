Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
});

Qualtrics.SurveyEngine.addOnReady(function()
{   
    /*Place your JavaScript here to run when the page is fully displayed*/
    // get the submission results list
    var results =  '${e://Field/results}'.split(',');


    //set default values
    var correct = "#71994b"
    var incorrect = "#b3293b"  
	var margin = {"left": 10, "right": 10, "top":20, "down":20};
	var width = 800;
    var height = 400;
    var submission_width = 20;
    var framework_width = 400;
    var rect_height = 60
    var first_row = 50
    var second_row = 130
    var third_row = 230
    var start_drawx = 100
    var mean_number = 2
    // var pass_rate = [0.0, 0.55, 0.88, 0.96, 0.98, 0.99, 0.99, 0.99, 1.0]
    var pass_rate = [0.0, 0.55, 0.88, 0.97, 0.98, 0.99, 0.99, 0.99, 1.0]
    var circle_r = 30
    var beat_number = 0

   //calculate how many percentage students you are over
   for(var i = 0; i < results.length; i++){
       if(results[i] > 0.99 && i < pass_rate.length)
       {
           beat_number = parseInt((1-(pass_rate[i])) * 100)
           break;
       }
   }
   
    //prepare the data to draw
    var framework_data = [
		{'x': start_drawx, 'y': first_row, 'width': framework_width, 'height':rect_height * (1+parseInt((results.length-1)/20))},
    ];
    
    var your_data = []
    
    for(var i = 0; i < results.length; i++)
    {
        var temp = {}
        temp['x'] = submission_width*(i%20) + start_drawx
        temp['y'] = first_row  + 60  * parseInt(i/20)
        temp['width'] = submission_width
        temp['height'] = rect_height
        temp['results'] = results[i]
        your_data.push(temp)
    }

//append the svg
    var svg = d3.select('#test2').append('svg')
            .attr('width', width-margin.left-margin.right)
            .attr('height', height-margin.top-margin.down)
            .attr('transformation', 'translate(' + margin.left + ',' + margin.top + ')')

            
    var rect_framework = svg.selectAll('.rect_framework')
        .data(framework_data)
        .enter()
        .append('rect');

    var framework_attributes = rect_framework.attr('x', function(d){return d.x;})
        .attr('y', function(d){return d.y;})
        .attr('width', function(d){return d.width;})
        .attr('height', function(d){return d.height;})
        .attr('fill', 'none')
        .attr('stroke', 'black')

    var rect_you = svg.selectAll('.rect_you')
        .data(your_data)
        .enter()
        .append('rect')

    var you_attributes = rect_you.attr('x', function(d){return d.x;})
        .attr('y', function(d){return d.y;})
        .attr('width', function(d){return d.width;})
        .attr('height', function(d){return d.height;})
        .attr('fill', function(d){if(d.results >=0.99) return correct;
            else return incorrect})
        .attr("stroke", "black")
        .attr('opacity', 0.7)


    var circle = svg.append("circle")
                    .attr("cx", start_drawx + 10)
                    .attr("cy", rect_height * (2+parseInt((results.length-1)/20)) + 50)
                    .attr("r", circle_r)
                    .attr("fill", '#fee08b')
                    .attr("opacity", 0.5)


    var text_data  = [{'x':  start_drawx + submission_width* parseInt((results.length)%21), 'y': rect_height * (1+ parseInt((results.length-1)/20))+ 65, 'text': "You tried: " + results.length + " times", "font_size": "15px", "color": "black"},
    {'x': 0,'y': first_row + 0.25 * rect_height, 'text': "Submission", "font_size": "15px", "color": "black"},
    {'x': 0,'y': first_row + 0.5 * rect_height, 'text': "sequence", "font_size": "15px", "color": "black"},
    {'x': 0,'y': rect_height * (2+parseInt((results.length-1)/20)) + 35, 'text': "Historical", "font_size": "15px", "color": "black"},
    {'x': 0,'y': rect_height * (2+parseInt((results.length-1)/20)) + 50, 'text': "first-time", "font_size": "15px", "color": "black"},
    {'x': 0,'y': rect_height * (2+parseInt((results.length-1)/20)) + 65, 'text': "passrate", "font_size": "15px", "color": "black"},
    {'x': start_drawx + 2*circle_r + 50,'y': rect_height * (2+parseInt((results.length-1)/20)) + 65, 'text': "You beat" + '\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0' + "students", "font_size": "15px", "color": "black"},
    {'x': start_drawx + 2*circle_r + 120,'y': rect_height * (2+parseInt((results.length-1)/20)) + 65, 'text': "" + beat_number + "\%", "font_size": "20px", "color": "green"},
    {'x': start_drawx + mean_number*submission_width, 'y': 35, 'text': "Mean attempts: " + mean_number, "font_size": "15px", "color": "black"},
    {'x': start_drawx - 6,'y': rect_height * (2+parseInt((results.length-1)/20)) + 55, 'text': "" + pass_rate[1], "font_size": "18px", "color": "black"},]

    var text = svg.selectAll('.text')
                    .data(text_data)
                    .enter()
                    .append('text');
        
    var text_label = text.attr("x", function(d) { return d.x; })
                    .attr("y", function(d) { return d.y; })
                    .text( function (d) { return d.text; })
                    .attr("font-family", "sans-serif")
                    .attr("font-size", function(d){return d.font_size})
                    .attr("fill", function(d){return d.color});

    var line_data = [{'x': start_drawx + mean_number*submission_width -1, "y": first_row - 15, "width": 2, "height": rect_height + 15}]


    var median_line = svg.selectAll('.median_line')
        .data(line_data)
        .enter()
        .append('rect')

    var line_attributes = median_line.attr('x', function(d){return d.x;})
    .attr('y', function(d){return d.y;})
    .attr('width', function(d){return d.width;})
    .attr('height', function(d){return d.height;})
    .attr('fill', "black")

    var legend_text = [{'x': 475, 'y': rect_height * (1+ parseInt((results.length-1)/20))+ 110, 'text': "correct"},
                {'x': 475, 'y': rect_height * (1+ parseInt((results.length-1)/20))+ 125, 'text': "incorrect"}]

    var legend_text = svg.selectAll('.legend_text')
            .data(legend_text)
            .enter()
            .append('text');

    var legend_text_label = legend_text.attr("x", function(d) { return d.x; })
              .attr("y", function(d) { return d.y; })
              .text( function (d) { return d.text; })
              .attr("font-family", "sans-serif")
              .attr("font-size", "12px")
              .attr("fill", "black");

    var legend_data = [
                {'x': 450, 'y': rect_height * (1+ parseInt((results.length-1)/20))+ 100, 'width': 15, 'height': 15, 'color': correct},
                {'x': 450, 'y': rect_height * (1+ parseInt((results.length-1)/20))+ 115, 'width': 15, 'height': 15, 'color': incorrect},
              ];

    var rect_legend = svg.selectAll('.rect_legend')
              .data(legend_data)
              .enter()
              .append('rect')
 
    var legend_attributes = rect_legend.attr('x', function(d){return d.x;})
              .attr('y', function(d){return d.y;})
              .attr('width', function(d){return d.width;})
              .attr('height', function(d){return d.height;})
              .attr('fill', function(d){return d.color;})
              .attr('opacity', 0.7)

});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	/*Place your JavaScript here to run when the page is unloaded*/

});