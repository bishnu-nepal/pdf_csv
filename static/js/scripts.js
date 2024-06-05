document.getElementById('convert').addEventListener('click', async () => {
    const fileInput = document.getElementById('upload');
    const message = document.getElementById('message');
    const downloadLink = document.getElementById('download');

    message.textContent = '';
    downloadLink.style.display = 'none';

    if (fileInput.files.length === 0) {
        message.textContent = 'Please select a PDF file to convert.';
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('pdf', file);

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            downloadLink.href = url;
            downloadLink.download = 'output.csv';
            downloadLink.style.display = 'block';

            message.textContent = 'The process is successful';
            message.style.color = '#28a745';
        } else {
            const errorData = await response.json();
            message.textContent = `Sorry !!! Error occurred during the process: ${errorData.error}`;
            message.style.color = '#d9534f';
        }
    } catch (error) {
        console.error('Error during the PDF to CSV conversion process:', error);
        message.textContent = 'Sorry !!! Error occurred during the process';
        message.style.color = '#d9534f';
    }
});
