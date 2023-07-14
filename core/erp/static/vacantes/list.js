$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        paging: true,
        serverSide: true,
        searching:true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata';
                $.extend(d, {
                    start: d.start,
                    length: d.length || 10,
                    search: {
                        value: d.search.value || ''
                    }
                });
                return d;
            },
            dataSrc: function (json) {
                // console.log(json);  // Verifica la respuesta JSON recibida
                return json.data;
            },
            beforeSend: function () {
                loading({'text': '...'});
            },
            complete: function () {
                setTimeout(function () {
                    $.LoadingOverlay("hide");
                }, 750);
            }
        },
        columns: [
            {"data": "id"},
            {"data": "posicion.name"},
            {"data": "description"},
            {"data": "min_salary"},
            {"data": "max_salary"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/vacante/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/vacante/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
