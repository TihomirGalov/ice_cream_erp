$(document).ready(function () {
    represent_top_sales_chart()
});

function change_total_sales(element) {
    return represent_top_sales_chart(element.value)
}

function represent_top_sales_chart(period) {
    const endpoint = window.origin.concat("/api/profit/")
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    $.get({"url": endpoint, "data": {"period": period}, headers: {'X-CSRFToken': csrftoken}}, function (data) {
        const chart_id = document.getElementById('total-sales-chart');

        chart_id.innerHTML = "";

        var options = {
            series: [{
                name: "Оборот", data: data.totals
            }], chart: {
                height: 350, type: 'line', zoom: {
                    enabled: false
                }
            }, dataLabels: {
                enabled: false
            }, stroke: {
                curve: 'straight'
            }, grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            }, xaxis: {
                categories: data.dates,
            }
        };

        var chart = new ApexCharts(chart_id, options);
        chart.render();
    });
}