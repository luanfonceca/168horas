function submitParentForm(element) {
  $(element).parents('form').submit();
}

$(document).ready(function() {
  $("#search-icon").click(function(e) {
    $("#id_search").val('');
    submitParentForm(this);
  });

  $("#search-close-icon").click(function() {
    $("#id_search").val('');
    submitParentForm(this);
  });

  $(".card").click(function(){
    var href = $(this).attr('data-href');
    if (href) {
      window.location.replace(href);
    }
  });

  $(".dropdown-form-button").click(function(){
    submitParentForm(this);
  });

  $(".card .card-action a").click(function(e) {
    e.stopPropagation();
  });
});