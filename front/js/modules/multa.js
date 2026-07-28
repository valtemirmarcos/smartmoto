async function iniciarMultas(filtros = {}) {

    
    // Monta os params ignorando valores vazios
    const params = new URLSearchParams();

    if (filtros.status)     params.append("status",     filtros.status);
    if (filtros.franqueado) params.append("franqueado", filtros.franqueado);
    if (filtros.frota)      params.append("frota",      filtros.frota);
    if (filtros.dataInicio) params.append("dataInicio", filtros.dataInicio);
    if (filtros.dataFim)    params.append("dataFim",    filtros.dataFim);
    console.log(filtros);
    const query    = params.toString() ? `?${params.toString()}` : "";
    console.log(`/api/multas/listar${query}`);
    const response = await api.get(`/api/multas/listar${query}`);
    const multa   = response.data.resultado || [];

    console.log(multa);
    if ($('#tabelaMultas').length) {

        if ($.fn.DataTable.isDataTable('#tabelaMultas')) {
            $('#tabelaMultas').DataTable().destroy();
        }
    
        $('#tabelaMultas').DataTable({
            data: multa,
            columns: [

                {
                    data: 'codigo',
                    defaultContent: '-'
                },
                {
                    data: 'locatario_nome',
                    defaultContent: '-',
                    visible: false
                },
                {
                    data: 'placa',
                    defaultContent: '-', 
                    visible: false
                },
                {
                    data: 'data_infracao',
                    defaultContent: '-',
                    render: function(data) {

                        if (!data) return '-';
                    
                        const [ano, mes, dia] = data.split('-');
                    
                        return `${dia}/${mes}/${ano}`;
                    
                    }
                },
                {
                    data: 'valor_multa',
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
                    data: 'valor_pago',
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
                    data: 'pontos',
                    render: function(data) {

                        let classe = 'bg-secondary';
                        
                        if (data >= 3) {
                            classe = 'bg-success';
                        }
                        if (data >= 6) {
                            classe = 'bg-warning';
                        }
                        if (data >= 7) {
                            classe = 'bg-danger';
                        }

                        return `
                            <span class="badge ${classe} text-white d-inline-block text-center">
                                ${data}
                            </span>
                        `;
                    }
                },
                {
                    data: 'status',
                    render: function(data, type, row) {
                
                        let classe = 'bg-secondary';
                        if (row.status_id == 1) {
                            classe = 'bg-secondary';
                        }
                        if (row.status_id == 2) {
                            classe = 'bg-warning';
                        }
                        if (row.status_id == 3) {
                            classe = 'bg-success';
                        }
                
                        return `
                            <span class="badge-status ${classe} text-white text-center">
                                ${data}
                            </span>
                        `;
                    }
                },
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-center',

                    render: function(data, type, row) {
                        return `
                            <div class="d-flex gap-2 justify-content-center">
                                <button 
                                    class="btn btn-sm btn-warning rounded-3 btnEditarMulta" data-id="${row.id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button 
                                    class="btn btn-sm btn-danger rounded-3 btnExcluirMulta" data-id="${row.id}">
                                    <i class="bi bi-trash-fill"></i>
                                </button>
                            </div>
                        `;
                    }
                }
            ],
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });
    
    }

}
async function prepararModalMulta() {
    document.querySelector("#modalFormMultas").reset();

    await carregarAutocompletePlaca("id", "inputMultaPlaca", "listaMultaPlacas");
    await carregarPagamentosModalCusto("selectMultasPagamentos", 2);
    await carregarStatusModalMulta("selectMultasStatus", 2);
    await carregarFranqueados("selectModalMultaFranqueado", false);
    mascaraMoeda(document.getElementById("inputMultasValorMulta"));
    mascaraMoeda(document.getElementById("inputMultasValorPago"));
    mascaraMoeda(document.getElementById("inputMultasValorRecebido"));
}
$(document).on('click','#modalFiltrarMulta',async function(){
    ModalManager.abrir("modalFiltroMulta");
    carregarFranqueados(null, true);
    carregarAutocompletePlaca("id");
    carregarStatusModalMulta("filtroMultaStatus",1);
});
$(document).on('click','#btModalFiltrar',async function(){
    const filtros = {
        franqueado: document.getElementById("selectModalFiltroMultaFranqueado")?.value     || null,
        frota:      document.getElementById("inputPlaca")?.value
                        ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                        : null,
        status:     document.getElementById("filtroMultaStatus")?.value     || null,
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };

    iniciarMultas(filtros);
    ModalManager.fechar("modalFiltroMulta");
});
$(document).on('click','#modalNovaMulta',async function(){
    ModalManager.abrir("modalMulta",{acao:"novo"});
    await prepararModalMulta();
    
});
$(document).on('click','.btnEditarMulta',async function(){
    await prepararModalMulta();
    const idMulta = this.dataset.id;
    
    const response  = await api.get(`/api/multas/listar?id=${idMulta}`);
    const multa = response.data.resultado[0];
    console.log("idMulta:",multa);

    document.getElementById("inputMultaPlaca").value = multa.placasf || "";
    document.getElementById("inputMultasCodigo").value = multa.codigo || "";
    document.getElementById("inputMultasPontuacao").value = multa.pontos || "";
    document.getElementById("inputMultasDataMulta").value = multa.data_infracao || "";
    document.getElementById("inputMultasDataNotificacao").value = multa.data_notificacao || "";
    document.getElementById("inputMultasDataIndicacao").value = multa.data_indicacao || "";
    document.getElementById("inputMultasDataPagamento").value = multa.data_pagamento || "";
    document.getElementById("inputMultasValorMulta").value = formatarMoeda(multa.valor_multa) || "";
    document.getElementById("inputMultasValorPago").value = formatarMoeda(multa.valor_pago) || "";
    document.getElementById("inputMultasValorRecebido").value = formatarMoeda(multa.valor_recebido) || "";
    document.getElementById("selectMultasPagamentos").value = multa.pagamento_id || "";
    document.getElementById("selectMultasStatus").value = multa.status_id || "";
    document.getElementById("areaMultasObs").value = multa.obs || "";

    ModalManager.abrir("modalMulta",{
        acao: "editar",
        multaId: idMulta,
        frotaId: multa.frota_id
    });

    
});
$(document).on('click','.btnExcluirMulta',async function(){
    const idMulta = this.dataset.id;
    ModalManager.abrir("modalExcluir");
    $('#btExcluir')
    .off('click')
    .on('click', async function () {
        try {
            await api.get(`/api/multas/ativaDesativa/${idMulta}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarMultas();
            Swal.fire({
                icon: 'success',
                title: 'Multa excluida com sucesso',
                text: 'esses dados são recuperaveis!',
                timer: 2000,
                showConfirmButton: false
            });
    
        } catch (err) {
            console.error(err);
            Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a multa.' });
        }
    });
});
$(document).on('click','#btMultasSalvar',async function(){
    const dados = ModalManager.getDados("modalMulta");
    let frotaId = document.getElementById("inputMultaPlaca").dataset.frotaId;
    if(dados.acao=="editar"){
        frotaId = dados.frotaId;
    }
    const response  = await api.get(`/api/locatarios/listar?placa=${frotaId}&status=1`);
    const locatario = response.data.resultado[0];

    const franquia_franquiador_locatario_id = locatario.franquia_franquiador_locatario_id;
    const payload = {
        franquia_franquiador_locatario_id:franquia_franquiador_locatario_id,
        frota_id: frotaId || null,
        codigo: document.getElementById("inputMultasCodigo").value || null,
        pontos: document.getElementById("inputMultasPontuacao").value  || 0,
        data_infracao: document.getElementById("inputMultasDataMulta").value  || null,
        data_notificacao: document.getElementById("inputMultasDataNotificacao").value || null,
        data_indicacao: document.getElementById("inputMultasDataIndicacao").value || null,
        data_pagamento: document.getElementById("inputMultasDataPagamento").value || null,
        valor_multa: limparMoeda(document.getElementById("inputMultasValorMulta").value),
        valor_pago: limparMoeda(document.getElementById("inputMultasValorPago").value),
        valor_recebido: limparMoeda(document.getElementById("inputMultasValorRecebido").value),
        pagamento_id: document.getElementById("selectMultasPagamentos").value  || null,
        status_id: document.getElementById("selectMultasStatus").value  || null,
        obs: document.getElementById("areaMultasObs").value || null
    }
    if (
        !payload.codigo ||
        !payload.frota_id || 
        !payload.data_infracao || 
        !payload.valor_multa ||
        !payload.pontos ||
        !payload.status_id
    ) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Preencha todos os campos obrigatórios.',
            customClass: {
                popup: 'swal-modal-top'
            }
        });
        return;
    }
    try{    

        if (dados.acao == 'novo'){
            console.log(JSON.stringify(payload));
            await api.post("/api/multas/create", payload);
        }else{
            console.log("alterar");
            const multaId = dados.multaId
            await api.put(`/api/multas/update/${multaId}`, payload);
        }

        ModalManager.fechar("modalMulta");  
        iniciarMultas();
        const placa = document.getElementById("inputMultaPlaca").value; 
        Swal.fire({
            icon: 'success',
            title: 'Multa salvas',
            text: 'Multa gravada para a moto:'+placa,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar a multa.' });
    }

      
});