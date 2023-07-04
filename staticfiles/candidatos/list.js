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
            {"data": "cedula"},
            {"data": "birthdate"},
            {"data": "gender.name"},
            {"data": "phone"},
            {"data": "email"},
            {"data": "address"},
            {"data": "desc"},
        ],
        columnDefs: [
            // {
            //
            //     targets: [4],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var html = '';
            //         $.each(row.gender, function (key,value) {
            //             html+= '<span class="badge badge-success">'+value.name+'</span>  '
            //         })
            //         return html;
            //     }
            // },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/candidato/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/candidato/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});