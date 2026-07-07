

/*
|--------------------------------------------------------------------------
| FROTA
|--------------------------------------------------------------------------
*/

/*
|--------------------------------------------------------------------------
| AUTOCOMPLETE DE PLACAS
|--------------------------------------------------------------------------
*/



async function carregarCores() {

    const select = document.getElementById("selectCor");

    if (!select) return;

    try {

        const response = await api.get("/api/frota/listar");
        const frotas   = response.data.resultado;
        // Remove duplicatas
        const cores = [...new Set(frotas.map(f => f.cor).filter(Boolean))];

        cores.forEach((cor) => {
            const option = document.createElement("option");
            option.value = cor;
            option.textContent = cor;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar cores:", err);
    }

}

async function carregarAnos() {

    const select = document.getElementById("selectAno");

    if (!select) return;

    try {

        const response = await api.get("/api/frota/listar");
        const frotas   = response.data.resultado;

        // Remove duplicatas e ordena do mais recente ao mais antigo
        const anos = [...new Set(frotas.map(f => f.ano).filter(Boolean))].sort((a, b) => b - a);

        anos.forEach((ano) => {
            const option = document.createElement("option");
            option.value = ano;
            option.textContent = ano;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar anos:", err);
    }

}
async function carregarStatus() {

    const select = document.getElementById("selectStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/frota/listar");
        const frotas   = response.data.resultado;

        // Remove duplicatas pelo status_id
        const vistos = new Set();

        frotas
            .filter(f => f.status_id && f.status)
            .forEach((frota) => {

                if (vistos.has(frota.status_id)) return;
                vistos.add(frota.status_id);

                const option = document.createElement("option");
                option.value = frota.status_id;
                option.textContent = frota.status;
                select.appendChild(option);

            });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}

async function iniciarFrota(filtros = {}) {

    const grid = document.querySelector(".row.g-4");

    grid.innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <p class="mt-3 text-muted">Carregando frotas...</p>
        </div>
    `;

    try {

        // Monta os params ignorando valores vazios
        const params = new URLSearchParams();

        if (filtros.status)     params.append("status",     filtros.status);
        if (filtros.franquiado) params.append("franquiado", filtros.franquiado);
        if (filtros.placa)      params.append("placa",      filtros.placa);
        if (filtros.cor)        params.append("cor",        filtros.cor);
        if (filtros.ano)        params.append("ano",        filtros.ano);

        const query    = params.toString() ? `?${params.toString()}` : "";
        const response = await api.get(`/api/frota/listar${query}`);
        const frotas   = response.data.resultado;

        if (!frotas.length) {

            grid.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-motorcycle fs-1 text-muted"></i>
                    <p class="mt-3 text-muted">Nenhuma frota encontrada.</p>
                </div>
            `;

            return;

        }

        grid.innerHTML = frotas.map((frota) => cardFrota(frota)).join("");

    } catch (err) {

        console.error(err);

        grid.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-exclamation-triangle fs-1 text-danger"></i>
                <p class="mt-3 text-danger">Erro ao carregar frotas.</p>
            </div>
        `;

    }

}

/*
|--------------------------------------------------------------------------
| CARD
|--------------------------------------------------------------------------
*/

function cardFrota(frota) {

    const alugada  = frota.status_id === 2;
    const badge    = alugada ? "bg-danger" : "bg-success";
    const locatario = alugada
        ? `<div class="text-danger small fw-bold mt-1"> ${frota.nome_locatario ?? "Sem locatário"}</div>`
        : `<div class="small fw-bold mt-1 invisible">Locatário: -</div>`;

    return `
        <div class="col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <div 
                class="card shadow-lg rounded-4 border-2 overflow-hidden w-100"
                style="cursor:pointer;"
                onclick="abrirModalFrota(${frota.id})"
            >
                <div class="card-body text-center">

                    <!-- DADOS -->
                    <div class="mb-3">
                        <div class="fw-bold small">RENAVAM: ${frota.renavam}</div>
                        <div class="text-muted small">Ano: ${frota.ano}</div>
                        <div class="text-muted small">Cor: ${frota.cor}</div>
                        ${locatario}
                    </div>

                    <!-- PLACA MERCOSUL -->
                    <div class="mercosul-plate mx-auto">
                        <div class="plate-top">
                            <div class="plate-country">
                                <img 
                                    src="https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg"
                                    alt="Brasil"
                                    class="flag-br"
                                >
                                <span>BRASIL</span>
                            </div>
                        </div>
                        <div class="plate-number">${frota.placa}</div>
                        <div class="plate-br">BR</div>
                    </div>

                    <!-- STATUS -->
                    <div class="mt-3">
                        <span class="badge ${badge}">${frota.status}</span>
                    </div>

                </div>
            </div>
        </div>
    `;

}



/*
|--------------------------------------------------------------------------
| BOTÃO FILTRAR
|--------------------------------------------------------------------------
*/

function iniciarBotaoFiltrar() {

    const botao  = document.getElementById("filtrarFrotas");
    const limpar = document.getElementById("limparFiltros");

    if (botao) {
        botao.addEventListener("click", () => {

            const filtros = {
                status:     document.getElementById("selectStatus")?.value     || null,
                franquiado: document.querySelector("select.form-select.rounded-4")?.value || null,
                placa:      document.getElementById("inputPlaca")?.value       || null,
                cor:        document.getElementById("selectCor")?.value        || null,
                ano:        document.getElementById("selectAno")?.value        || null,
            };

            iniciarFrota(filtros);

        });
    }

    if (limpar) {
        limpar.addEventListener("click", () => {

            // Reseta todos os campos
            const selectStatus     = document.getElementById("selectStatus");
            const selectCor        = document.getElementById("selectCor");
            const selectAno        = document.getElementById("selectAno");
            const inputPlaca       = document.getElementById("inputPlaca");
            const selectFranquiado = document.querySelector("select.form-select.rounded-4");

            if (selectStatus)     selectStatus.value     = "";
            if (selectCor)        selectCor.value        = "";
            if (selectAno)        selectAno.value        = "";
            if (inputPlaca)       inputPlaca.value       = "";
            if (selectFranquiado && !selectFranquiado.disabled) {
                selectFranquiado.value = "";
            }

            // Recarrega sem filtros
            iniciarFrota();

        });
    }

}



/*
|--------------------------------------------------------------------------
| LISTENER BOTÃO NOVA FROTA
|--------------------------------------------------------------------------
*/

function iniciarBotaoNovaFrota() {


    const btn = document.getElementById("btnNovaFrota");

    if (!btn) return;

    btn.addEventListener("click", () => abrirModalNovaFrota());

}

/*
|--------------------------------------------------------------------------
| INSTÂNCIA DO MODAL
|--------------------------------------------------------------------------
*/

let modalFrotaInstancia = null;

/*
|--------------------------------------------------------------------------
| ABRIR MODAL — NOVA FROTA
|--------------------------------------------------------------------------
*/


function abrirModalNovaFrota() {

    console.log("nova frota");
    const tabFrotaDados = document.querySelector('#tabsFrota [data-bs-target="#tabFrotaDados"]');
    bootstrap.Tab.getOrCreateInstance(tabFrotaDados).show();
    document.getElementById("tituloCadastroFrota").textContent = "Inserir Dados da Frota";
    document.getElementById("locatario").style.display         = "none";

    document.querySelector("#modalFrota form").reset();

    document.getElementById("modalFrotaAno").value    = new Date().getFullYear();
    document.getElementById("modalFrotaModelo").value = new Date().getFullYear();

    document.getElementById("btSalvar").dataset.frotaId = "";
    document.getElementById("btSalvar").dataset.modo    = "inserir";

    carregarFranqueados("selectFranquiadoModal", false); 
    carregarFrotaStatusModal();

    modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalFrota"));
    modalFrotaInstancia.show();

}

/*
|--------------------------------------------------------------------------
| ABRIR MODAL
|--------------------------------------------------------------------------
*/

async function abrirModalFrota(id) {
    console.log("abrirModalFrota");

    const tabFrotaDados = document.querySelector('#tabsFrota [data-bs-target="#tabFrotaDados"]');
    bootstrap.Tab.getOrCreateInstance(tabFrotaDados).show();

    document.getElementById("tituloCadastroFrota").textContent = "Alterar Dados da Frota";
    document.getElementById("locatario").style.display = "block";

    // Guarda o ID para usar no salvar
    document.getElementById("btSalvar").dataset.frotaId = id;
    document.getElementById("btSalvar").dataset.modo    = "editar";

    await carregarFrotaStatusModal();
    await carregarFranqueados("selectFranquiadoModal", false); 



    modalFrotaInstancia = new bootstrap.Modal(document.getElementById("modalFrota"));
    modalFrotaInstancia.show();

    try {

        const response = await api.get(`/api/frota/listar?id=${id}`);
        const frota    = response.data.resultado[0];

        document.getElementById("btEnviarDocumentoFrota").dataset.frotaId = id;
        document.getElementById("btnAbaDocumentosFrotaCustos").dataset.frotaId = id;

        document.getElementById("modalFrotaPlaca").value            = frota.placa    || "";
        document.getElementById("modalFrotaRenavam").value          = frota.renavam  || "";
        document.getElementById("modalFrotaAno").value              = frota.ano      || "";
        document.getElementById("modalFrotaModelo").value           = frota.modelo   || "";
        document.getElementById("modalFrotaCor").value              = frota.cor      || "";
        document.getElementById("selectFranquiadoModal").value      = frota.fraqueado_id || "";
        document.getElementById("modalFrotaStatus").value           = frota.status_id    || "";


        // Locatário
        const inputLocatario = document.querySelector("#locatario input");
        if (inputLocatario) inputLocatario.value = frota.nome_locatario || "Sem locatário";

        const responseAnexo = await api.get(`/api/anexos/listar?tipo=frota&codigo=${id}`);
        const anexo   = responseAnexo.data.resultado;
        carregarArquivosFrotas(anexo);

    } catch (err) {
        console.error("Erro ao carregar dados da frota:", err);
        alert("Erro ao carregar dados da frota.");
    }

}

/*
|--------------------------------------------------------------------------
| LIMPAR BACKDROP AO FECHAR
|--------------------------------------------------------------------------
*/

function iniciarEventosModal() {

    const modalEl = document.getElementById("modalFrota");

    if (!modalEl) return;

    modalEl.addEventListener("hidden.bs.modal", () => {

        // Remove backdrop residual
        document.querySelectorAll(".modal-backdrop").forEach(el => el.remove());
        document.body.classList.remove("modal-open");
        document.body.style.removeProperty("overflow");
        document.body.style.removeProperty("padding-right");

        modalFrotaInstancia = null;

    });

}

/*
|--------------------------------------------------------------------------
| CARREGAR FRANQUEADOS NO MODAL
|--------------------------------------------------------------------------
*/

async function carregarFranqueadosModal() {

    const select = document.getElementById("selectFranquiadoModal");

    if (!select) return;

    try {

        const response  = await api.get("/api/franquiado/listar");
        const franqueados = response.data.resultado;

        /*
        |--------------------------------------------------------------------------
        | APENAS 1 FRANQUEADO — bloqueia e já seleciona
        |--------------------------------------------------------------------------
        */

        if (franqueados.length === 1) {

            select.innerHTML = `<option value="${franqueados[0].id}">${franqueados[0].nome}</option>`;
            select.disabled  = true;
            return;

        }

        /*
        |--------------------------------------------------------------------------
        | MAIS DE 1 — exibe opção padrão + lista
        |--------------------------------------------------------------------------
        */

        select.innerHTML  = `<option value="" selected disabled>Selecione o franquiado</option>`;
        select.disabled   = false;

        franqueados.forEach((franqueado) => {
            const option       = document.createElement("option");
            option.value       = franqueado.id;
            option.textContent = franqueado.nome;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar franqueados no modal:", err);
    }

}

async function carregarFrotaStatusModal() {
    const select = document.getElementById("modalFrotaStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/frota/status");
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

/*
|--------------------------------------------------------------------------
| SALVAR — INSERIR OU ALTERAR
|--------------------------------------------------------------------------
*/

async function salvarFrota() {

    const btn = document.getElementById("btSalvar");

    if (!btn) return;

    btn.addEventListener("click", async () => {

        const modo = btn.dataset.modo;
        const id   = btn.dataset.frotaId;

        const payload = {
            placa:        document.getElementById("modalFrotaPlaca")?.value.trim()          || null,
            renavam:      document.getElementById("modalFrotaRenavam")?.value.trim()        || null,
            ano:          parseInt(document.getElementById("modalFrotaAno")?.value)         || null,
            modelo:       parseInt(document.getElementById("modalFrotaModelo")?.value)      || null,
            cor:          document.getElementById("modalFrotaCor")?.value.trim()            || null,
            fraqueado_id: parseInt(document.getElementById("selectFranquiadoModal")?.value) || null,
            status_id:    parseInt(document.getElementById("modalFrotaStatus")?.value)      || null,
        };

        /*
        |--------------------------------------------------------------------------
        | VALIDAÇÃO
        |--------------------------------------------------------------------------
        */

        const obrigatorios = ["placa", "renavam", "ano", "modelo", "cor", "fraqueado_id", "status_id"];
        const faltando     = obrigatorios.filter(campo => !payload[campo]);

        if (faltando.length) {
            alert("Preencha todos os campos obrigatórios.");
            return;
        }

        /*
        |--------------------------------------------------------------------------
        | LOADING
        |--------------------------------------------------------------------------
        */

        btn.disabled  = true;
        btn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Salvando...`;

        try {
            console.log(modo);
            if (modo === "inserir") {
                await api.post("/api/frota/create", payload);
            } else {
                await api.put(`/api/frota/update/${id}`, payload);
            }

            // modalFrotaInstancia?.hide();


            // vai para aba documentos
            const abaDocumentos = document.querySelector(
                '#tabsFrota [data-bs-target="#tabFrotaDocumentos"]'
            );

            bootstrap.Tab
                .getOrCreateInstance(abaDocumentos)
                .show();

            // guarda o id para upload
            document.getElementById("btEnviarDocumentoFrota").dataset.frotaId = id;

            Swal.fire({
                icon: 'success',
                title: 'Dados salvos',
                text: 'Assim que possivel adicione os documentos da frota',
                timer: 2000,
                showConfirmButton: false
            });

            iniciarFrota();
            return;


        } catch (err) {

            console.error("Erro ao salvar frota:", err);
            alert("Erro ao salvar. Tente novamente.");

        } finally {

            btn.disabled  = false;
            btn.innerHTML = "Salvar Alterações";

        }

    });

}

function iniciarAbasFrota() {

    const btnSalvar = document.getElementById("btSalvar");

    if (!btnSalvar) return;

    const abaDados = document.querySelector(
        '#tabsFrota [data-bs-target="#tabFrotaDados"]'
    );

    const abaDocumentos = document.querySelector(
        '#tabsFrota [data-bs-target="#tabFrotaDocumentos"]'
    );

    const abaCustos = document.querySelector(
        '#tabsFrota [data-bs-target="#tabFrotaCustos"]'
    );

    abaDados.addEventListener("shown.bs.tab", () => {
        btnSalvar.classList.remove("d-none");
    });

    abaDocumentos.addEventListener("shown.bs.tab", () => {
        btnSalvar.classList.add("d-none");
    });

    abaCustos.addEventListener("shown.bs.tab", () => {
        btnSalvar.classList.add("d-none");
    });

}

// habilita botão ao selecionar arquivo
$(document).on('change', '#frotaTipoDocumento, #frotaArquivo', function () {
    const tipoDocumento = document.getElementById("frotaTipoDocumento").value;
    const arquivo = document.getElementById("frotaArquivo").files.length;
    console.log("tipoDocumento",tipoDocumento);
    console.log("arquivo",arquivo);

    const possuiArquivo = arquivo > 0 && tipoDocumento!=="";

    $('#btEnviarDocumentoFrota').prop(
        'disabled',
        !possuiArquivo
    );

});

$(document).on('click', '#btEnviarDocumentoFrota', async function () {
    const frotaID = this.dataset.frotaId;
    const tipo = document.getElementById("frotaTipoDocumento").value;
    const parcela = document.getElementById("frotaNumeroDocumento").value;
    const arquivo = document.getElementById("frotaArquivo").files[0];

    if (!arquivo) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Selecione um arquivo para enviar.'
        });
        return;
    }
    try {
        const urltipo = parcela > 0 ? `frota-${tipo}-parcela-${parcela}` : `frota-${tipo}`;

        Swal.fire({
            title: 'Enviando '+tipo+'...',
            text: 'Aguarde alguns instantes.',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
        const response = await api.get(
            `/api/anexos/listar?tipo=${urltipo}&codigo=${frotaID}`
        );
        
        const formData = new FormData();
        formData.append("file", arquivo);
        formData.append("entidade_tipo", urltipo);
        formData.append("entidade_id", frotaID);
        console.log("atualizado");

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
            `/api/anexos/listar?tipo=frota&codigo=${frotaID}`
        );
    

        if (reposta.data.resultado?.length) {
            carregarArquivosFrotas(reposta.data.resultado);
            iniciarFrota();
        }

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Comprovante anexado com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

        document.getElementById("frotaArquivo").value = "";
        $('#btEnviarDocumentoFrota').prop('disabled', true);
    } catch (error) {

        // console.log(JSON.stringify(error) );
        console.log("ERRO COMPLETO:", JSON.stringify(error.response));
        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: error?.response?.data?.detail ||
                  'Não foi possível anexar o comprovante.'
        });

    }


});

function carregarArquivosFrotas(anexos) {

    const tbody = document.getElementById('listaDocumentosFrota');

    if (!anexos || anexos.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-3">
                    Nenhum documento inserido
                </td>
            </tr>
        `;

        return;
    }

    let html = '';

    anexos.forEach((anexo) => {

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

        const nomeArquivo =
            `${anexo.entidade_tipo}.${extensao}`;
//         const nomeArquivo = `${anexo.entidade_tipo}_${anexo.entidade_id}_${anexo.id}.${extensao}`;
        html += `
            <tr>
                <td>${nomeArquivo}</td>

                <td class="d-none d-lg-table-cell">
                ${descricao}
                </td>
            
                <td class="d-none d-lg-table-cell">
                    ${dataFormatada}
                </td>

                <td class="text-center">

                    <button
                        class="btn btn-sm btn-primary me-1"
                        onclick="baixarArquivo('frota',${anexo.id})"
                        title="Baixar arquivo">
                        <i class="bi bi-download"></i>
                    </button>

                    <button
                        class="btn btn-sm btn-danger"
                        onclick="excluirArquivo(${anexo.id}, () => atualizarTabelaFrota(${anexo.entidade_id}))"
                        title="Excluir arquivo">
                        <i class="bi bi-trash"></i>
                    </button>

                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

async function atualizarTabelaFrota(idFrota) {

    const response = await api.get(
        `/api/anexos/listar?tipo=frota&codigo=${idFrota}`
    );
    carregarArquivosFrotas(response.data.resultado);
    iniciarFrota();
}
