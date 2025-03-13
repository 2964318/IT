document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let messages = document.querySelectorAll('.alert');
        messages.forEach(message => {
            console.log("Removing message:", message.innerText);
            message.style.opacity = "0";
            setTimeout(() => message.remove(), 500); // 500ms 后完全移除
        });
    }, 3000); // 3秒后隐藏消息
});
