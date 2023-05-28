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
            {"data": "codigo"},
            {"data": "fullname"},
            {"data": "department.name"},
            {"data": "position.name"},
            {"data": "turn.name"},
            {"data": "salary"},
            {"data": "accounts.type"},
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
                    if (data.name === 'hired') {
                        html += '<span class="badge badge-success">' + data.name + '</span>';
                    } else if (data.name === 'dismissed') {
                        html += '<span class="badge badge-danger">' + data.name + '</span>';
                    } else {
                        html += data.name;
                    }
                    return html;
                }
            },


            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],

        initComplete: function (settings, json) {

        }
    });
});