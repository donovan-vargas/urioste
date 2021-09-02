function onclickhandler(e) {  
  var total = document.getElementById("sale_total").textContent
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