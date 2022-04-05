var endpoint = '/api/team_specific/'+league_id+'/'+display_name
var teamchart_endpoint = '/api/team_positionchart/'+league_id+'/'+display_name
var medianchart_endpoint = '/api/team_vs_median/'+league_id+'/'+display_name

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(response_data){
      console.log(response_data)
      $.each(response_data, function(index, item) {
        var row = "<tr>"
                + "<td>" + item.name + "</td>"
                + "<td>" + item.position + "</td>"
                + "<td>" + item.value + "</td>"
                + "<tr>";
        $('#tbody').append(row);
      })
    },
    error: function(error_data){
      console.log(error_data)
    }
  })

  $.ajax({
      method: "GET",
      url: teamchart_endpoint,
      success: function(response_data){
        var labels = [];
        var values = [];
        console.log(response_data)

        // sort response by team value
        response_data.sort(function(a, b) {
          return b.value - a.value;
        })

        response_data.forEach(function(entry) {
        labels.push(entry.position);
        values.push(entry.value);
      });

        // var colors = createColors(values)
        // console.log(colors)

        var chart_ctx = document.getElementById("myTeamChart").getContext("2d");

        var chart = new Chart(chart_ctx, {
          type: "pie",
          data: {
            labels: labels,
            datasets: [{
              label: 'Total Team Value',
              backgroundColor: ['rgba(255,60,60,0.6)','rgba(128,128,128,0.6)', 'rgba(255,165,0,0.6)', 'rgba(60,255,60,0.6)', 'rgba(60,60,255,0.6)'],
              borderColor: 'white',
              data: values,

            }]
          },
          options: {
            // indexAxis: 'y',
            responsive: true,
            // maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: 'Team Value by Position',
                font: {
                  weight: 'bold'
                },
              },
              datalabels: {
                display: true,
                formatter: (val, ctx) => {
                  return ctx.chart.data.labels[ctx.dataIndex];
                },
                color: '#fff',
                backgroundColor: '#404040',
                font: {
                  // weight: 'bold'
                },
                padding: {
                  top: 4,
                  right: 4,
                  left: 4,
                  bottom: 4
                }
              },
            }
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
      url: medianchart_endpoint,
      success: function(response_data){
        var labels = [];
        var values_median = [];
        var values_team = [];

        console.log(response_data)

        response_data.league_median.forEach(function(entry) {
        labels.push(entry.position);
        values_median.push(entry.value);
      });

        response_data.team_vals.forEach(function(entry) {
        values_team.push(entry.value);
      });

        // var colors = createColors(values)
        // console.log(colors)

        var chart_ctx = document.getElementById("medianRadar").getContext("2d");

        var chart = new Chart(chart_ctx, {
          type: "radar",
          data: {
            labels: labels,
            datasets: [
            {
                label: display_name,
                backgroundColor: 'rgba(60, 60, 255, 0.5)',
                borderColor: 'rgba(60, 60, 255, 0.5)',
                data: values_team,

              },
              {
                label: 'League Median',
                backgroundColor: 'rgba(255, 60, 60, 0.5)',
                borderColor: 'rgba(255, 60, 60, 0.5)',
                data: values_median,

              },
            ]
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Team Value vs League Median',
                font: {
                  weight: 'bold'
                },
              },
            },
            // indexAxis: 'y',
            responsive: true,
            // maintainAspectRatio: false,
          }
        });

      },
      error: function(error_data){
        console.log(error_data)
      }
  })
