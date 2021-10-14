function cargaMasiva() {
    let archivo = document.getElementById("cargau").files[0];
    console.log(archivo);
  
    const reader = new FileReader();
    reader.addEventListener("load", (event) => {
      console.log(event.target.result);
    });
  
    reader.readAsText(archivo, "UTF-8");
  }