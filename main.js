JavaScript

// Mobile menu toggle with improved accessibility and animation
const mobileMenuButton = document.getElementById('mobileMenuButton');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuIcon = mobileMenuButton.querySelector('i');

mobileMenuButton.addEventListener('click', () => {
    const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
    mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('hidden');
    mobileMenu.classList.toggle('slide-in');
    mobileMenuIcon.classList.toggle('fa-bars');
    mobileMenuIcon.classList.toggle('fa-times');
});

// Close mobile menu when clicking outside
document.addEventListener('click', (event) => {
    if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('slide-in');
        mobileMenuButton.setAttribute('aria-expanded', 'false');
        mobileMenuIcon.classList.add('fa-bars');
        mobileMenuIcon.classList.remove('fa-times');
    }
});

// Handle orientation change
window.addEventListener('orientationchange', () => {
    if (window.innerWidth > 768) {
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('slide-in');
        mobileMenuButton.setAttribute('aria-expanded', 'false');
        mobileMenuIcon.classList.add('fa-bars');
        mobileMenuIcon.classList.remove('fa-times');
    }
});

// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// Lazy load off-screen images
document.addEventListener("DOMContentLoaded", function() {
    var lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));

    if ("IntersectionObserver" in window) {
        let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove("lazy");
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }
});

// Error handling for chatbot iframe
const chatbotIframe = document.querySelector('#chatbot iframe');
chatbotIframe.onerror = function() {
    console.error('Error loading chatbot');
    chatbotIframe.style.display = 'none';
    const errorMessage = document.createElement('p');
    errorMessage.textContent = 'Sorry, our chatbot is currently unavailable. Please try again later.';
    chatbotIframe.parentNode.appendChild(errorMessage);
};

// Detect slow connections
function isSlowConnection() {
    return navigator.connection &&
           (navigator.connection.saveData === true ||
            (navigator.connection.type !== undefined && navigator.connection.type === "cellular"));
}

// Lazy load chatbot for slow connections
function lazyLoadChatbot() {
    const chatbotContainer = document.getElementById('chatbot');
    const chatbotObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = document.createElement('iframe');
                iframe.src = 'about:blank';
                iframe.srcdoc = document.getElementById('chatbotIframe').getAttribute('srcdoc');
                iframe.className = document.getElementById('chatbotIframe').className;
                document.getElementById('chatbotIframe').replaceWith(iframe);
                chatbotObserver.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px 0px 200px 0px' });

    chatbotObserver.observe(chatbotContainer);
}

// Initialize mobile optimizations
document.addEventListener('DOMContentLoaded', () => {
    if (isSlowConnection()) {
        lazyLoadChatbot();
    }
});

