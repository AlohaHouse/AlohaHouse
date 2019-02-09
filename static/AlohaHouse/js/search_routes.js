$('#submit-btn').on('click', function(){

    $('#routes-form').submit();
});

$('.search-route').on('click', function(){

    var label = $(this).clone(false);
    label.removeClass('search-route');
    label.addClass('search-route-no-hover');

    $('.routes-box').append(label);
});