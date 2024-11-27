document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const selectedFiles = document.getElementById('selected-files');
    const uploadForm = document.getElementById('upload-form');
    const uploadButton = document.getElementById('upload-button');
    const uploadSection = document.getElementById('upload-section');
    const authSection = document.getElementById('auth-section');
    const progressBars = document.getElementById('progress-bars');
    const uploadProgress = document.getElementById('upload-progress');

    // Check authentication status on page load and periodically
    function checkAuthStatus() {
        fetch('/auth-status')
            .then(response => response.json())
            .then(data => {
                if (data.authenticated) {
                    authSection.classList.add('d-none');
                    uploadSection.classList.remove('d-none');
                } else {
                    authSection.classList.remove('d-none');
                    uploadSection.classList.add('d-none');
                }
            })
            .catch(error => {
                console.error('Auth check failed:', error);
                // Show auth section on error
                authSection.classList.remove('d-none');
                uploadSection.classList.add('d-none');
            });
    }

    // Initial check
    checkAuthStatus();
    
    // Check auth status every 30 seconds
    setInterval(checkAuthStatus, 30000);

    // File selection handling
    dropArea.addEventListener('click', () => fileInput.click());
    
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            selectedFiles.innerHTML = '';
            uploadForm.classList.remove('d-none');
            
            Array.from(files).forEach((file, index) => {
                const filePreview = createFilePreview(file, index);
                selectedFiles.appendChild(filePreview);
            });
        }
    }

    function createFilePreview(file, index) {
        const div = document.createElement('div');
        div.className = 'file-preview';
        div.innerHTML = `
            <div class="file-info">
                <strong>${file.name}</strong>
                <br>
                <small>${formatFileSize(file.size)}</small>
            </div>
            <div class="file-actions">
                <button class="btn btn-sm btn-danger" onclick="removeFile(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        return div;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Upload handling
    uploadButton.addEventListener('click', async () => {
        const files = fileInput.files;
        if (files.length === 0) return;

        uploadProgress.classList.remove('d-none');
        uploadButton.disabled = true;

        for (let i = 0; i < files.length; i++) {
            const formData = new FormData();
            formData.append('video', files[i]);
            formData.append('title', document.getElementById('title').value || files[i].name);
            formData.append('description', document.getElementById('description').value);
            formData.append('privacy', document.getElementById('privacy').value);
            formData.append('tags', document.getElementById('tags').value);

            const progressDiv = createProgressBar(files[i].name);
            progressBars.appendChild(progressDiv);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                if (result.success) {
                    updateProgressBar(progressDiv, 100, 'success');
                    checkUploadStatus(result.video_id, progressDiv);
                } else {
                    updateProgressBar(progressDiv, 100, 'danger');
                    showError(progressDiv, result.error);
                }
            } catch (error) {
                updateProgressBar(progressDiv, 100, 'danger');
                showError(progressDiv, 'Upload failed');
            }
        }

        uploadButton.disabled = false;
    });

    function createProgressBar(filename) {
        const div = document.createElement('div');
        div.className = 'upload-progress-item';
        div.innerHTML = `
            <div class="d-flex justify-content-between mb-2">
                <span>${filename}</span>
                <span class="status">Uploading...</span>
            </div>
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
            <div class="error-message text-danger mt-2"></div>
        `;
        return div;
    }

    function updateProgressBar(progressDiv, percentage, status = 'primary') {
        const progressBar = progressDiv.querySelector('.progress-bar');
        const statusText = progressDiv.querySelector('.status');
        
        progressBar.style.width = `${percentage}%`;
        progressBar.className = `progress-bar bg-${status}`;
        
        if (status === 'success') {
            statusText.textContent = 'Completed';
        } else if (status === 'danger') {
            statusText.textContent = 'Failed';
        }
    }

    function showError(progressDiv, message) {
        const errorDiv = progressDiv.querySelector('.error-message');
        errorDiv.textContent = message;
    }

    async function checkUploadStatus(videoId, progressDiv) {
        try {
            const response = await fetch(`/upload-status/${videoId}`);
            const data = await response.json();
            
            if (data.status.uploadStatus === 'processed') {
                updateProgressBar(progressDiv, 100, 'success');
            } else if (data.status.uploadStatus === 'failed') {
                updateProgressBar(progressDiv, 100, 'danger');
                showError(progressDiv, 'Processing failed');
            } else {
                setTimeout(() => checkUploadStatus(videoId, progressDiv), 5000);
            }
        } catch (error) {
            showError(progressDiv, 'Status check failed');
        }
    }
});

function removeFile(index) {
    const input = document.getElementById('fileInput');
    const dt = new DataTransfer();
    
    Array.from(input.files)
        .filter((_, i) => i !== index)
        .forEach(file => dt.items.add(file));
    
    input.files = dt.files;
    
    if (input.files.length === 0) {
        document.getElementById('upload-form').classList.add('d-none');
    }
    
    document.getElementById('selected-files').children[index].remove();
}