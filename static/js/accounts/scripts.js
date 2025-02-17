

function signin()
{
container.classList.remove('right-panel-active');
} 
function signup()
{
container.classList.add('right-panel-active');
}
function forgotpassword() {
    // var 
    
}
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll(".fade-message");
        alerts.forEach(function(alert) {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000); // 5 seconds
});