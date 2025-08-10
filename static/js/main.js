// Basic JavaScript for Freak 'n Fries website
document.addEventListener('DOMContentLoaded', function() {
    console.log('Freak n Fries website loaded successfully!');
    
    // Flash message close functionality
    const flashCloseButtons = document.querySelectorAll('.flash-close');
    flashCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const flashMessage = this.parentElement;
            flashMessage.style.opacity = '0';
            flashMessage.style.transform = 'translateX(100%)';
            setTimeout(() => {
                flashMessage.remove();
            }, 300);
        });
    });
});