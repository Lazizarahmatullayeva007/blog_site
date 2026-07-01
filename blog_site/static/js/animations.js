document.addEventListener("DOMContentLoaded", () => {

    // Reveal animation
    const reveals = document.querySelectorAll(".reveal");

    reveals.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add("active");
        }, index * 200);
    });

    // Card animation
    const cards = document.querySelectorAll(".reveal-card");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }

        });

    }, {
        threshold: 0.15
    });

    cards.forEach(card => observer.observe(card));

});