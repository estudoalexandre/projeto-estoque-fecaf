$(document).ready(function () {
    console.log("tabulator.js");
    $('#produtoTabela').DataTable({
        "responsive": true,
        "paging": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "language": {
            "url": "/static/js/pt-BR.json"
        }
    });
});
