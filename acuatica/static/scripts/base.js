function onclickhandler(e) {  
  var total = document.getElementById("sale_total").textContent
  var coins = parseInt(e.value) - parseInt(total)
  console.log(coins);
  document.getElementById("coins").textContent = "$" + coins;
}

