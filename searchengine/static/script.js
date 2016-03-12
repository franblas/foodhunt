/*
* JS
*/

var apiUrl = "http://localhost:8001/"

function searchData(query, callback) {
  $.ajax({
    url: apiUrl + "searchfront?q=" + query,
    type: "GET",
    beforeSend: function() {
      $('#main-container').css({'text-align': 'center'})
      $('#main-container').append("<img id='loader' src='ajax-loader.gif'>")
    },
    complete: function() {
      $('#loader').remove()
      $('#main-container').css({'text-align': 'left'})
    },
    success: function(data){
       callback(data)
    }
  });
}

function submitQuery() {
  var q = $("#search-query").val();
  $("#main-container").html("");
  searchData(q, function(data) {
    var products = data.data.data
    var shops = data.data.shops

    for(var i=0; i<shops.length; i++) {
      html = "<div class='shop-container'><h3>" + shops[i].shop + "</h3><ul id='shop-" + shops[i].shop + "'></ul></div>"
      $("#main-container").append(html)
    }

    for(var j=0; j<products.length; j++) {
      var product = products[j]
      html = "<li>"
      html += "<span class='product product-name' title='" + product.name + "'>" + product.name.substring(0, 20) + "</span><br/>"
      //html += "<span class='product product-category'>" + product.category + "</span>"
      html += "<span class='product product-subcategory' title='" + product.subcategory + "'>" + product.subcategory.substring(0, 20) + "</span><br/>"
      html += "<span class='product product-price'>" + product.price + "€</span>"
      html += "<span class='product product-unit'>" + product.unit + "</span>"
      html += "</li>"
      $("#shop-" + product.shop).append(html)
    }

  });
}
