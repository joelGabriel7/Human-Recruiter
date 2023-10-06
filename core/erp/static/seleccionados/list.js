let tblApply;

function getData() {
    tblApply = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        paging: true,
        searching:true,
        destroy: true,
        deferRender: true,
        serverSide: true,  // Habilita el procesamiento en el lado del servidor
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata',
                'page': 'current',  // Envía el número de página actual al servidor
            },
            dataSrc: 'data',  // Indica la propiedad del objeto JSON que contiene los datos
        },
        columns: [
            {"data": "id"},
            {"data": "fullname"},
            {"data": "person__phone"},
            {"data": "vacants__posicion__name"},
            {"data": "vacants__max_salary"},
            {"data": "vacants__min_salary"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/select/edit/' + row.id + '/" rel="edit" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#' + row.id + '/"  rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

};

$(function (){

    let model_title = $('.modal-title');

    getData();
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        model_title.find('span').html('Crea un Aplicante');
        model_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#MyModalTurn').modal('show');
    });
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        model_title.find('span').html('Edita un Aplicante');
        model_title.find('i').removeClass().addClass('fas fa-edit')
        let tr = tblApply.cell($(this).closest('td , li')).index();
        let data = tblApply.row($(this).closest('tr')).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('select[name="person"]').val(data.person.id);
        $('select[name="vacants"]').val(data.vacants.id);
        $('#MyModalTurn').modal('show');
    });
    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        model_title.find('span').html('Edita un Aplicante');
        model_title.find('i').removeClass().addClass('fas fa-edit')
        let tr = tblApply.cell($(this).closest('td , li')).index();
        let data = tblApply.row($(this).closest('tr')).data();
        let parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro?', parameters, () => {
            Swal.fire({
                title: 'Alerta!',
                text: 'Registro Eliminado correctamente!',
                icon: 'success',
                timer: 2000,
            });
            tblApply.ajax.reload();
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
            $('#MyModalTurn').modal('hide');
            // getData();
            tblApply.ajax.reload();
        });
    });
    $('#MyModalTurn').on('shown.bs.modal', function () {
        // $('form')[0].reset();
    })
});