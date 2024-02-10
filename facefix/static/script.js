document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('upload-form');
    const outputSection = document.getElementById('output-section');
    const downloadLink = document.getElementById('download-link');

    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Assuming you're using fetch API to handle the form submission
        fetch('/process_video', {
            method: 'POST',
            body: new FormData(uploadForm)
        })
        .then(response => response.json())
        .then(data => {
            // Assuming the server responds with the processed video link
            downloadLink.href = data.video_link;
            downloadLink.innerHTML = 'Download Processed Video';
            outputSection.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    });
});
