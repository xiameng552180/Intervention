 Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
});

Qualtrics.SurveyEngine.addOnReady(function()
{	
    /*Place your JavaScript here to run when the page is fully displayed*/
    // var time_duration = '${e://Field/time_duration}'.split(',');

    //get the submission results and prerequisites_score lists from the server
    var results =  '${e://Field/results}'.split(',');
    var prerequisites_score = '${e://Field/prerequisites_score}'.split(',');

    //set default calues
	var margin = {"left": 10, "right": 10, "top":20, "down":20};
	var width = 800;
    var height = 400;
    var challenge_width = 180;
    var rect_height = 80
    var first_row = 50
    var second_row = 200
    var start_drawx = 50
    var mastered = "#71994b"
    var need_review = "#b3293b"
    var current = '#fee08b'
    var color = [need_review, need_review]

    //calculate the color of each prerequisite challenge
    for(var i = 0; i < 2; i++)
    {
        if(prerequisites_score[i] >= 0.5)
        color[i] = mastered
        else
        color[i] = need_review
    }

    //append the svg
    var svg = d3.select('#test3').append('svg')
    .attr('width', width-margin.left-margin.right)
    .attr('height', height-margin.top-margin.down)
    .attr('transformation', 'translate(' + margin.left + ',' + margin.top + ')')

    //week 12 prepare second multiple-choice question data
    // var url_list = ["https://pcrs.teach.cs.toronto.edu/csc108-2019-05/content/challenges/40/1", 
    //                 "https://pcrs.teach.cs.toronto.edu/csc108-2019-05/content/challenges/41/1",
    //                 "https://pcrs.teach.cs.toronto.edu/csc108-2019-01-9901-dev/content/challenges/166/1#multiple_choice-540"]

    // var url_list = ["https://pcrs.teach.cs.toronto.edu/csc108-2019-01-9901-dev/content/challenges/168/1",
    //                 "https://pcrs.teach.cs.toronto.edu/csc108-2019-01-9901-dev/content/challenges/22/1", 
    //                 "https://pcrs.teach.cs.toronto.edu/csc108-2019-01-9901-dev/content/challenges/36/1"]

    var url_list = ["https://pcrs.teach.cs.toronto.edu/csc108-2019-05/content/challenges/168/1",
                    "https://pcrs.teach.cs.toronto.edu/csc108-2019-05/content/challenges/22/1", 
                    "https://pcrs.teach.cs.toronto.edu/csc108-2019-05/content/challenges/36/1"]

    var challenge_data = [
        {'x': start_drawx, 'y': first_row, 'width': challenge_width, 'height':rect_height, "color": color[0], "url": url_list[1]},
        {'x': start_drawx + 250, 'y': first_row, 'width': challenge_width, 'height':rect_height, "color": color[1], "url": url_list[2]},
        {'x': start_drawx + 125, 'y': second_row, 'width': challenge_width, 'height':rect_height, "color": current, "url": ""},    
    ];
        
    var rect_challenge = svg.selectAll('.rect_challenge')
        .data(challenge_data)
        .enter()
        .append('rect');

    var challenge_attributes = rect_challenge.attr('x', function(d){return d.x;})
        .attr('y', function(d){return d.y;})
        .attr('width', function(d){return d.width;})
        .attr('height', function(d){return d.height;})
        .attr('fill', function(d){return d.color})
        .attr('opacity', 0.7)
        .attr('stroke', 'black')
        .on("click", function(d) {
            if(d.url != "")
            window.open(d.url);})
        .on("mouseover", function(d) {
            if(d.url!="")
            { d3.select(this).style("cursor", "pointer");
                d3.select(this).attr("opacity", 0.9);}
            })
        .on("mouseout", function(d) {
            d3.select(this).attr("opacity", 0.7);
            d3.select(this).style("cursor", "default");})


    //week 12 prepare second multiple-choice question data
    // var challenge_text = [{'x': start_drawx + 15, 'y': first_row + 40, 'text': "Passing Functions", "font_size": "18px", "color": "black", "url": url_list[1]},
    //     {'x': start_drawx + 15, 'y': first_row + 60, 'text': "as Arguments", "font_size": "18px", "color": "black", "url": url_list[1]},
    //     {'x': start_drawx + 256, 'y': first_row + 40, 'text': "Assigning Parameters", "font_size": "18px", "color": "black", "url": url_list[2]},
    //     {'x': start_drawx + 256, 'y': first_row + 60, 'text': "Default Values", "font_size": "18px", "color": "black", "url": url_list[2]},
    //     {'x': start_drawx + 140, 'y': second_row + 35, 'text': "Week 12", "font_size": "18px", "color": "black", "url": ""},
    //     {'x': start_drawx + 140, 'y': second_row + 53, 'text': "prepare exercises", "font_size": "18px", "color": "black", "url": ""},
    //     {'x': start_drawx + 400, 'y': second_row + rect_height - 30, 'text': "A\xa0\xa0\xa0\xa0\xa0\xa0 B: ", "font_size": "12px", "color": "black", "url":""},
    //     {'x': start_drawx + 455, 'y': second_row + rect_height - 30, 'text': "A is the prerequisite of B", "font_size": "12px", "color": "black", "url": ""}]

    //week 12 perform second multiple-choice question data
    var challenge_text = [{'x': start_drawx + 30, 'y': first_row + 35, 'text': "Creating Your", "font_size": "18px", "color": "black", "url": url_list[1]},
        {'x': start_drawx + 30, 'y': first_row + 60, 'text': "Own Types", "font_size": "18px", "color": "black", "url": url_list[1]},
        {'x': start_drawx + 291, 'y': first_row + 35, 'text': "Creating a", "font_size": "18px", "color": "black", "url": url_list[2]},
        {'x': start_drawx + 291, 'y': first_row + 60, 'text': "New Type", "font_size": "18px", "color": "black", "url": url_list[2]},
        {'x': start_drawx + 145, 'y': second_row + 35, 'text': "Calling Methods", "font_size": "18px", "color": "black", "url": ""},
        {'x': start_drawx + 145, 'y': second_row + 60, 'text': "inside Methods", "font_size": "18px", "color": "black", "url": ""},
        {'x': start_drawx + 400, 'y': second_row + rect_height - 30, 'text': "A\xa0\xa0\xa0\xa0\xa0\xa0\xa0 B: ", "font_size": "12px", "color": "black", "url":""},
        {'x': start_drawx + 455, 'y': second_row + rect_height - 30, 'text': "A is the prerequisite of B", "font_size": "12px", "color": "black", "url": ""}]

    var text = svg.selectAll('.text')
        .data(challenge_text)
        .enter()
        .append('text');

    var text_label = text.attr("x", function(d) { return d.x; })
       .attr("y", function(d) { return d.y; })
       .text( function (d) { return d.text; })
       .attr("font-family", "sans-serif")
       .attr("font-size", function(d){return d.font_size})
       .attr("fill", function(d){return d.color})
       .on('click', function (d){
        if(d.url != "")
        window.open(d.url);})
        .on("mouseover", function(d) {
            if(d.url!="")
            {
            d3.select(this).style("cursor", "pointer");
            }
        })
        .on("mouseout", function(d) {
            d3.select(this).style("cursor", "default");
        })


    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 0 12 12")
        .attr("refX", 6)
        .attr("refY", 6)
        .attr("markerWidth", 12)
        .attr("markerHeight", 12)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M2,2 L10,6 L2,10 L6,6 L2,2")
        .style("fill", 'black')


    svg.append("line")
            .attr('x1', start_drawx + challenge_width/2)
            .attr('y1', first_row + rect_height)
            .attr('x2', start_drawx + 125 + challenge_width/2- 2)
            .attr('y2', second_row - 2)
            .style("stroke", "black")
            .attr("marker-end", "url(#arrow)");
      
    svg.append("line")
            .attr('x1', start_drawx + 250 + challenge_width/2)
            .attr('y1', first_row + rect_height)
            .attr('x2', start_drawx + 125 + challenge_width/2 + 2)
            .attr('y2', second_row - 2)
            .style("stroke", "black")
            .attr("marker-end", "url(#arrow)");

    svg.append("line")
            .attr('x1', start_drawx + 410)
            .attr('y1', second_row + rect_height - 35)
            .attr('x2',  start_drawx + 430)
            .attr('y2', second_row + rect_height - 35)
            .style("stroke", "black")
            .attr("marker-end", "url(#arrow)");
 

    var legend_text = [{'x': 505, 'y': 275, 'text': "Mastered"},
            {'x': 505, 'y': 295, 'text': "Need to review"},
            {'x': 505, 'y': 315, 'text': "Currrent module"}]

    var legend_text = svg.selectAll('.legend_text')
            .data(legend_text)
            .enter()
            .append('text');

    var legend_text_label = legend_text.attr("x", function(d) { return d.x; })
              .attr("y", function(d) { return d.y; })
              .text( function (d) { return d.text; })
              .attr("font-family", "sans-serif")
              .attr("font-size", "12px")
              .attr("fill", "black")

    var legend_data = [
                {'x': 450, 'y': 260, 'width': 50, 'height': 20, 'color': mastered},
                {'x': 450, 'y': 280, 'width': 50, 'height': 20, 'color': need_review},
                {'x': 450, 'y': 300, 'width': 50, 'height': 20, 'color': current},
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