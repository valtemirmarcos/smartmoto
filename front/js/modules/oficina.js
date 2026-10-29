async function iniciarOficina(filtros = {}) {

    const params = new URLSearchParams();
    if (filtros.frota)      params.append("frota",      filtros.frota);
    if (filtros.dataInicio || filtros.dataFim) {
    
        if (filtros.dataInicio) {
            params.append("dataInicio", filtros.dataInicio);
        }
    
        if (filtros.dataFim) {
            params.append("dataFim", filtros.dataFim);
        }
    
    } else {
        // Caso contrário, usa mês e ano atuais
        params.append("dataInicio", primeiroDiaMesAtual());
        params.append("dataFim", ultimoDiaMesAtual());
    }

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/oficina/listar${query}`);
    const oficina   = response.data.resultado || [];
    // tabela
    if ($('#oficinaTableLista').length) {

        if ($.fn.DataTable.isDataTable('#oficinaTableLista')) {
            $('#oficinaTableLista').DataTable().destroy();
        }
    
        $('#oficinaTableLista').DataTable({
            data: oficina,
            columns: [
                {
                    data: 'fraqueado',
                    defaultContent: '-',
                    visible: false
                },
                {
                    data: 'locatario',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'placa',
                    defaultContent: '-'
                },
                {
                    data: 'data_servico',
                    defaultContent: '-',
                    render: function(data) {

                        if (!data) return '-';
                    
                        const [ano, mes, dia] = data.split('-');
                    
                        return `${dia}/${mes}/${ano}`;
                    
                    }
                },
                {
                    data: 'kilometragem',
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
                    data: 'obs',
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
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarManutencao" data-id="${row.id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button 
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirManutencao" data-id="${row.id}">
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
            pageLength:20,
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const total = dados.reduce((s, i) => s + Number(i.valor || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#modalManutencaoTotal').text(fmt(total));
            }
        });
    
    }

}
async function prepararModalManutencao() {
    document.querySelector("#frmModalManutencao").reset();

    await carregarAutocompletePlaca("id", "inputManutencaoPlaca", "listaManutencaoPlacas");
    await carregarFranqueados("selectModalManutencaoFranqueado", false);
    mascaraMoeda(document.getElementById("modalInputManutencaoValor"));
    mascaraMoeda(document.getElementById("modalInputManutencaoPagamento"));
    
}
$(document).on('click','#modalNovaManutencao',async function(){
    prepararModalManutencao();
    ModalManager.abrir("modalOficina",{acao:"novo"});

});
$(document).on('click','#modalFitrarManutencao',async function(){
    prepararModalManutencao();
    ModalManager.abrir("modalFiltroOficina");
});
$(document).on('click','#btModalFiltrarManutencao',async function(){
    const filtros = {
        frota:      document.getElementById("inputPlaca")?.value
                        ? document.getElementById("inputPlaca")?.dataset.frotaId || null
                        : null,
        dataInicio: document.getElementById("inputDataInicial")?.value || null,
        dataFim:    document.getElementById("inputDataFinal")?.value   || null,
    };
    iniciarOficina(filtros);
    ModalManager.fechar("modalFiltroOficina");
});
$(document).on('click','.btModalAlterarManutencao',async function(){
    await prepararModalManutencao();
    const manutencaoId = this.dataset.id;
    const response  = await api.get(`/api/oficina/listar?id=${manutencaoId}`);
    const oficina = response.data.resultado[0];
    console.log("oficina:",oficina);

    document.getElementById("inputManutencaoPlaca").value = oficina.placasf || "";
    document.getElementById("modalInputManutencaoDataServico").value = oficina.data_servico || "";
    document.getElementById("modalInputManutencaoKms").value = oficina.kilometragem || "";
    document.getElementById("modalInputManutencaoServico").value = oficina.descricao || "";
    document.getElementById("modalInputManutencaoValor").value = formatarMoeda(oficina.valor) || "";
    document.getElementById("modalInputManutencaoPagamento").value = formatarMoeda(oficina.pagamento) || "";
    document.getElementById("modalInputManutencaoObs").value = oficina.obs || "";

    ModalManager.abrir("modalOficina",{
        acao:"editar",
        manutencaoID: manutencaoId,
        frotaId: oficina.frota_id
    });
});
$(document).on('click','.btModalExcluirManutencao',async function(){
    ModalManager.abrir("modalExcluir");
    const manutencaoId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/oficina/ativaDesativa/${manutencaoId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarOficina();
            Swal.fire({
                icon: 'success',
                title: 'Manutenção excluida com sucesso',
                text: 'esses dados são recuperaveis!',
                timer: 2000,
                showConfirmButton: false
            });
    
        } catch (err) {
            console.error(err);
            Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a manutenção.' });
        }
        console.log('Excluir faturamento');
    });
});
$(document).on('click','#btModalSalvarManutencao',async function(){
    const dados = ModalManager.getDados("modalOficina");
    let frotaId = document.getElementById("inputManutencaoPlaca").dataset.frotaId;
    if(dados.acao=="editar"){
        frotaId = dados.frotaId;
    }
    const response  = await api.get(`/api/locatarios/listar?placa=${frotaId}&status=1`);
    const locatario = response.data.resultado[0];

    const franquia_franquiador_locatario_id = locatario.franquia_franquiador_locatario_id;
    
    const payload = {
        franquia_franquiador_locatario_id:franquia_franquiador_locatario_id,
        frota_id: frotaId || null,
        data_servico: document.getElementById("modalInputManutencaoDataServico").value  || null,
        descricao: document.getElementById("modalInputManutencaoServico").value  || null,
        valor: limparMoeda(document.getElementById("modalInputManutencaoValor").value),
        pagamento: limparMoeda(document.getElementById("modalInputManutencaoPagamento").value),
        obs: document.getElementById("modalInputManutencaoObs").value  || null,
        kilometragem: Number(document.getElementById("modalInputManutencaoKms").value)  || 0
    }
    if (
        !payload.frota_id || 
        !payload.data_servico || 
        !payload.descricao ||
        !payload.valor ||
        !payload.kilometragem
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
            await api.post("/api/oficina/create", payload);
        }else{
            console.log("alterar");
            const manutencaoID = dados.manutencaoID
            await api.put(`/api/oficina/update/${manutencaoID}`, payload);
        }

        ModalManager.fechar("modalOficina");  
        iniciarOficina();
        const placa = document.getElementById("inputManutencaoPlaca").value; 
        Swal.fire({
            icon: 'success',
            title: 'Manutenção salva',
            text: 'Manutenção gravada para a moto:'+placa,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar a manutenção.' });
    }
    console.log(payload);
    ModalManager.fechar("modalOficina");
});



