function iniciarDashboard() {

    // gráfico frota
    const frotaCanvas = document.getElementById('frotaChart');

    if (frotaCanvas) {

        new Chart(frotaCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Alugadas', 'Disponíveis'],
                datasets: [{
                    data: [30,70],
                    backgroundColor:['#FFD700','#28a745'],
                    hoverOffset:10
                }]
            },
            options:{
                plugins:{
                    legend:{position:'bottom'},
                    tooltip:{enabled:true},
                    datalabels:{
                        color:'#000',
                        font:{weight:'bold'},
                        formatter: v => v
                    }
                },
                cutout:'60%'
            },
            plugins:[ChartDataLabels]
        });

    }

    // gráfico semanais
    const semanaisCanvas = document.getElementById('semanaisChart');

    if (semanaisCanvas) {

        new Chart(semanaisCanvas, {
            type:'pie',
            data:{
                labels:['Em Dia','Atrasados'],
                datasets:[{
                    data:[80,20],
                    backgroundColor:['#28a745','#dc3545'],
                    hoverOffset:10
                }]
            },
            options:{
                plugins:{
                    legend:{position:'bottom'},
                    tooltip:{enabled:true},
                    datalabels:{
                        color:'#000',
                        font:{weight:'bold'},
                        formatter:v => v
                    }
                }
            },
            plugins:[ChartDataLabels]
        });

    }

    // tabela
    if ($('#frotaTable').length) {

        $('#frotaTable').DataTable({
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });

    }

}