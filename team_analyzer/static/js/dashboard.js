function showLoaderOnClick(url) {
      showLoader();
      window.location=url;
  }
function showLoader(){
      $('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div><p class="loader-text">Loading Your Team... This May Take A Minute</p></div>');
  }

$(window).on('load', function(){
  setTimeout(removeLoader, 0); //wait for page load PLUS two seconds.
});
function removeLoader(){
    $( "#loadingDiv" ).fadeOut(500, function() {
      // fadeOut complete. Remove the loading div
      $( "#loadingDiv" ).remove(); //makes page more lightweight
  });
}


// });

$(window).bind("pageshow", function(event) {
    if (event.originalEvent.persisted) {
        window.location.reload()
    }
});
