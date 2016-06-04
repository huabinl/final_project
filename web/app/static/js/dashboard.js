/*
 * COMP90055 Computing Project, Semester 1 2016
 * Author: Huabin Liu (ID. 658274)
 */

// configure for module loader
require.config({
    paths: {
        echarts: 'http://echarts.baidu.com/build/dist'
    }
});

// draw a qantitative analysis chart of tweets based on hour
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' // require the specific chart type
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('hourdata', function (data) {
            var myChart = ec.init(document.getElementById('hour1'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['tweet_melb']);
                road.push(d['tweet_road']);
                congestion.push(d['tweet_congestion']);
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['12:00AM','1:00AM','2:00AM', '3:00AM','4:00AM','5:00AM', '6:00AM', '7:00AM', '8:00AM', '9:00AM', '10:00AM', '11:00AM', '12:00PM', '1:00PM', '2:00PM', '3:00PM','4:00PM','5:00PM', '6:00PM', '7:00PM', '8:00PM', '9:00PM', '10:00PM', '11:00PM']
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:melb
                    },
                    {
                        name:'Road',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:road
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:congestion
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });

// draw a sentiment analysis chart of tweets based on hour
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' // require the specific chart type
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('hourdata', function (data) {
            var myChart = ec.init(document.getElementById('hour2'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['sentiment_melb'].toFixed(3));
                road.push(d['sentiment_road'].toFixed(3));
                congestion.push(d['sentiment_congestion'].toFixed(3));
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['12:00AM','1:00AM','2:00AM', '3:00AM','4:00AM','5:00AM', '6:00AM', '7:00AM', '8:00AM', '9:00AM', '10:00AM', '11:00AM', '12:00PM', '1:00PM', '2:00PM', '3:00PM','4:00PM','5:00PM', '6:00PM', '7:00PM', '8:00PM', '9:00PM', '10:00PM', '11:00PM']
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        data:melb,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
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
                        type:'line',
                        data:road,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        data:congestion,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });

// draw a qantitative analysis chart of tweets based on weekday
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' 
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('weekdaydata', function (data) {
            var myChart = ec.init(document.getElementById('weekday1'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['tweet_melb']);
                road.push(d['tweet_road']);
                congestion.push(d['tweet_congestion']);
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:melb
                    },
                    {
                        name:'Road',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:road
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:congestion
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });

// draw a sentiment analysis chart of tweets based on weekday
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' // require the specific chart type
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('weekdaydata', function (data) {
            var myChart = ec.init(document.getElementById('weekday2'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['sentiment_melb'].toFixed(3));
                road.push(d['sentiment_road'].toFixed(3));
                congestion.push(d['sentiment_congestion'].toFixed(3));
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        data:melb,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
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
                        type:'line',
                        data:road,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        data:congestion,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });

// draw a quantitative analysis chart of tweets based on period
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' 
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('perioddata', function (data) {
            var myChart = ec.init(document.getElementById('period1'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['tweet_melb']);
                road.push(d['tweet_road']);
                congestion.push(d['tweet_congestion']);
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['Off Peak', 'Morning Rush', 'Evening Rush']
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:melb
                    },
                    {
                        name:'Road',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:road
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        smooth:true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data:congestion
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });

// draw a sentiment analysis chart of tweets based on period
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar' // require the specific chart type
    ],
    function (ec) {
        // Initialize after dom ready
        $.getJSON('perioddata', function (data) {
            var myChart = ec.init(document.getElementById('period2'));
            var melb=[];
            var road=[];
            var congestion=[];
            data.forEach(function(d){
                melb.push(d['sentiment_melb'].toFixed(3));
                road.push(d['sentiment_road'].toFixed(3));
                congestion.push(d['sentiment_congestion'].toFixed(3));
            });
            option = {
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['Melbourne','Road','Congestion']
                },
                toolbox: {
                    show : true,
                    feature : {
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        boundaryGap : false,
                        data : ['Off Peak', 'Morning Rush', 'Evening Rush']
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                    }
                ],
                series : [
                    {
                        name:'Melbourne',
                        type:'line',
                        data:melb,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
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
                        type:'line',
                        data:road,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    },
                    {
                        name:'Congestion',
                        type:'line',
                        data:congestion,
                        markPoint : {
                            data : [
                                {type : 'max', name: 'max value'},
                                {type : 'min', name: 'min value'}
                            ]
                        },
                        markLine : {
                            data : [
                                {type : 'average', name : 'average'}
                            ]
                        }
                    }
                ]
            };
            // Load data into the ECharts instance 
            myChart.setOption(option); 
        });
    });