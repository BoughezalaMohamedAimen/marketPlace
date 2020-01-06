$(document).ready(function(){
  $('body').on('click','.spinner-right', function(){
    var value=($(this).prev().val()=='') ? 0 : parseInt($(this).prev().val())
    $(this).prev().val(value+1).change()
  })
  $('body').on('click','.spinner-left',function(){
    var value=($(this).next().val()=='') ? 1 : parseInt($(this).next().val())
    value=(value<=0) ? 1 : value
    $(this).next().val(value-1).change()
  })
  $('body').on('change','.cart-item-qtt',function(){

    product=$(this).attr('data-product')
    qtt=$(this).val()
    $.get({
      url:'/cart/update/'+product+'/'+qtt,
      data:{'attr':$(this).attr('data-attribute')},
      success:function(st){
      }
    })
})
})
