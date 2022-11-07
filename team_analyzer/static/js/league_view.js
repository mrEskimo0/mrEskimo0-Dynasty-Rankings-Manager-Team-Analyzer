
var endpoint = '/api/league_totalval/' + league_id
var total_players_endpoint = '/api/playertotal/' + league_id
var picks_endpoint = '/api/position_view_pick/' + league_id
var qbs_endpoint = '/api/position_view_qb/' + league_id
var wrs_endpoint = '/api/position_view_wr/' + league_id
var rbs_endpoint = '/api/position_view_rb/' + league_id
var tes_endpoint = '/api/position_view_te/' + league_id

function createColors(data){

  const green = 'rgba(60,255,60,'
  const red = 'rgba(255,60,60,'

  const sum = data.reduce((partialSum, a) => partialSum + a, 0);
  const avg = sum / data.length;
  var stdv = Math.sqrt(data.map(x => Math.pow(x - avg, 2)).reduce((a, b) => a + b) / data.length);
  var colors = [];
  for (let i of data){
    if (i > avg) {
      // green
      over = i - avg
      num = 0.3 + (over/stdv)
      // round num to nearest .1
      alpha = Math.round(num * 10) / 10

      if (alpha > 1){
        alpha = 1
      }

      color = green + alpha + ')'
      console.log(color)
      colors.push(color)

    }

    else {

      over = (i - avg) * -1
      num = 0.3 + (over/stdv)
      alpha = Math.round(num * 10) / 10

      if (alpha > 1){
        alpha = 1
      }

      color = red + alpha + ')'
      console.log(color)
      colors.push(color)
    }
  }
  return colors
}

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)
      console.log(colors)

      var chart_ctx = document.getElementById("myChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            borderColor: 'rgb(255, 99, 132)',
            data: values,

          }]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Total Team Value',
              font: {
                weight: 'bold'
              },
            },
            legend: {
              display: false
            }
          },
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
        }
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

$.ajax({
    method: "GET",
    url: total_players_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)
      console.log(colors)

      var chart_ctx = document.getElementById("myPlayerChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Player Value',
            backgroundColor: colors,
            borderColor: 'rgb(255, 99, 132)',
            data: values,

          }]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Total Player Value',
              font: {
                weight: 'bold'
              },
            },
            legend: {
              display: false
            }
          },
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
        }
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

// picks chart
$.ajax({
    method: "GET",
    url: picks_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)

      var chart_ctx = document.getElementById("myPicksChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "polarArea",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            data: values,
          }]
        },
        options: {
          plugins: {
            datalabels: {
              display: true,
              position: 'outside',
              anchor: 'end',
              padding: 6,
              formatter: (val, ctx) => {
                return ctx.chart.data.labels[ctx.dataIndex];
              },
            },
            legend: {
              labels: {

                pointStyle: 'circle',
                usePointStyle: true,
              }
            }
          },
          responsive: true,
          maintainAspectRatio: false,
        },
        plugins: [ChartDataLabels],
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

$.ajax({
    method: "GET",
    url: qbs_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)

      var chart_ctx = document.getElementById("myQBsChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "polarArea",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            data: values,
          }]
        },
        options: {
          plugins: {
            datalabels: {
              display: true,
              position: 'outside',
              anchor: 'end',
              padding: 6,
              formatter: (val, ctx) => {
                return ctx.chart.data.labels[ctx.dataIndex];
              },
            },
            legend: {
              labels: {

                pointStyle: 'circle',
                usePointStyle: true,
              }
            }
          },
          responsive: true,
          maintainAspectRatio: false,
        },
        plugins: [ChartDataLabels],
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

$.ajax({
    method: "GET",
    url: wrs_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)

      var chart_ctx = document.getElementById("myWRsChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "polarArea",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            data: values,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            datalabels: {
              display: true,
              position: 'outside',
              anchor: 'end',
              padding: 6,
              formatter: (val, ctx) => {
                return ctx.chart.data.labels[ctx.dataIndex];
              },
            },
            legend: {
              labels: {

                pointStyle: 'circle',
                usePointStyle: true,
              }
            }
          },
        },
        plugins: [ChartDataLabels],
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

$.ajax({
    method: "GET",
    url: rbs_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)

      var chart_ctx = document.getElementById("myRBsChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "polarArea",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            data: values,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            datalabels: {
              display: true,
              position: 'outside',
              anchor: 'end',
              padding: 6,
              formatter: (val, ctx) => {
                return ctx.chart.data.labels[ctx.dataIndex];
              },
            },
            legend: {
              labels: {

                pointStyle: 'circle',
                usePointStyle: true,
              }
            }
          },
        },
        plugins: [ChartDataLabels],
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})

$.ajax({
    method: "GET",
    url: tes_endpoint,
    success: function(response_data){
      var labels = [];
      var values = [];
      console.log(response_data)

      // sort response by team value
      response_data.sort(function(a, b) {
        return b.value - a.value;
      })

      response_data.forEach(function(entry) {
      labels.push(entry.display_name);
      values.push(entry.value);
    });

      var colors = createColors(values)

      var chart_ctx = document.getElementById("myTEsChart").getContext("2d");

      var chart = new Chart(chart_ctx, {
        type: "polarArea",
        data: {
          labels: labels,
          datasets: [{
            label: 'Total Team Value',
            backgroundColor: colors,
            data: values,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            datalabels: {
              display: true,
              position: 'outside',
              anchor: 'end',
              padding: 6,
              formatter: (val, ctx) => {
                return ctx.chart.data.labels[ctx.dataIndex];
              },
            },
            legend: {
              labels: {

                pointStyle: 'circle',
                usePointStyle: true,
              }
            }
          },
        },
        plugins: [ChartDataLabels],
      });

    },
    error: function(error_data){
      console.log(error_data)
    }
})
