async function carregarFranqueados(selectId = null, opcaoTodos = true) {

    const select = selectId 
        ? document.getElementById(selectId)
        : document.querySelector("select.form-select.rounded-4");

    if (!select) return;

    try {

        const response    = await api.get("/api/franquiado/listar");
        const franqueados = response.data.resultado;

        if (franqueados.length === 1) {
            select.innerHTML = `<option value="${franqueados[0].id}">${franqueados[0].nome}</option>`;
            select.disabled  = true;
            return;
        }

        select.disabled  = false;
        select.innerHTML = opcaoTodos
            ? `<option value="">Todos</option>`
            : `<option value="" selected disabled>Selecione o franquiado</option>`;

        franqueados.forEach((franqueado) => {
            const option       = document.createElement("option");
            option.value       = franqueado.id;
            option.textContent = franqueado.nome;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar franqueados:", err);
        select.innerHTML = `<option value="">Erro ao carregar</option>`;
    }

}
async function carregarAutocompletePlaca(tipo="id",inputId = "inputPlaca", listaId = "listaPlacas")  {
    
    const input  = document.getElementById(inputId);
    const lista  = document.getElementById(listaId);

    if (!input || !lista) return;

    let todasPlacas = [];

    try {

        const response = await api.get("/api/frota/listar");
        todasPlacas = response.data.resultado; // já tem os dados carregados
        console.log("todasPlacas");
        console.log(todasPlacas);
    } catch (err) {
        console.error("Erro ao carregar placas:", err);
        return;
    }

    /*
    |--------------------------------------------------------------------------
    | FILTRAR AO DIGITAR
    |--------------------------------------------------------------------------
    */

    input.addEventListener("input", () => {

        const termo = input.value.trim().toUpperCase();
        lista.innerHTML = "";

        if (!termo) {
            lista.style.display = "none";
            return;
        }

        const filtradas = todasPlacas.filter(f =>
            f.placa.toUpperCase().includes(termo)
        );

        if (!filtradas.length) {
            lista.style.display = "none";
            return;
        }

        filtradas.forEach((frota) => {

            const item = document.createElement("li");
            item.className = "list-group-item list-group-item-action";
            item.style.cursor = "pointer";
            item.textContent = `${frota.placa} — ${frota.cor} (${frota.ano})`;
            placaValor = frota.placa;
            if(tipo !== 'null'){
                placaValor = frota.id;
            }
            item.addEventListener("click", () => {
                input.value = frota.placa;
                input.dataset.frotaId = frota.id;
                lista.style.display = "none";
            });

            lista.appendChild(item);

        });

        lista.style.display = "block";

    });

    /*
    |--------------------------------------------------------------------------
    | FECHAR AO CLICAR FORA
    |--------------------------------------------------------------------------
    */

    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !lista.contains(e.target)) {
            lista.style.display = "none";
        }
    });

}

function toggleSenha(id, botao) {

    const input = document.getElementById(id);
    const icon = botao.querySelector('i');

    if (input.type === 'password') {

        input.type = 'text';

        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');

    } else {

        input.type = 'password';

        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');

    }

}
async function buscarCep(cep) {

    // REMOVE CARACTERES
    cep = cep.replace(/\D/g, '');

    if (cep.length !== 8) {
        return;
    }

    try {

        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);

        const dados = await response.json();

        // CEP NÃO ENCONTRADO
        if (dados.erro) {

            alert('CEP não encontrado');
            return;

        }
        return dados;


    } catch (erro) {

        console.error(erro);

        alert('Erro ao buscar CEP');

    }

}


function mostrarMensagem(
    mensagem,
    tipo = 'info',
    titulo = 'Mensagem'
) {

    const modal = document.getElementById('modalMensagem');

    const tituloEl = document.getElementById('modalMensagemTitulo');
    const textoEl  = document.getElementById('modalMensagemTexto');
    const iconeEl  = document.getElementById('modalMensagemIcone');
    const headerEl = modal.querySelector('.modal-header');

    tituloEl.innerHTML = titulo;
    textoEl.innerHTML  = mensagem;

    headerEl.className = 'modal-header text-white';
    iconeEl.className  = 'mb-3 fs-1';

    switch (tipo) {

        case 'success':
            headerEl.classList.add('bg-success');
            iconeEl.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
        break;

        case 'error':
            headerEl.classList.add('bg-danger');
            iconeEl.innerHTML = '<i class="bi bi-x-circle-fill text-danger"></i>';
        break;

        case 'warning':
            headerEl.classList.add('bg-warning');
            iconeEl.innerHTML = '<i class="bi bi-exclamation-triangle-fill text-warning"></i>';
        break;

        default:
            headerEl.classList.add('bg-dark');
            iconeEl.innerHTML = '<i class="bi bi-info-circle-fill text-dark"></i>';

    }

    const instancia = new bootstrap.Modal(modal, {
        backdrop: true,
        keyboard: true
    });

    instancia.show();

}
// lembrar de colocar nas outras telas 
function iniciarEventosModalGeral(modal) {

    const modalEl = document.getElementById(modal);

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


function limparMoeda(valor) {
    return parseFloat(
        valor.replace(/[R$\s.]/g, '').replace(',', '.')
    ) || 0;
}

function mascaraMoeda(input) {
    // Remove listener anterior para não duplicar
    const novoInput = input.cloneNode(true);
    input.parentNode.replaceChild(novoInput, input);

    novoInput.addEventListener("input", function () {
        let valor = this.value.replace(/\D/g, '');
        valor = (parseInt(valor || 0) / 100).toFixed(2);
        this.value = Number(valor).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    });
}

function obterExtensao(mimeType) {

    const extensoes = {
        "application/pdf": ".pdf",

        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",

        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",

        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",

        "application/vnd.ms-powerpoint": ".ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",

        "text/plain": ".txt",
        "text/csv": ".csv",

        "application/zip": ".zip",
        "application/x-rar-compressed": ".rar",
        "application/x-7z-compressed": ".7z"
    };

    return extensoes[mimeType] || "";
}
function dataHoraFormatada(dataStr){

    const data = new Date(dataStr);

    const dia = String(data.getDate()).padStart(2, "0");
    const mes = String(data.getMonth() + 1).padStart(2, "0");
    const ano = data.getFullYear();

    const hora = String(data.getHours()).padStart(2, "0");
    const min = String(data.getMinutes()).padStart(2, "0");
    const seg = String(data.getSeconds()).padStart(2, "0");

    const formatada = `${dia}/${mes}/${ano} ${hora}:${min}:${seg}`;

    return formatada;
}

async function baixarArquivo(tipo, idAnexo) {

    try {
        console.log("id:", idAnexo)
        const responseAnexo = await api.get(
            `api/anexos/listar?id=${idAnexo}`
        );
        let dados;
        let extensao = "pdf"
        if (responseAnexo.data.resultado?.length) {
            dados = responseAnexo.data.resultado[0]
            extensao = obterExtensao(responseAnexo.data.resultado[0].tipo_mime)
        }

        let chave = `${dados.id}${dados.franquia_franquiador_locatario_id ?? ''}`;

        const blob = await api.getBlob(
            `/api/anexos/imagem/${dados.entidade_tipo}/${dados.entidade_id}`
        );

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `${tipo}_${chave}${extensao}`;

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error(error);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível baixar o arquivo.'
        });
    }
}
async function excluirArquivo(idAnexo, callback = null) {

    const result = await Swal.fire({
        icon: 'warning',
        title: 'Excluir comprovante?',
        text: 'Deseja realmente remover o arquivo?',
        showCancelButton: true,
        confirmButtonText: 'Sim',
        cancelButtonText: 'Cancelar'
    });

    if (!result.isConfirmed) {
        return;
    }

    try {
        console.log("teste", idAnexo);
        await api.delete(`/api/anexos/delete/${idAnexo}`);

        if (typeof callback === 'function') {
            await callback();
        }

        Swal.fire({
            icon: 'success',
            title: 'Sucesso',
            text: 'Arquivo removido com sucesso!',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (error) {

        console.log(error);

        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Não foi possível excluir o arquivo.'
        });

    }

}