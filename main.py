from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Sistema Biblioteca FastAPI")

INVENTARIO_LIBROS = [
    {"titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez", "categoria": "Novela"},
    {"titulo": "El libro troll", "autor": "el rubius", "categoria": "historico"},
    {"titulo": "1984", "autor": "George Orwell", "categoria": "Distopía"},
    {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "categoria": "Clásico"},
    {"titulo": "La Odisea", "autor": "Homero", "categoria": "Épica"},
]

HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Biblioteca Personal</title>
  <style>
    /* Fondo estilo papel antiguo */
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #f5f1e9;
      background-image:
        radial-gradient(circle at 50% 50%, #f7f3eb 5%, transparent 25%),
        radial-gradient(circle at 25% 25%, #f1e8dc 5%, transparent 20%);
      background-repeat: repeat;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      min-height: 100vh;
      align-items: flex-start;
      padding-top: 30px;
    }}

    .container {{
      background: #fffdfa;
      max-width: 700px;
      width: 90%;
      padding: 25px 35px;
      border-radius: 12px;
      box-shadow: 0 8px 15px rgba(0,0,0,0.1);
      box-sizing: border-box;
      text-align: center;
    }}

    h1, h2, h3, h4 {{
      color: #3a4d24;
      margin-bottom: 20px;
      font-weight: 700;
      font-family: 'Georgia', serif;
    }}

    input, textarea, select, button {{
      width: 100%;
      padding: 12px 15px;
      margin: 10px 0;
      border-radius: 8px;
      border: 1.8px solid #9caf88;
      font-size: 16px;
      font-family: 'Arial', sans-serif;
      box-sizing: border-box;
      transition: border-color 0.3s ease;
    }}

    input:focus, textarea:focus, select:focus {{
      outline: none;
      border-color: #5a7d30;
      background-color: #f7f9f3;
    }}

    button {{
      background-color: #4caf50;
      color: white;
      border: none;
      cursor: pointer;
      font-weight: 700;
      letter-spacing: 0.05em;
      box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
      transition: background-color 0.3s ease;
      max-width: 250px;
      margin-left: auto;
      margin-right: auto;
      display: block;
    }}

    button:hover {{
      background-color: #388e3c;
    }}

    #panelUsuario, #detalleLibro, #registro {{
      display: none;
      margin-top: 30px;
      text-align: left;
    }}

    #catalogoGlobal div, #miBiblioteca div {{
      padding: 15px;
      margin: 8px 0;
      background-color: #e7ebd1;
      border: 1.6px solid #b6c78a;
      border-radius: 8px;
      font-family: 'Georgia', serif;
      color: #3a4d24;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    #catalogoGlobal div:hover, #miBiblioteca div:hover {{
      background-color: #d4dbb4;
    }}

    .detalle {{
      background-color: #fff8dc;
      border: 1.8px solid #f0e68c;
      padding: 20px;
      margin-top: 20px;
      border-radius: 8px;
      color: #6b5e00;
      font-family: 'Georgia', serif;
    }}

    /* Botones en los listados */
    #catalogoGlobal button, #miBiblioteca button {{
      width: auto;
      padding: 7px 12px;
      margin-left: 10px;
      border-radius: 6px;
      font-size: 14px;
      background-color: #6aaa4f;
      box-shadow: 0 3px 6px rgba(106, 170, 79, 0.4);
    }}

    #catalogoGlobal button:hover, #miBiblioteca button:hover {{
      background-color: #488235;
    }}

    /* Botón cerrar sesión */
    #cerrarSecion {{
      margin-top: 20px;
      max-width: 150px;
      background-color: #a44c4c;
      box-shadow: 0 4px 8px rgba(164, 76, 76, 0.4);
    }}

    #cerrarSecion:hover {{
      background-color: #7a3939;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Biblioteca Personal</h1>

    <div id="login">
      <h2>Ingresar usuario</h2>
      <input type="text" id="usuario" placeholder="Nombre de usuario" autocomplete="username" />
      <input type="password" id="clave" placeholder="Contraseña" autocomplete="current-password" />
      <button onclick="login()">Ingresar</button>
      <button onclick="mostrarRegistro()">Registrar usuario</button>
    </div>

    <div id="registro">
      <h2>Registrar Usuario</h2>
      <input type="text" id="nuevoNombre" placeholder="Nombre" />
      <input type="password" id="nuevaClave" placeholder="Contraseña" />
      <button onclick="agregarUsuario()">Registrar</button>
      <button onclick="volverLogin()">Volver</button>
    </div>

    <div id="panelUsuario">
      <h2>Biblioteca Global</h2>
      <div id="catalogoGlobal"></div>

      <h2>Mi Biblioteca</h2>
      <div id="miBiblioteca"></div>

      <h2>Agregar Libro Nuevo</h2>
      <input type="text" id="titulo" placeholder="Título del libro" />
      <input type="text" id="autor" placeholder="Autor" />
      <input type="text" id="categoria" placeholder="Categoría" />
      <button onclick="agregarLibroGlobal()">Agregar Libro</button>
    </div>

    <div id="detalleLibro">
      <h3 id="tituloDetalle"></h3>
      <p id="autorDetalle"></p>
      <p id="categoriaDetalle"></p>

      <textarea id="reseñaTexto" placeholder="Escribe tu reseña..."></textarea>
      <input type="number" id="calificacion" min="1" max="5" placeholder="Calificación (1 a 5)" />
      <button onclick="guardarReseña()">Guardar Reseña</button>

      <h4>Reseñas:</h4>
      <ul id="listaReseñas"></ul>
    </div>

    <button id="cerrarSecion" style="display:none;" onclick="logout()">Cerrar sesión</button>
  </div>

  <script>
    // Inventario inicial, solo si no existe ya en localStorage
    if (!localStorage.getItem("librosGlobal")) {{
      localStorage.setItem("librosGlobal", JSON.stringify({INVENTARIO_LIBROS}));
    }}

    let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
    let usuarioActual = null;
    let librosGlobal = JSON.parse(localStorage.getItem("librosGlobal")) || [];
    let reseñas = JSON.parse(localStorage.getItem("reseñas")) || {{}};
    let libroSeleccionado = null;

    function guardarDatos() {{
      localStorage.setItem("usuarios", JSON.stringify(usuarios));
      localStorage.setItem("librosGlobal", JSON.stringify(librosGlobal));
      localStorage.setItem("reseñas", JSON.stringify(reseñas));
    }}

    function login() {{
      const nombre = document.getElementById("usuario").value.trim();
      const clave = document.getElementById("clave").value;
      const user = usuarios.find(u => u.nombre === nombre && u.clave === clave);
      if (!user) {{
        alert("Usuario o clave incorrecta");
        return;
      }}
      usuarioActual = user;
      document.getElementById("login").style.display = "none";
      document.getElementById("registro").style.display = "none";
      document.getElementById("panelUsuario").style.display = "block";
      document.getElementById("cerrarSecion").style.display = "block";
      mostrarCatalogoGlobal();
      mostrarMiBiblioteca();
    }}

    function mostrarRegistro() {{
      document.getElementById("registro").style.display = "block";
      document.getElementById("login").style.display = "none";
    }}

    function volverLogin() {{
      document.getElementById("registro").style.display = "none";
      document.getElementById("login").style.display = "block";
    }}

    function agregarUsuario() {{
      const nombre = document.getElementById("nuevoNombre").value.trim();
      const clave = document.getElementById("nuevaClave").value;
      if (!nombre || !clave) {{
        alert("Completa todos los campos");
        return;
      }}
      if (usuarios.some(u => u.nombre === nombre)) {{
        alert("Nombre ya existe");
        return;
      }}
      usuarios.push({{ nombre, clave, biblioteca: [] }});
      guardarDatos();
      alert("Registrado exitosamente");
      document.getElementById("registro").style.display = "none";
      document.getElementById("login").style.display = "block";
    }}

    function logout() {{
      usuarioActual = null;
      document.getElementById("login").style.display = "block";
      document.getElementById("registro").style.display = "none";
      document.getElementById("panelUsuario").style.display = "none";
      document.getElementById("cerrarSecion").style.display = "none";
      document.getElementById("detalleLibro").style.display = "none";
      document.getElementById("usuario").value = "";
      document.getElementById("clave").value = "";
    }}

    function agregarLibroGlobal() {{
      const titulo = document.getElementById("titulo").value.trim();
      const autor = document.getElementById("autor").value.trim();
      const categoria = document.getElementById("categoria").value.trim();
      if (!titulo || !autor || !categoria) {{
        alert("Completa todos los campos");
        return;
      }}
      librosGlobal.push({{ titulo, autor, categoria }});
      guardarDatos();
      mostrarCatalogoGlobal();
      // Limpiar inputs
      document.getElementById("titulo").value = "";
      document.getElementById("autor").value = "";
      document.getElementById("categoria").value = "";
    }}

    function mostrarCatalogoGlobal() {{
      const cont = document.getElementById("catalogoGlobal");
      cont.innerHTML = "";
      librosGlobal.forEach((libro, i) => {{
        const div = document.createElement("div");
        div.innerHTML = `<strong>${{libro.titulo}}</strong> - ${{libro.autor}} (${{libro.categoria}})
          <div>
            <button onclick="agregarAMiBiblioteca(${{i}})">Agregar a mi biblioteca</button>
            <button onclick="verDetalle(${{i}})">Ver detalle</button>
          </div>`;
        cont.appendChild(div);
      }});
    }}

    function agregarAMiBiblioteca(index) {{
      const libro = librosGlobal[index];
      if (!usuarioActual.biblioteca.some(l => l.titulo === libro.titulo && l.autor === libro.autor)) {{
        usuarioActual.biblioteca.push(libro);
        guardarDatos();
        mostrarMiBiblioteca();
      }} else {{
        alert("Este libro ya está en tu biblioteca");
      }}
    }}

    function mostrarMiBiblioteca() {{
      const cont = document.getElementById("miBiblioteca");
      cont.innerHTML = "";
      usuarioActual.biblioteca.forEach((libro, i) => {{
        const div = document.createElement("div");
        div.innerHTML = `<strong>${{libro.titulo}}</strong> - ${{libro.autor}}
          <div>
            <button onclick="verDetalleDesdeMiBiblioteca(${{i}})">Ver detalle</button>
            <button onclick="eliminarDeMiBiblioteca(${{i}})">Eliminar</button>
          </div>`;
        cont.appendChild(div);
      }});
    }}

    function eliminarDeMiBiblioteca(index) {{
      usuarioActual.biblioteca.splice(index, 1);
      guardarDatos();
      mostrarMiBiblioteca();
    }}

    function verDetalle(index) {{
      const libro = librosGlobal[index];
      mostrarDetalle(libro);
    }}

    function verDetalleDesdeMiBiblioteca(index) {{
      const libro = usuarioActual.biblioteca[index];
      mostrarDetalle(libro);
    }}

    function mostrarDetalle(libro) {{
      libroSeleccionado = libro;
      document.getElementById("tituloDetalle").textContent = libro.titulo;
      document.getElementById("autorDetalle").textContent = "Autor: " + libro.autor;
      document.getElementById("categoriaDetalle").textContent = "Categoría: " + libro.categoria;
      document.getElementById("detalleLibro").style.display = "block";
      mostrarReseñas();
      // Scroll a detalle para mejor UX
      document.getElementById("detalleLibro").scrollIntoView({{behavior: "smooth"}});
    }}

    function mostrarReseñas() {{
      const list = document.getElementById("listaReseñas");
      list.innerHTML = "";
      const key = libroSeleccionado.titulo;
      const reseñasLibro = reseñas[key] || [];
      reseñasLibro.forEach(r => {{
        const li = document.createElement("li");
        li.textContent = `${{r.usuario}}: "${{r.texto}}" (Calificación: ${{r.cal}})`;
        list.appendChild(li);
      }});
    }}

    function guardarReseña() {{
      const texto = document.getElementById("reseñaTexto").value.trim();
      const cal = parseInt(document.getElementById("calificacion").value);
      if (!texto || isNaN(cal) || cal < 1 || cal > 5) {{
        alert("Completa todos los campos correctamente (texto y calificación de 1 a 5)");
        return;
      }}
      const key = libroSeleccionado.titulo;
      if (!reseñas[key]) reseñas[key] = [];
      reseñas[key].push({{ usuario: usuarioActual.nombre, texto, cal }});
      guardarDatos();
      document.getElementById("reseñaTexto").value = "";
      document.getElementById("calificacion").value = "";
      mostrarReseñas();
      alert("Reseña guardada ✅");
    }}
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
