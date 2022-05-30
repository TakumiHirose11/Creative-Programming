function ClickConnect(){
    console.log("60sごとに再接続");
    document.querySelector("colab-connect-button").click()
  }
  setInterval(ClickConnect,1000*60);