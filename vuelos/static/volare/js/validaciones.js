
console.log("Script de validaciones cargado correctamente");
//Validación del formulario de aerolíneas (CREATE y UPDATE)

function validarFormularioAerolinea() {
    const nombre = document.getElementById('nombre');
    const codigoIATA = document.getElementById('codigo_iata');
    const pais = document.getElementById('pais');
    const botonEnviar = document.getElementById('btn-enviar');
    
    if (!nombre || !codigoIATA || !pais || !botonEnviar) {
        return; 
    }

    function verificarFormulario() {
        const nombreValido = nombre.value.trim() !== '';
        const codigoValido = codigoIATA.value.trim() !== '' && codigoIATA.value.length >= 2;
        const paisValido = pais.value !== '';
        
        // Validar nombre
        if (!nombreValido) {
            nombre.classList.add('campo-invalido');
            nombre.classList.remove('campo-valido');
        } else {
            nombre.classList.remove('campo-invalido');
            nombre.classList.add('campo-valido');
        }
        
        //validar codigo IATA
        if (!codigoValido) {
            codigoIATA.classList.add('campo-invalido');
            codigoIATA.classList.remove('campo-valido');
        } else {
            codigoIATA.classList.remove('campo-invalido');
            codigoIATA.classList.add('campo-valido');
        }
        
        //validar pais
        if (!paisValido) {
            pais.classList.add('campo-invalido');
            pais.classList.remove('campo-valido');
        } else {
            pais.classList.remove('campo-invalido');
            pais.classList.add('campo-valido');
        }
        
        //habilitar/deshabilitar boton
        if (nombreValido && codigoValido && paisValido) {
            botonEnviar.disabled = false;
            botonEnviar.classList.remove('btn-deshabilitado');
            botonEnviar.classList.add('btn-habilitado');
        } else {
            botonEnviar.disabled = true;
            botonEnviar.classList.add('btn-deshabilitado');
            botonEnviar.classList.remove('btn-habilitado');
        }
    }
    
    //ejecutar validación inicial
    verificarFormulario();
    
    //añadir listeners para validación en tiempo real
    nombre.addEventListener('input', verificarFormulario);
    nombre.addEventListener('blur', verificarFormulario);
    codigoIATA.addEventListener('input', verificarFormulario);
    codigoIATA.addEventListener('blur', verificarFormulario);
    pais.addEventListener('change', verificarFormulario);
    
    //validacion final antes de enviar
    const formulario = document.getElementById('form-aerolinea');
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            if (nombre.value.trim() === '' || codigoIATA.value.trim() === '' || pais.value === '') {
                e.preventDefault();
                alert('Por favor, completa todos los campos obligatorios (Nombre, Código IATA y País).');
                return false;
            }
        });
    }
}

//confirmación antes de eliminar una aerolinea
function confirmarEliminacion() {
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            const nombreAerolinea = this.getAttribute('data-nombre');
            const confirmacion = confirm(
                `¿Estás seguro de que deseas eliminar la aerolínea "${nombreAerolinea}"?\n\n` +
                `Esta acción no se puede deshacer.`
            );
            
            if (!confirmacion) {
                e.preventDefault();
                return false;
            }
        });
    });
}

//efecto visual al pasar el raton sobre las tarjetas
function efectosTarjetas() {
    const tarjetas = document.querySelectorAll('.tarjeta');
    
    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        tarjeta.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}


//validacion del codigo IATA 
function validarCodigoIATA() {
    const codigoIATA = document.getElementById('codigo_iata');
    
    if (!codigoIATA) return;
    
    codigoIATA.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
        //limitar a 3 caracteres
        if (this.value.length > 3) {
            this.value = this.value.substring(0, 3);
        }
        //validar que solo sean letras
        const regex = /^[A-Z]{0,3}$/;
        if (!regex.test(this.value) && this.value !== '') {
            this.classList.add('campo-invalido');
        } else {
            this.classList.remove('campo-invalido');
        }
    });
}
//validacion del año de fundacion
function validarAnioFundacion() {
    const anioFundacion = document.getElementById('anio_fundacion');
    
    if (!anioFundacion) return;
    
    anioFundacion.addEventListener('input', function() {
        const anioActual = new Date().getFullYear();
        const valor = parseInt(this.value);
        
        if (isNaN(valor) || valor < 1900 || valor > anioActual) {
            this.classList.add('campo-invalido');
        } else {
            this.classList.remove('campo-invalido');
        }
    });
}

function mostrarMensajeExito() {
    const urlParams = new URLSearchParams(window.location.search);
    const mensaje = urlParams.get('mensaje');
    
    if (mensaje) {
        const div = document.createElement('div');
        div.className = 'mensaje-exito';
        div.textContent = decodeURIComponent(mensaje);
        div.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(div);
        setTimeout(() => {
            div.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => div.remove(), 300);
        }, 3000);
    }
}

//busqueda de aerolineas con AJAX
//actualiza la lista sin recargar la página
function buscarAerolineasAjax() {
    const inputBusqueda = document.getElementById('busqueda-aerolineas');
    const listaContainer = document.getElementById('lista-aerolineas');
    const resultadoDiv = document.getElementById('resultado-busqueda');
    if (!inputBusqueda || !listaContainer) {
        return; 
    }
    //variable para controlar el timeout del debounce
    let timeoutId = null;
    inputBusqueda.addEventListener('input', function() {
        const query = this.value.trim();
        //cancelar busqueda anterior si existe
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        //esperar 300ms después de que el usuario deje de escribir
        timeoutId = setTimeout(() => {
            realizarBusqueda(query);
        }, 300);
    });
    
    function realizarBusqueda(query) {
        resultadoDiv.innerHTML = '<em>Buscando...</em>';
        const url = `/buscar-aerolineas/?q=${encodeURIComponent(query)}`;
        
        //realizar petición AJAX con fetch
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la búsqueda');
                }
                return response.json();
            })
            .then(data => {
                actualizarLista(data.results);
                
                //mostrar numero de resultados
                if (query) {
                    resultadoDiv.innerHTML = `<strong>${data.results.length}</strong> resultado(s) encontrado(s)`;
                } else {
                    resultadoDiv.innerHTML = '';
                }
            })
            .catch(error => {
                console.error('Error al buscar aerolíneas:', error);
                resultadoDiv.innerHTML = '<span style="color: red;">Error al realizar la búsqueda</span>';
            });
    }
    
    function actualizarLista(resultados) {
        if (resultados.length === 0) {
            listaContainer.innerHTML = '<p>No se encontraron aerolíneas que coincidan con tu búsqueda.</p>';
            return;
        }
        
        //construir el HTML de la lista
        let html = '<ul class="lista">';
        
        resultados.forEach(aerolinea => {
            html += `
                <li>
                    <div class="info-aerolinea-lista">
                        <strong>${aerolinea.nombre}</strong>
                        ${aerolinea.codigo_iata ? `<span>(${aerolinea.codigo_iata})</span>` : ''}
                        — ${aerolinea.pais}
                        ${aerolinea.anio_fundacion ? `— Fundada en ${aerolinea.anio_fundacion}` : ''}
                    </div>
                    
                    <div class="acciones-lista">
                        <a href="/aerolineas/${aerolinea.id}/" class="btn-accion btn-ver">
                            Ver
                        </a>
                        <a href="/aerolineas/${aerolinea.id}/editar/" class="btn-accion btn-editar">
                            Editar
                        </a>
                        <form method="post" action="/aerolineas/${aerolinea.id}/eliminar/" style="display: inline;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
                            <button 
                                type="submit" 
                                class="btn-accion btn-eliminar" 
                                data-nombre="${aerolinea.nombre}">
                                Eliminar
                            </button>
                        </form>
                    </div>
                </li>
            `;
        });
        
        html += '</ul>';
        listaContainer.innerHTML = html;
        
        //reactivar confirmacion de eliminacion en los nuevos botones
        confirmarEliminacion();
    }
    
    //función auxiliar para obtener el token CSRF
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
}

//Inicialización al cargar la pagina
window.addEventListener('DOMContentLoaded', function() {
    console.log('DOM completamente cargado');
    
    //ejecutar todas
    validarFormularioAerolinea();
    confirmarEliminacion();
    efectosTarjetas();
    validarCodigoIATA();
    validarAnioFundacion();
    mostrarMensajeExito();
    buscarAerolineasAjax();
    
    console.log('Todas las validaciones y AJAX inicializadas');
});