async function iniciarRelCustoMoto(filtros = {}){
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
    const response = await api.get(`/api/relatorios/custo_moto${query}`);
    const custos   = response.data.resultado || [];
    if ($('#relCustoMotoTable').length) {

        if ($.fn.DataTable.isDataTable('#relCustoMotoTable')) {
            $('#relCustoMotoTable').DataTable().destroy();
        }
    
        $('#relCustoMotoTable').DataTable({
            data: custos,
            columns: [
                {
                    data: 'franqueado',
                    defaultContent: '-'
                },
                {
                    data: 'periodo',
                    defaultContent: '-'
                },
                {
                    data: 'placa',
                    defaultContent: '-'
                },
                {
                    data: 'royalties',
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
                    data: 'valor_oficina',
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
            // BOTÕES
            dom: 'Bfrtip',
            buttons: botoesExcelPdf("Custo por moto"),
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalRoyalties = dados.reduce((s, i) => s + Number(i.royalties || 0), 0);
                const totalManutencao = dados.reduce((s, i) => s + Number(i.valor_oficina || 0), 0);
                const totalSeguro = dados.reduce((s, i) => s + Number(i.seguro || 0), 0);
                const totalRastreador = dados.reduce((s, i) => s + Number(i.rastreador || 0), 0);
                const totalGeral = dados.reduce((s, i) => s + Number(i.total || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#totalRoyalties').text(fmt(totalRoyalties));
                $('#totalManutencao').text(fmt(totalManutencao));
                $('#totalSeguro').text(fmt(totalSeguro));
                $('#totalRastreador').text(fmt(totalRastreador));
                $('#totalGeral').text(fmt(totalGeral));
            }
        });
    }
}
$(document).on('click','#modalBtFiltroRelCustoMoto',async function(){
    ModalManager.abrir("modalFiltroCustoMoto");
});
$(document).on('click','#modalBtFiltrarRelCustoMoto',async function(){
    const filtros = {
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };
    iniciarRelCustoMoto(filtros);
    ModalManager.fechar("modalFiltroCustoMoto");
});
