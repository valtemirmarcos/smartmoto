function iniciarMulta() {

    // tabela
    if ($('#multaTableLista').length) {

        if ($.fn.DataTable.isDataTable('#multaTableLista')) {
            $('#multaTableLista').DataTable().destroy();
        }
    
        $('#multaTableLista').DataTable({
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });
    
    }

}