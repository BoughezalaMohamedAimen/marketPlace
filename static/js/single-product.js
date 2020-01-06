$(document).ready(function(){
$('.zoom').css('background','url('+$('.image-selected').attr('src')+')');
$('.zoom').hide();
$('.zoom').css({
      'background-size':'200% 200%',
      'background-repeat':'no-repeat'
})


$('.image-select').click(function(){
var image=$('.image-selected').attr('src');
$('.image-selected').attr('src',$(this).attr('src'));
$(this).attr('src',image);
$('.zoom').css('background','url('+$('.image-selected').attr('src')+')');
$('.zoom').css({
      'background-size':'200% 200%',
      'background-repeat':'no-repeat'
});
});



$('.image-selected').hover(function(){
  $('.zoom').fadeIn('fast');
},function(){
    $('.zoom').fadeOut('fast');
})




$(".image-selected").mousemove(function(e) {

  var offset = $(this).offset();
  var relativeX = (e.pageX - offset.left);
  var relativeY = (e.pageY - offset.top);

$('.zoom').css({
  'background-position': '-'+relativeX+'px -'+relativeY+'px '

})

});
});
