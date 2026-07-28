async function iniciarLocatarioMultas(locatario_id) {

    console.log("locatario_id:", locatario_id);

    const response = await api.get(`/api/multas/listar?locatario=${locatario_id}`);
    const locatario   = response.data.resultado || [];

    console.log(locatario);
    if ($('#tabelaLocatarioMultas').length) {

        if ($.fn.DataTable.isDataTable('#tabelaLocatarioMultas')) {
            $('#tabelaLocatarioMultas').DataTable().destroy();
        }
    
        $('#tabelaLocatarioMultas').DataTable({
            data: locatario,
            columns: [

                {
                    data: 'codigo',
                    defaultContent: '-'
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
                                    class="btn btn-sm btn-warning rounded-3 btnEditarLocatarioMulta" data-id="${row.id}" data-locatarioid="${row.locatario_id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button 
                                    class="btn btn-sm btn-danger rounded-3 btnExcluirLocatarioMulta" data-id="${row.id}" data-locatarioid="${row.locatario_id}">
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
async function carregarStatusModalMulta(id,tipo) {
    // tipo 1 para filtro e 2 para formulario
    const select = document.getElementById(id);
    if (!select) return;

    try {

        const response = await api.get("/api/filtros/multas/status");
        const status   = response.data.resultado || [];
        console.log(status);
        if(tipo == 1){
            select.innerHTML = `<option value="" >Todos</option>`;
        }else{
            select.innerHTML = `<option value="" selected disabled>Selecione o status</option>`;
        }
        

        status.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.id;
            option.textContent = s.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
async function carregarPagamentosModalCusto(id, tipo) {

    const select = document.getElementById(id);

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/pagamentos");
        const pagamentos   = response.data.resultado;
        if(tipo == 1){
            select.innerHTML = `<option value="" >Todos</option>`;
        }else{
            select.innerHTML = `<option value="" selected disabled>Selecione o pagamento</option>`;
        }
        

        pagamentos.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.id;
            option.textContent = s.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
function limparModalLocatarioMulta() {

    document.getElementById("inputLocatarioMultasCodigo").value = "";
    document.getElementById("inputLocatarioMultasDataMulta").value = "";
    document.getElementById("inputLocatarioMultasDataNotificacao").value = "";
    document.getElementById("inputLocatarioMultasDataPagamento").value = "";
    document.getElementById("inputLocatarioMultasValorMulta").value = "";
    document.getElementById("inputLocatarioMultasValorPago").value = "";
    document.getElementById("inputLocatarioMultasValorRecebido").value = "";
    document.getElementById("inputLocatarioMultasPontuacao").value = 0;
    document.getElementById("selectLocatarioMultasStatus").selectedIndex = 0;
    document.getElementById("selectLocatarioMultasPagamentos").selectedIndex = 0;
    document.getElementById("areaLocatarioMultasObs").value = "";

}
$(document).on('click','.btnInserirNovaMulta',async function(){
    limparModalLocatarioMulta();
    const locatarioId = document.getElementById("btnAbaLocatarioMultas").dataset.locatarioId;
    const response  = await api.get(`/api/locatarios/listar?id=${locatarioId}`);
    const locatario = response.data.resultado[0];
    const frotaId = locatario.frota_id;
    const franquia_franquiador_locatario_id = locatario.franquia_franquiador_locatario_id;
    document.getElementById("inputLocatarioMultasPlaca").value = locatario.placa;
    ModalManager.abrir('modalLocatarioMulta',{
        acao:"novo",
        locatarioId: locatarioId,
        frotaId: frotaId,
        franquia_franquiador_locatario_id: franquia_franquiador_locatario_id
    });
    
});
$(document).on('click','.btnEditarLocatarioMulta',async function(){
    const idMulta = this.dataset.id;
    const locatarioId = this.dataset.locatarioid;
    const response  = await api.get(`/api/multas/listar?id=${idMulta}`);
    const locatarioMultas = response.data.resultado[0];
    const frotaId = locatarioMultas.frota_id;
    const franquia_franquiador_locatario_id = locatarioMultas.franquia_franquiador_locatario_id;

    document.getElementById("inputLocatarioMultasPlaca").value = locatarioMultas.placa || "";
    document.getElementById("inputLocatarioMultasCodigo").value = locatarioMultas.codigo || "";
    document.getElementById("inputLocatarioMultasDataMulta").value = locatarioMultas.data_infracao || "";
    document.getElementById("inputLocatarioMultasDataNotificacao").value = locatarioMultas.data_notificacao || "";
    document.getElementById("inputLocatarioMultasDataPagamento").value = locatarioMultas.data_pagamento || "";
    document.getElementById("inputLocatarioMultasValorMulta").value = formatarReal(locatarioMultas.valor_multa) || "";
    document.getElementById("inputLocatarioMultasValorPago").value = formatarReal(locatarioMultas.valor_pago) || "";
    document.getElementById("inputLocatarioMultasValorRecebido").value = formatarReal(locatarioMultas.valor_recebido) || "";
    document.getElementById("inputLocatarioMultasPontuacao").value = locatarioMultas.pontos || "0";
    document.getElementById("selectLocatarioMultasStatus").selectedIndex = locatarioMultas.status_id || "";
    document.getElementById("selectLocatarioMultasPagamentos").selectedIndex = locatarioMultas.pagamento_id || "";
    document.getElementById("areaLocatarioMultasObs").value = locatarioMultas.obs || "";

    console.log(idMulta, locatarioId);
    
    ModalManager.abrir('modalLocatarioMulta',{
        acao:"editar",
        multaId: idMulta,
        locatarioId: locatarioId,
        frotaId: frotaId,
        franquia_franquiador_locatario_id: franquia_franquiador_locatario_id
    });
});
$(document).on('click','.btnExcluirLocatarioMulta',function(){
    const idMulta = this.dataset.id;
    const locatarioId = this.dataset.locatarioid;
    console.log("excluir");
    // $('#btExcluir').attr('id', 'btExcluirMulta');
    ModalManager.abrir('modalExcluir',{
        multaId: idMulta,
        locatarioId: locatarioId
    });

    $('#btExcluir')
    .off('click')
    .on('click', async function () {
        try {
            const dados = ModalManager.getDados('modalExcluir');
            const locatarioId = dados.locatarioId;
            console.log("excluir multa", dados);
            await api.get(`/api/multas/ativaDesativa/${dados.multaId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarLocatarioMultas(locatarioId);
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
$(document).on('shown.bs.tab', '#btnAbaLocatarioMultas', function () {
    const locatarioId = document.getElementById("btnAbaLocatarioMultas").dataset.locatarioId;
    iniciarLocatarioMultas(locatarioId);
    console.log("aba multas:",locatarioId);
    carregarPagamentosModalCusto("selectLocatarioMultasPagamentos",2);
    carregarStatusModalMulta("selectLocatarioMultasStatus",2);
    mascaraMoeda(document.getElementById("inputLocatarioMultasValorMulta"));
    mascaraMoeda(document.getElementById("inputLocatarioMultasValorPago"));
    mascaraMoeda(document.getElementById("inputLocatarioMultasValorRecebido"));
});
$(document).on('click','#btLocatariosMultasSalvar',async function(){
    
    const dados = ModalManager.getDados('modalLocatarioMulta');
    const locatarioId = dados.locatarioId;
    const payload = {
        franquia_franquiador_locatario_id:dados.franquia_franquiador_locatario_id,
        frota_id:dados.frotaId,
        codigo:document.getElementById("inputLocatarioMultasCodigo").value,
        pontos:document.getElementById("inputLocatarioMultasPontuacao").value || 0,
        data_infracao:document.getElementById("inputLocatarioMultasDataMulta").value || null,
        data_notificacao:document.getElementById("inputLocatarioMultasDataNotificacao").value || null,
        data_pagamento: document.getElementById("inputLocatarioMultasDataPagamento").value || null,
        data_indicacao:document.getElementById("inputLocatarioMultasDataIndicacao").value || null,
        valor_multa:limparMoeda(document.getElementById("inputLocatarioMultasValorMulta").value),
        status_id:document.getElementById("selectLocatarioMultasStatus").value|| 1,
        valor_pago:limparMoeda(document.getElementById("inputLocatarioMultasValorPago").value),
        valor_recebido:limparMoeda(document.getElementById("inputLocatarioMultasValorRecebido").value),
        pagamento_id:document.getElementById("selectLocatarioMultasPagamentos").value|| null,
        obs: document.getElementById("areaLocatarioMultasObs").value|| null
    }
    if (
        !payload.codigo ||
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
            const multaId = dados.multaId
            await api.put(`/api/multas/update/${multaId}`, payload);
            
        }

        ModalManager.fechar('modalLocatarioMulta');
        iniciarLocatarioMultas(locatarioId);
        const placa = document.getElementById("inputLocatarioMultasPlaca").value; 
        Swal.fire({
            icon: 'success',
            title: 'Multa salvas',
            text: 'Multa inserida para a moto:'+placa,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar a multa.' });
    }
    // 
});
// $(document).on('click', '#btExcluirMulta', async function () {


// });