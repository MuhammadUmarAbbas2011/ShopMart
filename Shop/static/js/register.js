const togglePasswordVisibility = (passwordField, toggleIcon) => {
    const passwordInput = document.getElementById(passwordField),
        icon = document.getElementById(toggleIcon);
    icon.addEventListener('click', () => {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.add('ri-eye-line');
            icon.classList.remove('ri-eye-off-line');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('ri-eye-line');
            icon.classList.add('ri-eye-off-line');
        }
    });
}
togglePasswordVisibility('password', 'toggle-icon');