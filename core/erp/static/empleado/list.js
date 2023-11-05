$(function () {
    tblEmploye= $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        paging: true,
        serverSide: true,
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
                return d;  // Agrega este retorno
            },
            dataSrc: function (json) {
                console.log(json.data);
                return json.data;
            },
            beforeSend: function () {
                loading({'text': '...'});
            },
            complete: function () {
                setTimeout(function () {
                    $.LoadingOverlay("hide");
                }, 500);
            }
        },
        columns: [
            {"data": "hiring_date"},
            {"data": "codigo"},
            {"data": "full_name"},
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

                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let html = '';
                    html += '<span class="badge badge-success">$' + data + '</span>  '
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
                    } else if (data === 'Licencia') {
                        html += '<span class="badge badge-info">' + data + '</span>';
                    } else if (data === 'Vacaciones') {
                        html += '<span class="badge badge-primary">' + data + '</span>';
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
                    let buttons = '<a href="#' + row.id + '/" type="button" rel="active" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-plus"></i></a>';
                    buttons += '&nbsp;';
                    buttons += '<a href="#' + row.id + '/" type="button" rel="deactive" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '&nbsp;';
                    buttons += '<a href="/erp/empleados/edit/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],

        initComplete: function (settings, json) {

        }
    });
});

$(function () {
    $('#data tbody').on('click', 'a[rel="deactive"]', function () {
         let tr = tblEmploye.cell($(this).closest('td li')).index();
         let data = tblEmploye.row($(this).closest('tr')).data();
         let parameters = new FormData();
         parameters.append('action', 'deactive');
         parameters.append('id', data.id);
         submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro despedir este empleado?', parameters, () => {
             Swal.fire({
                 title: 'Alerta!',
                 text: 'Empleado despedido correctamente!',
                 icon: 'success',
                 timer: 2000,
             });
             tblEmploye.ajax.reload();
         });
     });

     $('#data tbody').on('click', 'a[rel="active"]', function () {
        let tr = tblEmploye.cell($(this).closest('td li')).index();
        let data = tblEmploye.row($(this).closest('tr')).data();
        let parameters = new FormData();
        parameters.append('action', 'active');
        parameters.append('id', data.id);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro recontratar a este empleado?', parameters, () => {
            Swal.fire({
                title: 'Alerta!',
                text: 'Empleado recontratado correctamente!',
                icon: 'success',
                timer: 2000,
            });
            tblEmploye.ajax.reload();
        });
    });
 });


$(function () {
    $('.generar_report').on('click', function () {
        $("#ModalSelectReport").modal('show')
    })

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',

    });

})



