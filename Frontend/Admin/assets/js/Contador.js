function ContadorU(){
    fetch('http://localhost:3000/Usuarios/Contador', {
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
        document.getElementById('cusers').innerHTML = response.Cantidad;
      })
  }
  function ContadorP(){
    fetch('http://localhost:3000/Publicaciones/Contador', {
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
        document.getElementById('cpublis').innerHTML = response.Cantidad;
      })
  }
  ContadorU();
  ContadorP();