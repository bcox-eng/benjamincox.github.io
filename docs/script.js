document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const rootElement = document.documentElement;

    // Check for saved user preference, if any, on load
    const currentTheme = localStorage.getItem('theme');

    // If the user previously chose light mode, apply it
    if (currentTheme === 'light') {
        rootElement.classList.add('light-mode');
        if (toggleButton) toggleButton.textContent = '🌙'; // Moon to switch to Dark
    } else {
        // Default is dark mode (no class)
        if (toggleButton) toggleButton.textContent = '☀️'; // Sun to switch to Light
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            rootElement.classList.toggle('light-mode');

            let theme = 'dark';
            if (rootElement.classList.contains('light-mode')) {
                theme = 'light';
                toggleButton.textContent = '🌙';
            } else {
                theme = 'dark';
                toggleButton.textContent = '☀️';
            }
            localStorage.setItem('theme', theme);
        });
    }

    const viewMoreBtn = document.getElementById('view-more-projects');
    if (viewMoreBtn) {
        viewMoreBtn.addEventListener('click', () => {
            const hiddenProjects = document.querySelectorAll('.hidden-project');
            hiddenProjects.forEach(project => {
                project.classList.remove('hidden-project');
            });
            viewMoreBtn.parentElement.style.display = 'none';
        });
    }
});
