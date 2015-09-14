$(function(){

  var chart = null

  $('#nav a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
    chart.update()
  })

  //table detail
  $.getJSON('/json/tablet.json',function(data){
    initTableData($('.tablet tbody'), data)
  })

  $.getJSON('/json/table6.json',function(data){
    initTableData($('.table6 tbody'), data)
  })

  $.getJSON('/json/table7.json',function(data){
    initTableData($('.table7 tbody'), data)
  })

  $.getJSON('/json/table8.json',function(data){
    initTableData($('.table8 tbody'), data)
  })


  //chart
  $.getJSON('/json/distribute.json',function(data){
    nv.addGraph(function() {
      chart = nv.models.lineChart()
        .options({
          transitionDuration: 300,
          useInteractiveGuideline: true
        })
      ;

      // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
      chart.xAxis
        .axisLabel("收益")
        .tickFormat(d3.format(',.0f'))
        .staggerLabels(true)
      ;

      chart.yAxis
        .axisLabel('人数')
        .tickFormat(function(d) {
          if (d == null) {
            return 'N/A';
          }
          return d3.format(',.0f')(d);
        })
      ;

      var chartData = [
        {
          area: true,
          values: data.reverse(),
          key: "总收益分布",
          color: "#337ab7",
          fillOpacity: .8
        }
      ]

      d3.select('#distribute_chart').append('svg')
        .datum(chartData)
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  })

  //tag cloud
  $.getJSON('/json/x678.json',function(data){
    initTagData($('#x678Tags ul'), data)

    $('#x678Canvas').tagcanvas({
      textColour: '#5B94C5',
      outlineColour: '#337AB7',
      reverse: true,
      depth: 0.8,
      maxSpeed: 0.05
    },'x678Tags')
  })

  $.getJSON('/json/x67t.json',function(data){
    initTagData($('#x67tTags ul'), data)
    $('#x67tCanvas').tagcanvas({
      textColour: '#5B94C5',
      outlineColour: '#337AB7',
      reverse: true,
      depth: 0.8,
      maxSpeed: 0.05
    },'x67tTags')
  })

  $.getJSON('/json/x78t.json',function(data){
    initTagData($('#x78tTags ul'), data)
    $('#x78tCanvas').tagcanvas({
      textColour: '#5B94C5',
      outlineColour: '#337AB7',
      reverse: true,
      depth: 0.8,
      maxSpeed: 0.05
    },'x78tTags')
  })

  $.getJSON('/json/weibo.json',function(data){
    initTableData($('.tableWeibo tbody'), data)
  })

  var initTagData = function($ul, data){
    var i = 0
    var html = ''
    for(; i < data.length; i++){
      html += '<li><a href="http://xueqiu.com/'+ data[i].uid +'" target="_blank">'+data[i].nickname+'</a></li>'
    }

    $ul.html(html)
  }

  var initTableData = function($tbody, data){
    var i = 0
    var html = ''
    for (; i < data.length; i++)
      html += '<tr><td>'+ data[i].nickname +'</td><td>'+ data[i].user_id +'</td><td>'+ float2(data[i].m) +'</td></tr>'
    $tbody.html(html)
  }

  var float2 = d3.format('.2f')
})
