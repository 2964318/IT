document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll('.alert');
        messages.forEach(message => {
            console.log("Removing message:", message.innerText);
            message.style.opacity = "0";
            setTimeout(() => message.remove(), 500); // Complete removal after 500ms
        });
    }, 3000); // Hide message after 3 seconds
});
