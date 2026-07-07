function iniciarDespesaFixa() {

    // tabela
    if ($('#despesa_fixaTableLista').length) {

        if ($.fn.DataTable.isDataTable('#despesa_fixaTableLista')) {
            $('#despesa_fixaTableLista').DataTable().destroy();
        }
    
        $('#despesa_fixaTableLista').DataTable({
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });
    
    }

}