const API_BASE = 'http://localhost:3001';

// ============================================================
//  INICIAR LOCATÁRIOS (listagem + filtros)
// ============================================================

async function iniciarLocatario(filtros = { status: "1" }) {

    const grid = document.querySelector(".row.g-4");

    grid.innerHTML = `
        <div class="col-12 text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <p class="mt-3 text-muted">Carregando locatários...</p>
        </div>
    `;

    try {

        const params = new URLSearchParams();

        if (filtros.status)     params.append("status",     filtros.status);
        if (filtros.placa)      params.append("placa",      filtros.placa);
        if (filtros.plano)      params.append("plano",      filtros.plano);
        if (filtros.nome)       params.append("nome",       filtros.nome);
        if (filtros.cpf)        params.append("cpf",        filtros.cpf);
        if (filtros.dataInicio) params.append("dataInicio", filtros.dataInicio);
        if (filtros.dataFim)    params.append("dataFim",    filtros.dataFim);

        const query    = params.toString() ? `?${params.toString()}` : "";
        const response = await api.get(`/api/locatarios/listar${query}`);
        const locatarios = response.data.resultado;

        console.log(locatarios);

        if (!locatarios.length) {

            grid.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-motorcycle fs-1 text-muted"></i>
                    <p class="mt-3 text-muted">Nenhum locatário encontrado.</p>
                </div>
            `;

            return;

        }

        grid.innerHTML = locatarios.map((locatario) => cardLocatarios(locatario)).join("");

    } catch (err) {

        console.error(err);

        grid.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-exclamation-triangle fs-1 text-danger"></i>
                <p class="mt-3 text-danger">Erro ao carregar locatários.</p>
            </div>
        `;

    }

}

// ============================================================
//  CARD
// ============================================================

function cardLocatarios(locatario) {

    console.log("id:" + locatario.id);

    const ativo   = locatario.status_id === 1;
    const bgativo = ativo ? "bg-success" : "bg-danger";

    return `
        <div class="col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">

            <div
                class="card shadow-lg rounded-4 border-2 overflow-hidden h-100 cliente-card"
                data-bs-toggle="modal"
                data-bs-target="#modalLocatario"
                style="cursor:pointer;"
                onclick="abrirModalLocatario(${locatario.id},${locatario.user_locatario_id})"
            >

                <div class="bg-dark text-white text-center py-3">
                    <div class="fw-bold small">${locatario.nome}</div>
                    <div class="small opacity-75">CPF: ${locatario.cpf}</div>
                </div>

                <div class="card-body">

                    <div class="mercosul-plate mx-auto mb-4">
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
                        <div class="plate-number">${locatario.placa}</div>
                        <div class="plate-br">BR</div>
                    </div>

                    <div class="d-flex flex-column gap-2">

                        <div class="d-flex justify-content-between">
                            <span class="text-muted">Plano</span>
                            <span class="fw-bold">${locatario.plano}</span>
                        </div>

                        <div class="d-flex justify-content-between">
                            <span class="text-muted">Pgto:</span>
                            <span class="fw-bold">${locatario.dia_semana}</span>
                        </div>

                    </div>

                </div>

                <div class="card-footer bg-white border-0 pb-4 text-center">
                    <span class="badge ${bgativo} px-4 py-2 rounded-pill">
                        ${ativo ? "Ativo" : "Inativo"}
                    </span>
                </div>

            </div>

        </div>
    `;

}

// ============================================================
//  CARREGAR SELECTS (filtros e modal)
// ============================================================

async function carregarPlanos() {

    const select = document.getElementById("selectPlanos");
    if (!select) return;

    try {

        const response   = await api.get("/api/locatarios/listar");
        const locatarios = response.data.resultado;

        const vistos = new Set();
        const planos = locatarios
            .filter(p => p.plano_id && p.plano)
            .filter(p => {
                if (vistos.has(p.plano_id)) return false;
                vistos.add(p.plano_id);
                return true;
            });

        planos.forEach((p) => {
            const option       = document.createElement("option");
            option.value       = p.plano_id;
            option.textContent = p.plano;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar planos:", err);
    }

}

async function carregarStatusLocatario() {

    const select = document.getElementById("selectStatus");
    if (!select) return;

    try {

        const response   = await api.get("/api/locatarios/listar");
        const locatarios = response.data.resultado;

        const vistos = new Set();
        const status = locatarios
            .filter(s => s.status_id && s.status)
            .filter(s => {
                if (vistos.has(s.status_id)) return false;
                vistos.add(s.status_id);
                return true;
            })
            .sort((a, b) => a.status.localeCompare(b.status));

        status.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.status_id;
            option.textContent = s.status;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar os status:", err);
    }

}

async function carregarPlanosModal() {

    const select = document.getElementById("modalLocatarioPlano");
    if (!select) return;

    try {

        const response = await api.get("/api/filtros/planos");
        const planos   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione o plano</option>`;

        planos.forEach((plano) => {
            const option       = document.createElement("option");
            option.value       = plano.id;
            option.textContent = plano.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar planos:", err);
    }

}

async function carregarFrotasModal(apenasDisponiveis = true) {

    const select = document.getElementById("modalLocatarioFrota");
    if (!select) return;

    try {

        const url      = apenasDisponiveis ? "/api/frota/listar?status=1" : "/api/frota/listar";
        const response = await api.get(url);
        const frotas   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione a frota</option>`;

        frotas.forEach((frota) => {
            const option       = document.createElement("option");
            option.value       = frota.id;
            option.textContent = frota.placa_formatado || frota.placa;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar frotas:", err);
    }

}

// ============================================================
//  FILTROS
// ============================================================

function iniciarBotaoFiltrarLocatarios() {

    const botao  = document.getElementById("filtrarLocatarios");
    const limpar = document.getElementById("limparFiltros");

    if (botao) {
        botao.addEventListener("click", () => {

            const filtros = {
                status:     document.getElementById("selectStatus")?.value || null,
                franquiado: document.querySelector("select.form-select.rounded-4")?.value || null,
                placa:      document.getElementById("inputPlaca")?.value
                                ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                                : null,
                nome:       document.getElementById("inputNome")?.value        || null,
                cpf:        document.getElementById("inputCpf")?.value         || null,
                plano:      document.getElementById("selectPlanos")?.value     || null,
                dataInicio: document.getElementById("inputDataInicial")?.value || null,
                dataFim:    document.getElementById("inputDataFinal")?.value   || null,
            };

            iniciarLocatario(filtros);

        });
    }

    if (limpar) {
        limpar.addEventListener("click", () => {

            const selectStatus     = document.getElementById("selectStatus");
            const selectFranquiado = document.querySelector("select.form-select.rounded-4");
            const inputPlaca       = document.getElementById("inputPlaca");
            const inputNome        = document.getElementById("inputNome");
            const inputCpf         = document.getElementById("inputCpf");
            const selectPlanos     = document.getElementById("selectPlanos");
            const inputDataInicial = document.getElementById("inputDataInicial");
            const inputDataFinal   = document.getElementById("inputDataFinal");

            if (selectStatus)     selectStatus.value = "";
            if (selectFranquiado && !selectFranquiado.disabled) selectFranquiado.value = "";
            if (inputPlaca)       inputPlaca.value   = "";
            if (inputNome)        inputNome.value    = "";
            if (inputCpf)         inputCpf.value     = "";
            if (selectPlanos)     selectPlanos.value = "";
            if (inputDataInicial) inputDataInicial.value = "";
            if (inputDataFinal)   inputDataFinal.value   = "";

            iniciarLocatario();

        });
    }

}

// ============================================================
//  MODAL — INSTÂNCIA E EVENTOS
// ============================================================

let modalLocatarioInstancia = null;

function iniciarEventosModalLocatario() {

    const modalEl = document.getElementById("modalLocatario");
    if (!modalEl) return;

    modalEl.addEventListener("hidden.bs.modal", () => {

        document.querySelectorAll(".modal-backdrop").forEach(el => el.remove());
        document.body.classList.remove("modal-open");
        document.body.style.removeProperty("overflow");
        document.body.style.removeProperty("padding-right");

        modalLocatarioInstancia = null;

    });

}

// ============================================================
//  BOTÃO NOVO LOCATÁRIO
// ============================================================

function iniciarBotaoNovoLocatario() {

    const btn = document.getElementById("btnNovoLocatario");
    if (!btn) return;

    btn.addEventListener("click", () => abrirModalNovoLocatario());

}

function abrirModalNovoLocatario() {

    document.querySelector("#modalLocatario .modal-title").textContent = "Inserir Dados do Locatário";
    document.querySelector("#modalLocatario form").reset();

    // Marca o botão como modo "novo"
    const btSalvar = document.getElementById("btSalvarLocatario");
    btSalvar.dataset.modo        = "novo";
    btSalvar.dataset.locatarioId = "";

    carregarFranqueados("modalLocatarioFranquiado", false);
    carregarFrotasModal(true);
    carregarPlanosModal();

    modalLocatarioInstancia = new bootstrap.Modal(document.getElementById("modalLocatario"));
    modalLocatarioInstancia.show();

}

// ============================================================
//  ABRIR MODAL — ALTERAR LOCATÁRIO
// ============================================================

async function abrirModalLocatario(id, user_locatario_id) {

    const tabLocatarioDados = document.querySelector('#tabsLocatario [data-bs-target="#tabLocatarioDados"]');
    bootstrap.Tab.getOrCreateInstance(tabLocatarioDados).show();

    document.querySelector("#modalLocatario .modal-title").textContent = "Alterar Dados do Locatário";

    const btSalvar = document.getElementById("btSalvarLocatario");
    btSalvar.dataset.locatarioId = id;
    btSalvar.dataset.user_locatario_id = user_locatario_id;
    btSalvar.dataset.modo        = "editar";

    await carregarFranqueados("modalLocatarioFranquiado", false);
    await carregarFrotasModal(false);
    await carregarPlanosModal();

    modalLocatarioInstancia = new bootstrap.Modal(document.getElementById("modalLocatario"));
    modalLocatarioInstancia.show();

    try {

        const response  = await api.get(`/api/locatarios/listar?id=${id}`);
        const locatario = response.data.resultado[0];
        
        console.log(locatario);
        btSalvar.dataset.franquia_franquiador_locatario_id = locatario.franquia_franquiador_locatario_id;
        document.getElementById("btEnviarDocumentoLocatario").dataset.franquia_franquiador_locatario_id = locatario.franquia_franquiador_locatario_id;
        document.getElementById("btEnviarDocumentoLocatario").dataset.locatarioId = id;
        document.getElementById("btnAbaLocatarioMultas").dataset.locatarioId = id;

        document.getElementById("statusLocatario").checked          = locatario.status_id === 1;
        document.getElementById("modalLocatarioFranquiado").value   = locatario.fraqueado_id         || "";
        document.getElementById("modalLocatarioNome").value         = locatario.nome                 || "";
        document.getElementById("modalLocatarioEmail").value        = locatario.email                || "";
        document.getElementById("modalLocatarioCpf").value          = locatario.cpf                  || "";
        document.getElementById("modalLocatarioCnh").value          = locatario.cnh                  || "";
        document.getElementById("modalLocatarioDataContrato").value = locatario.data_inicio_contrato || "";
        document.getElementById("modalLocatarioCep").value          = locatario.cep                  || "";
        document.getElementById("modalLocatarioEndereco").value     = locatario.endereco             || "";
        document.getElementById("modalLocatarioNumero").value       = locatario.numero               || "";
        document.getElementById("modalLocatarioComplemento").value  = locatario.complemento          || "";
        document.getElementById("modalLocatarioCidade").value       = locatario.cidade               || "";
        document.getElementById("modalLocatarioUf").value           = locatario.uf                   || "";
        document.getElementById("modalLocatarioFrota").value        = locatario.frota_id             || "";
        document.getElementById("modalLocatarioPlano").value        = locatario.plano_id             || "";

        // Senha sempre em branco ao editar
        document.getElementById("senhaLocatario").value          = "";
        document.getElementById("confirmarSenhaLocatario").value = "";

        const responseAnexo = await api.get(`/api/anexos/listar?tipo=locatario&codigo=${id}`);
        const anexo   = responseAnexo.data.resultado;
        carregarArquivosLocatarios(anexo);

    } catch (err) {
        console.error("Erro ao carregar dados do locatário:", err);
        alert("Erro ao carregar dados do locatário.");
    }

}

// ============================================================
//  BOTÃO SALVAR — INSERT ou UPDATE
// ============================================================

function iniciarBotaoSalvarLocatario() {

    const btn = document.getElementById("btSalvarLocatario");
    if (!btn) return;

    btn.addEventListener("click", async () => {

        if (!validarFormLocatario()) return;

        const modo = btn.dataset.modo;
        const id   = btn.dataset.locatarioId;
        const franquia_franquiador_locatario_id = btn.dataset.franquia_franquiador_locatario_id;
        const user_locatario_id = btn.dataset.user_locatario_id;
        const payload = montarPayload();
        console.log(JSON.stringify(payload));


        // No update, só envia senha se o usuário preencheu
        if (modo === "editar" && !payload.password) {
            delete payload.password;
        }

        try {

            setBotaoSalvarLoading(true);

            if (modo === "novo") {
                await api.post("/api/user/create", payload);
            } else {
                await api.put(`/api/user/update/${user_locatario_id}?tipo=3`, payload);
                // alert("Locatário atualizado com sucesso!");
            }

            // modalLocatarioInstancia?.hide();

            // vai para aba documentos
            const abaDocumentos = document.querySelector(
                '#tabsLocatario [data-bs-target="#tabLocatarioDocumentos"]'
            );

            bootstrap.Tab
                .getOrCreateInstance(abaDocumentos)
                .show();

            // guarda o id para upload
            document.getElementById("btEnviarDocumentoLocatario").dataset.locatarioId = id;
            document.getElementById("btEnviarDocumentoLocatario").dataset.franquia_franquiador_locatario_id = franquia_franquiador_locatario_id;

            Swal.fire({
                icon: 'success',
                title: 'Dados salvos',
                text: 'Assim que possivel adicione os documentos do locatario',
                timer: 2000,
                showConfirmButton: false
            });

            iniciarLocatario(); // recarrega a listagem

        } catch (err) {

            console.error("Erro ao salvar locatário:", err);
            const msg = err.response?.data?.message ?? err.message ?? "Erro desconhecido.";
            Swal.fire({
                icon: 'error',
                title: 'Erro',
                text: 'Erro ao salvar locatário'+ msg
            });
            // alert("Erro ao salvar: " + msg);

        } finally {

            setBotaoSalvarLoading(false);

        }

    });

}

// ============================================================
//  MONTAR PAYLOAD
// ============================================================

function montarPayload() {

    const senha = document.getElementById("senhaLocatario").value.trim();

    const payload = {
        nome:                 document.getElementById("modalLocatarioNome").value.trim(),
        email:                document.getElementById("modalLocatarioEmail").value.trim(),
        tipoAcessoID:         3, // fixo: locatário
        status:               document.getElementById("statusLocatario").checked ? 1 : 2,
        franqueado_id:        Number(document.getElementById("modalLocatarioFranquiado").value) || null,
        franquia_id:          Number(document.getElementById("modalLocatarioFranquiado").value) || null,
        cpf:                  document.getElementById("modalLocatarioCpf").value.trim(),
        cnh:                  document.getElementById("modalLocatarioCnh").value.trim(),
        endereco:             document.getElementById("modalLocatarioEndereco").value.trim(),
        numero:               document.getElementById("modalLocatarioNumero").value.trim(),
        complemento:          document.getElementById("modalLocatarioComplemento").value.trim(),
        cep:                  document.getElementById("modalLocatarioCep").value.trim(),
        cidade:               document.getElementById("modalLocatarioCidade").value.trim(),
        uf:                   document.getElementById("modalLocatarioUf").value,
        frota_id:             Number(document.getElementById("modalLocatarioFrota").value) || null,
        plano_id:             Number(document.getElementById("modalLocatarioPlano").value) || null,
        data_inicio_contrato: document.getElementById("modalLocatarioDataContrato").value,
    };

    if (senha) payload.password = senha;

    return payload;

}

// ============================================================
//  VALIDAÇÃO
// ============================================================

function validarFormLocatario() {

    const btn  = document.getElementById("btSalvarLocatario");
    const modo = btn.dataset.modo;

    const nome  = document.getElementById("modalLocatarioNome").value.trim();
    const email = document.getElementById("modalLocatarioEmail").value.trim();
    const cpf   = document.getElementById("modalLocatarioCpf").value.trim();
    const senha = document.getElementById("senhaLocatario").value;
    const conf  = document.getElementById("confirmarSenhaLocatario").value;
    const frota = document.getElementById("modalLocatarioFrota").value;
    const plano = document.getElementById("modalLocatarioPlano").value;

    if (!nome)  { alert("Informe o nome do locatário.");   return false; }
    if (!email) { alert("Informe o e-mail do locatário."); return false; }
    if (!cpf)   { alert("Informe o CPF do locatário.");    return false; }

    // Senha obrigatória apenas no novo cadastro
    if (modo === "novo" && !senha) {
        alert("Informe a senha para o novo locatário.");
        return false;
    }

    if (senha && senha !== conf) {
        alert("A senha e a confirmação não coincidem.");
        return false;
    }

    if (!frota) { alert("Selecione a frota.");  return false; }
    if (!plano) { alert("Selecione o plano.");  return false; }

    return true;

}

// ============================================================
//  FEEDBACK VISUAL NO BOTÃO SALVAR
// ============================================================

function setBotaoSalvarLoading(loading) {

    const btn = document.getElementById("btSalvarLocatario");
    if (!btn) return;

    if (loading) {
        btn.disabled   = true;
        btn.innerHTML  = `<span class="spinner-border spinner-border-sm me-2"></span>Salvando...`;
    } else {
        btn.disabled   = false;
        btn.innerHTML  = `Salvar`;
    }

}

// ============================================================
//  TOGGLE SENHA
// ============================================================

function toggleSenha(inputId, btn) {

    const input = document.getElementById(inputId);
    const icon  = btn.querySelector("i");

    if (input.type === "password") {
        input.type     = "text";
        icon.className = "bi bi-eye-slash";
    } else {
        input.type     = "password";
        icon.className = "bi bi-eye";
    }

}

async function buscarCepLocatario() {

    let cep = document.getElementById('modalLocatarioCep').value;
    
    const endereco = document.getElementById('modalLocatarioEndereco');
    const cidade   = document.getElementById('modalLocatarioCidade');
    const uf       = document.getElementById('modalLocatarioUf');

    try {
        endereco.disabled = true;
        cidade.disabled   = true;
        uf.disabled       = true;
   
        // LOADING VISUAL
        endereco.value = 'Carregando...';
        cidade.value   = 'Carregando...';

        const dados = await buscarCep(cep);
        if (!dados) {
            endereco.value = '';
            cidade.value   = '';
            return;
        }
        // PREENCHE CAMPOS
        document.getElementById('modalLocatarioEndereco').value = dados.logradouro || '';

        document.getElementById('modalLocatarioCidade').value = dados.localidade || '';

        document.getElementById('modalLocatarioUf').value = dados.uf || '';

        // FOCO NO NÚMERO
        document.getElementById('modalLocatarioNumero').focus();

    } catch (erro) {

        console.error(erro);

        alert('Erro ao buscar CEP');

    } finally {
        // REABILITA
        endereco.disabled = false;
        cidade.disabled   = false;
        uf.disabled       = false;
    }

}

function iniciarAbasLocatario() {

    const btnSalvar = document.getElementById("btSalvarLocatario");

    if (!btnSalvar) return;

    const abaDados = document.querySelector(
        '#tabsLocatario [data-bs-target="#tabLocatarioDados"]'
    );
    const abaMultas = document.querySelector(
        '#tabsLocatario [data-bs-target="#tabLocatarioMultas"]'
    );
    const abaDocumentos = document.querySelector(
        '#tabsLocatario [data-bs-target="#tabLocatarioDocumentos"]'
    );

    abaDados.addEventListener('shown.bs.tab', () => {
        btnSalvar.classList.remove('d-none');
    });
    abaMultas.addEventListener('shown.bs.tab', () => {
        btnSalvar.classList.add('d-none');
    });
    abaDocumentos.addEventListener('shown.bs.tab', () => {
        btnSalvar.classList.add('d-none');
    });
}

// habilita botão ao selecionar arquivo
$(document).on('change', '#locatarioTipoDocumento, #locatarioArquivo', function () {
    const tipoDocumento = document.getElementById("locatarioTipoDocumento").value;
    const arquivo = document.getElementById("locatarioArquivo").files.length;
    const possuiArquivo = arquivo > 0 && tipoDocumento!=="";

    $('#btEnviarDocumentoLocatario').prop(
        'disabled',
        !possuiArquivo
    );

});

$(document).on('click', '#btEnviarDocumentoLocatario', async function () {
    const locatarioId = this.dataset.locatarioId;
    const franquia_franquiador_locatario_id = this.dataset.franquia_franquiador_locatario_id;
    const tipo = document.getElementById("locatarioTipoDocumento").value;
    const parcela = document.getElementById("locatarioNumeroDocumento").value;
    const arquivo = document.getElementById("locatarioArquivo").files[0];

    // console.log("locatarioId:"+locatarioId);
    // console.log("franquia_franquiador_locatario_id:"+franquia_franquiador_locatario_id);
    // console.log("tipo:"+tipo);
    // console.log("parcela:"+parcela);
    // console.log("arquivo:"+arquivo);
    // return ;

    if (!arquivo) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Selecione um arquivo para enviar.'
        });
        return;
    }
    try {
        const urltipo = parcela > 0 ? `locatario-${tipo}-parte-${parcela}` : `locatario-${tipo}`;

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
            `/api/anexos/listar?tipo=${urltipo}&codigo=${locatarioId}`
        );
        
        const formData = new FormData();
        formData.append("file", arquivo);
        formData.append("entidade_tipo", urltipo);
        formData.append("entidade_id", locatarioId);
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
            `/api/anexos/listar?tipo=locatario&codigo=${locatarioId}`
        );
    

        if (reposta.data.resultado?.length) {
            carregarArquivosLocatarios(reposta.data.resultado);
            iniciarLocatario();
        }

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Comprovante anexado com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

        document.getElementById("locatarioArquivo").value = "";
        $('#btEnviarDocumentoLocatario').prop('disabled', true);
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

function carregarArquivosLocatarios(anexos) {

    const tbody = document.getElementById('listaDocumentosLocatario');

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
                        onclick="baixarArquivo('locatario', ${anexo.id})"
                        title="Baixar arquivo">
                        <i class="bi bi-download"></i>
                    </button>

                    <button
                        class="btn btn-sm btn-danger"
                        onclick="excluirArquivo(${anexo.id}, () => atualizarTabelaLocatario(${anexo.entidade_id}))"
                        title="Excluir arquivo">
                        <i class="bi bi-trash"></i>
                    </button>

                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

async function atualizarTabelaLocatario(idLocatario) {

    const response = await api.get(
        `/api/anexos/listar?tipo=locatario&codigo=${idLocatario}`
    );
    carregarArquivosLocatarios(response.data.resultado);
    iniciarLocatario();
}

