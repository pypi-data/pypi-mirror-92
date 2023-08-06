$.extend($.fn.dataTable.defaults, {
  language: {
    "processing": "<i class='fa fa-spinner fa-spin'></i>"
  }
});

$(document).ready(function () {
  $('#notifications > span').map(function (i, e) {
    var category = $(e).attr('data-category');
    var title = $(e).attr('data-title');
    var message = $(e).attr('data-message');
    new PNotify({
      'title': title,
      'text': message,
      'type': category,
      'styling': 'bootstrap3',
      'hide': true,
      'delay': 10000
    })
  });

  $('#windowFullScreen').click(function () {
    var elem = document.body;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { /* Firefox */
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
      elem.msRequestFullscreen();
    }
  });

  $('#iframe-modal iframe').on('load', function (event) {
    $('#iframe-modal-spinner').hide();
    $(this).show();
  });

  $(document).on('click', '.modal-link', function (event) {
    var url = $(this).attr('data-url');
    $('#iframe-modal iframe').hide();
    $('#iframe-modal-spinner').show();
    $('#iframe-modal iframe').attr('src', url);
    $('#iframe-modal').modal();
  });

  $('input[type="checkbox"]').each(function (idx) {
    var klass = $(this).attr('class');
    if (klass && klass.includes('checkbox')) {
      // enable icheckbox later
    } else {
      var a = new Switchery(this, { 'color': '#bbe33d' });
    }
  });

});
