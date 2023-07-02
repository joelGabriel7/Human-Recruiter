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
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "image"},
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
                    var buttons = '<a href="/user/update/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/user/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },

            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;"  alt="">'
                }
            },


        ],
        initComplete: function (settings, json) {

        }
    });
});