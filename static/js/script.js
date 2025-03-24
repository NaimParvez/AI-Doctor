document.addEventListener('DOMContentLoaded', () => {
    const messagesDiv = document.querySelector('.messages');
    const chatInput = document.querySelector('#chat-input');
    const sendIcon = document.querySelector('.send-icon');
    const micIcon = document.querySelector('.mic-icon');
    const cameraIcon = document.querySelector('.camera-icon');
    const attachIcon = document.querySelector('.attach-icon');
    const fileUpload = document.querySelector('#file-upload');
    const inputArea = document.querySelector('.input-area');
    const attachModal = document.querySelector('.attach-modal');
    const closeModal = document.querySelector('.close-modal');
    const selectFilesButton = document.querySelector('.select-files');
    const recentFilesList = document.querySelector('#recent-files-list');

    let uploadedFile = null;
    let recentFiles = JSON.parse(localStorage.getItem('recentFiles')) || [];

    const addMessage = (sender, content, filePath = null, audioPath = null) => {
        const div = document.createElement('div');
        div.className = `message ${sender} fade-in`;
        let html = '<div class="message-content">';
        if (content) html += `<p>${content}</p>`;
        if (filePath) {
            if (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.jpeg') || filePath.endsWith('.gif')) {
                html += `<img src="${filePath}" class="uploaded-image">`;
            } else if (filePath.endsWith('.pdf')) {
                html += `<a href="${filePath}" target="_blank">View PDF: ${filePath.split('/').pop()}</a>`;
            }
        }
        if (audioPath) html += `<audio controls src="${audioPath}"></audio>`;
        html += '</div>';
        div.innerHTML = html;
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    const showThinking = () => {
        const div = document.createElement('div');
        div.className = 'message doctor thinking';
        div.innerHTML = '<div class="message-content"><p>Thinking...</p></div>';
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        return div;
    };

    const removeThinking = (thinkingDiv) => {
        if (thinkingDiv) thinkingDiv.remove();
    };

    const displayUploadedFile = (filename, filePath) => {
        const existingPreview = document.querySelector('.file-preview');
        if (existingPreview) existingPreview.remove();

        const previewDiv = document.createElement('div');
        previewDiv.className = 'file-preview';
        previewDiv.innerHTML = `
            <span>File: ${filename}</span>
            <button class="cancel-file">Cancel</button>
        `;
        inputArea.insertBefore(previewDiv, inputArea.firstChild);

        uploadedFile = { filename, filePath };

        const cancelButton = previewDiv.querySelector('.cancel-file');
        cancelButton.addEventListener('click', () => {
            previewDiv.remove();
            uploadedFile = null;
            fileUpload.value = '';
        });
    };

    const updateRecentFiles = (filename, filePath) => {
        recentFiles = recentFiles.filter(file => file.filePath !== filePath);
        recentFiles.unshift({ filename, filePath });
        if (recentFiles.length > 5) recentFiles.pop();
        localStorage.setItem('recentFiles', JSON.stringify(recentFiles));
        renderRecentFiles();
    };

    const renderRecentFiles = () => {
        recentFilesList.innerHTML = '';
        recentFiles.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span>${file.filename}</span>
                <button class="remove-file">×</button>
            `;
            fileItem.addEventListener('click', () => {
                displayUploadedFile(file.filename, file.filePath);
                attachModal.style.display = 'none';
            });
            fileItem.querySelector('.remove-file').addEventListener('click', (e) => {
                e.stopPropagation();
                recentFiles = recentFiles.filter(f => f.filePath !== file.filePath);
                localStorage.setItem('recentFiles', JSON.stringify(recentFiles));
                renderRecentFiles();
            });
            recentFilesList.appendChild(fileItem);
        });
    };

    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text && !uploadedFile) return;

        const thinkingDiv = showThinking();

        let filePath = null, audioPath = null;

        if (uploadedFile) {
            filePath = uploadedFile.filePath;
        }

        const messageData = {
            text: text,
            image_path: filePath,
            audio_path: audioPath,
            generate_speech: true
        };
        const response = await fetch('/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(messageData)
        }).then(res => res.json());

        removeThinking(thinkingDiv);
        addMessage('user', text, filePath);
        addMessage('doctor', response.response, null, response.audio);

        chatInput.value = '';
        if (uploadedFile) {
            const previewDiv = document.querySelector('.file-preview');
            if (previewDiv) previewDiv.remove();
            uploadedFile = null;
        }
    };

    sendIcon.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => e.key === 'Enter' && sendMessage());

    cameraIcon.addEventListener('click', () => fileUpload.click());

    attachIcon.addEventListener('click', () => {
        renderRecentFiles();
        attachModal.style.display = 'flex';
    });

    closeModal.addEventListener('click', () => {
        attachModal.style.display = 'none';
    });

    selectFilesButton.addEventListener('click', () => fileUpload.click());

    const uploadArea = document.querySelector('.upload-area');
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#1e90ff';
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#555';
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#555';
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileUpload(files[0]);
    });

    fileUpload.addEventListener('change', async () => {
        const file = fileUpload.files[0];
        if (!file) return;
        handleFileUpload(file);
    });

    const handleFileUpload = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const uploadResponse = await fetch('/chat/upload', {
            method: 'POST',
            body: formData
        }).then(res => res.json());

        if (uploadResponse.error) {
            addMessage('doctor', uploadResponse.error);
            return;
        }

        if (uploadResponse.file_type === 'image' || uploadResponse.file_type === 'pdf') {
            displayUploadedFile(file.name, uploadResponse.file_path);
            updateRecentFiles(file.name, uploadResponse.file_path);
            attachModal.style.display = 'none';
        } else {
            const audioPath = uploadResponse.file_path;
            const transcription = uploadResponse.transcription;
            addMessage('user', transcription, null, audioPath);

            const messageData = {
                text: transcription,
                image_path: null,
                audio_path: audioPath,
                generate_speech: true
            };
            const response = await fetch('/chat/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(messageData)
            }).then(res => res.json());

            addMessage('doctor', response.response, null, response.audio);
        }
    };

    let mediaRecorder;
    let audioChunks = [];
    let startTime;

    micIcon.addEventListener('click', async () => {
        if (micIcon.classList.contains('recording')) {
            const elapsedTime = Date.now() - startTime;
            if (elapsedTime < 1000) {
                addMessage('doctor', 'Recording too short. Please record for at least 1 second.');
                micIcon.classList.remove('recording');
                return;
            }
            mediaRecorder.stop();
            micIcon.classList.remove('recording');
        } else {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
                audioChunks = [];
                startTime = Date.now();

                mediaRecorder.ondataavailable = (e) => {
                    audioChunks.push(e.data);
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    if (audioBlob.size < 100) {
                        addMessage('doctor', 'Recording is empty or too small. Please try again.');
                        return;
                    }

                    const formData = new FormData();
                    formData.append('file', audioBlob, 'recording.webm');

                    const uploadResponse = await fetch('/chat/upload', {
                        method: 'POST',
                        body: formData
                    }).then(res => res.json());

                    if (uploadResponse.error) {
                        addMessage('doctor', uploadResponse.error);
                        return;
                    }

                    chatInput.value = uploadResponse.transcription;
                };

                mediaRecorder.start();
                micIcon.classList.add('recording');
            } catch (e) {
                console.error('Error accessing microphone:', e);
                addMessage('doctor', 'Could not access microphone. Please check permissions.');
            }
        }
    });
});