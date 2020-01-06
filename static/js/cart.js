$(document).ready(function (){

  /***************************************************ADD TO  CART AJAX  ************************************************************/

  $('.add-to-cart').click(function(){

      $('.cart-tab-header').click()
        var product=$(this).attr('data-product')
        var product_with_attribute=$(this).prev().val();
        /*******************************************PRODUCT EXIST IN CURRENT CART ******************************************/
        if($('.cart-tab input[data-product='+product+']').length)
        {
          if(product_with_attribute=='')
          {
            qtt=parseInt($('.cart-tab input[data-product='+product+']').val())
            $('.cart-tab input[data-product='+product+']').val(qtt+1).change()
          }
          else
          {
            var exists=false;
            $('.cart-tab input[data-product='+product+']').each(function(){
              if($(this).attr('data-attribute')==product_with_attribute)
              exists=true;
            })
            if(exists==true)
            {
              qtt=parseInt($('.cart-tab input[data-product='+product+'][data-attribute='+product_with_attribute+']').val())
              $('.cart-tab input[data-product='+product+'][data-attribute='+product_with_attribute+']').val(qtt+1).change()

            }
            else {
              $.get({
               url:'/cart/add/'+product,
               data:{'attr':$(this).prev().val()},
               success:function(st){
                   $('.cart-tab .items').append(st)
                   $('.commander').removeClass('d-none')
                           setTimeout(function(){$('.close-tab').click()},1000)
               }
             })
            }

            setTimeout(function(){$('.close-tab').click()},1000)
          }


        } /*******************************************PRODUCT DOES NOT EXIST IN CURRENT CART ******************************************/
        else
        {
          $.get({
           url:'/cart/add/'+product,
           data:{'attr':$(this).prev().val()},
           success:function(st){
               $('.cart-tab .items').append(st)
               $('.commander').removeClass('d-none')
                       setTimeout(function(){$('.close-tab').click()},1000)
           }
         })
        }


  })

/***************************************************REMOVE FROM CART AJAX  ************************************************************/

$('body').on('click','.delete-cart',function(){
  item=$(this).attr('data-product')
  $.get({
    url:'/cart/delete/'+item,
    success:function(st){
        $('.cart-tab .items').html(st)
        $('.commander').addClass('d-none')
    }
  })
})

/******************************************CART TAB ANIMATION **************************************************************/
  $('.cart-tab-header').click(function(){

        $('.cart-tab').css('right','0');
        $(this).css('right','-100%');
  })
  /******************************************CART TOGGLE ANIMATION **************************************************************/

$('.cart-menu').click(function(){
  if($('.cart-tab').css('right')!=0)
      $('.cart-tab-header').click()
  else
      $('.close-tab').click()
})

/******************************************CART TAB CLOSING ANIMATION **************************************************************/

  $('.close-tab').click(function(){
    $('.cart-tab').css('right','-100%')
    $('.cart-tab-header').css('right','0');
  })
/*********************************************************************************************************************/
})
