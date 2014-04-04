// Capture an enter event
(function($) {
    $.fn.onEnter = function(func) {
        this.bind('keypress', function(e) {
            if (e.keyCode == 13) {
                func.apply(this, [e]);    
            }
        });
        return this;
     };
})(jQuery);

// Replace one class with another
jQuery.fn.replaceClass = function(toReplace,replaceWith){
    return $(this).each(function(){
        return $(this).removeClass(toReplace).addClass(replaceWith);
    });
}

$(function() {

    // Un/favorite an article
    $('.favorite').click(function() {
        var id = $(this).closest('article').attr('id');

        // Set the HTTP verb and adjust display of button
        var verb = 'POST';
        if ($(this).hasClass('loved')) {
            $(this).replaceClass('loved', 'unloved'); 
            $(this).replaceClass('glyphicon-heart', 'glyphicon-heart-empty');
            var verb = 'DELETE';
        }
        else if ($(this).hasClass('unloved')) {
            $(this).replaceClass('unloved', 'loved');
            $(this).replaceClass('glyphicon-heart-empty', 'glyphicon-heart'); 
        };

        // Try an HTTP request
        jQuery.ajax({
            url: '/favorites',
            type: verb,
            headers: {'id': id}
        });

        // Remove unfavorited items from view on favorites
        if ($(this).hasClass('slideparent')) {
            $('#' + id).closest('.row').slideUp();
        };
    });

    // Toggle a condensed view
    $('h2 a.glyphicon-list').click(function() {
        $('.fold').toggle();
    });

    // Show/hide the add box
    $('h2 a.glyphicon-plus').click(function() {
        $('#articlebox').toggle();
        $('#articlebox').focus();
        $(this).hasClass('glyphicon-plus') ? 
            $(this).replaceClass('glyphicon-plus', 'glyphicon-minus') : 
            $(this).replaceClass('glyphicon-minus', 'glyphicon-plus');
    });

    // Add an article
    $('#articlebox').onEnter(function(e) {
        $(this).prop('disabled', true);
        jQuery.ajax({
            url: '/',
            type: 'POST',
            headers: {'article': $(this).val()},
            statusCode: {
                200: function() {
                    $('header h1').text('reloading...');
                    location.reload();
                },
                400: function() {
                    $('#articlebox')
                        .val('')
                        .prop('disabled', false)
                        .attr('placeholder', "I couldn't save that :(");
                }
            }
        });
    });

    // Delete an article
    $('article a.delete').click(function(e) {
        var id = $(this).attr('article-id');
        $.ajax({
            url: '/articles/' + id,
            type: 'DELETE',
            statusCode: {
                200: function() {
                    $('#' + id).closest('.row').slideUp();
                },
                500: function() {
                    $('#' + id + ' p a.delete').text('Error :(');
                }
            }
        });
    });
});
