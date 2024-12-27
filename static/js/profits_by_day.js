function change_date() {
    let date = document.getElementById('calendar').value;
    represent_profits_for_day(date);
}

function represent_profits_for_day(date){
    const endpoint = window.origin.concat("/api/day_profits/");
    const csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    console.log(date);
    $.get({"url": endpoint, "data": {"date": date}, headers: {'X-CSRFToken': csrftoken}}, function (data) {
        let chart_id = document.getElementById('profits-by-day');

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