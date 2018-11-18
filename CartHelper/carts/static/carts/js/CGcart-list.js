+ function($) {

  var source = document.getElementById("cart-list-entry").innerHTML;
  var cartListTemp = Handlebars.compile(source);
  source = document.getElementById('data-list-entry').innerHTML;
  var dataListTemp = Handlebars.compile(source);
  source = document.getElementById('fault-list-entry').innerHTML;
  var faultListTemp = Handlebars.compile(source);
  source = document.getElementById('fault-header').innerHTML;
  var faultHeaderTemp = Handlebars.compile(source);
  source = document.getElementById('select-option').innerHTML;
  var selectOptTemp = Handlebars.compile(source);

  var fleetOption = document.getElementById('Yamaha 2015');
  var cartList = document.getElementById('cart_list');
  var dataList = document.getElementById('data_list')
  var cartListobj
  var cartDataobj
  var faultArrayobj = []
  var fleetcarts
  var allCartsListed = true
  var selectedCarts = []

  fleetOption.addEventListener("click", function(e){
    console.log("test 1")
    cartlist = document.getElementById('fleet_carts_list').dataset.value
    cartdata = document.getElementById('data_collection_list').dataset.value
    updateList(cartlist, cartdata)
  })

  window.onload = function(){
    if($("#fleet_dropdown").text() != "Select Fleet") {
      cartlist = document.getElementById('fleet_carts_list').dataset.value
      cartdata = document.getElementById('data_collection_list').dataset.value
      updateList(cartlist, cartdata)
    }
  };

  cartList.addEventListener('click', function(e){
    //console.log(e.target)
    //console.log("a.list-group-item list-group-item-action")
    if(e.target && e.target.matches("li.list-group-item.list-group-item-action") && !e.target.matches("li.list-group-item-success.list-group-item.list-group-item-action")){
      e.target.className = "list-group-item list-group-item-action list-group-item-success"
      allCartsListed = false
      selectedCarts.push(e.target.dataset.cartnumber)
      //console.log(selectedCarts)
      updateDataList()
    }
    else if(e.target && e.target.matches("li.list-group-item.list-group-item-action.list-group-item-success")){
      e.target.className = "list-group-item list-group-item-action"
      index = selectedCarts.indexOf(e.target.dataset.cartnumber)
      if(index > -1){
        selectedCarts.splice(index, 1)
      }
      if(selectedCarts.length == 0){
        allCartsListed = true
        document.getElementById('data_table').removeChild(document.getElementById('data_table').lastChild)
      }
      updateDataList()
    }
  })

  function updateDataList() {
    if (allCartsListed == false){
      document.getElementById('data_list').innerHTML = ""
      loop1:
      for( var i in selectedCarts){
        loop2:
        for( var x in cartListobj){
          if( cartListobj[x].fields.number == selectedCarts[i]){
            for( var y in cartDataobj){
              if( cartListobj[x].pk == cartDataobj[y].fields.cart){
                context = {
                  cartNumber: selectedCarts[i],
                  ampHours: cartDataobj[y].fields.amp_hours,
                  miles: cartDataobj[y].fields.mileage,
                  hours: cartDataobj[y].fields.hours
                }
                document.getElementById('data_list').insertAdjacentHTML('beforeend', dataListTemp(context))
                if( selectedCarts.length == 1){
                  document.getElementById('data_table').insertAdjacentHTML('beforeend', faultHeaderTemp())
                  for(z=0; z<72; z++){
                    if( faultArrayobj[z][0].fields.cart == cartListobj[x].pk) {
                      for(var g in faultArrayobj[z]){
                        if( faultArrayobj[z][g].fields.hour != 0 && (faultArrayobj[z][g].fields.code != faultArrayobj[z][g - 1].fields.code || faultArrayobj[z][g].fields.hour != faultArrayobj[z][g - 1].fields.hour)){
                          context = { faultCode: faultArrayobj[z][g].fields.code,
                                      faultHour: faultArrayobj[z][g].fields.hour,
                                      faultDesc: getFaultDesc(faultArrayobj[z][g].fields.code)}
                          document.getElementById('fault_list').insertAdjacentHTML('beforeend', faultListTemp(context))
                        }
                      }
                      break loop1;
                    }
                  }
                }
                break loop2;
              }
            }
          }
        }
      }
      if( selectedCarts.length == 2){
        document.getElementById('data_table').removeChild(document.getElementById('data_table').lastChild)
      }

    }
    else {
      document.getElementById('data_list').innerHTML = ""
      document.getElementById('cart_list').innerHTML = ""
      cartlist = document.getElementById('fleet_carts_list').dataset.value
      cartdata = document.getElementById('data_collection_list').dataset.value
      updateList(cartlist, cartdata)
    }
  }

  var updateList = function(cartList, cartData) {
    //cartList.empty();
    //dataList.empty();
    cartListobj = JSON.parse(cartList)
    cartDataobj = JSON.parse(cartData)
    var x = 1
    for( var cart in cartListobj) {
      faultArrayobj.push(JSON.parse(eval("document.getElementById('fleet_fault_list_" + x.toString() + "').dataset.value")));
      x++;
    }
    console.log("beginning update process" + cartDataobj.length)
    for (i = 0; i < cartDataobj.length; i++) {
      context = {cartNumber: cartListobj[i].fields.number}
      console.log(context)
      document.getElementById('cart_list').insertAdjacentHTML('beforeend', cartListTemp(context))
    }
    var cartnumber;
    for (i = 0; i < cartDataobj.length; i++) {
      for(x = 0; x < cartListobj.length; x++) {
        if(cartListobj[x].pk == cartDataobj[i].fields.cart) {
          cartnumber = cartListobj[x].fields.number
        }
      }
      context = {cartNumber: cartnumber,
                 ampHours: cartDataobj[i].fields.amp_hours,
                 miles: cartDataobj[i].fields.mileage,
                 hours: cartDataobj[i].fields.hours}
      document.getElementById('data_list').insertAdjacentHTML('beforeend', dataListTemp(context))
    }
  }
  var getFaultDesc = function(faultCode) {
    switch(faultCode){
      case 8: return "Field amplifier not calibrated correctly high reverse field"
      case 22:
      case 20: return "Re-start with tow switch"
      case 21: return "Charging required."
      case 23:
      case 24:
      case 25: return "Cool down MCU."
      case 26: return "Check motor wiring."
      case 27: return "Warm up MCU."
      case 28:
      case 29:
      case 30:
      case 31:
      case 32:
      case 33: return "Try to replace MCU."
      case 34:
      case 35: return "Check TPS or TPS circuit."
      case 36: return "Check TPS or shift switch"
      case 37: return "Check shift switch and wiring."
      case 38:
      case 39: return "Check main relay."
      case 40:
      case 41: return "Charging required."
      case 42: return "Too much regenerative current. Re-start with tow switch."
      case 43: return "Cool down the vehicle."
      case 44:
      case 45:
      case 46: return "Check speed sensor and wiring."
      case 47: return "Showing speed status."
      case 48: return "Showing overvoltage status."
      case 49: return "Showing charging status."
      case 50:
      case 51:
      case 52:
      case 53: return "Showing temperature status."
      case 54:
      case 55:
      case 56: return "Showing derating status."
      case 58: return "Showing speed status."
      case 59: return "Charging status."
      default: "Invalid Fault Code!"

    }
  }
}(jQuery);
