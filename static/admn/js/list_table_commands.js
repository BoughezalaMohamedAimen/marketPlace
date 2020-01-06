$(document).ready(function(){
  var selected=[];
  $('.custom-checkbox-all').click(function(){
    //alert()
    $('.custom-checkbox-table-row').prop('checked', $(this).is(':checked')).change();

  })


  $('.custom-checkbox-table-row').change(function(){
    selected=[];
    $('.custom-checkbox-table-row').each(function(){
      if($(this).is(':checked'))
        selected.push($(this).next().html())
      })
      $('.selected-count').html('('+selected.length+')')
  })
  $('#action').click(function(){
    //deleting objects
     if($('#bulk-table-action').val()=='delete')
      window.location.assign($('#bulk-table-action').attr('data-delete')+'?elements='+selected.join(','))

      //changing products categories
      if($('#bulk-table-action').val()=='cat')
      {
        $('#changeCatModal').modal('show')
        $('input[name=elementsBulk]').val(selected.join(','))
      }
      //changing commande status
      if($('#bulk-table-action').val()=='etat')
      {
        $('#changeEtatModal').modal('show')
        $('input[name=elementsBulk]').val(selected.join(','))
      }

  })

  $('.changer-categorie-bulk').click(function(){
      $('#changeCatModal form').submit()
  })

})
