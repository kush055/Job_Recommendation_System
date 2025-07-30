document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('filePreview');

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            preview.innerText = `Selected: ${file.name}`;
        }
    });

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            preview.innerText = `Selected: ${file.name}`;
        }
    });
});
// This script handles the drag-and-drop functionality for file uploads