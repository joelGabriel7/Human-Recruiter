$(function () {
    tblVacations = $('#data').DataTable({
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
                    var buttons = '<a href="/erp/vacations/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> &nbsp;';
                    buttons += '<a href="/erp/vacations/generar_reporte_vacaciones/'+  row.id + '/" type="button" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file"></i></a> &nbsp;';
                    buttons += '<a href="#' + row.id + '/" type="button" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
$(function () {
    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        let tr = tblVacations.cell($(this).closest('td li')).index();
        let data = tblVacations.row($(this).closest('tr')).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar esta solicitud?', parameters, () => {
            Swal.fire({
                title: 'Alerta!',
                text: 'Registro eliminado correctamente!',
                icon: 'success',
                timer: 2000,
            });
            tblVacations.ajax.reload();
        });
    });
});
