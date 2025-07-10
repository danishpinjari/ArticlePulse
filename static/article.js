// Typing effect for headline
document.addEventListener("DOMContentLoaded", function () {
    const typingText = document.getElementById("typing-text");

    // Phrases to cycle through
    const phrases = [
        "Stay Informed. Stay Ahead.",
        "AI-Powered News Summaries",
        "Real-Time Sentiment Analysis",
        "Explore the World with ArticlePulse"
    ];

    let currentPhraseIndex = 0;
    let currentCharIndex = 0;
    let isDeleting = false;
    const typingSpeed = 100;
    const pauseTime = 1500;

    function type() {
        const currentPhrase = phrases[currentPhraseIndex];
        if (isDeleting) {
            currentCharIndex--;
        } else {
            currentCharIndex++;
        }

        typingText.textContent = currentPhrase.substring(0, currentCharIndex);

        if (!isDeleting && currentCharIndex === currentPhrase.length) {
            isDeleting = true;
            setTimeout(type, pauseTime);
        } else if (isDeleting && currentCharIndex === 0) {
            isDeleting = false;
            currentPhraseIndex = (currentPhraseIndex + 1) % phrases.length;
            setTimeout(type, 300);
        } else {
            setTimeout(type, typingSpeed);
        }
    }

    type(); // Start typing animation
});
