async function iniciarFranqueados(filtros = {}) {

    const params = new URLSearchParams();

    if (filtros.cnpj) params.append("cnpj",removerCaracteresEspeciais(filtros.cnpj));
    if (filtros.cpf) params.append("cpf",removerCaracteresEspeciais(filtros.ativo));
    if (filtros.status) params.append("status",filtros.status);

    const query    = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(`/api/franquiado/listar${query}`);
    const franquiado   = response.data.resultado || [];
    console.log(franquiado);
    // tabela
    if ($('#franqueadoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#franqueadoTableLista')) {
            $('#franqueadoTableLista').DataTable().destroy();
        }
    
        $('#franqueadoTableLista').DataTable({
            data: franquiado,
            columns: [
                {
                    data: 'id',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'razao_social',
                    defaultContent: '-',
                    visible: true
                },
                {
                    data: 'cnpj',
                    defaultContent: '-',
                    render: function(data) {
                        return formatarCNPJ(data);
                    }
                },
                {
                    data: 'quantidade_motos',
                    defaultContent: '-'
                },
                {
                    data: 'status_id',
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
                                    class="btn btn-sm btn-success rounded-3 btRestaurarFranqueado"
                                    data-id="${row.id}"
                                    title="Restaurar franqueado">
                                    <i class="bi bi-arrow-counterclockwise"></i>
                                </button>
                            `;
                        } else {
                            botaoExcluirRestaurar = `
                                <button
                                    class="btn btn-sm btn-danger rounded-3 btModalExcluirFranqueado"
                                    data-id="${row.id}"
                                    title="Excluir franqueado">
                                    <i class="bi bi-trash-fill"></i>
                                </button>
                            `;
                        }
                
                        return `
                            <div class="d-flex gap-2 justify-content-center">
                                <button
                                    class="btn btn-sm btn-warning rounded-3 btModalAlterarFranqueado"
                                    data-id="${row.id}"
                                    title="Alterar franqueado">
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
async function prepararModalFranqueado() {
    document.querySelector("#frmModalFranqueado").reset();
    mascaraCNPJ(document.getElementById("inputModalFranqueadoCnpj"));
    mascaraCPF(document.getElementById("inputModalFranqueadoCpf"));
    formatarCEP(document.getElementById("inputModalFranqueadoCep"));
}
$(document).on('click','#modalNovoFranqueado',async function(){
    prepararModalFranqueado();
    ModalManager.abrir("modalFranqueado",{acao:"novo"});

});
$(document).on('click','#modalFitrarFranqueado',async function(){
    prepararModalFranqueado();
    ModalManager.abrir("modalFiltroFranqueado");
});
$(document).on('click','#btModalFiltrarFranqueado',async function(){
    const filtros = {
        cnpj: document.getElementById("inputFiltroFranqueadoCNPJ")?.value || null,
        cpf: document.getElementById("inputFiltroFranqueadoCPF")?.value   || null,
        status: document.getElementById("selectFiltroFranqueadoStatus")?.value   || null,
    };
    iniciarFranqueados(filtros);
    ModalManager.fechar("modalFiltroFranqueado");
});
$(document).on('click','.btModalAlterarFranqueado',async function(){
    prepararModalFranqueado();
    const franqueadoId = this.dataset.id;
    const response  = await api.get(`/api/franquiado/listar?id=${franqueadoId}`);
    const franquiado = response.data.resultado[0];
    console.log("franquiado:",franquiado);

    document.getElementById("inputModalFranqueadoNome").value = franquiado.nome || "";
    document.getElementById("inputModalFranqueadoCpf").value = formatarCPF(franquiado.cpf) || "";
    document.getElementById("inputModalFranqueadoRazaoSocial").value = franquiado.razao_social || "";
    document.getElementById("inputModalFranqueadoCnpj").value = formatarCNPJ(franquiado.cnpj) || "";
    document.getElementById("inputModalFranqueadoCep").value = formatarCEP(franquiado.cep) || "";
    document.getElementById("inputModalFranqueadoEndereco").value = franquiado.endereco || "";
    document.getElementById("inputModalFranqueadoNumero").value = franquiado.numero || "";
    document.getElementById("inputModalFranqueadoComplemento").value = franquiado.complemento || "";
    document.getElementById("inputModalFranqueadoCidade").value = franquiado.cidade || "";
    document.getElementById("inputModalFranqueadoUf").value = franquiado.uf || "";
    document.getElementById("inputModalFranqueadoStatus").value = franquiado.status_id || "";
    
    ModalManager.abrir("modalFranqueado",{
        acao:"editar",
        franqueadoId: franqueadoId
    });
});
$(document).on('click','.btModalExcluirFranqueado',async function(){
    ModalManager.abrir("modalExcluir");
    const franqueadoId = this.dataset.id;

    $('#btExcluir')
    .off('click')
    .on('click',async function () {
        try {
            await api.get(`/api/franquiado/ativaDesativa/${franqueadoId}?ativa=2`);
            ModalManager.fechar('modalExcluir');
            iniciarFranqueados();
            Swal.fire({
                icon: 'success',
                title: 'Franqueado excluido com sucesso',
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
$(document).on('click','#btModalSalvarFranqueado',async function(){
    const dados = ModalManager.getDados("modalFranqueado");
    const payload = {
        nome: document.getElementById("inputModalFranqueadoNome")?.value || null,
        cpf: document.getElementById("inputModalFranqueadoCpf")?.value || null,
        razao_social: document.getElementById("inputModalFranqueadoRazaoSocial")?.value || null,
        cnpj: document.getElementById("inputModalFranqueadoCnpj")?.value || null,
        cep: document.getElementById("inputModalFranqueadoCep")?.value || null,
        endereco: document.getElementById("inputModalFranqueadoEndereco")?.value || null,
        numero: document.getElementById("inputModalFranqueadoNumero")?.value|| null,
        complemento: document.getElementById("inputModalFranqueadoComplemento")?.value || null,
        cidade: document.getElementById("inputModalFranqueadoCidade")?.value || null,
        uf: document.getElementById("inputModalFranqueadoUf")?.value || null,
        status: document.getElementById("inputModalFranqueadoStatus")?.value || null,
    }

    if (
        !payload.nome || 
        !payload.cpf || 
        !payload.razao_social ||
        !payload.cnpj ||
        !payload.cep ||
        !payload.endereco ||
        !payload.numero ||
        !payload.cidade ||
        !payload.uf ||
        !payload.status 
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
            await api.post("/api/franquiado/create", payload);
        }else{
            console.log("editar");
            const franqueadoId = dados.franqueadoId
            await api.put(`/api/franquiado/update/${franqueadoId}`, payload);
        }

        ModalManager.fechar("modalFranqueado");  
        iniciarFranqueados();
        const franqueado  = document.getElementById("inputModalFranqueadoRazaoSocial").value; 

        Swal.fire({
            icon: 'success',
            title: 'Franqueado salvo',
            text: 'Franqueado gravado no sistema:'+franqueado,
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar o codigo.' });
    }
    console.log(payload);
    ModalManager.fechar("modalFranqueado");
});


$(document).on('click','.btRestaurarFranqueado',async function(){
    const franqueadoId = this.dataset.id;
    try {
        await api.get(`/api/franquiado/ativaDesativa/${franqueadoId}?ativa=1`);
        iniciarFranqueados();
        Swal.fire({
            icon: 'success',
            title: 'Franqueado reativado com sucesso',
            text: 'esses dados são recuperaveis!',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir a manutenção.' });
    }
});
$(document).on('blur','#inputModalFranqueadoCep',async function(){
    const cep  = document.getElementById("inputModalFranqueadoCep").value; 
    let resultado  = await buscarCep(cep);
    document.getElementById("inputModalFranqueadoEndereco").value = resultado.logradouro; 
    document.getElementById("inputModalFranqueadoCidade").value = resultado.localidade; 
    document.getElementById("inputModalFranqueadoUf").value = resultado.uf; 
    document.getElementById("inputModalFranqueadoCep").value = resultado.cep; 
    console.log(resultado);
});
