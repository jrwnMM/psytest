let barChart = document.getElementById('barChart').getContext('2d');
// Global Options
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontColor = '#777';

let riasecBarChart = new Chart(barChart, {
    type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
    labels:['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional'],
    datasets:[{
        label:'Result',
        data:[
        {{obj.realistic|floatformat:1}},
        {{obj.investigative|floatformat:1}},
        {{obj.artistic|floatformat:1}},
        {{obj.social|floatformat:1}},
        {{obj.enterprising|floatformat:1}},
        {{obj.conventional|floatformat:1}}
        ],
        backgroundColor:[
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(255, 99, 132, 0.6)'
        ],
        borderWidth:1,
        borderColor:'#777',
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
    }]
    },
    options:{
    title:{
        display:true,
        text:'Bar Chart',
        fontSize:25
    },
    legend:{
        display:false,
        position:'right',
        labels:{
        fontColor:'#000'
        }
    },
    layout:{
        padding:{
        left:50,
        right:0,
        bottom:0,
        top:0
        }
    },
    tooltips:{
        enabled:true
    }
    }
});
let riasecPieChart = new Chart(pieChart, {
    type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data:{
    labels:['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional'],
    datasets:[{
        label:'Result',
        data:[
        {{obj.realistic|floatformat:1}},
        {{obj.investigative|floatformat:1}},
        {{obj.artistic|floatformat:1}},
        {{obj.social|floatformat:1}},
        {{obj.enterprising|floatformat:1}},
        {{obj.conventional|floatformat:1}}
        ],
        backgroundColor:[
        'rgba(255, 99, 132, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(255, 99, 132, 0.6)'
        ],
        borderWidth:1,
        borderColor:'#777',
        hoverBorderWidth:3,
        hoverBorderColor:'#000'
    }]
    },
    options:{
    title:{
        display:true,
        text:'Pie Chart',
        fontSize:25
    },
    legend:{
        display:true,
        position:'right',
        labels:{
        fontColor:'#000'
        }
    },
    layout:{
        padding:{
        left:50,
        right:0,
        bottom:0,
        top:0
        }
    },
    tooltips:{
        enabled:true
    }
    }
});