// JavaScript to retain the selected category after submission
document.addEventListener("DOMContentLoaded", () => {
    // Get the URL parameters
    const params = new URLSearchParams(window.location.search);
    const selectedCategory = params.get("category");

    // If a category is selected, set it as the selected option in the dropdown
    if (selectedCategory) {
        const categoryDropdown = document.getElementById("category");
        categoryDropdown.value = selectedCategory;
    }
});

const text = "Welcome to ArticlePulse";
let i = 0;
const speed = 100; // Speed of typing effect in milliseconds

function typeWriter() {
    if (i < text.length) {
        document.getElementById("typing-text").textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    } else {
        // Pause before restarting
        setTimeout(() => {
            document.getElementById("typing-text").textContent = ""; // Clear the text
            i = 0; // Reset the index
            typeWriter(); // Restart the typing
        }, 2000); // Adjust this delay as needed
    }
}

// Start typing effect on page load
window.onload = typeWriter;