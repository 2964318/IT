$(document).ready(function () {
    $("#registerForm").submit(function (e) {
        e.preventDefault();  // Block page refresh

        $.ajax({
            url: "/register/",
            type: "POST",
            data: $(this).serialize(),  // Getting form data
            success: function (response) {
                window.location.href = "/dashboard/";  // Successful registration, jump
            },
            error: function (xhr) {
                $("#registerAlert").removeClass("d-none").text(xhr.responseText);  // Display error messages
            }
        });
    });
});
//login
$(document).ready(function () {
    $("#loginForm").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: "/login/",  // Django Login URL
            type: "POST",
            data: $(this).serialize(),  // Getting form data
            success: function (response) {
                window.location.href = response.redirect_url;  // Jump based on the `redirect_url` returned by the backend.
            },
            error: function (xhr) {
                $("#loginAlert").removeClass("d-none").text("Invalid username or password"); // error
            }
        });
    });
});
//change password
$(document).ready(function () {
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // 阻止默认提交（防止页面刷新）

        $.ajax({
            url: "/change-password/",  // Django handles URLs for changing passwords
            type: "POST",
            data: $(this).serialize(),  // Getting form data
            success: function (response) {
                alert("Password changed successfully! Redirecting...");
                window.location.href = "/dashboard/";  // Jump after successful modification
            },
            error: function (xhr) {
                $("#changePasswordAlert").removeClass("d-none").text("Password change failed. Please check your input.");  // display error message
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

    // Handling AJAX Submission of Password Change Requests
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // Blocking default form submission
        console.log("form submit");  //Check if an event is triggered

        $.ajax({
            url: "/change-password/",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                alert("Password changed successfully!");
                $("#changePasswordModal").modal("hide");  // Close pop-up window
            },
            error: function (xhr) {
                $("#changePasswordError")
                    .removeClass("d-none")
                    .text("Error: " + xhr.responseText);
            }
        });
    });
});


