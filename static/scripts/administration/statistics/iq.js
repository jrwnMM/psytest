$(document).ready(() => {
  $.get("iq_stats/", function (response) {
    var $data = response.avg;
    var $labels = response.labels;

    let IQChart = new Chart(iqChart, {
      type: "line", // bar, horizontalBar, pie, line, doughnut, radar, polarArea
      data: {
        labels: $labels,
        datasets: [
          {
            data: $data,
            backgroundColor: [
              "rgba(66, 141, 239, 0.6)",
              "rgba(54, 162, 235, 0.6)",
              "rgba(255, 206, 86, 0.6)",
              "rgba(75, 192, 192, 0.6)",
              "rgba(153, 102, 255, 0.6)",
              "rgba(255, 159, 64, 0.6)",
              "rgba(255, 99, 132, 0.6)",
            ],
            borderWidth: 1,
            borderColor: "#777",
            hoverBorderWidth: 3,
            hoverBorderColor: "#000",
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        legend: {
          display: false,
        },
        tooltips: {
          enabled: true,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      },
    });
  });
});
