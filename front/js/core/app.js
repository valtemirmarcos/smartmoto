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
        if (pagina === "rel_custos") {
            iniciarRelCusto();
        }
        if (pagina === "rel_lucros") {
            iniciarRelLucro();
        }
        if (pagina === "rel_custo_moto") {
            iniciarRelCustoMoto();
        }
        if (pagina === "rel_lucro_moto") {
            iniciarRelLucroMoto();
        }
        if (pagina === "despesa_fixa") {
            carregarFranqueados(null, true);
            carregarAutocompletePlaca();
        }
        if (pagina === "operacional") {

        }
        if (pagina === "codigo") {
            iniciarCodigos();
        }
        if (pagina === "plano") {
            iniciarPlanos();
        }
        if (pagina === "franqueado") {
            iniciarFranqueados();
        }
        if (pagina === "usuario") {
            iniciarUsuarios();
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
function mostrarMenuFranquia() {

    const menu = `
        <ul class="nav flex-column m-0 p-0">

            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('dashboardFranquia')">
                    Dashboard
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('operacional')">
                    Operacional
                </a>
            </li>

            <!-- Relatórios -->
            <li class="nav-item">
                <a class="nav-link"
                   data-bs-toggle="collapse"
                   href="#relatoriosSubmenu"
                   role="button"
                   aria-expanded="false"
                   aria-controls="relatoriosSubmenu">
                    Relatórios <i class="bi bi-chevron-down"></i>
                </a>

                <div class="collapse submenu" id="relatoriosSubmenu">
                    <div class="collapse-inner">

                        <a href="#" onclick="carregarPagina('rel_semanais')">
                            Semanais
                        </a>

                        <a href="#" onclick="carregarPagina('rel_multas')">
                            Multas
                        </a>

                        <a href="#" onclick="carregarPagina('rel_oficina')">
                            Oficina
                        </a>

                        <a href="#" onclick="carregarPagina('rel_franqueados')">
                            Franqueados
                        </a>
                        <a href="#" onclick="carregarPagina('rel_locatarios')">
                            Locatarios
                        </a>
                    </div>
                </div>
            </li>

            <!-- Configurações -->
            <li class="nav-item">
                <a class="nav-link"
                   data-bs-toggle="collapse"
                   href="#configuracoesSubmenu"
                   role="button"
                   aria-expanded="false"
                   aria-controls="configuracoesSubmenu">
                    Configurações <i class="bi bi-chevron-down"></i>
                </a>

                <div class="collapse submenu" id="configuracoesSubmenu">
                    <div class="collapse-inner">
                        <a href="#" onclick="carregarPagina('usuario')">
                            Usuários
                        </a>
                        <a href="#" onclick="carregarPagina('franqueado')">
                            Franqueados
                        </a>

                        <a href="#" onclick="carregarPagina('despesa_fixa')">
                            Despesas Recorrentes
                        </a>
                        <a href="#" onclick="carregarPagina('plano')">
                            Planos
                        </a>
                        <a href="#" onclick="carregarPagina('codigo')">
                            Códigos
                        </a>
                    </div>
                </div>
            </li>

        </ul>
    `;

    document.getElementById("menu-principal").innerHTML = menu;
}
function mostrarMenuFranqueado() {

    const menu = `
        <ul class="nav flex-column m-0 p-0">

            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('dashboard')">
                    Dashboard
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('frota')">
                    Frota
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('locatario')">
                    Locatários
                </a>
            </li>

            <!-- Financeiro -->
            <li class="nav-item">
                <a class="nav-link"
                   data-bs-toggle="collapse"
                   href="#financeiroSubmenu"
                   role="button"
                   aria-expanded="false"
                   aria-controls="financeiroSubmenu">
                    Financeiro <i class="bi bi-chevron-down"></i>
                </a>

                <div class="collapse submenu" id="financeiroSubmenu">
                    <div class="collapse-inner">
                        <a href="#" onclick="carregarPagina('calcao')">
                            Calções
                        </a>

                        <a href="#" onclick="carregarPagina('semanal')">
                            Semanais
                        </a>

                        <a href="#" onclick="carregarPagina('multa')">
                            Multas
                        </a>

                        <a href="#" onclick="carregarPagina('faturamento')">
                            Faturamentos
                        </a>
                    </div>
                </div>
            </li>

            <!-- Oficina -->
            <li class="nav-item">
                <a class="nav-link" href="#" onclick="carregarPagina('oficina')">
                    Oficina
                </a>
            </li>

            <!-- Relatórios -->
            <li class="nav-item">
                <a class="nav-link"
                   data-bs-toggle="collapse"
                   href="#relatoriosSubmenu"
                   role="button"
                   aria-expanded="false"
                   aria-controls="relatoriosSubmenu">
                    Relatórios <i class="bi bi-chevron-down"></i>
                </a>

                <div class="collapse submenu" id="relatoriosSubmenu">
                    <div class="collapse-inner">

                        <a href="#" onclick="carregarPagina('rel_custos')">
                            Custos
                        </a>

                        <a href="#" onclick="carregarPagina('rel_lucros')">
                            Lucro
                        </a>

                        <a href="#" onclick="carregarPagina('rel_custo_moto')">
                            Custo por Moto
                        </a>

                        <a href="#" onclick="carregarPagina('rel_lucro_moto')">
                            Lucro por Moto
                        </a>

                    </div>
                </div>
            </li>

            <!-- Configurações -->
            <li class="nav-item">
                <a class="nav-link"
                   data-bs-toggle="collapse"
                   href="#configuracoesSubmenu"
                   role="button"
                   aria-expanded="false"
                   aria-controls="configuracoesSubmenu">
                    Configurações <i class="bi bi-chevron-down"></i>
                </a>

                <div class="collapse submenu" id="configuracoesSubmenu">
                    <div class="collapse-inner">

                        <a href="#" onclick="carregarPagina('despesa_fixa')">
                            Despesas Recorrentes
                        </a>

                    </div>
                </div>
            </li>

        </ul>
    `;

    document.getElementById("menu-principal").innerHTML = menu;
}