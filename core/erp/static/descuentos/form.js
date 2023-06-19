let fv;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: window.location.pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="name"]').value,
                                    pattern: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        }
                    }
                },
                code: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: window.location.pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="code"]').value,
                                    pattern: 'code',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        }
                    }
                },
                order: {
                    validators: {
                        notEmpty: {
                             message: 'Establezca una posicion'
                        },
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un item'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var args = {
                'params': new FormData(fv.form),
                'form': fv.form
            };
            submit_with_formdata(args);
        });
});

$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="type"]')
        .on('change.select2', function () {
            fv.revalidateField('type');
        });

    $('[name="order"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });
});
