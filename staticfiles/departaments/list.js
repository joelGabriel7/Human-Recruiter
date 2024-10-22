let tblDepartaments;

function getData() {
    tblDepartaments = $('#data').DataTable({
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
            {"data": "name"},
            {"data": "description"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#' + row.id + '/"   rel="edit" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#' + row.id + '/" type="button" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {
    let model_title = $('.modal-title');
    // let tr = tblDepartaments.cell($(this).closest('td , li')).index();
    //   let data = tblDepartaments.row($(this).closest('tr')).data();
    //delete
    getData()
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        model_title.find('span').html('Crea un Departamento');
        model_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#MyModalDepartament').modal('show');
    });
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        let tr = tblDepartaments.cell($(this).closest('td li')).index();
        let data = tblDepartaments.row($(this).closest('tr')).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="name"]').val(data.name);
        $('input[name="description"]').val(data.description);
        $('#MyModalDepartament').modal('show');

    });
    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        let tr = tblDepartaments.cell($(this).closest('td li')).index();
        let data = tblDepartaments.row($(this).closest('tr')).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el departamento?', parameters, () => {
            Swal.fire({
                title: 'Alerta!',
                text: 'Registro eliminado correctamente!',
                icon: 'success',
                timer: 2000,
            });
            tblDepartaments.ajax.reload();
        });
    });
    $('form').on('submit', function (e) {
        e.preventDefault();
        let parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, () => {
            Swal.fire({
                title: 'Alerta!',
                text: 'Registro agregado correctamente!',
                icon: 'success',
                timer: 2000,
            });
            $('#MyModalDepartament').modal('hide');
            // getData();
            tblDepartaments.ajax.reload();
        });
    });
});