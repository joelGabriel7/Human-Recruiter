$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "hiring_date"},
            {"data": "codigo"},
            {"data": "person__firstname"},
            {"data": "department__name"},
            {"data": "position__name"},
            {"data": "turn__name"},
            {"data": "salary"},
            {"data": "estado"},
            {"data": "desc"},
        ],
        columnDefs: [
            {

                targets: [1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    html += '<span class="badge badge-secondary">' + data + '</span>  '
                    return html;
                }
            },

            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    if (data === 'Contratado') {
                        html += '<span class="badge badge-success">' + data + '</span>';
                    } else if (data === 'Despedido') {
                        html += '<span class="badge badge-danger">' + data + '</span>';
                    } else {
                        html += data;
                    }
                    return html;
                }
            },


            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/empleados/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/empleados/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],

        initComplete: function (settings, json) {

        }
    });
});