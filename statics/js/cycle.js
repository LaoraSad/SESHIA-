

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("daily-log-form");

    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Ocurrió un error al guardar el registro.");
                return;
            }

            if (data.success) {
                alert(data.message);
            } else {
                alert("No fue posible guardar el registro.");
            }

        } catch (error) {
            console.error(error);
            alert("Error de conexión con el servidor.");
        }
    });
});