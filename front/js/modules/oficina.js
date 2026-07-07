function iniciarOficina() {

    // tabela
    if ($('#oficinaTableLista').length) {

        if ($.fn.DataTable.isDataTable('#oficinaTableLista')) {
            $('#oficinaTableLista').DataTable().destroy();
        }
    
        $('#oficinaTableLista').DataTable({
            language:{
                url:'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json'
            },
            pageLength:5
        });
    
    }

}