/*
 * COMP90055 Computing Project, Semester 1 2016
 * Author: Huabin Liu (ID. 658274)
 */

var melb_location = {lat: -37.814107, lng: 144.963280};
var pointArray1 = new google.maps.MVCArray();
var pointArray2 = new google.maps.MVCArray();
buildMap('heatmap1', pointArray1);
buildMap('heatmap2', pointArray2);

// initialize heap map
function buildMap(element_id, pointArray) {
    function initMap() {
        var map = new google.maps.Map(document.getElementById(element_id), {
            zoom: 13,
            center: melb_location,
            mapTypeId: google.maps.MapTypeId.HYBRID
        });
        var heatmap = new google.maps.visualization.HeatmapLayer({
            data: pointArray,
            map: map
        });
    }
    google.maps.event.addDomListener(window, 'load', initMap);
}

// once hitting submit button
$("#form").submit(function(e){
    e.preventDefault();
    if ($('#weekday option:selected').val() === '0') {
        alert("please pick a weekday!");
    } else if ($('#hour option:selected').val() === '0') {
        alert("please pick an hour!");
    } else {
        var weekday = $('#weekday option:selected').val();
        var c_hour = parseInt($('#hour option:selected').val());
        var p_hour = c_hour-1;

        // request related data
        $.getJSON('mapdata/'+weekday, function (data) {
            var bottom5 = data['bottom_5'][c_hour];
            var top5 = data['top_5'][c_hour];

            // configure for module loader
            require.config({
                paths: {
                    echarts: 'http://echarts.baidu.com/build/dist'
                }
            });
            // draw a bar chart for suburbs with maximum growth/reduction of road tweets
            require(
                [
                    'echarts',
                    'echarts/chart/bar'
                ],
                function (ec) {
                    var myChart = ec.init(document.getElementById('top')); 
                    var labelRight = {normal: {label : {position: 'right'}}};

                    regionName = [];
                    regionTweet = []
                    for (var key in bottom5) {
                        regionName.push(key);
                        regionTweet.push({value:bottom5[key], itemStyle:labelRight});
                    }
                    for (var key in top5) {
                        regionName.push(key);
                        regionTweet.push(top5[key]);
                    }
                    option = {
                        tooltip : {
                            trigger: 'axis',
                            axisPointer : {            
                                type : 'shadow'
                            }
                        },
                        toolbox: {
                            show : true,
                            feature : {
                                dataView : {show: true, readOnly: false},
                                restore : {show: true},
                                saveAsImage : {show: true}
                            }
                        },
                        grid: {
                            y: 80,
                            y2: 30
                        },
                        xAxis : [
                            {
                                type : 'value',
                                position: 'top',
                                splitLine: {lineStyle:{type:'dashed'}},
                            }
                        ],
                        yAxis : [
                            {
                                type : 'category',
                                axisLine: {show: false},
                                axisLabel: {show: false},
                                axisTick: {show: false},
                                splitLine: {show: false},
                                data : regionName
                            }
                        ],
                        series : [
                            {
                                name:'number of tweets',
                                type:'bar',
                                stack: 'total',
                                itemStyle : { normal: {
                                    color: 'orange',
                                    borderRadius: 5,
                                    label : {
                                        show: true,
                                        position: 'left',
                                        formatter: '{b}'
                                    }
                                }},
                                data : regionTweet
                            }
                        ]
                    };
                    myChart.setOption(option);
                }
            );
            
            // update heat maps
            update(p_hour, pointArray1);
            update(c_hour, pointArray2);
            function update(hour, pointArray) {
                pointArray.clear();
                var hour_tweet = data['hour_tweet'][hour];
                for (i = 0; i < hour_tweet.length; i++) {
                    pointArray.push(new google.maps.LatLng(hour_tweet[i]['latitude'], hour_tweet[i]['longitude']));
                }
            }
        });
    }
});