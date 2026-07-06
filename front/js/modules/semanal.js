async function iniciarSemanal(filtros = {}) {

    try {

        const params = new URLSearchParams();

        if (filtros.franquiado) params.append("franquiado", filtros.franquiado);
        if (filtros.placa) params.append("placa", filtros.placa);
        if (filtros.status) params.append("status", filtros.status);
        if (filtros.dataInicio) params.append("dataInicio", filtros.dataInicio);
        if (filtros.dataFim) params.append("dataFim", filtros.dataFim);

        const query = params.toString() ? `?${params.toString()}` : "";
        const response = await api.get(`/api/semanais/listar${query}`);

        const semanais = response.data.resultado || [];

        const $table = $('#semanalTableLista');

        if (!$table.length) return;

        // destrói com segurança
        if ($.fn.DataTable.isDataTable('#semanalTableLista')) {
            $table.DataTable().destroy();
        }

        const searchSalva = localStorage.getItem('searchSemanais') || '';

        const table = $table.DataTable({
            data: semanais,
            pageLength: -1,
            lengthMenu: [[5,10,25,50,-1],[5,10,25,50,"Todos"]],
            paging: true,

            columns: [
                { data: 'id' },
                { data: 'nome_franquiado', visible: false },
                { data: 'nome_locatario', visible: false },
                { data: 'placa' },

                {
                    data: 'data_prevista',
                    render: d => d ? new Date(d + 'T00:00:00').toLocaleDateString('pt-BR') : '-'
                },

                { data: 'dia_semana', visible: false },

                {
                    data: 'valor',
                    render: v => Number(v || 0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})
                },

                {
                    data: 'valor_pago',
                    render: v => Number(v || 0).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})
                },

                {
                    data: 'data_pagamento',
                    render: d => d ? new Date(d).toLocaleDateString('pt-BR') : '-'
                },

                {
                    data: 'status',
                    render: (data, type, row) => {

                        let classe = 'bg-secondary';
                        if (row.status_id === 1) classe = 'bg-primary';
                        if (row.status_id === 2) classe = 'bg-success';
                        if (row.status_id === 3) classe = 'bg-danger';

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
                            <button class="btn btn-sm btn-warning btn-editar-semanais" data-id="${row.id}">
                                <i class="bi bi-pencil-fill"></i>
                            </button>

                            <button class="btn btn-sm btn-danger btn-excluir-semanais" data-id="${row.id}" style="display:none">
                                <i class="bi bi-trash-fill"></i>
                            </button>
                        </div>
                    `
                }
            ],

            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },

            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalPago = dados
                .filter(i => i.status_id === 2)
                .reduce((s, i) => s + Number(i.valor_pago || 0), 0);
                const totalAberto = dados
                    .filter(i => i.status_id === 1)
                    .reduce((s, i) => s + Number(i.valor || 0), 0);
                const totalAtrasado = dados
                    .filter(i => i.status_id === 3)
                    .reduce((s, i) => s + Number(i.valor || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#valorPago').text(fmt(totalPago));
                $('#valorAberto').text(fmt(totalAberto));
                $('#valorAtrasado').text(fmt(totalAtrasado));
            }
        });

        table.on('order.dt', function () {
            const order = table.order(); 
            // exemplo: [[3, "asc"]]
        
            localStorage.setItem('orderSemanais', JSON.stringify(order));
        });

        const orderSalva = localStorage.getItem('orderSemanais');

        if (orderSalva) {
            table.order(JSON.parse(orderSalva)).draw();
        }
        // 🔎 reaplica busca
        if (searchSalva && searchSalva !== "null") {
            table.search(searchSalva).draw();
        }

        // 💾 salva busca (CORRETO e seguro)
        $table.off('search.dt').on('search.dt', function () {
            localStorage.setItem('searchSemanais', table.search());
        });

    } catch (error) {
        console.error(error);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível carregar os Semanais.'
        });
    }
}

async function carregarStatusFiltrosSemanais() {

    const select = document.getElementById("selectStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/semanais/listar");
        const semanais = response.data.resultado || [];

        // Remove duplicatas pelo status_id
        const vistos = new Set();

        semanais
            .filter(s => s.status_id && s.status)
            .forEach((semanais) => {

                if (vistos.has(semanais.status_id)) return;
                vistos.add(semanais.status_id);

                const option = document.createElement("option");
                option.value = semanais.status_id;
                option.textContent = semanais.status;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}

function iniciarBotaoFiltrarSemanais() {

    const botao  = document.getElementById("filtrarSemanais");
    const limpar = document.getElementById("limparFiltros");

    if (botao) {
        botao.addEventListener("click", () => {
            
            const filtros = {
                franquiado: document.getElementById("selectFranquiado")?.value     || null,
                placa:      document.getElementById("inputPlaca")?.value
                                ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                                : null,
                status:     document.getElementById("selectStatus")?.value     || null,
                dataInicio: document.getElementById("inputDataInicial")?.value || null,
                dataFim:    document.getElementById("inputDataFinal")?.value   || null,
            };
            iniciarSemanal(filtros);

        });
    }

    if (limpar) {
        limpar.addEventListener("click", () => {
            // // Reseta todos os campos
            const selectFranquiado = document.getElementById("selectFranquiado");
            const inputPlaca       = document.getElementById("inputPlaca");
            const selectStatus     = document.getElementById("selectStatus");
            const inputDataInicial = document.getElementById("inputDataInicial");
            const inputDataFinal   = document.getElementById("inputDataFinal");


            if (selectFranquiado && !selectFranquiado.disabled) {
                selectFranquiado.value = "";
            }
            if (inputPlaca)       inputPlaca.value       = "";
            if (selectStatus)     selectStatus.value     = "";
            if (inputDataInicial) inputDataInicial.value = "";
            if (inputDataFinal)   inputDataFinal.value   = "";
            
            // 🔥 LIMPA BUSCA DO DATATABLE
            const table = $('#semanalTableLista').DataTable();
            table.search('').draw();

            // 🔥 LIMPA LOCALSTORAGE
            localStorage.removeItem('searchSemanais');
            localStorage.removeItem('orderSemanais');
            // Recarrega sem filtros
            iniciarSemanal();

        });
    }

}
async function carregarStatusModalSemanais() {

    const select = document.getElementById("semanalStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/semanais/status");
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

function iniciarBotaoNovoSemanal() {

    const btn = document.getElementById("btnNovoSemanal");

    if (!btn) return;

    btn.addEventListener("click", () => {
        console.log("clicou");
        document.getElementById("formSemanal").reset(); // ✅ direto pelo id
        document.getElementById("modalInputPlaca").disabled = false;;
        // Volta para a aba Dados
        const tabDados = document.querySelector('#tabsSemanal [data-bs-target="#tabDados"]');
        bootstrap.Tab.getOrCreateInstance(tabDados).show();

        mascaraMoeda(document.getElementById("semanalValorPrevisto"));
        mascaraMoeda(document.getElementById("semanalValorRecebido"));

        document.getElementById("btSalvarSemanal").dataset.id   = "";
        document.getElementById("btSalvarSemanal").dataset.modo = "inserir";

        carregarFranqueados("selectFranquiadoModal", false);
        carregarAutocompletePlaca("id", "modalInputPlaca", "modalListaPlacas");
        carregarStatusModalSemanais(); // carregar o select de status

        modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalSemanal"));
        modalFrotaInstancia.show();

    });

}

$(document).on('click', '.btn-editar-semanais', async function () {
    const id = $(this).data('id');
    console.log(id);
    document.getElementById("btEnviarArquivo").dataset.semanalId = id;
    const tabDados = document.querySelector('#tabsSemanal [data-bs-target="#tabDados"]');
    bootstrap.Tab.getOrCreateInstance(tabDados).show();
    try {    
        const response = await api.get(`/api/semanais/listar?id=${id}`);
        const semanais   = response.data.resultado[0];

        if (!semanais) return;

        document.getElementById("tituloSemanal").textContent = "Editar Semanal:"+semanais.placa;

        await carregarFranqueados("selectFranquiadoModal", false);
        document.getElementById("selectFranquiadoModal").value = semanais.franquiado_id || "";
        document.getElementById("modalInputPlaca").disabled = true;
        document.getElementById("modalInputPlaca").value           = semanais.placa         || "";
        document.getElementById("modalInputPlaca").dataset.frotaId = semanais.frota_id;
        document.getElementById("semanalDataVencimento").value        = semanais.data_prevista || "";
        document.getElementById("semanalDataRecebimento").value        = semanais.data_pagamento || "";
        document.getElementById("semanalValorPrevisto").value  = Number(semanais.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        document.getElementById("semanalValorRecebido").value = Number(semanais.valor_pago).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        await carregarStatusModalSemanais();
        document.getElementById("semanalStatus").value  = semanais.status_id || "";

        document.getElementById("btSalvarSemanal").dataset.id   = semanais.id;
        document.getElementById("btSalvarSemanal").dataset.modo = "editar";
        document.getElementById("btEnviarArquivo").dataset.franquia_franquiador_locatario_id = semanais.franquia_franquiador_locatario_id;

        mascaraMoeda(document.getElementById("semanalValorPrevisto"));
        mascaraMoeda(document.getElementById("semanalValorRecebido"));


        const responseAnexo = await api.get(`/api/anexos/listar?tipo=semanal&codigo=${id}`);
        const anexo   = responseAnexo.data.resultado[0];
        carregarArquivosSemanal(anexo);

        
        modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalSemanal"));
        modalFrotaInstancia.show();
    } catch (err) {
        console.error("Erro ao carregar semanal:", err);
    }

});


$(document).on('click', '#btSalvarSemanal', async function () {

    const modo = this.dataset.modo;
    let id = this.dataset.id;

    const payload = {
        franquia_franquiador_locatario_id: parseInt(document.getElementById("selectFranquiadoModal").value),
        frota_id: parseInt(document.getElementById("modalInputPlaca").dataset.frotaId),
        data_prevista: document.getElementById("semanalDataVencimento").value,
        data_pagamento: document.getElementById("semanalDataRecebimento").value,
        valor: limparMoeda(document.getElementById("semanalValorPrevisto").value),
        valor_pago: limparMoeda(document.getElementById("semanalValorRecebido").value),
        status_id: parseInt(document.getElementById("semanalStatus").value),
    };

    if (
        !payload.data_prevista ||
        !payload.data_pagamento ||
        !payload.valor ||
        !payload.valor_pago ||
        !payload.status_id
    ) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Preencha todos os campos obrigatórios.'
        });
        return;
    }

    try {

        const abaDocumentosAtiva = document.querySelector(
            '#tabDocumentos.active.show'
        );

        // ==========================
        // PRIMEIRA ETAPA - SALVA DADOS
        // ==========================
        if (!abaDocumentosAtiva) {

            let response;

            if (modo === "inserir") {

                response = await api.post(
                    "/api/semanais/create",
                    payload
                );

                // ajuste conforme retorno da sua API
                const novoId =
                    response?.data?.resultado?.id ||
                    response?.data?.data?.resultado?.id;

                if (novoId) {
                    id = novoId;
                    this.dataset.id = novoId;
                    this.dataset.modo = "editar";
                }

            } else {

                await api.put(
                    `/api/semanais/update/${id}`,
                    payload
                );

            }

            // vai para aba documentos
            const abaDocumentos = document.querySelector(
                '#tabsSemanal [data-bs-target="#tabDocumentos"]'
            );

            bootstrap.Tab
                .getOrCreateInstance(abaDocumentos)
                .show();

            // guarda o id para upload
            document.getElementById("btEnviarArquivo").dataset.semanalId = id;

            // altera texto do botão
            this.innerHTML = `
                <i class="bi bi-check-circle me-1"></i>
                Finalizar
            `;

            Swal.fire({
                icon: 'success',
                title: 'Dados salvos',
                text: 'Agora envie o documento da semanal.',
                timer: 2000,
                showConfirmButton: false
            });

            return;
        }

        // ==========================
        // SEGUNDA ETAPA - FINALIZA
        // ==========================

        bootstrap.Modal
            .getInstance(document.getElementById("modalSemanal"))
            .hide();

        iniciarSemanal();

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Semanal salva com sucesso!',
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

$(document).on('click', '.btn-excluir-semanais', async function () {
    const id = $(this).data('id');
    console.log(id);
    try {    
        document.getElementById("btConfirmarExcluir").dataset.id = id;
        modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalExcluir"));
        modalFrotaInstancia.show();
    } catch (err) {
        console.error("Erro ao excluir semanal:", err);
    }
});

$(document).on('click', '#btConfirmarExcluir', async function () {

    const id = this.dataset.id;

    try {

        await api.get(`/api/semanais/ativaDesativa/${id}?ativa=0`);

        bootstrap.Modal.getInstance(document.getElementById("modalExcluir")).hide();

        iniciarSemanal();

        Swal.fire({ icon: 'success', title: 'Excluído!', text: 'Semanal excluído com sucesso.', timer: 2000, showConfirmButton: false });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir o Semanal.' });
    }

});

$(document).on('click', '#btnGerarSemanais', async function () {

    // abre loading
    document.getElementById('loadingModal').style.display = 'flex';

    const hoje = new Date();

    const payload = {
        status_id: 1,
        ano: hoje.getFullYear(),
        mes: hoje.getMonth() + 1
    };

    try {
        const response = await api.post("/api/semanais/automatico", payload);

        console.log("gerando semanais", payload);

        // mensagem sucesso
        Swal.fire({
            icon: 'success',
            title: 'Sucesso!',
            text: 'Semanais gerados com sucesso!',
            confirmButtonColor: '#FFC107'
        });
        iniciarSemanal();

    } catch (error) {
        console.error(error);

        Swal.fire({
            icon: 'error',
            title: 'Erro!',
            text: 'Não foi possível gerar os semanais.',
            confirmButtonColor: '#d33'
        });

    } finally {
        // sempre fecha o loading
        document.getElementById('loadingModal').style.display = 'none';
    }
});

$('#semanalTableLista').on('search.dt', function () {
    const table = $('#semanalTableLista').DataTable();
    localStorage.setItem('searchSemanais', table.search());
});


function carregarArquivosSemanal(anexo) {

    const tbody = document.getElementById('listaArquivosSemanal');

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
                    onclick="baixarArquivo('semanal',${anexo.id})"
                    title="Baixar arquivo"
                >
                    <i class="bi bi-download"></i>
                </button>
    
                <button
                    class="btn btn-sm btn-danger"
                    onclick="excluirArquivo(${anexo.id}, () => atualizarTabelaSemanal(${anexo.entidade_id}))"
                    title="Excluir arquivo"
                >
                    <i class="bi bi-trash"></i>
                </button>
    
            </td>
        </tr>
    `;
}


let arquivoSelecionado = null;

// habilita botão ao selecionar arquivo
$(document).on('change', '#semanalArquivo', function () {

    const possuiArquivo = this.files.length > 0;

    $('#btEnviarArquivo').prop(
        'disabled',
        !possuiArquivo
    );

});

$(document).on('click', '#btEnviarArquivo', async function () {

    const semanalId = this.dataset.semanalId;
    const franquia_franquiador_locatario_id = this.dataset.franquia_franquiador_locatario_id;

    const arquivo = document.getElementById("semanalArquivo").files[0];

    if (!arquivo) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Selecione um arquivo para enviar.'
        });
        return;
    }

    try {

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
            `/api/anexos/listar?tipo=semanal&codigo=${semanalId}`
        );

        const formData = new FormData();
        formData.append("file", arquivo);
        formData.append("entidade_tipo", "semanal");
        formData.append("entidade_id", semanalId);
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
            `/api/anexos/listar?tipo=semanal&codigo=${semanalId}`
        );
    

        if (reposta.data.resultado?.length) {
            carregarArquivosSemanal(reposta.data.resultado[0]);
            iniciarSemanal();
        }

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Comprovante anexado com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

        document.getElementById("semanalArquivo").value = "";
        $('#btEnviarArquivo').prop('disabled', true);

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




async function atualizarTabelaSemanal(idSemanal) {

    const response = await api.get(
        `/api/anexos/listar?tipo=semanal&codigo=${idSemanal}`
    );

    carregarArquivosSemanal(response.data.resultado);
    iniciarSemanal()
}