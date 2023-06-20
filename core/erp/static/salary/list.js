var current_date;
var input_year;
var select_month, select_employee;
var tblSalary;
var salary = {
    model: {},
    getEmployeesIds: function () {
        return select_employee.select2('data').map(value => value.id);
    },
    list: function () {
        var parameters = {
            'action': 'search',
            'year': input_year.datetimepicker('date').format("YYYY"),
            'month': select_month.val(),
            'pks': JSON.stringify(salary.getEmployeesIds())
        };
        tblSalary = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: "",
                beforeSend: function () {
                    loading({'text': '...'});
                },
                complete: function () {
                    setTimeout(function () {
                        $.LoadingOverlay("hide");
                    }, 750);
                }
            },
            columns: [
                {data: "employee.codigo"},
                {data: "employee.person.firstname"},
                {data: "employee.person.cedula"},
                {data: "employee.accounts.number"},
                {data: "salary.year"},
                {data: "salary.month.name"},
                {data: "income"},
                {data: "expenses"},
                {data: "total_amount"},
                {data: "id"},
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
                    targets: [-2, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: [-5, -6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a class="btn btn-success btn-xs btn-flat" rel="detail" data-toggle="tooltip" title="Detalle"><i style="color: #FFFFFF" class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/receipt/' + row.id + '/" target="_blank" data-toggle="tooltip" title="Imprimir" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-file-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};


$(function () {
    current_date = moment().format("YYYY_MM_DD");
    input_year = $('input[name="year"]');
    select_month = $('select[name="month"]');
    select_employee = $('select[name="employee"]');

    input_year.datetimepicker({
        viewMode: 'years',
        format: 'YYYY',
        useCurrent: false,
        locale: 'es'
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('.btnSearch').on('click', function () {
        salary.list();
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblSalary.cell($(this).closest('td, li')).index(),
                row = tblSalary.row(tr.row).data();
            salary.model = row;
            $('#tblHeadings').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_headings',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                ordering: false,
                lengthChange: false,
                searching: false,
                paginate: false,
                columnDefs: [
                    {
                        targets: [0],
                        class: 'text-left',
                        render: function (data, type, row) {
                            return data.toUpperCase();
                        }
                    },
                    {
                        targets: [1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: [-1, -2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (data === '---') {
                                return data;
                            }
                            return '$' + data
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalSalary').modal('show');
        });

    $('.btnPrintReceiptEmployee').on('click', function () {
        var url = pathname + 'print/receipt/' + salary.model.id + '/';
        window.open(url, '_blank').focus();
    });

    $('.btnExportSalariesPdf').on('click', function () {
        $.ajax({
            url: pathname,
            data: {
                'year': input_year.datetimepicker('date').format("YYYY"),
                'month': select_month.val(),
                'pks': JSON.stringify(salary.getEmployeesIds()),
                'action': 'export_salaries_pdf'
            },
            type: 'POST',
            xhrFields: {
                responseType: 'blob'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            beforeSend: function () {
                loading({'text': '...'});
            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    var a = document.createElement("a");
                    document.body.appendChild(a);
                    a.style = "display: none";
                    const blob = new Blob([request], {type: 'application/pdf'});
                    const url = URL.createObjectURL(blob);
                    a.href = url;
                    a.download = "salarios_pdf_" + current_date + ".pdf";
                    a.click();
                    window.URL.revokeObjectURL(url);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {
                $.LoadingOverlay("hide");
            }
        });
    });

    $('.btnExportSalariesExcel').on('click', function () {
        $.ajax({
            url: pathname,
            data: {
                'year': input_year.datetimepicker('date').format("YYYY"),
                'month': select_month.val(),
                'pks': JSON.stringify(salary.getEmployeesIds()),
                'action': 'export_salaries_excel'
            },
            type: 'POST',
            xhrFields: {
                responseType: 'blob'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            beforeSend: function () {
                loading({'text': '...'});
            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    var a = document.createElement("a");
                    document.body.appendChild(a);
                    a.style = "display: none";
                    const blob = new Blob([request], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
                    const url = URL.createObjectURL(blob);
                    a.href = url;
                    a.download = "salarios_excel_" + current_date + ".xlsx";
                    a.click();
                    window.URL.revokeObjectURL(url);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            },
            complete: function () {
                $.LoadingOverlay("hide");
            }
        });
    });

    select_employee.select2({
        theme: 'bootstrap4',
        language: "es",
        placeholder: 'Buscar..',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_employee'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {

        })
        .on('select2:clear', function (e) {

        });
});