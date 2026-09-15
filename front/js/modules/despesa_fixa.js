async function iniciarDespesaFixa(filtros = {}) {

    const params = new URLSearchParams();
    if (filtros.frota)      params.append("frota",      filtros.frota);

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/despesasFixas/listar${query}`);
    const despesasFixas   = response.data.resultado || [];

    // tabela
    if ($('#despesa_fixaTableLista').length) {

        if ($.fn.DataTable.isDataTable('#despesa_fixaTableLista')) {
            $('#despesa_fixaTableLista').DataTable().destroy();
        }
    
        $('#despesa_fixaTableLista').DataTable({
            data: despesasFixas,
            columns: [
                {
                    data: 'franqueado',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'placa',
                    defaultContent: '-'
                },
                {
                    data: 'descricao',
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
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-center',

                    render: function(data, type, row) {
                        return `
                            <div class="d-flex gap-2 justify-content-center">
                                <button 
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarDespesasFixas" data-id="${row.id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button 
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirDespesasFixas" data-id="${row.id}">
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
            pageLength:15,
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const total = dados.reduce((s, i) => s + Number(i.valor || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#modalDespesasFixasTotal').text(fmt(total));
            }
        });
    
    }

}
async function prepararModalDespesasFixas() {
    document.querySelector("#frmModalDespesasFixas").reset();

    await carregarAutocompletePlaca("id", "inputDespesasFixasPlaca", "listaDespesasFixasPlacas");
    await carregarFranqueados("selectModalDespesasFixasFranqueado", false);
    mascaraMoeda(document.getElementById("modalInputDespesasFixasValor"));
    
}
$(document).on('click','#btModalFiltroDespesaFixa',async function(){
    ModalManager.abrir("modalFiltroDespesaFixa");
});
$(document).on('click','#btModalFiltrarDespesasFixas',async function(){
    const filtros = {
        frota:      document.getElementById("inputPlaca")?.value
                        ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                        : null,
    };
    iniciarDespesaFixa(filtros);
    ModalManager.fechar("modalFiltroDespesaFixa");
});
$(document).on('click','#btModalNovaRecorrencia',async function(){
    await prepararModalDespesasFixas();
    ModalManager.abrir("modalDespesaFixa",{acao: "novo"});
});
$(document).on('click','.btModalAlterarDespesasFixas',async function(){
    console.log("alterar");
    await prepararModalDespesasFixas();
    const despesaFixaId = this.dataset.id;
    const response = await api.get(`/api/despesasFixas/listar?id=${despesaFixaId}`);
    const despesasFixas   = response.data.resultado[0];

    document.getElementById("inputDespesasFixasPlaca").value = despesasFixas.placa || "";
    document.getElementById("inputModalDespesasFixasDespesa").value = despesasFixas.descricao || "";
    document.getElementById("modalInputDespesasFixasValor").value = formatarMoeda(despesasFixas.valor) || "";

    ModalManager.abrir("modalDespesaFixa",{
        acao:"editar",
        despesaFixaId: despesaFixaId,
        frotaId: despesasFixas.frota_id
    });
});
$(document).on('click','#btModalSalvarDespesasFixas',async function(){
    const dados = ModalManager.getDados("modalDespesaFixa");
    let franquia_franquiador_locatario_id = document.getElementById("selectModalDespesasFixasFranqueado").value;
    let frotaId = document.getElementById("inputDespesasFixasPlaca").dataset.frotaId;
    if(dados.acao=="editar"){
        frotaId = dados.frotaId;
    }
    const payload = {
        franquia_franquiador_locatario_id:franquia_franquiador_locatario_id,
        frota_id:frotaId,
        data:dataAtual(),
        descricao:document.getElementById("inputModalDespesasFixasDespesa").value  || null,
        valor:limparMoeda(document.getElementById("modalInputDespesasFixasValor").value),
    }
    if (
        !payload.frota_id || 
        !payload.descricao ||
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
            await api.post("/api/despesasFixas/create", payload);
        }else{
            console.log("alterar");
            const despesaFixaId = dados.despesaFixaId;
            console.log("codigo:"+despesaFixaId);
            await api.put(`/api/despesasFixas/update/${despesaFixaId}`, payload);
        }

        ModalManager.fechar("modalDespesaFixa");
        iniciarDespesaFixa();
        const placa = document.getElementById("inputDespesasFixasPlaca").value; 
        Swal.fire({
            icon: 'success',
            title: 'Despesa fixa salva',
            text: 'Despesa fixa gravada para a moto:'+placa,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar a despesa fixa.' });
    }

    
});
$(document).on('click','.btModalExcluirDespesasFixas',async function(){
    ModalManager.abrir("modalExcluir");
    const despesaFixaId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/despesasFixas/ativaDesativa/${despesaFixaId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarDespesaFixa();
            Swal.fire({
                icon: 'success',
                title: 'Despesa Fixa excluida com sucesso',
                text: 'esses dados são recuperaveis!',
                timer: 2000,
                showConfirmButton: false
            });
    
        } catch (err) {
            console.error(err);
            Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a Despesa Fixa.' });
        }
    });
});
$(document).on('click','#btModalRemoverFiltrosDespesasFixas',async function(){
    iniciarDespesaFixa();
    ModalManager.fechar("modalFiltroDespesaFixa");
});
