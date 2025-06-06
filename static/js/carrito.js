document.addEventListener('DOMContentLoaded', () => {
    let carritoItems = JSON.parse(localStorage.getItem('carrito')) || [];
    const contenedor = document.getElementById('carrito-items');
    const totalPrecio = document.getElementById('total-precio');

    function renderCarrito() {
        contenedor.innerHTML = '';
        let total = 0;

        if (carritoItems.length === 0) {
            contenedor.innerHTML = `<div class="carrito-vacio">Tu carrito está vacío.</div>`;
        } else {
            carritoItems.forEach((item, idx) => {
                const div = document.createElement('div');
                div.classList.add('carrito-item');
                div.innerHTML = `
                    <img src="${item.imagen || 'https://via.placeholder.com/60'}" alt="${item.nombre}" class="carrito-img" />
                    <span>${item.nombre}</span>
                    <span class="carrito-precio">$${item.precio} MXN</span>
                    <button class="btn-eliminar" data-idx="${idx}" title="Eliminar">✕</button>
                `;
                contenedor.appendChild(div);
                total += parseFloat(item.precio);
            });
        }
        totalPrecio.textContent = `$${total.toFixed(2)} MXN`;
    }

    // Delegación de eventos para eliminar productos
    document.getElementById('carrito-items').addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-eliminar')) {
            const idx = parseInt(e.target.getAttribute('data-idx'));
            const nombre = carritoItems[idx].nombre;
            carritoItems.splice(idx, 1);
            localStorage.setItem('carrito', JSON.stringify(carritoItems));
            renderCarrito();
            mostrarToast(`"${nombre}" eliminado del carrito.`);
        }
    });

    renderCarrito();
});

function finalizarCompra() {
    const form = document.getElementById('form-compra');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Obtener datos del formulario
    const datos = {
        nombre: form.nombre ? form.nombre.value : "",
        direccion: form.direccion.value,
        telefono: form.telefono.value,
        pago: form.pago.value
    };

    // Obtener productos del carrito
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    // Enviar datos al backend
    fetch('/finalizar-compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            datos,
            carrito
        })
    })
    .then(response => response.json())
    .then(data => {
        mostrarToast('¡Gracias por tu compra!');
        localStorage.removeItem('carrito');
        setTimeout(() => {
            window.location.href = '/';
        }, 1800);
    })
    .catch(error => {
        mostrarToast('Error al finalizar la compra');
        console.error(error);
    });
}

function mostrarToast(mensaje) {
    const toast = document.getElementById('toast');
    toast.textContent = mensaje;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 1500);
}