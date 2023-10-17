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
            {"data": "id"},
            {"data": "fullname"},
            {"data": "start_date"},
            {"data": "end_date"},
            {"data": "motivo"},
            {"data": "observaciones"},
            {"data": "state_vacations.name"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    if (data === 'Acceptada') {
                        html += '<span class="badge badge-success">' + data + '</span>';
                    } else if (data === 'Denegada') {
                        html += '<span class="badge badge-danger">' + data + '</span>';
                    } else if (data === 'Pendiente') {
                        html += '<span class="badge badge-info">' + data + '</span>';
                    } else if (data === 'Finalizada') {
                        html += '<span class="badge badge-warning">' + data + '</span>';
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
                    var buttons = '<a href="/erp/vacations/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});