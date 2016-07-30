function submitParentForm(element) {
  $(element).parents('form').submit();
}

function getUrlParameter(sParam) {
  var sPageURL = decodeURIComponent(window.location.search.substring(1)),
      sURLVariables = sPageURL.split('&'),
      sParameterName,
      i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined ? true : sParameterName[1];
    }
  }
}

function replaceUrlParameter(param, newval, search) {
    var regex = new RegExp("([?;&])" + param + "[^&;]*[;&]?");
    var query = search.replace(regex, "$1").replace(/&$/, '');

    return (query.length > 2 ? query + "&" : "?") + (newval ? param + "=" + newval : '');
}

$(document).ready(function() {
  var page_url = getUrlParameter('page');
  var page = $('.pagination .active').text().trim();
  if (page != page_url) {
    var params = replaceUrlParameter('page', page, window.location.search);

    window.history.pushState(
      "object or string", "Title", window.location.pathname + params
    );
  }

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