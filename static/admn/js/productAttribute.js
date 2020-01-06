  let attributes=[];
$(document).ready(function(){
  // alert(window.location)
  //attribute class
  function attribut (nom){
              this.nom=nom;
              this.get_selected_values = function () {
                var selected=[];
                $('.selected[data-attribute-name='+this.nom+']').each(function(){
                  selected.push($(this).attr('data-value-id')+','+$(this).html())
                })

                    return selected;
                  }
  }





//when selecting attribute
  $('.attribute-value').click(function(){
      $(this).toggleClass('selected');
       attributes=[];
       $('.selected').each(function(){
         if(!attribute_is_created_in_attributes_array($(this).attr('data-attribute-name')))
          attributes.push(new attribut($(this).attr('data-attribute-name')))
       })
       console.log(attributes)
  })

console.log(attributes)

$('.generate').click(function(){

    // cartesian(attributes[0].get_selected_values(),attributes[1].get_selected_values(),attributes[2].get_selected_values())
    var allArrays =[];
    for(var i=0;i<attributes.length;i++)
      allArrays.push(attributes[i].get_selected_values())
      $('.result').html('')
      var allcombinations=allPossibleCases(allArrays)
      console.log(allcombinations)
     // console.log(cartesian(attributes[0].get_selected_values(),attributes[1].get_selected_values(),attributes[2].get_selected_values()));
    for(var i=0;i<allcombinations.length;i++)
    $('.result').html($('.result').html()+build_product_attribute_form(allcombinations[i],i))
      $('.result').html($('.result').html()+'<input type="hidden" name="lentgh" value="'+allcombinations.length+'">')
})






function build_product_attribute_form(product_with_attribute,index){
  var title=''
  var attributes_ids=''
  for(i=0;i<product_with_attribute.split(':').length;i++)
  {
    title+=product_with_attribute.split(':')[i].split(',')[1]+'-'
    attributes_ids+=product_with_attribute.split(':')[i].split(',')[0]+','
  }
  var attributes_values=attributes_ids.substring(0, attributes_ids.length - 1).split(',')
  console.log('*******************')
  console.log(attributes_ids.substring(0, attributes_ids.length - 1))
  var  html = '<div class="col-md-6  attribute">'
    html +='<div class="container text-center border shadow py-3 mb-2">'
      html +='<b class="text-dark">'+title.substring(0, title.length - 1)+'</b>'
      html +='<div class="row">'
        html +='<div class="col-md-6">'
          html +='<label>Prix</label>'
          html +='<input type="text" class="form-control text-center" name="form-'+index+'-prix">'
        html +='</div>'
        html +='<div class="col-md-6">'
          html +='<label>Stock</label>'
          html +='<input type="text" class="form-control text-center" name="form-'+index+'-stock">'
          html +='<select name="form-'+index+'-attributevalues" multiple class="d-none">'
          for(var j=0;j<attributes_values.length;j++)
            html +='<option value="'+attributes_values[j]+'" selected>'+attributes_values[j]+'</option>'
          html +='</select>'
          html +='<input type="hidden" value="'+$('.productid').html()+'" name="form-'+index+'-produit">'
        html +='</div>'
      html +='</div>'
    html +='</div>'
  html +='</div>';
  return html;
}


// $('.submit').click(function(){
//   // var formData = JSON.stringify($("#productattributes").serializeArray());
//   console.log(formData)
//   $.ajax({
//     type: "POST",
//     url: window.location,
//     data: formData,
//     success: function(response){
//       alert(response)
//     },
//     dataType: "json",
//     contentType : "application/json"
// });
// })





function attribute_is_created_in_attributes_array(attribute_name){
  for(var i=0;i<attributes.length;i++)
    if(attributes[i].nom==attribute_name)
      return true;
  return false;

}





function allPossibleCases(arr) {
  if (arr.length == 1) {
    return arr[0];
  } else {
    var result = [];
    var allCasesOfRest = allPossibleCases(arr.slice(1));  // recur with the rest of array
    for (var i = 0; i < allCasesOfRest.length; i++) {
      for (var j = 0; j < arr[0].length; j++) {
        result.push(arr[0][j] +":"+ allCasesOfRest[i]);
      }
    }
    return result;
  }

}
})
