/*
 * COMP90055 Computing Project, Semester 1 2016
 * Author: Huabin Liu (ID. 658274)
 */

$(document).ready(function() {
    // initialize drop down menu of date
    $.getJSON('alldate', function (data) {
        var list = document.getElementById("dateSelectDropdown"); 
        for (var i = 0; i < data.length; i++){                
            var opt = data[i];
            var li = document.createElement("li");
            var link = document.createElement("a");             
            var text = document.createTextNode(opt);
            link.appendChild(text);
            link.href = "#";
            li.appendChild(link);
            list.appendChild(li);
        }
    });
});
var map;
var markers = [];
var image1 = '../static/img/pink_flag.png';
var image2 = '../static/img/green_flag.png';

// initialize road map
function initMap() {
    var melb_location = {lat: -37.814107, lng: 144.963280};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: melb_location,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
}
google.maps.event.addDomListener(window, 'load', initMap);

// update the map by ading markers and info windows
$(document.body).on('click', '.dropdown-menu li a', function (e) {
    $.getJSON('date/'+$(this).text(), function (data) {
        deleteMarker();
        var tweets = data['tweets'];
        for (i = 0; i < tweets.length; i++) {
            var myloc = {lat: tweets[i]['latitude'], lng: tweets[i]['longitude']};
            var infoWindow = new google.maps.InfoWindow({
                content: 'User:' + tweets[i]['user'] + '</br>' + 'Tweet:' + tweets[i]['text'] + '</br>' + 'Time:' + tweets[i]['time'] + '</br>' + 'Road:' + tweets[i]['road'] + '</br>' + 'Sentiment:' + tweets[i]['sentiment'].toFixed(3).toString() 
            });
            var marker;
            if (tweets[i]['congestion']) {
                marker = new google.maps.Marker({
                    position: myloc,
                    map: map,
                    icon: image1,
                    infowindow: infoWindow
                });
            } else {
                marker = new google.maps.Marker({
                    position: myloc,
                    map: map,
                    icon: image2,
                    infowindow: infoWindow
                });
            }

            markers.push(marker);
            google.maps.event.addListener(marker, 'click', function() {
                this.infowindow.open(map, this);
            });
        }

        // configure for module loader
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });
        // draw a scatter chart for sentiment distribution of road tweets
        require(
            [
                'echarts',
                'echarts/chart/scatter'
            ],
            function (ec) {
                // Initialize after dom ready
                var myChart = ec.init(document.getElementById('sentiment'));
                var congestion_data = [];
                var road_data = [];
                for (i = 0; i < tweets.length; i++) {
                    if (tweets[i]['congestion']) {
                        congestion_data.push([tweets[i]['timeline'], tweets[i]['sentiment'].toFixed(3)]);
                    } else {
                        road_data.push([tweets[i]['timeline'], tweets[i]['sentiment'].toFixed(3)]);
                    }
                }
                
                option = {
                    tooltip : {
                        trigger: 'axis',
                        showDelay : 0,
                        formatter : function (params) {
                            if (params.value.length > 1) {
                                return params.seriesName + ' :<br/>' + params.value[0] + ' ' + params.value[1].toFixed(3);
                            }
                            else {
                                return params.seriesName + ' :<br/>' + params.name + ' : ' + params.value;
                            }
                        },  
                        axisPointer:{
                            show: true,
                            type : 'cross',
                            lineStyle: {
                                type : 'dashed',
                                width : 1
                            }
                        }
                    },
                    legend: {
                        data:['Congestion','Road']
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            dataView : {show: true, readOnly: false},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    xAxis : [
                        {
                            type : 'value',
                            scale : true
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            scale : true
                        }
                    ],
                    series : [
                        {
                            name:'Congestion',
                            type:'scatter',
                            data: congestion_data,
                            markPoint : {
                                data : [
                                    {type : 'max', name: 'max'},
                                    {type : 'min', name: 'min'}
                                ]
                            },
                            markLine : {
                                data : [
                                    {type : 'average', name: 'average'}
                                ]
                            }
                        },
                        {
                            name:'Road',
                            type:'scatter',
                            data: road_data,
                            markPoint : {
                                data : [
                                    {type : 'max', name: 'max'},
                                    {type : 'min', name: 'min'}
                                ]
                            },
                            markLine : {
                                data : [
                                    {type : 'average', name: 'average'}
                                ]
                            }
                        }
                    ]
                };
                myChart.setOption(option); 
            }
        );
        // draw a bar chart for busiest roads
        require(
            [
                'echarts',
                'echarts/chart/bar'
            ],
            function (ec) {
                // Initialize after dom ready
                var myChart = ec.init(document.getElementById('road'));
                var topRoad = data['top_road'];
                var roadName = [];
                var roadTweet = [];
                for (var key in topRoad) {
                    roadName.push(key);
                    roadTweet.push(topRoad[key]);
                }

                option = {
                    tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['Road Tweets']
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            dataView : {show: true, readOnly: false},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    xAxis : [
                        {
                            type : 'category',
                            data : roadName
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : [
                        {
                            name : 'Road Tweets',
                            type : 'bar',
                            data : roadTweet,
                            markPoint : {
                                data : [
                                    {type : 'max', name: 'max'}
                                ]
                            }
                        }
                    ]
                };
        
                // Load data into the ECharts instance 
                myChart.setOption(option); 
            }
        );
        // remove all markers from the map
        function deleteMarker() {
            for (i = 0; i < markers.length; i++){
                markers[i].setMap(null);
            }
            markers = [];
        }
    });
});
