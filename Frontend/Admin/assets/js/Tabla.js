function DatosU(){
    var tabla = document.querySelector('#contenidousers')
    var cadena =''

    fetch('http://localhost:3000/Usuarios/Tabla', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(res => res.json())
      .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
      })
      .then(response => {
        console.log(response);
        response.forEach(element => {
          console.log(element)
          if(element.username !="admin"){
            cadena += `<tr>
            <td> ${element.no} </td>
            <td> ${element.name} </td>
            <td> ${element.username} </td>
            <td> ${element.email} </td>
            <td> ${element.gender} </td>
            <td> ${element.password} </td>
            <td> <button value=${element.username} type="button" class="btn btn-info btn-sm"><i class="material-icons">visibility</i></button> <button value=${element.username} type="button" class="btn btn-success btn-sm"><i class="material-icons">edit</i></button> <button value=${element.username} type="button" class="btn btn-danger btn-sm"><i class="material-icons">delete</i></button> </td>
            </tr>`
          }          
        });
        tabla.innerHTML = cadena
      })
  }
  DatosU();