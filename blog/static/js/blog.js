$(function() {

   var current = location.pathname;

   $('#base-nav li a').each(function() {
      var $this = $(this);
      $this.removeClass('active');
      if ($this.attr('href') === current) {
         $this.addClass('active');
      }
   });
});


function showPostComments(btn_id) {

   var s = document.getElementById("btn-" + btn_id).innerHTML

   if (s === "show comments") {
      document.getElementById("btn-" + btn_id).innerHTML = "hide comments"
      $('#comment-' + btn_id).show()
   }
   else if (s === "hide comments") {
      document.getElementById("btn-" + btn_id).innerHTML = "show comments"
      $('#comment-' + btn_id).hide()
   }

}
