async function iniciarRelCusto(filtros = {}){
    const params = new URLSearchParams();
    if (filtros.dataInicio || filtros.dataFim) {
    
        if (filtros.dataInicio) {
            params.append("dataInicio", filtros.dataInicio);
        }
    
        if (filtros.dataFim) {
            params.append("dataFim", filtros.dataFim);
        }
    
    } else {
        // Caso contrário, usa mês e ano atuais
        params.append("dataInicio", primeiroDiaMesAtual());
        params.append("dataFim", ultimoDiaMesAtual());
    }
    console.log(primeiroDiaMesAtual(), ultimoDiaMesAtual());
    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/relatorios/custos${query}`);
    const custos   = response.data.resultado || [];
    if ($('#relCustoTable').length) {

        if ($.fn.DataTable.isDataTable('#relCustoTable')) {
            $('#relCustoTable').DataTable().destroy();
        }
    
        $('#relCustoTable').DataTable({
            data: custos,
            columns: [
                {
                    data: 'nome',
                    defaultContent: '-'
                },
                {
                    data: 'periodo',
                    defaultContent: '-'
                },
                {
                    data: 'manutencao',
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
                    data: 'royaties',
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
                    data: 'seguro',
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
                    data: 'rastreador',
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
                    data: 'total',
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
            ],
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:20,
            dom: 'Bfrtip',
            buttons: botoesExcelPdf("Custos totais"),
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalManutencao = dados.reduce((s, i) => s + Number(i.manutencao || 0), 0);
                const totalRoyaties = dados.reduce((s, i) => s + Number(i.royaties || 0), 0);
                const totalSeguro = dados.reduce((s, i) => s + Number(i.seguro || 0), 0);
                const totalRastreador = dados.reduce((s, i) => s + Number(i.rastreador || 0), 0);
                const totalGeral = dados.reduce((s, i) => s + Number(i.total || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#totalManutencao').text(fmt(totalManutencao));
                $('#totalRoyaties').text(fmt(totalRoyaties));
                $('#totalSeguro').text(fmt(totalSeguro));
                $('#totalRastreador').text(fmt(totalRastreador));
                $('#totalGeral').text(fmt(totalGeral));
            }
        });
    }
}
$(document).on('click','#modalBtFiltroRelCusto',async function(){
    ModalManager.abrir("modalFiltroCusto");
});
$(document).on('click','#modalBtFiltrarRelCusto',async function(){
    const filtros = {
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };
    iniciarRelCusto(filtros);
    ModalManager.fechar("modalFiltroCusto");
});
