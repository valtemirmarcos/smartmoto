function iniciarFaturamento() {

    // tabela
    if ($('#faturamentoTableLista').length) {

        if ($.fn.DataTable.isDataTable('#faturamentoTableLista')) {
            $('#faturamentoTableLista').DataTable().destroy();
        }
    
        $('#faturamentoTableLista').DataTable({
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });
    
    }

}