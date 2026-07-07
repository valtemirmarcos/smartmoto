async function iniciarCalcao(filtros = {}) {

    try {
        // Monta os params ignorando valores vazios
        const params = new URLSearchParams();

        if (filtros.franquiado) params.append("franquiado", filtros.franquiado);
        if (filtros.placa)      params.append("placa",      filtros.placa);
        if (filtros.status)     params.append("status",     filtros.status);
        if (filtros.formaPagamento)     params.append("formaPagamento",     filtros.formaPagamento);
        if (filtros.dataInicio) params.append("dataInicio", filtros.dataInicio);
        if (filtros.dataFim)    params.append("dataFim",    filtros.dataFim);

        const query    = params.toString() ? `?${params.toString()}` : "";
        console.log(query);
        const response = await api.get(`/api/calcoes/listar${query}`);

        const calcoes = response.data.resultado || [];

        if ($.fn.DataTable.isDataTable('#calcaoTableLista')) {
            $('#calcaoTableLista').DataTable().destroy();
        }

        $('#calcaoTableLista').DataTable({

            data: calcoes,

            columns: [

                {
                    data: 'placa',
                    defaultContent: '-'
                },

                {
                    data: 'data_deposito',
                    defaultContent: '-',
                    render: function(data) {

                        if (!data) return '-';

                        const dataObj = new Date(data);

                        return dataObj.toLocaleDateString('pt-BR');
                    }
                },

                {
                    data: 'pagamento',
                    defaultContent: '-'
                },

                {
                    data: 'valor',
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
                    data: 'valor_atual',
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
                    data: 'status',
                    render: function(data) {

                        let classe = 'bg-secondary';

                        if (data === 'Ativo') {
                            classe = 'bg-success';
                        }

                        if (data === 'Recolhido') {
                            classe = 'bg-danger';
                        }

                        if (data === 'Devolvido') {
                            classe = 'bg-warning';
                        }

                        return `
                            <span class="badge-status ${classe} text-white">
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
                            <div class="d-flex justify-content-center gap-2">
                    
                                <button
                                    class="btn btn-sm btn-warning rounded-3 btn-editar-calcao"
                                    data-id="${row.id}"
                                >
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                    
                                <button
                                    class="btn btn-sm btn-danger rounded-3 btn-excluir-calcao"
                                    data-id="${row.id}"
                                >
                                    <i class="bi bi-trash-fill"></i>
                                </button>
                    
                            </div>
                        `;
                    }
                }

            ],



            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },

            pageLength: 5,

            responsive: true,

            destroy: true

        });

    } catch (error) {

        console.error(error);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível carregar os calções.'
        });

    }

}

async function carregarStatusCalcao() {

    const select = document.getElementById("selectStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/calcoes/listar");
        const calcoes   = response.data.resultado;

        // Remove duplicatas pelo status_id
        const vistos = new Set();

        calcoes
            .filter(c => c.status_id && c.status)
            .forEach((calcoes) => {

                if (vistos.has(calcoes.status_id)) return;
                vistos.add(calcoes.status_id);

                const option = document.createElement("option");
                option.value = calcoes.status_id;
                option.textContent = calcoes.status;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
async function carregarFormasPagamento() {

    const select = document.getElementById("selectFormasPgto");

    if (!select) return;

    try {

        const response = await api.get("/api/calcoes/listar");
        const calcoes   = response.data.resultado;

        // Remove duplicatas pelo status_id
        const vistos = new Set();

        calcoes
            .filter(c => c.forma_pagamento_id && c.pagamento)
            .forEach((calcoes) => {

                if (vistos.has(calcoes.forma_pagamento_id)) return;
                vistos.add(calcoes.forma_pagamento_id);

                const option = document.createElement("option");
                option.value = calcoes.forma_pagamento_id;
                option.textContent = calcoes.pagamento;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}

function iniciarBotaoFiltrarCalcao() {

    const botao  = document.getElementById("filtrarCalcoes");
    const limpar = document.getElementById("limparFiltros");

    if (botao) {
        botao.addEventListener("click", () => {
            
            const filtros = {
                franquiado: document.getElementById("selectFranquiado")?.value     || null,
                placa:      document.getElementById("inputPlaca")?.value
                                ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                                : null,
                status:     document.getElementById("selectStatus")?.value     || null,
                formaPagamento:     document.getElementById("selectFormasPgto")?.value     || null,
                dataInicio: document.getElementById("inputDataInicial")?.value || null,
                dataFim:    document.getElementById("inputDataFinal")?.value   || null,
            };

            iniciarCalcao(filtros);

        });
    }

    if (limpar) {
        limpar.addEventListener("click", () => {

            // Reseta todos os campos
            const selectFranquiado = document.getElementById("selectFranquiado");
            const inputPlaca       = document.getElementById("inputPlaca");
            const selectStatus     = document.getElementById("selectStatus");
            const selectFormasPgto = document.getElementById("selectFormasPgto");
            const inputDataInicial = document.getElementById("inputDataInicial");
            const inputDataFinal   = document.getElementById("inputDataFinal");


            if (selectFranquiado && !selectFranquiado.disabled) {
                selectFranquiado.value = "";
            }
            if (inputPlaca)       inputPlaca.value       = "";
            if (selectStatus)     selectStatus.value     = "";
            if (selectFormasPgto) selectFormasPgto.value = "";
            if (inputDataInicial) inputDataInicial.value = "";
            if (inputDataFinal)   inputDataFinal.value   = "";
            
            // Recarrega sem filtros
            iniciarCalcao();

        });
    }

}

function iniciarBotaoNovoCalcao() {

    const btn = document.getElementById("btnNovoCalcao");

    if (!btn) return;

    btn.addEventListener("click", () => abrirModalNovoCalcao());

}
async function carregarStatusModalCalcao() {

    const select = document.getElementById("modalCalcaoStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/calcao/status");
        const status   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione o status</option>`;

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
async function carregarStatusModal() {
    const select = document.getElementById("modalCalcaoStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/calcao/status");
        const status   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione o status</option>`;

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
async function carregarFormasPagamento() {

    const select = document.getElementById("modalFormasPagamentos");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/pagamentos");
        const pagamentos   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione a forma de pagamento</option>`;

        pagamentos.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.id;
            option.textContent = s.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar pagamentos:", err);
    }

}
function abrirModalNovoCalcao() {

    document.getElementById("tituloCalcao").textContent = "Inserir novo calção";
    document.querySelector("#modalCalcao form").reset();

    // ✅ Aplica máscara após reset
    mascaraMoeda(document.getElementById("modalValorCalcao"));
    mascaraMoeda(document.getElementById("modalValorEfetivo"));

    document.getElementById("btModalSalvar").dataset.calcaoID = "";
    document.getElementById("btModalSalvar").dataset.modo = "inserir";

    carregarFranqueados("selectFranquiadoModal", false); 
    carregarAutocompletePlaca("id","modalInputPlaca", "modalListaPlacas"); 
    carregarStatusModal();
    carregarFormasPagamento();

    modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalCalcao"));
    modalFrotaInstancia.show();
}

// ✅ Use document em vez de #calcaoTableLista
$(document).on('click', '.btn-editar-calcao', async function () {

    const id = $(this).data('id');

    try {
        const tabCalcaoDados = document.querySelector('#calcaoTabs [data-bs-target="#calcaoDados"]');
        bootstrap.Tab.getOrCreateInstance(tabCalcaoDados).show();

        const response = await api.get(`/api/calcoes/listar?id=${id}`);
        const calcao   = response.data.resultado[0];

        document.getElementById("btEnviarDocumentoCalcao").dataset.calcaoId = id;

        if (!calcao) return;

        document.getElementById("tituloCalcao").textContent = "Editar Calção";

        document.getElementById("modalInputPlaca").value           = calcao.placa         || "";
        document.getElementById("modalInputPlaca").dataset.frotaId = calcao.frota_id;
        document.getElementById("modalDataPagamento").value        = calcao.data_deposito || "";
        document.getElementById("modalValorCalcao").value  = Number(calcao.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        document.getElementById("modalValorEfetivo").value = Number(calcao.valor_atual).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        await carregarFranqueados("selectFranquiadoModal", false);
        document.getElementById("selectFranquiadoModal").value = calcao.franquia_franquiador_locatario_id || "";

        await carregarStatusModalCalcao();
        document.getElementById("modalCalcaoStatus").value = calcao.status_id || "";

        await carregarFormasPagamento();
        document.getElementById("modalFormasPagamentos").value = calcao.forma_pagamento_id || "";

        document.getElementById("btModalSalvar").dataset.id   = calcao.id;
        document.getElementById("btModalSalvar").dataset.modo = "editar";

        mascaraMoeda(document.getElementById("modalValorCalcao"));
        mascaraMoeda(document.getElementById("modalValorEfetivo"));

        const anexo = await api.get(
            `/api/anexos/listar?tipo=calcao&codigo=${calcao.id}`
        );
        carregarArquivosCalcao(anexo.data.resultado[0]);

        new bootstrap.Modal(document.getElementById("modalCalcao")).show();

    } catch (err) {
        console.error("Erro ao carregar calção:", err);
    }

});

$(document).on('click', '#btModalSalvar', async function () {

    const modo = this.dataset.modo;
    const id   = this.dataset.id;

    const payload = {
        franquia_franquiador_locatario_id: parseInt(document.getElementById("selectFranquiadoModal").value),
        frota_id:           parseInt(document.getElementById("modalInputPlaca").dataset.frotaId),
        data_deposito:      document.getElementById("modalDataPagamento").value,
        forma_pagamento_id: parseInt(document.getElementById("modalFormasPagamentos").value),
        valor:              limparMoeda(document.getElementById("modalValorCalcao").value),
        valor_atual:        limparMoeda(document.getElementById("modalValorEfetivo").value),
        status_id:          parseInt(document.getElementById("modalCalcaoStatus").value),
    };
    console.log("payload:",JSON.stringify(payload) );
    if (!payload.frota_id || !payload.data_deposito || !payload.forma_pagamento_id || !payload.status_id) {
        Swal.fire({ icon: 'warning', title: 'Atenção', text: 'Preencha todos os campos obrigatórios.' });
        return;
    }

    try {

        if (modo === "inserir") {
            await api.post("/api/calcoes/create", payload);
        } else {
            await api.put(`/api/calcoes/update/${id}`, payload);
        }

        // bootstrap.Modal.getInstance(document.getElementById("modalCalcao")).hide();
        const tabCalcaoDocumentos = document.querySelector('#calcaoTabs [data-bs-target="#calcaoDocumentos"]');
        bootstrap.Tab.getOrCreateInstance(tabCalcaoDocumentos).show();
        document.getElementById("btEnviarDocumentoCalcao").dataset.calcaoId = id;
        iniciarCalcao();

        Swal.fire({
            icon: 'success',
            title: 'Dados salvos',
            text: 'Assim que possivel adicione comprovante do calção',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar o calção.' });
    }

});

$(document).on('click', '.btn-excluir-calcao', function () {

    const id = $(this).data('id');

    document.getElementById("btConfirmarExcluir").dataset.id = id;

    new bootstrap.Modal(document.getElementById("modalExcluir")).show();

});

$(document).on('click', '#btConfirmarExcluir', async function () {

    const id = this.dataset.id;

    try {

        await api.get(`/api/calcoes/ativaDesativa/${id}?ativa=0`);

        bootstrap.Modal.getInstance(document.getElementById("modalExcluir")).hide();

        iniciarCalcao();

        Swal.fire({ icon: 'success', title: 'Excluído!', text: 'Calção excluído com sucesso.', timer: 2000, showConfirmButton: false });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir o calção.' });
    }

});
// ocultar o botao salvar quando estiver em documentos
function iniciarAbasCalcao() {

    const btnSalvar = document.getElementById("btModalSalvar");

    if (!btnSalvar) return;

    const abaDados = document.querySelector(
        '#calcaoTabs [data-bs-target="#calcaoDados"]'
    );

    const abaDocumentos = document.querySelector(
        '#calcaoTabs [data-bs-target="#calcaoDocumentos"]'
    );

    abaDocumentos.addEventListener("shown.bs.tab", () => {
        btnSalvar.classList.add("d-none");
    });

    abaDados.addEventListener("shown.bs.tab", () => {
        btnSalvar.classList.remove("d-none");
    });

}

// habilita botão ao selecionar arquivo
$(document).on('change', '#calcaoArquivo', function () {
    const arquivo = document.getElementById("calcaoArquivo").files.length;
    console.log("arquivo",arquivo);

    const possuiArquivo = arquivo > 0;

    $('#btEnviarDocumentoCalcao').prop(
        'disabled',
        !possuiArquivo
    );

});

$(document).on('click', '#btEnviarDocumentoCalcao', async function () {

    const calcaoId = this.dataset.calcaoId;
   
    const arquivo = document.getElementById("calcaoArquivo").files[0];

    if (!arquivo) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Selecione um arquivo para enviar.'
        });
        return;
    }

    try {
        const listarCalcao = await api.get(`/api/calcoes/listar?id=${calcaoId}`);
        const calcao   = listarCalcao.data.resultado[0];
        const franquia_franquiador_locatario_id = calcao.franquia_franquiador_locatario_id;

        Swal.fire({
            title: 'Enviando comprovante...',
            text: 'Aguarde alguns instantes.',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await api.get(
            `/api/anexos/listar?tipo=calcao&codigo=${calcaoId}`
        );
 
        const formData = new FormData();
        formData.append("file", arquivo);
        formData.append("entidade_tipo", "calcao");
        formData.append("entidade_id", calcaoId);
        formData.append("franquia_franquiador_locatario_id", franquia_franquiador_locatario_id);

        if (response.data.resultado?.length) {
            let idAnexo = response.data.resultado[0].id;
            await api.post(
                `/api/anexos/update/${idAnexo}`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );
        }else{
            await api.post(
                `/api/anexos/create`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );
        }
        const reposta = await api.get(
            `/api/anexos/listar?tipo=calcao&codigo=${calcaoId}`
        );
    
        if (reposta.data.resultado?.length) {
            carregarArquivosCalcao(reposta.data.resultado[0]);
            iniciarCalcao();
        }

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Comprovante anexado com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

        document.getElementById("calcaoArquivo").value = "";
        $('#btEnviarDocumentoCalcao').prop('disabled', true);

    } catch (error) {

        console.log(JSON.stringify(error.response?.data) );

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: error?.response?.data?.detail ||
                  'Não foi possível anexar o comprovante.'
        });

    }

});

function carregarArquivosCalcao(anexo) {

    const tbody = document.getElementById('listaDocumentosCalcao');

    if (!anexo || !anexo.tipo_mime) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-3">
                    Nenhum documento inserido
                </td>
            </tr>
        `;

        return;
    }

    const dataFormatada = dataHoraFormatada(anexo.created_at);

    let extensao = 'arquivo';
    let descricao = 'Documento';

    switch (anexo.tipo_mime) {
        case 'application/pdf':
            extensao = 'pdf';
            descricao = 'PDF';
            break;

        case 'image/jpeg':
        case 'image/jpg':
            extensao = 'jpg';
            descricao = 'Imagem JPG';
            break;

        case 'image/png':
            extensao = 'png';
            descricao = 'Imagem PNG';
            break;

        case 'application/msword':
            extensao = 'doc';
            descricao = 'Word DOC';
            break;

        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            extensao = 'docx';
            descricao = 'Word DOCX';
            break;

        case 'application/vnd.ms-excel':
            extensao = 'xls';
            descricao = 'Excel XLS';
            break;

        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            extensao = 'xlsx';
            descricao = 'Excel XLSX';
            break;

        default:
            descricao = anexo.tipo_mime;
    }

    const nomeArquivo = anexo.entidade_tipo+'_'+anexo.entidade_id+anexo.id+'.'+extensao;

        tbody.innerHTML = `
        <tr>
            <td>${nomeArquivo}</td>
            <td>${descricao}</td>
            <td>${dataFormatada}</td>
    
            <td class="text-center">
    
                <button
                    class="btn btn-sm btn-primary me-1"
                    onclick="baixarArquivo('calca',${anexo.id})"
                    title="Baixar arquivo"
                >
                    <i class="bi bi-download"></i>
                </button>
    
                <button
                    class="btn btn-sm btn-danger"
                    onclick="excluirArquivo(${anexo.id}, () => atualizarTabelaCalcao(${anexo.entidade_id}))"
                    title="Excluir arquivo"
                >
                    <i class="bi bi-trash"></i>
                </button>
    
            </td>
        </tr>
    `;
}
async function atualizarTabelaCalcao(idCalcao) {

    const response = await api.get(
        `/api/anexos/listar?tipo=calcao&codigo=${idCalcao}`
    );

    carregarArquivosCalcao(response.data.resultado[0]);
    iniciarCalcao();
}