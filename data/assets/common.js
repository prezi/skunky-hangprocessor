$(document).on("click", '.expando', function() {
  if ($(this).hasClass('collapsed')) {
    $(this).removeClass('collapsed');
    $(this).nextAll().fadeIn();
  }
  else {
    $(this).addClass('collapsed');
    $(this).nextAll().fadeOut();
  }
})

$('.expando.collapsed').nextAll().hide();

$(document).on("click", '.threadhead .threadid', function() {
  var head = $(this).closest('.threadhead');
  var next = head.nextUntil('.threadhead');
  if (head.hasClass('collapsed')) {
    head.removeClass('collapsed');
    $(this).attr('rowspan', next.length + 1);
    next.show();
  }
  else {
    head.addClass('collapsed');
    $(this).removeAttr('rowspan');
    next.hide();
  }
});

$(document).on("click", 'table.data td', function() {
  var row = $(this).closest('tr');
  row.toggleClass('highlight');
});

$('.threadhead').each(function() {
  var crashthread = $(this).closest('.dumpthreads').attr('data-crashthread');
  var thisthread = $(this).attr('data-threadid');
  if (thisthread != crashthread) {
    $(this).addClass('collapsed');
    $('.threadid', this).removeAttr('rowspan');
    $(this).nextUntil('.threadhead').hide();
  }
});

$.fn.isAfter = function(elem) {
  if (typeof(elem) == "string") {
    elem = $(elem);
  }
  return this.add(elem).index(elem) == 0;
};

$(document).on('input', '.tablefilter', function() {
  var input = this;
  var words = $(input).val().split(/\s+/);

  // first table.data after this in DOM position
  var table = $('table.data').filter(function() {
    return $(this).isAfter(input);
  }).first();

  var shown = 0;
  var rows = $('tbody tr', table).each(function() {
    var t = $(this).text();
    for (var i = 0; i < words.length; ++i) {
      if (t.indexOf(words[i]) == -1) {
        $(this).hide();
        return;
      }
    }
    $(this).show();
    ++shown;
  });
  var totaltext;
  if (shown == rows.length) {
    totaltext = '';
  }
  else {
    totaltext = "Showing " + shown + " of " + rows.length;
  }
  $(this).nextAll('.filtertotal').text(totaltext);
});
