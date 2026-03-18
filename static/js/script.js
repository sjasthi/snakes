// DataTable Init
$(document).ready(function() {
    if ($('#quotesTable').length) {
        $('#quotesTable').DataTable({
            pageLength: 25,
            order: [[0, 'asc']],
            columnDefs: [
                { width: '5%', targets: 0 },
                { width: '95%', targets: 1 }
            ]
        });
    }
});