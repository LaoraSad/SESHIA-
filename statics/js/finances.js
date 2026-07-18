document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("transaction-form");

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
                alert(data.message || "Ocurrió un error.");
                return;
            }

            const transactionsList = document.getElementById("transactions-list");

            if (transactionsList) {
                transactionsList.insertAdjacentHTML(
                    "afterbegin",
                    data.transaction_html
                );
            }

            form.reset();

        } catch (error) {
            console.error(error);
            alert("Error de conexión con el servidor.");
        }
    });
});