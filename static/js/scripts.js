$(document).ready(function () {
    $("#registerForm").submit(function (e) {
        e.preventDefault();  // 阻止页面刷新

        $.ajax({
            url: "/register/",
            type: "POST",
            data: $(this).serialize(),  // 获取表单数据
            success: function (response) {
                window.location.href = "/dashboard/";  // 注册成功，跳转
            },
            error: function (xhr) {
                $("#registerAlert").removeClass("d-none").text(xhr.responseText);  // 显示错误信息
            }
        });
    });
});
//login
$(document).ready(function () {
    $("#loginForm").submit(function (e) {
        e.preventDefault();  // 阻止表单默认提交（避免页面刷新）

        $.ajax({
            url: "/login/",  // Django 登录 URL
            type: "POST",
            data: $(this).serialize(),  // 获取表单数据
            success: function (response) {
                window.location.href = response.redirect_url;  // 根据后端返回的 `redirect_url` 跳转
            },
            error: function (xhr) {
                $("#loginAlert").removeClass("d-none").text("Invalid username or password"); // 显示错误
            }
        });
    });
});
//change password
$(document).ready(function () {
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // 阻止默认提交（防止页面刷新）

        $.ajax({
            url: "/change-password/",  // Django 处理修改密码的 URL
            type: "POST",
            data: $(this).serialize(),  // 获取表单数据
            success: function (response) {
                alert("Password changed successfully! Redirecting...");
                window.location.href = "/dashboard/";  // 修改成功后跳转
            },
            error: function (xhr) {
                $("#changePasswordAlert").removeClass("d-none").text("Password change failed. Please check your input.");  // 显示错误
            }
        });
    });
});
//account settings
$(document).ready(function () {
    // 💡 点击 Change Password 按钮，显示模态框
    $("#changePasswordBtn").click(function () {
        $("#changePasswordModal").modal("show");
    });

    // 💡 处理 AJAX 提交密码修改请求
    $("#changePasswordForm").submit(function (e) {
        e.preventDefault();  // 阻止默认表单提交
        console.log("form submit");  // 检查事件是否触发

        $.ajax({
            url: "/change-password/",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                alert("Password changed successfully!");
                $("#changePasswordModal").modal("hide");  // 关闭弹窗
            },
            error: function (xhr) {
                $("#changePasswordError")
                    .removeClass("d-none")
                    .text("Error: " + xhr.responseText);
            }
        });
    });
});


