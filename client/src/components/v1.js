Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
});

Qualtrics.SurveyEngine.addOnReady(function()
{					
    /*Place your JavaScript here to run when the page is fully displayed*/

    //read data
    var time_duration = '${e://Field/time_duration}'.split(',');
    var results =  '${e://Field/results}'.split(',');

    //Set the default values
    var window_size = 3 // how many recent submission yuo want to show, if you want to show 4, then the number here is 3
    var time_threshold = 20
    var recent_timeduration = []
    var recent_results = []
    var correct = "#71994b"
    var incorrect = "#b3293b"
    
     //get the recent timeturation and results from whole timeduration list and results list

    if(time_duration.length <= window_size)
    { 
        for(var i = 0; i < results.length-1; i++){
            recent_timeduration.push(time_duration[i])
        }   

        for(var i = 0; i < results.length; i++){
            recent_results.push(results[i])
        }
    }

    else{
        for(i = time_duration.length-window_size; i < time_duration.length; i++){
            recent_timeduration.push(time_duration[i])
        }

        for(i = results.length - window_size -1; i < results.length; i++){
            recent_results.push(results[i])
        }
    }

    // set the new interval, if the time duration is longer than time_threshold,then it's set to time_threshold
    var time_threshold = 20
    for(i = 0; i < recent_timeduration.length; i++){
        if(recent_timeduration[i] > time_threshold)
        recent_timeduration[i] = time_threshold
    }
 
    //set default values for drawing
    var margin = {"left": 10, "right": 10, "top":20, "down":20};
    var width = 800;
    var height = 400;
    var submission_width = 5;
    var framework_width = 350;
    var start_drawx = 60
    var long_reflection = 60
    var short_reflection = 20
    var first_row = 30
    var second_row = 250
    var third_row = 140
    var rect_height = 60

  
  //append svg
  var svg = d3.select('#test1').append('svg')
          .attr('width', width-margin.left-margin.right)
          .attr('height', height-margin.top-margin.down)
          .attr('transformation', 'translate(' + margin.left + ',' + margin.top + ')')

  
  // prepare data for drawing
  var framework_data = [
  {'x': 20, 'y': first_row, 'width': framework_width, 'height':60},
  {'x': 20, 'y': second_row, 'width': framework_width, 'height':60},
  {'x': 20, 'y': third_row, 'width': framework_width + 80, 'height':60},
  ];
    
  var good_data = [
      {'x': start_drawx, 'y': first_row, 'width': submission_width, 'height': 60, 'color': incorrect},
      {'x': start_drawx + long_reflection, 'y': first_row, 'width': submission_width, 'height': 60, 'color': incorrect},
      {'x': start_drawx + 2*long_reflection, 'y': first_row, 'width': submission_width, 'height': 60, 'color': incorrect},
      {'x': start_drawx + 3*long_reflection, 'y': first_row, 'width': submission_width, 'height': 60, 'color': correct},
  ];

  var bad_data = [
    {'x': start_drawx, 'y': third_row, 'width': submission_width, 'height': 60, 'color': incorrect},
    {'x': start_drawx + short_reflection, 'y': third_row, 'width': submission_width, 'height': 60, 'color': incorrect},
    {'x': start_drawx + 2*short_reflection, 'y': third_row, 'width': submission_width, 'height': 60, 'color': incorrect},
    {'x': start_drawx + 3*short_reflection, 'y': third_row, 'width': submission_width, 'height': 60, 'color': correct},
];

  var your_data = [{'x': start_drawx, 'y': second_row, 'width': submission_width, 'height': 60, 'results': recent_results[0]},]

  var offset = 0
  for(var i = 1; i < recent_results.length; i++)
  {
      var temp = {}
      offset += recent_timeduration[i-1]/time_threshold * long_reflection
      temp['x'] = start_drawx + offset
      temp['y'] = second_row
      temp['width'] = submission_width
      temp['height'] = 60
      temp['results'] = recent_results[i]
      your_data.push(temp)
  }

  var reflect_data = [
    {'x': start_drawx+submission_width, 'y': third_row, 'width': short_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+short_reflection+submission_width, 'y': third_row, 'width': short_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+2*short_reflection+submission_width, 'y': third_row, 'width': short_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+3*short_reflection+submission_width, 'y': third_row, 'width': 0, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+submission_width, 'y': first_row, 'width': long_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+long_reflection+submission_width, 'y': first_row, 'width': long_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+2*long_reflection+submission_width, 'y': first_row, 'width': long_reflection-submission_width, 'height': 60, 'color': '#fee08b'},
    {'x': start_drawx+3*long_reflection+submission_width + 35, 'y': first_row, 'width': 90, 'height': 60, 'color': '#3182bd'},
    {'x': start_drawx + 3*short_reflection + 35, 'y': third_row, 'width': 295, 'height': 60, 'color': '#3182bd'},
    
];

  var legend_data = [
    {'x': 600, 'y': 30, 'width': 5, 'height': 60, 'color': incorrect},
    {'x': 600, 'y': 105, 'width': 5, 'height': 60, 'color': correct},
    {'x': 600, 'y': 180, 'width': 30, 'height': 60, 'color': '#fee08b'},
    {'x': 600, 'y': 255, 'width': 30, 'height': 60, 'color': '#3182bd'},
  ];

  var text = [{'x': 0, 'y': first_row - 5, 'text': "Good students: more reflection time + less review time:"},
                {'x': 0, 'y': second_row - 5, 'text': "Your recent submission records:"},
                {'x': 0, 'y': third_row - 5, 'text': "Struggling students: less reflection time + more review time:"}]

  var legend_text = [{'x': 610, 'y': 60, 'text': "incorrect submission"},
                {'x': 610, 'y': 130, 'text': "correct submission"},
                {'x': 640, 'y': 200, 'text': "reflection time"},
                {'x': 640, 'y': 270, 'text': "time needed"},
                {'x': 640, 'y': 290, 'text': "for exam review"}]

  var dot_text = [{'x': 20, 'y': first_row + rect_height/2, 'text': "..."},
                {'x': 20, 'y': second_row + rect_height/2, 'text': "..."},
                {'x': 20, 'y': third_row + rect_height/2, 'text': "..."},
                {'x': start_drawx + 3*long_reflection + submission_width, 'y': first_row + rect_height/2, 'text': "..."},
                {'x': start_drawx + 3*short_reflection + 3, 'y': third_row + rect_height/2, 'text': "..."}]

  var latest_text = [{'x': start_drawx + 3*long_reflection, 'y': first_row + rect_height+12, 'text': "latest submission", "size": "12px", "color": "black"},
                {'x': your_data[your_data.length-1].x, 'y': second_row + rect_height+12, 'text': "latest submission","size": "15px", "color": "red"},
                {'x': start_drawx + 3*short_reflection, 'y': third_row + rect_height+12, 'text': "latest submission","size": "12px", "color": "black"},
                {'x': framework_width + 20, 'y': first_row + rect_height+12, 'text': "exam","size": "12px", "color": "black"},
                {'x': framework_width + 20, 'y': second_row + rect_height+12, 'text': "exam","size": "12px", "color": "black"},
                {'x': framework_width + 100, 'y': third_row + rect_height+12, 'text': "exam","size": "12px", "color": "black"}]
              
  var threshold_text = [ {'x': start_drawx + submission_width + 3, 'y': first_row + rect_height/2, 'text': ">=20(s)"},
                {'x': start_drawx + long_reflection + submission_width + 3, 'y': first_row + rect_height/2, 'text': ">=20(s)"},
                {'x': start_drawx + 2*long_reflection + submission_width + 3, 'y': first_row + rect_height/2, 'text': ">=20(s)"}]


  // draw a grey background to hightlight the your submission records(middle row)
//   svg.append("rect")
//   .attr('x', 0)
//   .attr('y', second_row - 25)
//   .attr('width', framework_width + 55)
//   .attr('height', rect_height + 40)
//   .attr('fill', "grey")
//   .attr('opacity', "0.3")

  //draw all the things

  var text = svg.selectAll('text')
                .data(text)
                .enter()
                .append('text');

  var text_label = text.attr("x", function(d) { return d.x; })
                  .attr("y", function(d) { return d.y; })
                  .text( function (d) { return d.text; })
                  .attr("font-family", "sans-serif")
                  .attr("font-size", "18px")
                  .attr("fill", "black");

  var rect_good = svg.selectAll('.rect_good')
                      .data(good_data)
                      .enter()
                      .append('rect')
  
  var good_attributes = rect_good.attr('x', function(d){return d.x;})
                .attr('y', function(d){return d.y;})
                .attr('width', function(d){return d.width;})
                .attr('height', function(d){return d.height;})
                .attr('fill', function(d){return d.color;})

  var rect_bad = svg.selectAll('.rect_bad')
                .data(bad_data)
                .enter()
                .append('rect')

  var bad_attributes = rect_bad.attr('x', function(d){return d.x;})
            .attr('y', function(d){return d.y;})
            .attr('width', function(d){return d.width;})
            .attr('height', function(d){return d.height;})
            .attr('fill', function(d){return d.color;})

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

  //highlight the current submission
  svg.append("rect")
     .attr('x', your_data[your_data.length-1].x)
     .attr('y', your_data[your_data.length-1].y)
     .attr('width', your_data[your_data.length-1].width)
     .attr('height', your_data[your_data.length-1].height)
     .attr('fill', "none")
     .attr('stroke', "yellow")

  
  // var x = d3.scaleLinear().domain([0, 100])
  //                         .range([0, 400])
  
  // svg.append("g")
  //    .attr("transform", "translate(0," + second_row + ")")
  //    .call(d3.axisBottom(x).ticks());

  var rect_reflect = svg.selectAll('.rect_reflect')
             .data(reflect_data)
             .enter()
             .append('rect')

  var reflect_attributes = rect_reflect.attr('x', function(d){return d.x;})
            .attr('y', function(d){return d.y;})
            .attr('width', function(d){return d.width;})
            .attr('height', function(d){return d.height;})
            .attr('fill', function(d){return d.color;})
            .attr('opacity', 0.7)

  var rect_legend = svg.selectAll('.rect_legend')
            .data(legend_data)
            .enter()
            .append('rect')

  var reflect_attributes = rect_legend.attr('x', function(d){return d.x;})
            .attr('y', function(d){return d.y;})
            .attr('width', function(d){return d.width;})
            .attr('height', function(d){return d.height;})
            .attr('fill', function(d){return d.color;})


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

  var dot_text = svg.selectAll('.dot_text')
              .data(dot_text)
              .enter()
              .append('text');

  var dot_text_label = dot_text.attr("x", function(d) { return d.x; })
                .attr("y", function(d) { return d.y; })
                .text( function (d) { return d.text; })
                .attr("font-family", "sans-serif")
                .attr("font-size", "30px")
                .attr("fill", "black");

  var latest_text = svg.selectAll('.latest_text')
                .data(latest_text)
                .enter()
                .append('text')
  
  var latest_text_label = latest_text.attr("x", function(d) { return d.x; })
                  .attr("y", function(d) { return d.y; })
                  .text( function (d) { return d.text; })
                  .attr("font-family", "sans-serif")
                  .attr("font-size", function(d){
                      return d.size
                  })
                  .attr("fill", function(d){
                      return d.color
                  });

  var threshold_text = svg.selectAll('.threshold_text')
                .data(threshold_text)
                .enter()
                .append('text');
  
  var threshold_text_label = threshold_text.attr("x", function(d) { return d.x; })
                  .attr("y", function(d) { return d.y; })
                  .text( function (d) { return d.text; })
                  .attr("font-family", "sans-serif")
                  .attr("font-size", "12px")
                  .attr("fill", "black");

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
	});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	/*Place your JavaScript here to run when the page is unloaded*/

});