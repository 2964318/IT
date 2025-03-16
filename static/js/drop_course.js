document.addEventListener("DOMContentLoaded", function () {
    console.log("drop_course.js loaded ✅");

    let dropButton = document.getElementById("drop-btn");

    if (dropButton) {
        console.log("Drop button found ✅");

        dropButton.addEventListener("click", function () {
            console.log("Drop button clicked ✅");

            let enrollmentId = this.getAttribute("data-enrollment-id");
            console.log("Enrollment ID:", enrollmentId);

            if (!enrollmentId) {
                alert("Error: Enrollment ID not found.");
                return;
            }

            if (!confirm("Are you sure you want to drop this course?")) {
                return;
            }

            fetch(`/drop/${enrollmentId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
            .then(response => {
                console.log("Response received ✅", response);
                return response.json();
            })
            .then(data => {
                console.log("Response data ✅", data);
                if (data.error) {
                    alert("Failed to drop course: " + data.error);
                } else {
                    alert("Course dropped successfully");
                    location.reload();
                }
            })
            .catch(error => console.error('Fetch error:', error));
        });
    } else {
        console.error("Drop button NOT found ❌");
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log("CSRF Token:", cookieValue);
    return cookieValue;
}
