async function iniciarRelLucro(filtros = {}){
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
    const lucros   = response.data.resultado || [];
    if ($('#relLucroTable').length) {

        if ($.fn.DataTable.isDataTable('#relLucroTable')) {
            $('#relLucroTable').DataTable().destroy();
        }
    
        $('#relLucroTable').DataTable({
            data: lucros,
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
                    data: 'bruto',
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
                    data: 'liquido',
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
            buttons: botoesExcelPdf("Lucros totais"),
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalBruto = dados.reduce((s, i) => s + Number(i.bruto || 0), 0);
                const totalLiquido = dados.reduce((s, i) => s + Number(i.liquido || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#totalBruto').text(fmt(totalBruto));
                $('#totalLiquido').text(fmt(totalLiquido));

            }
        });
    }
}
$(document).on('click','#modalBtFiltroRelLucro',async function(){
    ModalManager.abrir("modalFiltroLucro");
});
$(document).on('click','#modalBtFiltrarRelLucro',async function(){
    const filtros = {
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };
    iniciarRelLucro(filtros);
    ModalManager.fechar("modalFiltroLucro");
});
