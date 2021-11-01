function DatosTop2(){
    var tabla = document.querySelector('#contenidotop2')
    var cadena =''

    fetch('http://localhost:3000/Publicaciones/Usuarios', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(res => res.json())
      .catch(err => {
        console.error('Error:', err)
        //alert("Ocurrio un error, ver la consola")
      })
      .then(response => {
        console.log(response);
        response.forEach(element => {
          console.log(element)
          if(element.username !="admin"){
            cadena += `<tr>
            <td> ${element.posicion} </td>
            <td> ${element.username} </td>
            <td> ${element.cantidad} </td>
            </tr>`
          }          
        });
        tabla.innerHTML = cadena
      })
  }
  DatosTop2();