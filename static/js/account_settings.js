document.addEventListener("DOMContentLoaded", function() {
    let deactivateButton = document.getElementById("deactivateAccountBtn");
    if (deactivateButton) {
        deactivateButton.addEventListener("click", function() {
            let modal = new bootstrap.Modal(document.getElementById("deactivateAccountModal"));
            modal.show();
        });
    }

    let confirmDeactivateButton = document.getElementById("confirmDeactivateBtn");
    if (confirmDeactivateButton) {
        confirmDeactivateButton.addEventListener("click", function() {
            fetch("/request_deactivate_account/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);  // Prompt message
                window.location.reload();  // Reload page
            })
            .catch(error => console.error("Error:", error));
        });
    }
});

// Obtain the CSRF Token
function getCSRFToken() {
    let csrfTokenElement = document.querySelector("input[name='csrfmiddlewaretoken']");
    return csrfTokenElement ? csrfTokenElement.value : "";
}
