async function iniciarDashboard() {

    const response = await api.get(`/api/relatorios/dashboard`);
    const dashboard   = response.data.resultado || [];
    console.log(dashboard.resumo_financeiro_frota);
    document.getElementById("bruto_semanal").textContent = formatarMoeda(dashboard.total_semanal);
    document.getElementById("bruto_mensal").textContent = formatarMoeda(dashboard.total_mensal);
    document.getElementById("multas_aberto").textContent = dashboard.multas_emAberto;

    // gráfico frota
    const frotaCanvas = document.getElementById('frotaChart');

    if (frotaCanvas) {
        let status_frota = dashboard.status_frota;
        const labels = status_frota.map(item => item.status);
        const dados = status_frota.map(item => item.quantidade);

        new Chart(frotaCanvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dados,
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
        let status_pgto_semanais = dashboard.status_pgto_semanais;
        const labels = status_pgto_semanais.map(item => item.status);
        const dados = status_pgto_semanais.map(item => item.quantidade);
        const cores = status_pgto_semanais.map(item => item.cor);
        new Chart(semanaisCanvas, {
            type:'pie',
            data:{
                labels:labels,
                datasets:[{
                    data:dados,
                    backgroundColor:cores,
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
            data: dashboard.resumo_financeiro_frota,
            columns: [
                {
                    data: 'placa',
                    defaultContent: '-'
                },
                {
                    data: 'totalSemanal',
                    render: function(data) {

                        return Number(data || 0).toLocaleString(
                            'pt-BR',
                            {
                                style: 'currency',
                                currency: 'BRL'
                            }
                        );
                    }
                },
                {
                    data: 'totalMensal',
                    render: function(data) {

                        return Number(data || 0).toLocaleString(
                            'pt-BR',
                            {
                                style: 'currency',
                                currency: 'BRL'
                            }
                        );
                    }
                },
                {
                    data: 'ultimoStatus',
                    defaultContent: '-'
                },
                {
                    data: 'statusFrota',
                    defaultContent: '-'
                },
            ],
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:100
        });

    }

}