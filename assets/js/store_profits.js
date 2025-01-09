$(document).ready(function () {
    represent_store_profits()
});


function represent_store_profits(period) {
    const endpoint = window.origin.concat("/api/store_profits/")
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.get({"url": endpoint, "data": {"period": period}, headers: {'X-CSRFToken': csrftoken}}, function (data) {
        let chart_id = document.getElementById('store-profits-chart');

        chart_id.innerHTML = "";

        var options = {
            series: [{
                name: "", data: data['totals']
            }], chart: {
                type: 'bar', height: 170
            }, plotOptions: {
                bar: {
                    horizontal: false,
                }
            }, colors: ['#333f52'], dataLabels: {
                enabled: false,
            }, xaxis: {
                categories: data['stores']
            },

        };
        var chart = new ApexCharts(chart_id, options);
        chart.render();
    });
}