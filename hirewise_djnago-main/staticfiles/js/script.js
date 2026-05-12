// script.js — Hirewise (Django Edition)
// Minimal JS — page interactions only, no fetch/JWT needed (Django handles auth)

// Resume filename display on auth page
document.addEventListener('DOMContentLoaded', function () {
    const resumeInput = document.getElementById('resume-file');
    const fileChosenName = document.getElementById('file-chosen-name');
    if (resumeInput && fileChosenName) {
        resumeInput.addEventListener('change', function () {
            if (resumeInput.files.length > 0) {
                fileChosenName.textContent = '✓ ' + resumeInput.files[0].name;
            } else {
                fileChosenName.textContent = '';
            }
        });
    }

    // Auto-dismiss flash messages after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 4000);
    });
});
