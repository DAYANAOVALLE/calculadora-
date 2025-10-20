from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Sistema Biblioteca FastAPI")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device‑width, initial‑scale=1.0">
  <title>Biblioteca Personal</title>
  <style>
    body {
        font‑family: Arial, sans‑serif;
        margin: 0;
        padding: 0;
        background‑color: #f4f4f4;
    }
    h1, h2 {
        text‑align: center;
        color: #333;
    }
    .container {
        max‑width: 800px;
        margin: 20px auto;
        padding: 20px;
        background: #fff;
        border‑radius: 8px;
        box‑shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    input, textarea, button, select {
        display: block;
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border‑radius: 4px;
        border: 1px solid #ccc;
        box‑sizing: border‑box;
    }
    button {
        background‑color: #28a745;
        color: white;
        border: none;
        cursor: pointer;
        transition: background‑color 0.3s;
    }
    button:hover {
        background‑color: #218838;
    }
    #panelUsuario, #detalleLibro, #registro {
        display: none;
        margin‑top: 20px;
    }
    #catalogoGlobal div, #miBiblioteca div {
        padding: 10px;
        margin: 5px 0;
        background‑color: #e9ecef;
        border: 1px solid #ccc;
        border‑radius: 4px;
    }
    #catalogoGlobal div:hover, #miBiblioteca div:hover {
        background‑color: #dee2e6;
    }
    .detalle {
        background‑color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 15px;
        margin‑top: 10px;
        border‑radius: 4px;
    }
    /* botones dentro de los listados */
    #catalogoGlobal button, #miBiblioteca button {
        display: inline‑block;
        width: auto;
        padding: 5px 10px;
        margin‑left: 10px;
        border‑radius: 4px;
        font‑size: 14px;
    }
  </style>
</head>
<body>
  <div id="login">
    <h2>Ingresar usuario</h2>
    <input type="text" id="usuario" placeholder="Nombre de usuario">
    <input type="password" id="clave" placeholder="Contraseña">
    <button onclick="login()">Ingresar</button>
    <button onclick="mostrarRegistro()">Registrar usuario</button>
  </div>

  <div id="registro">
    <h2>Registrar Usuario</h2>
    <input type="text" id="nuevoNombre" placeholder="Nombre">
    <input type="password" id="nuevaClave" placeholder="Contraseña">
    <button onclick="agregarUsuario()">Registrar</button>
  </div>

  <div id="panelUsuario">
    <h2>Biblioteca Global</h2>
    <div id="catalogoGlobal"></div>

    <h2>Mi Biblioteca</h2>
    <div id="miBiblioteca"></div>

    <h2>Agregar Libro</h2>
    <input type="text" id="titulo" placeholder="Título del libro">
    <input type="text" id="autor" placeholder="Autor">
    <input type="text" id="categoria" placeholder="Categoría">
    <button onclick="agregarLibroGlobal()">Agregar Libro</button>
  </div>

  <div id="detalleLibro">
    <h3 id="tituloDetalle"></h3>
    <p id="autorDetalle"></p>
    <p id="categoriaDetalle"></p>

    <textarea id="reseñaTexto" placeholder="Escribe tu reseña..."></textarea>
    <input type="number" id="calificacion" min="1" max="5" placeholder="Calificación (1 a 5)">
    <button onclick="guardarReseña()">Guardar Reseña</button>

    <h4>Reseñas:</h4>
    <ul id="listaReseñas"></ul>
  </div>

  <button id="cerrarSecion" style="display:none;" onclick="logout()">Cerrar sesión</button>

  <script>
    let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
    let usuarioActual = null;
    let librosGlobal = JSON.parse(localStorage.getItem("librosGlobal")) || [];
    let reseñas = JSON.parse(localStorage.getItem("reseñas")) || {};
    let libroSeleccionado = null;

    function guardarDatos() {
      localStorage.setItem("usuarios", JSON.stringify(usuarios));
      localStorage.setItem("librosGlobal", JSON.stringify(librosGlobal));
      localStorage.setItem("reseñas", JSON.stringify(reseñas));
    }

    function login() {
      const nombre = document.getElementById("usuario").value;
      const clave = document.getElementById("clave").value;
      const user = usuarios.find(u => u.nombre === nombre && u.clave === clave);
      if (!user) {
        alert("Usuario o clave incorrecta");
        return;
      }
      usuarioActual = user;
      document.getElementById("login").style.display = "none";
      document.getElementById("registro").style.display = "none";
      document.getElementById("panelUsuario").style.display = "block";
      document.getElementById("cerrarSecion").style.display = "block";
      mostrarCatalogoGlobal();
      mostrarMiBiblioteca();
    }

    function mostrarRegistro() {
      document.getElementById("registro").style.display = "block";
      document.getElementById("login").style.display = "none";
    }

    function agregarUsuario() {
      const nombre = document.getElementById("nuevoNombre").value;
      const clave = document.getElementById("nuevaClave").value;
      if (!nombre || !clave) {
        alert("Completa todos los campos");
        return;
      }
      if (usuarios.some(u => u.nombre === nombre)) {
        alert("Nombre ya existe");
        return;
      }
      usuarios.push({ nombre, clave, biblioteca: [] });
      guardarDatos();
      alert("Registrado exitosamente");
      document.getElementById("registro").style.display = "none";
      document.getElementById("login").style.display = "block";
    }

    function logout() {
      usuarioActual = null;
      document.getElementById("login").style.display = "block";
      document.getElementById("registro").style.display = "none";
      document.getElementById("panelUsuario").style.display = "none";
      document.getElementById("cerrarSecion").style.display = "none";
      document.getElementById("detalleLibro").style.display = "none";
      document.getElementById("usuario").value = "";
      document.getElementById("clave").value = "";
    }

    function agregarLibroGlobal() {
      const titulo = document.getElementById("titulo").value;
      const autor = document.getElementById("autor").value;
      const categoria = document.getElementById("categoria").value;
      if (!titulo || !autor || !categoria) {
        alert("Completa todos los campos");
        return;
      }
      librosGlobal.push({ titulo, autor, categoria });
      guardarDatos();
      mostrarCatalogoGlobal();
    }

    function mostrarCatalogoGlobal() {
      const cont = document.getElementById("catalogoGlobal");
      cont.innerHTML = "";
      librosGlobal.forEach((libro, i) => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${libro.titulo}</strong> - ${libro.autor} (${libro.categoria})
          <button onclick="agregarAMiBiblioteca(${i})">Agregar a mi biblioteca</button>
          <button onclick="verDetalle(${i})">Ver detalle</button>`;
        cont.appendChild(div);
      });
    }

    function agregarAMiBiblioteca(index) {
      const libro = librosGlobal[index];
      if (!usuarioActual.biblioteca.some(l => l.titulo === libro.titulo && l.autor === libro.autor)) {
        usuarioActual.biblioteca.push(libro);
        guardarDatos();
        mostrarMiBiblioteca();
      } else {
        alert("Este libro ya está en tu biblioteca");
      }
    }

    function mostrarMiBiblioteca() {
      const cont = document.getElementById("miBiblioteca");
      cont.innerHTML = "";
      usuarioActual.biblioteca.forEach((libro, i) => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${libro.titulo}</strong> - ${libro.autor}
          <button onclick="verDetalleDesdeMiBiblioteca(${i})">Ver detalle</button>
          <button onclick="eliminarDeMiBiblioteca(${i})">Eliminar</button>`;
        cont.appendChild(div);
      });
    }

    function eliminarDeMiBiblioteca(index) {
      usuarioActual.biblioteca.splice(index, 1);
      guardarDatos();
      mostrarMiBiblioteca();
    }

    function verDetalle(index) {
      const libro = librosGlobal[index];
      mostrarDetalle(libro);
    }

    function verDetalleDesdeMiBiblioteca(index) {
      const libro = usuarioActual.biblioteca[index];
      mostrarDetalle(libro);
    }

    function mostrarDetalle(libro) {
      libroSeleccionado = libro;
      document.getElementById("tituloDetalle").textContent = libro.titulo;
      document.getElementById("autorDetalle").textContent = "Autor: " + libro.autor;
      document.getElementById("categoriaDetalle").textContent = "Categoría: " + libro.categoria;
      document.getElementById("detalleLibro").style.display = "block";
      mostrarReseñas();
    }

    function mostrarReseñas() {
      const list = document.getElementById("listaReseñas");
      list.innerHTML = "";
      const key = libroSeleccionado.titulo;
      const reseñasLibro = reseñas[key] || [];
      reseñasLibro.forEach(r => {
        const li = document.createElement("li");
        li.textContent = `${r.usuario}: "${r.texto}" (Calificación: ${r.cal})`;
        list.appendChild(li);
      });
    }

    function guardarReseña() {
      const texto = document.getElementById("reseñaTexto").value;
      const cal = parseInt(document.getElementById("calificacion").value);
      if (!texto || isNaN(cal) || cal < 1 || cal > 5) {
        alert("Completa todos los campos correctamente (texto y calificación de 1 a 5)");
        return;
      }
      const key = libroSeleccionado.titulo;
      if (!reseñas[key]) reseñas[key] = [];
      reseñas[key].push({ usuario: usuarioActual.nombre, texto, cal });
      guardarDatos();
      document.getElementById("reseñaTexto").value = "";
      document.getElementById("calificacion").value = "";
      mostrarReseñas();
      alert("Reseña guardada ✅");
    }

  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(HTML_PAGE)

if __name__ == "__main__":
    import uvicorn, os
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)
