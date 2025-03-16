$(document).ready(function () {
    $("#registerForm").submit(function (e) {
        e.preventDefault();  // Block page refresh

        $.ajax({
            url: "/register/",
            type: "POST",
            data: $(this).serialize(),  // Get form data
            success: function (response) {
                window.location.href = "/dashboard/";  // Registration successful, jump
            },
            error: function (xhr) {
                $("#registerAlert").removeClass("d-none").text(xhr.responseText);  // error message
            }
        });
    });
});
//login
$(document).ready(function () {
    $("#loginForm").submit(function (e) {
        e.preventDefault();  // Prevent form submission by default (avoid page refreshes)

        $.ajax({
            url: "/login/",  // Django login URL
            type: "POST",
            data: $(this).serialize(),  // Get form data
            success: function (response) {
                window.location.href = response.redirect_url;  // Jump according to 'redirect_url' returned by the backend
            },
            error: function (xhr) {
                $("#loginAlert").removeClass("d-none").text("Invalid username or password"); // Display error
            }
        });
    });
});
//change password
$(document).ready(function () {
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // Block default commits (prevents page refreshes)

        $.ajax({
            url: "/change-password/",  
            type: "POST",
            data: $(this).serialize(),  // Get form data
            success: function (response) {
                alert("Password changed successfully! Redirecting...");
                window.location.href = "/dashboard/";  // After the modification is successful, jump
            },
            error: function (xhr) {
                $("#changePasswordAlert").removeClass("d-none").text("Password change failed. Please check your input.");  
            }
        });
    });
});
//account settings
$(document).ready(function () {
    // Click the Change Password button to display the modal box
    $("#changePasswordBtn").click(function () {
        $("#changePasswordModal").modal("show");
    });

    // Handle AJAX submit password change requests
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // Prevents default form submission
        console.log("form submit");  // Check whether the event is triggered

        $.ajax({
            url: "/change-password/",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                alert("Password changed successfully!");
                $("#changePasswordModal").modal("hide");  // Close popup
            },
            error: function (xhr) {
                $("#changePasswordError")
                    .removeClass("d-none")
                    .text("Error: " + xhr.responseText);
            }
        });
    });
});


