/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

let ns = {};

ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    return {
        'bacon_number': function(name) {
            let ajax_options = {
                type: 'GET',
                url: 'api/v1/actor/' + name +'/bacon_number',
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
                .done(function(data) {
                    data['name'] = name;
                    console.log(data);
                    $event_pump.trigger('model_show_results', data);
                })
                .fail(function(xhr, textStatus, errorThrown) {
                    $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
                })
        },
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $name = $('#name');

    // return the API
    return {
        reset: function() {
            $name.val('');
            $name.val('').focus();
        },
        update_editor: function(name) {
            $name.val(name);
            $name.val(name).focus();
        },
        show_results: function(name, bacon_number) {
            console.log(name);
            console.log(bacon_number);
            $('.result').append(`<p>${name} bacon number is ${bacon_number}</p>`)
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $name = $('#name');

    // Validate input
    function validate(name) {
        return name !== "";
    }

    // Create our event handlers
    $('#bacon_number').click(function(e) {
        let name = $name.val();

        e.preventDefault();

        if (validate(name)) {
            model.bacon_number(name)
        } else {
            alert('Problem with the name');
        }
    });

    // Handle the model events
    $event_pump.on('model_show_results', function(e, data) {
        console.log(data);
        view.show_results(data['name'], data['degrees']);
        view.reset();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));