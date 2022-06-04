$(document).ready(()=>{
    $.get("personality_male/", function(response){
        var $data = []
        var $labels = response.labels
        $.map(response.avg, function(avg, i){
            $data = [...$data, avg]
        })
        
        let PersonalityMaleChart = new Chart(PersonalityMale, {
            type:'line', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
            data:{
              labels:$labels,
              datasets:[{
                data:$data,
                backgroundColor:[
                  'rgba(66, 141, 239, 0.6)',
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
              maintainAspectRatio: false,
              responsive: true,
              legend:{
                display:false,
              },
              tooltips:{
                enabled:true
              }
            }
          });
    })
})