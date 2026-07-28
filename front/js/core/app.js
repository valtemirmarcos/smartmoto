async function carregarPagina(pagina) {

    const conteudo = document.getElementById("conteudo");
    localStorage.setItem("paginaAtual", pagina);
    try {
        console.log(pagina);
        const response = await fetch(`./pages/${pagina}.html`);
        console.log(response);

        const html = await response.text();

        conteudo.innerHTML = html;
        ModalManager.iniciar();

        // inicia dashboard
        if (pagina === "dashboard") {
            iniciarDashboard();
        }
        if (pagina === "frota") {
            iniciarFrota();
            carregarFranqueados(null, true);
            carregarAutocompletePlaca();
            carregarCores(); 
            carregarAnos();
            carregarStatus();
            iniciarBotaoFiltrar();
            iniciarBotaoNovaFrota(); 
            iniciarEventosModal();
            salvarFrota();
            iniciarAbasFrota();
        }
        if (pagina === "locatario") {
            iniciarLocatario();
            carregarFranqueados(null, true);
            carregarAutocompletePlaca("id");
            carregarPlanos();
            carregarStatusLocatario();
            iniciarBotaoFiltrarLocatarios();
            iniciarBotaoNovoLocatario();
            iniciarEventosModalLocatario();
            iniciarBotaoSalvarLocatario();
            iniciarAbasLocatario();
            // iniciarLocatarioMultas();
        }
        if (pagina === "calcao") {
            iniciarCalcao();
            carregarFranqueados(null, true);
            carregarAutocompletePlaca("id");
            carregarStatusCalcao();
            carregarFormasPagamento();
            iniciarBotaoFiltrarCalcao();
            iniciarBotaoNovoCalcao();
            iniciarEventosModalGeral("modalCalcao");
            carregarStatusModalCalcao();
            iniciarAbasCalcao();
        }
        if (pagina === "semanal") {
            iniciarSemanal();
            carregarFranqueados(null, true);
            carregarAutocompletePlaca("id");
            carregarStatusFiltrosSemanais();
            iniciarBotaoFiltrarSemanais();
            iniciarBotaoNovoSemanal();
            iniciarEventosModalGeral("modalSemanal");
        }
        if (pagina === "custo") {
            // iniciarCusto();
            // carregarFranqueados(null, true);
            // carregarAutocompletePlaca("id");
        }
        if (pagina === "multa") {
            iniciarMultas();
            // carregarAutocompletePlaca("id");
        }
        if (pagina === "faturamento") {
            iniciarFaturamento();
            carregarStatusFiltrosFaturamento();
            carregarStatusFaturamento();
        }
        if (pagina === "oficina") {
            iniciarOficina();
        }
        if (pagina === "despesa_fixa") {
            iniciarDespesaFixa();
        }
        
    } catch(err) {
        console.log(err);
        conteudo.innerHTML = `
            <div class="alert alert-danger">
                Erro ao carregar página
            </div>
        `;

    }

}
