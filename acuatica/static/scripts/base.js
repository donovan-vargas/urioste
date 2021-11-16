function onclickhandler(e) {
  var total = document.getElementById("sale_total").textContent
  var charge = document.getElementById("charge").value
  var discount = document.getElementById("descuento").value
  console.log(charge)
  total = parseInt(total) + parseInt(charge) - parseInt(discount);
  var coins = parseInt(e.value) - parseInt(total)
  console.log(coins);
  document.getElementById("coins").textContent = "$" + coins;
}

function get_photo(){

  updatefotoclient = document.getElementById("id_image_source").value;
  console.log(updatefotoclient);
      //updatefotoclient.style.display = "none"

  document.getElementById("display").src = updatefotoclient;
  texto_oculto = document.getElementById("id_image_source")  
};