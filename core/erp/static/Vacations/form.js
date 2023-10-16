$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',

    });
});

$(function () {
    $('#start_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        icons: {
            time: 'far fa-clock'
        }
    });
});

$(function () {
    $('#end_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        icons: {
            time: 'far fa-clock'
        }
    });
});