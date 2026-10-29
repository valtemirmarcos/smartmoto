async function iniciarPlanos(filtros = {}) {

    const params = new URLSearchParams();

    if (filtros.plano) params.append("plano",filtros.plano);
    if (filtros.ativo) params.append("ativo",filtros.ativo);

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/planos/listar${query}`);
    const planos   = response.data.resultado || [];
    console.log(planos);
    // tabela
    if ($('#planoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#planoTableLista')) {
            $('#planoTableLista').DataTable().destroy();
        }
    
        $('#planoTableLista').DataTable({
            data: planos,
            columns: [
                {
                    data: 'id',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'plano',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'descricao',
                    defaultContent: '-'
                },
                {
                    data: 'semanas',
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
                
                        if (row.status == 2) {
                            botaoExcluirRestaurar = `
                                <button
                                    class="btn btn-sm btn-success rounded-3 btRestaurarPlano"
                                    data-id="${row.id}"
                                    title="Restaurar plano">
                                    <i class="bi bi-arrow-counterclockwise"></i>
                                </button>
                            `;
                        } else {
                            botaoExcluirRestaurar = `
                                <button
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirPlano"
                                    data-id="${row.id}"
                                    title="Excluir plano">
                                    <i class="bi bi-trash-fill"></i>
                                </button>
                            `;
                        }
                
                        return `
                            <div class="d-flex gap-2 justify-content-center">
                                <button
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarPlano"
                                    data-id="${row.id}"
                                    title="Alterar plano">
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
async function prepararModalPlano() {
    document.querySelector("#frmModalPlano").reset();
    mascaraMoeda(document.getElementById("inputModalPlanoValor"));
}
$(document).on('click','#modalNovoPlano',async function(){
    prepararModalPlano();
    ModalManager.abrir("modalPlano",{acao:"novo"});

});
$(document).on('click','#modalFitrarPlano',async function(){
    prepararModalPlano();
    ModalManager.abrir("modalFiltroPlano");
});
$(document).on('click','#btModalFiltrarPlano',async function(){
    const filtros = {
        plano: document.getElementById("inputFiltroPlanoPlano")?.value || null,
        ativo: document.getElementById("selectFiltroPlanoStatus")?.value   || null,
    };
    iniciarPlanos(filtros);
    ModalManager.fechar("modalFiltroPlano");
});
$(document).on('click','.btModalAlterarPlano',async function(){
    await prepararModalPlano();
    const planoId = this.dataset.id;
    const response  = await api.get(`/api/planos/listar?id=${planoId}`);
    const planos = response.data.resultado[0];
    console.log("planos:",planos);

    document.getElementById("inputModalPlanoPlano").value = planos.plano || "";
    document.getElementById("inputModalPlanoDescricao").value = planos.descricao || "";
    document.getElementById("inputModalPlanoSemanas").value = planos.semanas || "";
    document.getElementById("inputModalPlanoValor").value = formatarMoeda(planos.valor) || "";

    ModalManager.abrir("modalPlano",{
        acao:"editar",
        planoId: planoId
    });
});
$(document).on('click','.btModalExcluirPlano',async function(){
    ModalManager.abrir("modalExcluir");
    const planoId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/planos/ativaDesativa/${planoId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarPlanos();
            Swal.fire({
                icon: 'success',
                title: 'Plano excluido com sucesso',
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
$(document).on('click','#btModalSalvarPlano',async function(){
    const dados = ModalManager.getDados("modalPlano");
    const payload = {
        plano:document.getElementById("inputModalPlanoPlano").value || null,
        descricao: document.getElementById("inputModalPlanoDescricao").value || null,
        semanas: document.getElementById("inputModalPlanoSemanas").value || null,
        valor: limparMoeda(document.getElementById("inputModalPlanoValor").value),
    }

    if (
        !payload.plano || 
        !payload.descricao || 
        !payload.semanas ||
        !payload.valor 
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
            await api.post("/api/planos/create", payload);
        }else{
            console.log("editar");
            const planoId = dados.planoId
            await api.put(`/api/planos/update/${planoId}`, payload);
        }

        ModalManager.fechar("modalPlano");  
        iniciarPlanos();
        const plano  = document.getElementById("inputModalPlanoPlano").value; 

        Swal.fire({
            icon: 'success',
            title: 'Plano salvo',
            text: 'Plano gravado no sistema:'+plano,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar o codigo.' });
    }
    console.log(payload);
    ModalManager.fechar("modalPlano");
});


$(document).on('click','.btRestaurarPlano',async function(){
    const planoId = this.dataset.id;
    try {
        await api.get(`/api/planos/ativaDesativa/${planoId}?ativa=1`);
        iniciarPlanos();
        Swal.fire({
            icon: 'success',
            title: 'Plano reativado com sucesso',
            text: 'esses dados são recuperaveis!',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a manutenção.' });
    }
})
