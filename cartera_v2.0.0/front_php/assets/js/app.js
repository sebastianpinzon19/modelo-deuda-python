const API_URL = "http://localhost:8000"; // backend FastAPI

// ================= TRM =================
async function cargarTrm() {
    try {
        let res = await fetch(`${API_URL}/trm`);
        let data = await res.json();
        document.getElementById("trm-display").innerText =
            `TRM: USD ${data.usd} | EUR ${data.eur}`;
    } catch (e) {
        document.getElementById("trm-display").innerText = "TRM no disponible";
    }
}

function abrirTrmModal() {
    document.getElementById("trm-modal").style.display = "flex";
}

function cerrarTrmModal() {
    document.getElementById("trm-modal").style.display = "none";
}

async function guardarTrm() {
    let usd = document.getElementById("trm-usd").value;
    let eur = document.getElementById("trm-eur").value;

    await fetch(`${API_URL}/trm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usd, eur })
    });

    cerrarTrmModal();
    cargarTrm();
}

// ================= Formularios =================
function mostrarFormulario() {
    let proceso = document.getElementById("proceso-select").value;
    let cont = document.getElementById("formularios");
    cont.innerHTML = "";

    if (proceso === "modelo_deuda") {
        cont.innerHTML = `
            <h3>Modelo de Deuda</h3>
            <p>Suba Cartera y Anticipos</p>
            <input type="file" id="file-cartera"><br><br>
            <input type="file" id="file-anticipos"><br><br>
            <button class="btn" onclick="ejecutarProceso('modelo_deuda')">Ejecutar</button>
        `;
    }

    if (proceso === "anticipos") {
        cont.innerHTML = `
            <h3>Procesar Anticipos</h3>
            <input type="file" id="file-anticipos"><br><br>
            <button class="btn" onclick="ejecutarProceso('anticipos')">Ejecutar</button>
        `;
    }

    if (proceso === "cartera") {
        cont.innerHTML = `
            <h3>Procesar Cartera</h3>
            <input type="file" id="file-cartera"><br><br>
            <label>Fecha de cierre:</label>
            <input type="date" id="fecha-cierre"><br><br>
            <button class="btn" onclick="ejecutarProceso('cartera')">Ejecutar</button>
        `;
    }

    if (proceso === "unificado") {
        cont.innerHTML = `
            <h3>Procesador Unificado</h3>
            <p>Suba carpeta comprimida con Balance, Situación, Focus, Dotación, Acumulado</p>
            <input type="file" id="file-unificado"><br><br>
            <button class="btn" onclick="ejecutarProceso('unificado')">Ejecutar</button>
        `;
    }
}

// ================= Ejecución =================
async function ejecutarProceso(tipo) {
    let formData = new FormData();

    if (tipo === "modelo_deuda") {
        formData.append("cartera", document.getElementById("file-cartera").files[0]);
        formData.append("anticipos", document.getElementById("file-anticipos").files[0]);
    }
    if (tipo === "anticipos") {
        formData.append("anticipos", document.getElementById("file-anticipos").files[0]);
    }
    if (tipo === "cartera") {
        formData.append("cartera", document.getElementById("file-cartera").files[0]);
        formData.append("fecha_cierre", document.getElementById("fecha-cierre").value);
    }
    if (tipo === "unificado") {
        formData.append("unificado", document.getElementById("file-unificado").files[0]);
    }

    let res = await fetch(`${API_URL}/procesar/${tipo}`, {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        alert("Error en el procesamiento");
        return;
    }

    let blob = await res.blob();
    let url = window.URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.href = url;
    a.download = `${tipo}_resultado.xlsx`;
    document.body.appendChild(a);
    a.click();
    a.remove();
}

// Inicializar
cargarTrm();
