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

$(function() {

    // Show/hide the add box
    $('h1 a').click(function() {
        $('#articlebox').toggle();
        $('#articlebox').focus();
        $(this).text() == '+' ? $(this).text('-') : $(this).text('+');
    });

    // Add an article
    $('#articlebox').onEnter(function(e) {
        $(this).prop('disabled', true);
        jQuery.ajax({
            url: '/save',
            type: 'POST',
            headers: {'article': $(this).val()},
            statusCode: {
                200: function() {
                    $('h1').text('reloading...');
                    location.reload();
                },
                400: function() {
                    $('#articlebox').val('');
                    $('#articlebox').prop('disabled', false);
                    $('#articlebox').attr('placeholder', "I couldn't save that :(");
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
