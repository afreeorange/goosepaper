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

    // Show/hide the search
    $('h2 a.glyphicon-search').click(function() {
        $('#articlebox').hide();

        $('#searchbox').toggle();
        $('#searchbox').focus();
        
        $(this).toggleClass('red');
        $('h2 a.glyphicon-plus').removeClass('red');
    });

    // Show/hide the add box
    $('h2 a.glyphicon-plus').click(function() {
        $('#searchbox').hide();

        $('#articlebox').toggle();
        $('#articlebox').focus();

        $(this).toggleClass('red');
        $('h2 a.glyphicon-search').removeClass('red');
    });

    // Toggle a condensed view
    $('h2 a.glyphicon-list').click(function() {
        $('.fold').toggle();
        $.cookie('collapse') ? $.removeCookie('collapse') : $.cookie('collapse', true);
        $(this).toggleClass('folded-icon');
    });

    // Infinite scroll the page
    $('#content').infinitescroll({
        navSelector: 'nav',
        nextSelector: 'nav a',
        itemSelector: '#content article',
        animate: true,
        loading: {
            finishedMsg: "<h3>No more articles, Heidi</h3>",
            img: "data:image/gif;base64,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",
            msgText: "<h4>fetching more...</h4>",
        }
    });

    // Un/favorite an article
    $('#content').on('click', '.favorite', function() {
        var id = $(this).closest('article').attr('id');

        // Set the HTTP verb and adjust display of button
        var verb = 'POST';
        if ($(this).hasClass('red')) {
            $(this).replaceClass('red', 'gray'); 
            $(this).replaceClass('glyphicon-heart', 'glyphicon-heart-empty');
            var verb = 'DELETE';
        }
        else if ($(this).hasClass('gray')) {
            $(this).replaceClass('gray', 'red');
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
        }); // End Ajax call
    });

    // Search articles
    $('#searchbox').onEnter(function(e) {
        location.replace('/search/' + $(this).val());
    });

    // Delete an article
    $('#content').on('click', '.delete', function(e) {
        var id = $(this).attr('article-id');
        $.ajax({
            url: '/articles/' + id,
            type: 'DELETE',
            statusCode: {
                200: function() {
                    $('#' + id).slideUp();
                },
                500: function() {
                    $('#' + id + ' p a.delete').text('Error :(');
                }
            }
        }); // End Ajax call
    });

});
