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