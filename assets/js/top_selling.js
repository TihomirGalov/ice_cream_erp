$(document).ready(function () {
    represent_top_selling()
});

function change_top_selling(element) {
    return represent_top_selling(element.value)
}

function represent_top_selling(period) {
    const endpoint = window.origin.concat("/api/top_selling/")
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.get({"url": endpoint, "data": {"period": period}, headers: {'X-CSRFToken': csrftoken}}, function (data) {
        let chart_id = document.getElementById('top-selling-chart');

        chart_id.innerHTML = "";

        var options = {
            series: [{
                name: "", data: data['amounts']
            }], chart: {
                type: 'bar', height: 170
            }, plotOptions: {
                bar: {
                    horizontal: false,
                }
            }, colors: ['#333f52'], dataLabels: {
                enabled: false,
            }, xaxis: {
                categories: data['ice_creams']
            },

        };
        var chart = new ApexCharts(chart_id, options);
        chart.render();

    });
}