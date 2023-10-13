function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel()
                }
            },
        }
    })
}

function loading(args) {
    if (!args.hasOwnProperty('fontawesome')) {
        args.fontawesome = 'fas fa-circle-notch fa-spin';
    }
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: args.fontawesome,
        custom: $("<div>", {
            css: {
                'font-family': "'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif'",
                'font-size': '16px',
                'font-weight': 'normal',
                'text-align': 'center',
                'position': 'absolute',
                'top': '36%',
                'width': '100%',
            },
            text: args.text
        })
    });
}


function submit_with_formdata(args) {
    if (!args.hasOwnProperty('type')) {
        args.type = 'type';
    }
    if (!args.hasOwnProperty('theme')) {
        args.theme = 'material';
    }
    if (!args.hasOwnProperty('title')) {
        args.title = 'Confirmación';
    }
    if (!args.hasOwnProperty('icon')) {
        args.icon = 'fas fa-info-circle';
    }
    if (!args.hasOwnProperty('content')) {
        args.content = '¿Esta seguro de realizar la siguiente acción?';
    }
    if (!args.hasOwnProperty('pathname')) {
        args.pathname= window.location.pathname ;
    }
    $.confirm({
        type: args.type,
        theme: args.theme,
        title: args.title,
        icon: args.icon,
        content: args.content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: args.pathname,
                        data: args.params,
                        type: 'POST',
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': csrftoken
                        },
                        processData: false,
                        contentType: false,
                        beforeSend: function () {
                            loading({'text': '...'});
                        },
                        success: function (request) {
                            if (!request.hasOwnProperty('error')) {
                                if (args.hasOwnProperty('success')) {
                                    args.success(request);
                                } else {
                                    location.href = $(args.form).attr('data-url');
                                }
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
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}

function validate_text_box(args) {
    if (!args.hasOwnProperty('type')) {
        args.type = 'numbers';
    }
    var key = args.event.keyCode || args.event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = key > 47 && key < 58;
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    switch (args.type) {
        case "numbers":
            return numbers;
        case "numbers_spaceless":
            return numbers_spaceless;
        case "letters":
            return letters;
        case "numbers_letters":
            return numbers || letters;
        case "letters_spaceless":
            return letters_spaceless;
        case "decimals":
            return decimals;
    }
    return true;
}

function load_image(args) {
    if (!args.hasOwnProperty('alt')) {
        args.alt = '';
    }
    Swal.fire({
        imageUrl: args.url,
        imageWidth: '100%',
        imageHeight: 250,
        imageAlt: args.alt,
        animation: false
    })
}