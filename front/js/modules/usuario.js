async function iniciarUsuarios(filtros = {}) {

    const params = new URLSearchParams();

    if (filtros.nome) params.append("nome",filtros.nome);
    if (filtros.email) params.append("email",filtros.email);
    if (filtros.status) params.append("status",filtros.status);
    if (filtros.acesso) params.append("acesso",filtros.acesso);

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/user/listar${query}`);
    let user   = response.data.resultado || [];
    const tipoLogado = Number(window.dadosUsuarioLogado?.tipoAcessoID);
    if (tipoLogado !== 1) {
        user = user.filter((u) => Number(u.tipoAcessoID) !== 1);
    }
    console.log(user);
    // tabela
    if ($('#UsuarioTableLista').length) {

        if ($.fn.DataTable.isDataTable('#UsuarioTableLista')) {
            $('#UsuarioTableLista').DataTable().destroy();
        }
    
        $('#UsuarioTableLista').DataTable({
            data: user,
            columns: [
                {
                    data: 'id',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'nome',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'email',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'setor',
                    defaultContent: '-'
                },
                {
                    data: 'status',
                    render: function(data) {

                        let classe = 'bg-secondary';
                        let status = "";

                        if (data === 1) {
                            classe = 'bg-success';
                            status = "Ativo"
                        }else{
                            classe = 'bg-danger';
                            status = "Inativo"
                        }

                        return `
                            <span class="badge-status ${classe} text-white">
                                ${status}
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
                        let botaoExcluirRestaurar = '';
                        
                        if (row.status_id == 2) {
                            botaoExcluirRestaurar = `
                                <button
                                    class="btn btn-sm btn-success rounded-3 btRestaurarUsuario"
                                    data-id="${row.id}"
                                    title="Restaurar usuario">
                                    <i class="bi bi-arrow-counterclockwise"></i>
                                </button>
                            `;
                        } else {
                            botaoExcluirRestaurar = `
                                <button
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirUsuario"
                                    data-id="${row.id}"
                                    title="Excluir usuario">
                                    <i class="bi bi-trash-fill"></i>
                                </button>
                            `;
                        }
                
                        return `
                            <div class="d-flex gap-2 justify-content-center">
                                <button
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarUsuario"
                                    data-id="${row.id}"
                                    title="Alterar usuario">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                
                                ${botaoExcluirRestaurar}
                            </div>
                        `;
                    }
                }
            ],
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:20
        });
    
    }

}
async function prepararModalUsuario() {
    document.querySelector("#frmModalUsuario").reset();
    filtroSetor("selectModalUsuarioSetor", "");
}
async function filtroSetor(input, tipo) {

    const select = document.getElementById(input);

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/usuarios/acessos");
        const setor   = response.data.resultado;
        if(tipo=='filtro'){
            select.innerHTML = `<option value="">Todos</option>`;
        }else{
            select.innerHTML = `<option value="" selected disabled>Selecione o status</option>`;
        }
        

        setor.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.id;
            option.textContent = s.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
$(document).on('click','#modalNovoUsuario',async function(){
    await prepararModalUsuario();
    $('#selectModalUsuarioSetor').prop('disabled', false);
    $('#inputModalUsuarioEmail').prop('disabled', false);
    carregarFranqueados("selectModalUsuarioFranqueado", false, true);
    ModalManager.abrir("modalUsuario",{acao:"novo"});

});
$(document).on('change', '#selectModalUsuarioSetor', function () {

    document.getElementById("inputModalUsuarioNome").value = "";
    const exibirFranqueado = Number(this.value) === 2;
    const $linha = $('#rowModalUsuarioFranqueado');
    const $franqueado = $('#selectModalUsuarioFranqueado');

    $linha.toggle(exibirFranqueado);

    // Obrigatório somente para o setor 2
    $franqueado.prop('required', exibirFranqueado);

    if (!exibirFranqueado) {
        $franqueado.val('');
    }

});
$(document).on('change', '#selectModalUsuarioFranqueado', function () {

    document.getElementById("inputModalUsuarioNome").value = this.options[this.selectedIndex].text;

});

$(document).on('click','#modalFitrarUsuario',async function(){
    await prepararModalUsuario();
    ModalManager.abrir("modalFiltroUsuario");
    filtroSetor("selectFiltroUsuarioSetor", "filtro");
});
$(document).on('click','#btModalFiltrarUsuario',async function(){
    const filtros = {
        nome: document.getElementById("inputFiltroUsuarioNome")?.value || null,
        email: document.getElementById("inputFiltroUsuarioEmail")?.value   || null,
        acesso: document.getElementById("selectFiltroUsuarioSetor")?.value   || null,
        status: document.getElementById("selectFiltroUsuarioStatus")?.value   || null,
    };
    iniciarUsuarios(filtros);
    ModalManager.fechar("modalFiltroUsuario");
});
$(document).on('click','#btModalRemoverFiltroUsuario',async function(){
    iniciarUsuarios();
    ModalManager.fechar("modalFiltroUsuario");
});

$(document).on('click','.btModalAlterarUsuario',async function(){
    await prepararModalUsuario();

    const usuarioId = this.dataset.id;
    const response  = await api.get(`/api/user/listar?id=${usuarioId}`);
    const user = response.data.resultado[0];
    console.log("franquiado:",user);

    document.getElementById("selectModalUsuarioSetor").value = user.tipoAcessoID || "";
    document.getElementById("selectModalUsuarioStatus").value = user.status || "";
    document.getElementById("inputModalUsuarioNome").value = user.nome || "";
    document.getElementById("inputModalUsuarioEmail").value = user.email || "";
    
    $('#selectModalUsuarioSetor').prop('disabled', true);
    $('#inputModalUsuarioEmail').prop('disabled', true);
    $('#rowModalUsuarioFranqueado').hide();
    ModalManager.abrir("modalUsuario",{
        acao:"editar",
        usuarioId: usuarioId
    });
});
$(document).on('click','.btModalExcluirUsuario',async function(){
    ModalManager.abrir("modalExcluir");
    const usuarioId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/franquiado/ativaDesativa/${usuarioId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarUsuarios();
            Swal.fire({
                icon: 'success',
                title: 'Usuario excluido com sucesso',
                text: 'esses dados são recuperaveis!',
                timer: 2000,
                showConfirmButton: false
            });
    
        } catch (err) {
            console.error(err);
            Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a manutenção.' });
        }
        console.log('Excluir codigos');
    });
});

$(document).on('click', '#btModalSalvarUsuario', async function () {
    const dados = ModalManager.getDados("modalUsuario");

    const campo = (id) => document.getElementById(id)?.value ?? "";

    const toIntOrNull = (valor) => {
        if (valor === "" || valor === null || valor === undefined) {
            return null;
        }

        const numero = Number(valor);
        return Number.isInteger(numero) ? numero : null;
    };

    const senha = campo("inputModalUsuarioSenha");
    const confirmarSenha = campo("inputModalUsuarioConfirmarSenha");

    const payload = {
        tipoAcessoID: toIntOrNull(campo("selectModalUsuarioSetor")),
        status: toIntOrNull(campo("selectModalUsuarioStatus")),
        email: campo("inputModalUsuarioEmail").trim() || null,
        nome: campo("inputModalUsuarioNome").trim() || null,
        password: senha || null,
        franqueado_id: toIntOrNull(
            campo("selectModalUsuarioFranqueado")
        ),
        franquia_id: toIntOrNull(
            window.dadosUsuarioLogado?.franquia_id
        )
    };
    if(payload.franqueado_id === null){
        delete payload.franqueado_id;
    }
    console.log(payload);

    // Validação dos campos obrigatórios
    if (
        payload.tipoAcessoID === null ||
        payload.status === null ||
        !payload.email ||
        !payload.nome
    ) {
        Swal.fire({
            icon: 'warning',
            title: 'Atenção',
            text: 'Preencha todos os campos obrigatórios.',
            customClass: { popup: 'swal-modal-top' }
        });
        return;
    }

    try {
        if (dados.acao === 'novo') {

            // Senha obrigatória na criação
            if (!senha || !confirmarSenha) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Atenção',
                    text: 'Informe a senha e sua confirmação.',
                    customClass: { popup: 'swal-modal-top' }
                });
                return;
            }

            if (senha !== confirmarSenha) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Atenção',
                    text: 'A senha e a confirmação devem ser iguais.',
                    customClass: { popup: 'swal-modal-top' }
                });
                return;
            }

            await api.post("/api/user/create", payload);

        } else if (dados.acao === 'editar') {

            // Na edição, senha vazia significa manter a senha atual
            if (!senha) {
                delete payload.password;
            } else {
                if (!confirmarSenha) {
                    Swal.fire({
                        icon: 'warning',
                        title: 'Atenção',
                        text: 'Confirme a nova senha.',
                        customClass: { popup: 'swal-modal-top' }
                    });
                    return;
                }

                if (senha !== confirmarSenha) {
                    Swal.fire({
                        icon: 'warning',
                        title: 'Atenção',
                        text: 'A senha e a confirmação devem ser iguais.',
                        customClass: { popup: 'swal-modal-top' }
                    });
                    return;
                }
            }

            if (dados.usuarioId == null) {
                throw new Error("ID do usuário não informado.");
            }

            await api.put(
                `/api/user/update/${dados.usuarioId}`,
                payload
            );

        } else {
            throw new Error("Ação do modal inválida.");
        }

        const usuario = payload.nome;

        await iniciarUsuarios();
        ModalManager.fechar("modalUsuario");

        Swal.fire({
            icon: 'success',
            title: 'Usuário salvo',
            text: 'Usuário gravado no sistema: ' + usuario,
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error("Erro ao salvar usuário:", err);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível salvar o usuário.',
            customClass: { popup: 'swal-modal-top' }
        });
    }
});



$(document).on('click','.btRestaurarUsuario',async function(){
    const usuarioId = this.dataset.id;
    try {
        await api.get(`/api/franquiado/ativaDesativa/${usuarioId}?ativa=1`);
        iniciarUsuarios();
        Swal.fire({
            icon: 'success',
            title: 'Usuario reativado com sucesso',
            text: 'esses dados são recuperaveis!',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a manutenção.' });
    }
});
$(document).on('blur','#inputModalUsuarioCep',async function(){
    const cep  = document.getElementById("inputModalUsuarioCep").value; 
    let resultado  = await buscarCep(cep);
    document.getElementById("inputModalUsuarioEndereco").value = resultado.logradouro; 
    document.getElementById("inputModalUsuarioCidade").value = resultado.localidade; 
    document.getElementById("inputModalUsuarioUf").value = resultado.uf; 
    document.getElementById("inputModalUsuarioCep").value = resultado.cep; 
    console.log(resultado);
});



$(document).on('click', '[data-toggle-senha]', function () {
    const idInput = this.dataset.toggleSenha;
    const input = document.getElementById(idInput);
    const icone = this.querySelector('i');

    if (!input || !icone) return;

    const mostrar = input.type === 'password';

    input.type = mostrar ? 'text' : 'password';

    icone.classList.toggle('fa-eye', !mostrar);
    icone.classList.toggle('fa-eye-slash', mostrar);

    this.setAttribute(
        'aria-label',
        mostrar ? 'Ocultar senha' : 'Mostrar senha'
    );

    this.title = mostrar ? 'Ocultar senha' : 'Mostrar senha';
});

const formUsuario = document.getElementById('frmModalUsuario');
const senhaUsuario = document.getElementById('inputModalUsuarioSenha');
const confirmarSenhaUsuario = document.getElementById(
    'inputModalUsuarioConfirmarSenha'
);

function validarSenhasUsuario() {
    const senhasConferem =
        senhaUsuario.value === confirmarSenhaUsuario.value;

    confirmarSenhaUsuario.setCustomValidity(
        senhasConferem ? '' : 'As senhas não conferem.'
    );

    confirmarSenhaUsuario.classList.toggle(
        'is-invalid',
        !senhasConferem && confirmarSenhaUsuario.value.length > 0
    );

    return senhasConferem;
}

senhaUsuario.addEventListener('input', validarSenhasUsuario);
confirmarSenhaUsuario.addEventListener('input', validarSenhasUsuario);

formUsuario.addEventListener('submit', (event) => {
    event.preventDefault();

    if (!validarSenhasUsuario()) {
        confirmarSenhaUsuario.reportValidity();
        return;
    }

    if (!formUsuario.checkValidity()) {
        formUsuario.reportValidity();
        return;
    }

    // Integrar aqui com a função de cadastro/API existente.
});
