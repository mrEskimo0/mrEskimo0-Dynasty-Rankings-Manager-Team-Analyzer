$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});



function check_boxes(reload) {
  if (reload == true){
    console.log('do nothing')
  }
  else{
    var my_list = $('.try_checkbox li');
    my_list.each(function(){
      $(this).find('input').prop('checked', true);
    })

  }
}

function look_at_boxes(){
  var my_list = $('.try_checkbox li');
  var checkedbox = false;
  my_list.each(function(){
    if ($(this).find('input').is(':checked')){
      console.log('box is checked')
      checkedbox = true
    }
    else{
      console.log('no check')

    }
  })
  if (checkedbox == false){
    my_list.each(function(){
      $(this).find('input').prop('checked', true);
    })
  }

}

look_at_boxes()

$('#submit-ranks').click(function(event){
  var new_values_dict = {}
  $('.player-value').each(function() {
    var old_val = $(this).attr('value');
    var new_val = $(this).val();

    if (new_val != old_val) {
      var player_name = $(this).parent().parent().find(".player-name").text()
      new_values_dict[player_name] = new_val
    }
  })
  var endpoint = $('#submit-ranks').attr("data-url")
  $.ajax({
    type: "POST",
    url: endpoint,
    data: {
      senddata: JSON.stringify(new_values_dict),
    },
    success: function(){
      console.log('Players Successfully Updated')
      location.reload();
    }
  })
})

function add_percent() {
  var btn = $(this).parent().parent().find(".btn.btn-secondary.percent")
  var old_val = parseInt(btn.text())
  if (old_val >= 100){
    console.log("Max % Increase")
  }
  else{
    btn.html(old_val + 1 + " %");
  }
}

function min_percent() {
  var btn = $(this).parent().parent().find(".btn.btn-secondary.percent")
  var old_val = parseInt(btn.text())
  if (old_val <= -100){
    console.log("Max % Decrease")
  }
  else{
    btn.html(old_val - 1 + " %");
  }
}

$(".addbutton2").on('click', add_percent);
$(".minbutton2").on('click', min_percent);

function apply_percent() {
  var box = $(this).parent().parent().parent().find(".player-value")
  var old_val = parseFloat(box.val())
  var current_percent = parseInt($(this).text())
  var new_val = old_val + (old_val * (current_percent/100))
  var rounded_val = Math.round((new_val + Number.EPSILON)*100) / 100
  box.val(rounded_val)
}

$(".btn.btn-secondary").on('click', apply_percent);

function swap_players_up() {
  var this_row = $(this).closest('tr');
  var this_points = this_row.find(".player-value");
  var this_points_num = this_points.val();
  var this_row_num = this_row.find(".count");
  var this_row_num_actual = this_row_num.text();

  var prev_row = this_row.prev();
  var prev_points = prev_row.find(".player-value");
  var prev_points_num = prev_points.val();
  var prev_row_num = prev_row.find(".count");
  var prev_row_num_actual = prev_row_num.text();

  if (prev_points_num === undefined){
    console.log('previous row unavailable')
  }
  else {
    prev_points.val(this_points_num);
    prev_row_num.text(this_row_num_actual);
    this_points.val(prev_points_num);
    this_row_num.text(prev_row_num_actual);
    prev_row.before(this_row);
  }

}

function swap_players_down() {
  var this_row = $(this).closest('tr');
  var this_points = this_row.find(".player-value");
  var this_points_num = this_points.val();
  var this_row_num = this_row.find(".count");
  var this_row_num_actual = this_row_num.text();

  var next_row = this_row.next();
  var next_points = next_row.find(".player-value");
  var next_points_num = next_points.val();
  var next_row_num = next_row.find(".count");
  var next_row_num_actual = next_row_num.text();

  if (next_points_num === undefined){
    console.log('previous row unavailable')
  }
  else{
    next_points.val(this_points_num);
    next_row_num.text(this_row_num_actual);
    this_points.val(next_points_num);
    this_row_num.text(next_row_num_actual);
    next_row.after(this_row);
  }
}

$(".addbutton").on('click', swap_players_up);
$(".minbutton").on('click', swap_players_down);
