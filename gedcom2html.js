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


   // arrows = "i[id^=show_row_]";
   // $(arrows).each(function(index, value)
   // {
      // if $(value).hasClass('fa-arrow-circle-right')
      // {
         
      // }
   // }



// $('li').click(function() {
  // $(this).children('ul').toggle();
// });

// function updateParents(){
   // items = "[id^=parent_]";
   // $(items).each(function(index, value)
   // {
      // id = $(value).attr('id');
      // $(id).hide();
      // $(id).removeClass('glyphicon-chevron-down');
   // });
// }



// $(function () {
    // $('.tree li').hide();
    // $('.tree>ul>li').show();
    // $('.tree li').on('click', function (e) {
        // var children = $(this).find('> ul > li');
        // if (children.is(":visible")) children.hide('fast');
        // else children.show('fast');
        // e.stopPropagation();
    // });
// });