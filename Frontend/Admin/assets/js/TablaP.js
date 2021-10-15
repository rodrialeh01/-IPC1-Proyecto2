function DatosP(){
    var tabla = document.querySelector('#contenidopublicaciones')
    var cadena =''

    fetch('http://localhost:3000/Publicaciones/Tabla', {
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
        cadena += `<tr width="100%">
            <td> ${element.no} </td>
            <td> ${element.tipo} </td>
            <td> ${element.username} </td>
            <td> ${element.date} </td>
            <td> ${element.category} </td>
            <td class="text-primary"> ${element.url} </td>
            <td> <button value=${element.url} type="button" class="btn btn-info btn-sm"><i class="material-icons">visibility</i></button> <button value=${element.url} type="button" class="btn btn-success btn-sm"><i class="material-icons">edit</i></button> <button value=${element.url} type="button" class="btn btn-danger btn-sm"><i class="material-icons">delete</i></button> </td>
            </tr>`        
        });
        tabla.innerHTML = cadena
      })
  }
  DatosP();