console.log("Javascript OK")


$(document).ready(function(){

var location_input=$('input[id="id_search"]');
location_input.autocomplete({
    source: "/api/get_products/",
    minLength: 2,
    });

//   keeps same width as box
jQuery.ui.autocomplete.prototype._resizeMenu = function () {
    var ul = this.menu.element;
    ul.outerWidth(this.element.outerWidth());
  }

});

