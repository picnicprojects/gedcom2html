function toggle_tree(id){
   $('#ul_'+id).toggle(1000);
   if ($('#'+id).hasClass('fa-arrow-circle-right') == true)
   {
      $('#'+id).removeClass('fa-arrow-circle-right');
      $('#'+id).addClass('fa-arrow-circle-down');
   }
   else
   {
      $('#'+id).removeClass('fa-arrow-circle-down');
      $('#'+id).addClass('fa-arrow-circle-right');
   }
}

$(document).ready(function() {
   arrows = "[id^=ul_parent_]";
   $(arrows).each(function(index, value)
   {
      $(value).hide(1000);
   });
   arrows = "[id^=ul_children_]";
   $(arrows).each(function(index, value)
   {
      $(value).hide(1000);
   });
});