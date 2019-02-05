$('#favolite-form').submit(e => {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

    var $form = $(this);

    $.ajax({
        'url': $form.attr('action'),
        'type': 'POST',
        'data': $form.serialize(),
        'dataType': 'json'
    }).done( response => {
        // 成功したら
        alert('fjsdflkjslkfjlskjflksfl')
    });

});