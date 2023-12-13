function fixTitlePositions() {
    const elements = document.querySelectorAll('g.g-gtitle text');
    elements.forEach(textElement => {
        try {
            textElement.setAttribute('x', '10');
        } catch (e) {}
        try {
            textElement.removeAttribute('text-anchor');
        } catch (e) {}
    });
    setTimeout(fixTitlePositions, 50);
}

fixTitlePositions()
