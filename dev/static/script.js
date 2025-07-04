document.addEventListener('DOMContentLoaded', function() {
    // Constants
    const outputFormatSelect = document.getElementById('output_format');
    const convertForm = document.getElementById('uploadForm');
    const loadingDiv = document.getElementById('loading');

    // Show loading animation during conversion
    if (convertForm) {
        convertForm.addEventListener('submit', function() {
            loadingDiv.style.display = 'block';
        });
    }

    const bitrateInput = document.getElementById('bitrate');

    if (bitrateInput) {
        // Saat form dikirim, pastikan bitrate selalu diakhiri dengan 'k'
        convertForm.addEventListener('submit', function () {
            let val = bitrateInput.value.trim().toLowerCase();
            if (!val.endsWith('k')) {
                if (!isNaN(val)) {
                    bitrateInput.value = val + 'k';
                }
            }
        });
    }
});

// ❗ This must be outside DOMContentLoaded
window.addEventListener('beforeunload', function () {
    navigator.sendBeacon('/shutdown');
});