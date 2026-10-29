async function iniciarFaturamento(filtros = {}) {

    const hoje = new Date();

    const params = new URLSearchParams();
    
    if (filtros.status) {
        params.append("status", filtros.status);
    }
    
    // Se informou período, usa período
    if (filtros.dataInicio || filtros.dataFim) {
    
        if (filtros.dataInicio) {
            params.append("dataInicio", filtros.dataInicio);
        }
    
        if (filtros.dataFim) {
            params.append("dataFim", filtros.dataFim);
        }
    
    } else {
        // Caso contrário, usa mês e ano atuais
        params.append("mes", filtros.mes || (hoje.getMonth() + 1));
        params.append("ano", filtros.ano || String(hoje.getFullYear()).slice(-2));
    }
    
    const query = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/faturamentos/listar${query}`);

    const faturamentos = response.data.resultado || [];
    console.log(faturamentos);
    if ($('#faturamentoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#faturamentoTableLista')) {
            $('#faturamentoTableLista').DataTable().destroy();
        }
    
        $('#faturamentoTableLista').DataTable({
            data: faturamentos,
            pageLength: -1,
            lengthMenu: [[5,10,25,50,-1],[5,10,25,50,"Todos"]],
            paging: true,
            columns: [
                {
                    data: 'franquiado',
                    defaultContent: '-'
                },
                {
                    data: null,
                    title: 'Periodo',
                    render: function(data, type, row) {
                        const mes = String(row.mes).padStart(2, '0');
                        const ano = String(row.ano).slice(-2);
            
                        return `${mes}/${ano}`;
                    }
                },
                {
                    data: 'valor_entrada',
                    render: v => Number(v || 0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})
                },
                {
                    data: 'valor_saida',
                    render: v => Number(v || 0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})
                },
                {
                    data: null,
                    render: function (data, type, row) {
                        const liquido = Number(row.valor_entrada || 0) - Number(row.valor_saida || 0);
                
                        const valor = liquido.toLocaleString('pt-BR', {
                            style: 'currency',
                            currency: 'BRL'
                        });
                
                        return liquido < 0
                            ? `<span class="text-danger fw-bold">${valor}</span>`
                            : `<span>${valor}</span>`;
                    }
                },
                {
                    data: 'data_pagamento',
                    render: d => d ? new Date(d).toLocaleDateString('pt-BR') : '-'
                },
                {
                    data: 'pagamento',
                    defaultContent: '-'
                },
                {
                    data: 'status',
                    render: (data, type, row) => {

                        let classe = 'bg-secondary';
                        if (row.status_id === 1) classe = 'bg-danger';
                        if (row.status_id === 2) classe = 'bg-success';

                        return `<span class="badge-status ${classe} text-white">${data ?? '-'}</span>`;
                    }
                },
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-center',
                    render: (data, type, row) => `
                        <div class="d-flex justify-content-center gap-2">
                            <button class="btn btn-sm btn-warning editarModalFaturamento" data-id="${row.id}">
                                <i class="bi bi-pencil-fill"></i>
                            </button>

                            <button class="btn btn-sm btn-danger excluirModalFaturamento" data-id="${row.id}">
                                <i class="bi bi-trash-fill"></i>
                            </button>
                        </div>
                    `
                }
            ],
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:20,
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalEntrada = dados.reduce((s, i) => s + Number(i.valor_entrada || 0), 0);
                const totalSaida = dados.reduce((s, i) => s + Number(i.valor_saida || 0), 0);
                const totalLiquido = totalEntrada-totalSaida;
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#totalEntrada').text(fmt(totalEntrada));
                $('#totalSaida').text(fmt(totalSaida));
                $('#totalLiquido').text(fmt(totalLiquido));
            }
        });
    
    }

}
async function carregarStatusFiltrosFaturamento() {

    const select = document.getElementById("selectStatusFaturamento");

    if (!select) return;

    try {

        const response = await api.get("/api/faturamentos/listar");
        const faturamentos = response.data.resultado || [];

        // Remove duplicatas pelo status_id
        const vistos = new Set();

        faturamentos
            .filter(s => s.status_id && s.status)
            .forEach((faturamentos) => {

                if (vistos.has(faturamentos.status_id)) return;
                vistos.add(faturamentos.status_id);

                const option = document.createElement("option");
                option.value = faturamentos.status_id;
                option.textContent = faturamentos.status;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
async function carregarStatusFaturamento() {

    const select = document.getElementById("selectModalFaturamentoStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/faturamentos/status");
        const faturamentos = response.data.resultado || [];

        faturamentos
            .forEach((faturamentos) => {

                const option = document.createElement("option");
                option.value = faturamentos.id;
                option.textContent = faturamentos.texto;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
$(document).on('click', '#btModalFiltroFaturamento', async function () {
    const selectStatus     = document.getElementById("selectStatusFaturamento");
    const inputDataInicial = document.getElementById("inputDataInicial");
    const inputDataFinal   = document.getElementById("inputDataFinal");

    if (selectStatus)     selectStatus.value     = "";
    if (inputDataInicial) inputDataInicial.value = "";
    if (inputDataFinal)   inputDataFinal.value   = "";
    ModalManager.abrir("modalFiltroFaturamento");
});
$(document).on('click', '#btModalNovoFaturamento', async function () {

    document.getElementById("frmFaturamento").reset();
    await carregarFranqueados("selectFranquiadoModal", false);
    const franquiadoID = document.getElementById("selectFranquiadoModal").value;
    aplicarMascaraMesAno("#modalFaturamentoMesAno");
    mascaraMoeda(document.getElementById("modalFaturamentoEntrada"));
    mascaraMoeda(document.getElementById("modalFaturamentoSaida"));
    document.getElementById("modalFaturamentoMesAno").value = obterMesAnoAtual();
    ModalManager.abrir("modalFaturamento",{
        acao:"novo",
        franquiadoID: franquiadoID,
    });
});
$(document).on('click', '.editarModalFaturamento', async function () {
    await carregarFranqueados("selectFranquiadoModal", false);
    const franquiadoID = document.getElementById("selectFranquiadoModal").value;
    let faturamentoID = this.dataset.id;
    const response = await api.get(`/api/faturamentos/listar?id=${faturamentoID}`);
    const faturamento = response.data.resultado[0];
    document.getElementById("modalFaturamentoMesAno").value = formatarMesAno(faturamento.mes, faturamento.ano) || "";
    document.getElementById("modalFaturamentoEntrada").value = formatarReal(faturamento.valor_entrada) || "0";
    document.getElementById("modalFaturamentoSaida").value = formatarReal(faturamento.valor_saida) || "0";
    document.getElementById("modalFaturamentoDataPagamento").value = faturamento.data_pagamento || "";
    document.getElementById("modalFaturamentoTipo").value = primeiraLetraMaiuscula(faturamento.tipo_pagamento) || "";
    document.getElementById("selectModalFaturamentoStatus").value  = faturamento.status_id || "";
    // console.log(faturamento);
    aplicarMascaraMesAno("#modalFaturamentoMesAno");
    mascaraMoeda(document.getElementById("modalFaturamentoEntrada"));
    mascaraMoeda(document.getElementById("modalFaturamentoSaida"));

    // 
    // 
    
    ModalManager.abrir("modalFaturamento",{
        acao:"editar",
        franquiadoID: franquiadoID,
        faturamentoID: faturamentoID
    });
});
$(document).on('click', '.excluirModalFaturamento', function () {

    ModalManager.abrir("modalExcluir");

    $('#btExcluir')
    .off('click')
    .on('click', function () {
        console.log('Excluir faturamento');
        ModalManager.fechar("modalExcluir");
    });
    
});
$(document).on('click', '#btFiltrarFaturamento', async function () {
    const filtros = {
        status:     document.getElementById("selectStatusFaturamento")?.value     || null,
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null
    }
    iniciarFaturamento(filtros);
    ModalManager.fechar("modalFiltroFaturamento");
});
$(document).on('click', '#modalBtSalvarFaturamento', async function () {
    const dados = ModalManager.getDados("modalFaturamento");

    const response = await api.get(`/api/franquiado/listar?id=${dados.franquiadoID}`);
    const franquiado = response.data.resultado[0] || None;
    const [mes, ano] = document.getElementById("modalFaturamentoMesAno").value.split("/");
    console.log(mes, ano);
    const payload = {
        franquia_franquiador_locatario_id: parseInt(franquiado.franquia_franquiador_locatario_id),
        mes: mes,
        ano: ano,
        frota_id:0,
        valor_entrada: limparMoeda(document.getElementById("modalFaturamentoEntrada").value),
        valor_saida: limparMoeda(document.getElementById("modalFaturamentoSaida").value),
        data_pagamento: document.getElementById("modalFaturamentoDataPagamento").value,
        tipo_pagamento: limparLetrasNumeros(document.getElementById("modalFaturamentoTipo").value),
        status_id: parseInt(document.getElementById("selectModalFaturamentoStatus").value)
    };
    if (
        !payload.franquia_franquiador_locatario_id ||
        !payload.mes || 
        !payload.ano ||
        !payload.valor_entrada ||
        !payload.data_pagamento || 
        !payload.tipo_pagamento ||
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
    try {
        console.log(JSON.stringify(payload));
        if(dados.acao == 'novo'){
            console.log("inserir");
            await api.post("/api/faturamentos/create", payload);
        }else{
            let faturamentoID = dados.faturamentoID;
            console.log("faturamentoID:",faturamentoID);
            await api.put(`/api/faturamentos/update/${faturamentoID}`, payload);
        }
        ModalManager.fechar("modalFaturamento");
        iniciarFaturamento();

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Faturamento salvo com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {

        console.error(err);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível salvar o Semanal.'
        });
    }    

});