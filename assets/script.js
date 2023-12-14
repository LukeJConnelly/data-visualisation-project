function fixTitlePositions() {
    const elements = document.querySelectorAll('g.g-gtitle text');
    elements.forEach(textElement => {
        try {
            textElement.setAttribute('x', textElement.textContent.includes("Times") ? '10' : '30');
        } catch (e) {}
        try {
            textElement.removeAttribute('text-anchor');
        } catch (e) {}
    });
    setTimeout(fixTitlePositions, 50);
}

fixTitlePositions()
