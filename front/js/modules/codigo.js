async function iniciarCodigos(filtros = {}) {

    const params = new URLSearchParams();
    if (filtros.codigo && filtros.codigo > 0) params.append("codigo",filtros.codigo);
    if (filtros.sequencia && filtros.sequencia > 0) params.append("sequencia",filtros.sequencia);
    if (filtros.descricao) params.append("descricao",filtros.descricao);
    if (filtros.categoria) params.append("categoria",filtros.codigo);

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/codigos/listar${query}`);
    const codigos   = response.data.resultado || [];
    console.log(codigos);
    // tabela
    if ($('#codigoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#codigoTableLista')) {
            $('#codigoTableLista').DataTable().destroy();
        }
    
        $('#codigoTableLista').DataTable({
            data: codigos,
            columns: [
                {
                    data: 'depara_id',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'codigo',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'descricao',
                    defaultContent: '-'
                },
                {
                    data: 'obs',
                    defaultContent: '-'
                },
                {
                    data: 'cor',
                    defaultContent: '-'
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
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarCodigo" data-id="${row.id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button 
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirCodigo" data-id="${row.id}">
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
            pageLength:20
        });
    
    }

}
async function filtroCodigosCategorias() {

    const select = document.getElementById("selectModalCodigoIdCategoria");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/codigos/categorias");
        const codigos   = response.data.resultado;

        select.innerHTML = `<option value="" selected disabled>Selecione a categoria</option>`;

        codigos.forEach((s) => {
            const option       = document.createElement("option");
            option.value       = s.id;
            option.textContent = s.texto;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Erro ao carregar status:", err);
    }

}
async function prepararModalCodigo() {
    document.querySelector("#frmModalCodigo").reset();
    filtroCodigosCategorias();
    
}
$(document).on('click','#modalNovoCodigo',async function(){
    prepararModalCodigo();
    ModalManager.abrir("modalCodigo",{acao:"novo"});

});
$(document).on('click','#modalFitrarCodigo',async function(){
    prepararModalCodigo();
    ModalManager.abrir("modalFiltroCodigo");
});
$(document).on('click','#btModalFiltrarCodigo',async function(){
    const filtros = {
        sequencia:    document.getElementById("inputFiltroIdCategoria")?.value || null,
        codigo:       document.getElementById("inputFiltroSequencia")?.value   || null,
        descricao:    document.getElementById("inputFiltroInformacao")?.value   || null,
        categoria:    document.getElementById("inputFiltroCategoria")?.value   || null,
    };
    iniciarCodigos(filtros);
    ModalManager.fechar("modalFiltroCodigo");
});
$(document).on('click','.btModalAlterarCodigo',async function(){
    await prepararModalCodigo();
    const codigoId = this.dataset.id;
    const response  = await api.get(`/api/codigos/listar?id=${codigoId}`);
    const codigos = response.data.resultado[0];
    console.log("codigos:",codigos);

    document.getElementById("selectModalCodigoIdCategoria").value = codigos.depara_id || "";
    document.getElementById("inputModalCodigoSequencia").value = codigos.codigo || "";
    document.getElementById("inputModalCodigoInformacao").value = codigos.descricao || "";
    document.getElementById("inputModalCodigoCategoria").value = codigos.obs || "";
    document.getElementById("inputModalCodigoAdicional").value = codigos.cor || "";

    ModalManager.abrir("modalCodigo",{
        acao:"editar",
        codigoId: codigoId
    });
});
$(document).on('click','.btModalExcluirCodigo',async function(){
    ModalManager.abrir("modalExcluir");
    const codigoId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/codigos/ativaDesativa/${codigoId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarCodigos();
            Swal.fire({
                icon: 'success',
                title: 'Codigo excluido com sucesso',
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
$(document).on('click','#btModalSalvarCodigo',async function(){
    const dados = ModalManager.getDados("modalCodigo");

    
    const payload = {
        depara_id:document.getElementById("selectModalCodigoIdCategoria").value || null,
        codigo: document.getElementById("inputModalCodigoSequencia").value || null,
        descricao: document.getElementById("inputModalCodigoInformacao").value || null,
        obs: document.getElementById("inputModalCodigoCategoria").value || null,
        cor: document.getElementById("inputModalCodigoAdicional").value || null,
    }

    if (
        !payload.depara_id || 
        !payload.codigo || 
        !payload.descricao ||
        !payload.obs 
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
            await api.post("/api/codigos/create", payload);
        }else{
            console.log("editar");
            const codigoId = dados.codigoId
            await api.put(`/api/codigos/update/${codigoId}`, payload);
        }

        ModalManager.fechar("modalCodigo");  
        iniciarCodigos();
        const descricao  = document.getElementById("inputModalCodigoInformacao").value; 
        const codigo =  document.getElementById("inputModalCodigoSequencia").value
        Swal.fire({
            icon: 'success',
            title: 'Codigo salvo',
            text: 'Codigo gravado no sistema:'+codigo+' - '+descricao,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar o codigo.' });
    }
    console.log(payload);
    ModalManager.fechar("modalCodigo");
});

$(document).on('change','#selectModalCodigoIdCategoria',async function(){
    let categoria = $(this).find(':selected').text();
    document.getElementById("inputModalCodigoCategoria").value = categoria;
});


