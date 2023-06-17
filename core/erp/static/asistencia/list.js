let input_date_range;
let tblAssistance;
let current_date;
let assistance = {
    list: function () {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        tblAssistance = $('#tblAssistance').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url:  window.location.pathname,
                type: 'POST',
                data: parameters,
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "assistance.date_joined"},
                {"data": "employee.fullname"},
                {"data": "employee.person.cedula"},
                {"data": "employee.department.name"},
                {"data": "employee.position.name"},
                {"data": "description"},
                {"data": "state"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.description)) {
                            return row.description;
                        }
                        return 'Sin detalles';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.state) {
                            return '<span class="badge badge-success badge-pill">Si</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">No</span>';
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    current_date = moment().format("YYYY_MM_DD");
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        });

    $('.drp-buttons').hide();

    $('.btnSearchAssistances').on('click', function () {
        assistance.list();
    });

     $('.btnUpdateAssistance').on('click', function () {
        var start_date = input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD');
        var end_date = input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD');
        if (start_date !== end_date) {
            message_error('Para editar una asistencia se debe hacer de un dia en especifico no en rango');
            return false;
        }
        var currentUrl = location.pathname;
        var updatedUrl = currentUrl.replace('/list/', '/update/');
       location.href = updatedUrl + start_date + '/';
    });
})