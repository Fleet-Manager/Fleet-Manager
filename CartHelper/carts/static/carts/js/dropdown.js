$(function(){
  // document.onload(function(){
  //   if($("#fleet_dropdown").text() != "Select Fleet") {
  //     console.log($("#fleet_dropdown").text())
  //   }
  // })

  $(".dropdown-item").click(function(){
     if($("#fleet_dropdown").text() != $(this).text()) {
       var new_selected_fleet = $.trim($(this).text())
       console.log(new_selected_fleet)
       $.get("/", { selected_fleet: new_selected_fleet })
     }
     $("#fleet_dropdown").text(new_selected_fleet);
  })
})
