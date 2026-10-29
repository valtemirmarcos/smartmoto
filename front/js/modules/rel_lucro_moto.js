async function iniciarRelLucroMoto(filtros = {}){
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
    const response = await api.get(`/api/relatorios/lucro_moto${query}`);
    const lucros   = response.data.resultado || [];
    if ($('#relLucroMotoTable').length) {

        if ($.fn.DataTable.isDataTable('#relLucroMotoTable')) {
            $('#relLucroMotoTable').DataTable().destroy();
        }
    
        $('#relLucroMotoTable').DataTable({
            data: lucros,
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
                    data: 'valores_semanais',
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
            buttons: botoesExcelPdf("Lucro por moto"),
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const lucroTotalBruto = dados.reduce((s, i) => s + Number(i.valores_semanais || 0), 0);
                const lucroTotalLiquido = dados.reduce((s, i) => s + Number(i.liquido || 0), 0);

                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#lucroTotalBruto').text(fmt(lucroTotalBruto));
                $('#lucroTotalLiquido').text(fmt(lucroTotalLiquido));

            }
        });
    }
}
$(document).on('click','#modalBtFiltroRelLucroMoto',async function(){
    ModalManager.abrir("modalFiltroLucroMoto");
});
$(document).on('click','#modalBtFiltrarRelLucroMoto',async function(){
    const filtros = {
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };
    iniciarRelLucroMoto(filtros);
    ModalManager.fechar("modalFiltroLucroMoto");
});
