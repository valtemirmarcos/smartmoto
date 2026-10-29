async function iniciarCusto(id) {
    
    const frotaId =id;

    console.log("frotaid:", frotaId);

    const response = await api.get(`/api/custo/listar?frota=${frotaId}`);
    const custos   = response.data.resultado || [];

    console.log(custos);
    if ($('#custoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#custoTableLista')) {
            $('#custoTableLista').DataTable().destroy();
        }
        $('#custoTableLista').DataTable({
            data: custos,
            columns: [

                {
                    data: 'custo',
                    defaultContent: '-'
                },
                {
                    data: 'data_vencimento',
                    defaultContent: '-',
                    render: function(data) {

                        if (!data) return '-';
                    
                        const [ano, mes, dia] = data.split('-');
                    
                        return `${dia}/${mes}/${ano}`;
                    
                    }
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

                        if (data === 'Pago') {
                            classe = 'bg-success';
                        }

                        if (data === 'Atrasado') {
                            classe = 'bg-danger';
                        }

                        if (data === 'Aberto') {
                            classe = 'bg-primary';
                        }

                        return `
                            <span class="badge-status ${classe} text-white">
                                ${data}
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
                        return `
                            <div class="d-flex justify-content-center gap-2">
                                <button class="btn btn-sm btn-warning rounded-3 btnEditarCusto" data-id="${row.id}" data-frotaid="${row.frota_id}">
                                    <i class="bi bi-pencil-fill"></i>
                                </button>
                                <button class="btn btn-sm btn-danger rounded-3 btnExcluirCusto" data-id="${row.id}" data-frotaid="${row.frota_id}">
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
            pageLength:5,
            footerCallback: function () {

                const api = this.api();
                const dados = api.rows({ search: 'applied' }).data().toArray();
                const totalPago = dados
                .filter(i => i.status_id === 2)
                .reduce((s, i) => s + Number(i.valor || 0), 0);
                const totalAberto = dados
                    .filter(i => i.status_id === 1)
                    .reduce((s, i) => s + Number(i.valor || 0), 0);
                const fmt = v => v.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });

                $('#valorPago').text(fmt(totalPago));
                $('#valorAberto').text(fmt(totalAberto));
            }
        });
    
    }

}
async function carregarStatusModalCusto() {

    const select = document.getElementById("modalFrotaCustoStatus");

    if (!select) return;

    try {

        const response = await api.get("/api/filtros/custos/status");
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
function limparModalCusto() {

    document.getElementById("modalFrotaCustoCusto").value = "";
    document.getElementById("modalFrotaCustoParcela").value = 1;
    document.getElementById("modalFrotaCustoVencimento").value = "";
    document.getElementById("modalFrotaCustoValor").value = "";
    document.getElementById("modalFrotaCustoStatus").selectedIndex = 0;

}
$(document).on('click', '.btnEditarCusto',async function () {
    const idCusto = this.dataset.id;
    const frotaId = this.dataset.frotaid;
    mascaraMoeda(document.getElementById("modalFrotaCustoValor"));
    console.log("idCusto:",idCusto);
    console.log("frotaId:",frotaId);

    const response = await api.get(`/api/custo/listar?id=${idCusto}`);
    const custo   = response.data.resultado[0];

    if (!custo) return;

    ModalManager.abrir('modalCusto', {
        modo: 'editar',
        id: idCusto,
        frotaId: frotaId
    });

    document.getElementById("modalFrotaCustoCusto").value = custo.custo || "";
    document.getElementById("modalFrotaCustoParcela").value = custo.parcela || "";
    document.getElementById("modalFrotaCustoVencimento").value = custo.data_vencimento || "";
    document.getElementById("modalFrotaCustoValor").value = Number(custo.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    await carregarStatusModalCusto();
    document.getElementById("modalFrotaCustoStatus").value  = custo.status_id || "";
});
$(document).on('click', '.btnInserirNovoCusto', async function () {
    limparModalCusto();
    mascaraMoeda(document.getElementById("modalFrotaCustoValor"));
    await carregarStatusModalCusto();
    ModalManager.abrir('modalCusto', {
        modo: 'novo',
        frotaId: document.getElementById("btnAbaDocumentosFrotaCustos").dataset.frotaId
    });
    

});
$(document).on('click', '.btnExcluirCusto', function () {
    const idCusto = this.dataset.id;
    const frotaId = this.dataset.frotaid;
    $('#btExcluir').attr('id', 'btExcluirCusto');
    ModalManager.abrir('modalExcluir',{
        id: idCusto,
        frotaId: frotaId
    });

});
$(document).on('click', '#btSalvarCusto', async function () {

    const dados = ModalManager.getDados('modalCusto');
    const frotaId = dados.frotaId;
    const payload = {
        frota_id: parseInt(dados.frotaId),
        data_vencimento:document.getElementById("modalFrotaCustoVencimento").value,
        custo:document.getElementById("modalFrotaCustoCusto").value,
        parcela:parseInt(document.getElementById("modalFrotaCustoParcela").value),
        valor: limparMoeda(document.getElementById("modalFrotaCustoValor").value),
        status_id:parseInt(document.getElementById("modalFrotaCustoStatus").value)
    }
    if (
        !payload.data_vencimento ||
        !payload.custo ||
        !payload.parcela ||
        !payload.valor ||
        !payload.status_id
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

    try {

        if (dados.modo === 'novo') {
            await api.post("/api/custo/create", payload);
        } else {
            const id = dados.id;
            await api.put(`/api/custo/update/${id}`, payload);
        }

        ModalManager.fechar('modalCusto');

        iniciarCusto(frotaId);

        Swal.fire({
            icon: 'success',
            title: 'Dados salvos',
            text: 'Assim que possivel adicione comprovante do calção',
            timer: 2000,
            showConfirmButton: false
        });

    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível salvar o custo.' });
    }
});

$(document).on('shown.bs.tab', '#btnAbaDocumentosFrotaCustos', function () {

    const frotaId = document.getElementById("btnAbaDocumentosFrotaCustos").dataset.frotaId;

    console.log("frotaId:", frotaId);

    iniciarCusto(frotaId);

});
$(document).on('click', '#btExcluirCusto', async function () {
    try {
        
        const dados = ModalManager.getDados('modalExcluir');
        console.log(dados);
        await api.get(`/api/custo/ativaDesativa/${dados.id}?ativa=2`);
        ModalManager.fechar('modalExcluir');

        iniciarCusto(dados.frotaId);
        Swal.fire({
            icon: 'success',
            title: 'Custo excluido com sucesso',
            text: 'esses dados são recuperaveis!',
            timer: 2000,
            showConfirmButton: false
        });
    } catch (err) {
        console.error(err);
        Swal.fire({ icon: 'error', title: 'Erro', text: 'Não foi possível excluir o custo.' });
    }

});
