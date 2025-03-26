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

    const addMessage = (sender, content, filePath = null, audioPath = null, isTyping = false) => {
        const div = document.createElement('div');
        div.className = `message ${sender} fade-in`;
        let html = `
            <img src="/static/images/doctor-avatar.png" class="avatar" onerror="this.src='https://via.placeholder.com/40';">
            <div class="message-content">
                ${content ? '<p></p>' : ''}
                ${filePath ? (filePath.endsWith('.png') || filePath.endsWith('.jpg') || filePath.endsWith('.jpeg') || filePath.endsWith('.gif') 
                    ? `<img src="${filePath}" class="uploaded-image">` 
                    : filePath.endsWith('.pdf') 
                    ? `<a href="${filePath}" target="_blank">View PDF: ${filePath.split('/').pop()}</a>` 
                    : '') : ''}
                ${audioPath ? `<audio controls src="${audioPath}"></audio>` : ''}
            </div>
        `;
        div.innerHTML = html;
        messagesDiv.appendChild(div);

        if (content && isTyping) {
            const p = div.querySelector('p');
            typeMessage(p, content);
        } else if (content) {
            div.querySelector('p').textContent = content;
        }

        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };

    const typeMessage = (element, text) => {
        let index = 0;
        element.textContent = '';
        const interval = setInterval(() => {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
            } else {
                clearInterval(interval);
            }
        }, 30); // Adjust the speed of typing (30ms per character)
    };

    const showThinking = () => {
        const div = document.createElement('div');
        div.className = 'message doctor thinking';
        div.innerHTML = `
            <img src="/static/images/doctor-avatar.png" class="avatar" onerror="this.src='https://via.placeholder.com/40';">
            <div class="message-content"><p>Thinking...</p></div>
        `;
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

        // Clear the textbox immediately after capturing the text
        chatInput.value = '';

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

        try {
            const response = await fetch('/chat/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(messageData)
            });

            if (!response.ok) {
                throw new Error(`Failed to send message: ${response.statusText}`);
            }

            const data = await response.json();

            removeThinking(thinkingDiv);
            addMessage('user', text, filePath);
            addMessage('doctor', data.response, null, data.audio, true);
        } catch (error) {
            console.error('Error sending message:', error);
            removeThinking(thinkingDiv);
            addMessage('doctor', 'Error sending message: ' + error.message);
        } finally {
            // Clear the file preview and reset uploadedFile
            if (uploadedFile) {
                const previewDiv = document.querySelector('.file-preview');
                if (previewDiv) previewDiv.remove();
                uploadedFile = null;
            }
        }
    };

    sendIcon.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => e.key === 'Enter' && sendMessage());

    cameraIcon.addEventListener('click', () => {
        // On mobile devices, this will prompt to take a photo or select from gallery
        fileUpload.setAttribute('accept', 'image/*'); // Restrict to images only for camera
        fileUpload.click();
    });

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
        uploadArea.style.borderColor = '#ff6f61';
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#627288';
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#627288';
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileUpload(files[0]);
    });

    fileUpload.addEventListener('change', async () => {
        const file = fileUpload.files[0];
        if (!file) return;

        // Validate file type on the frontend
        const allowedImageTypes = ['image/png', 'image/jpeg', 'image/gif'];
        const allowedAudioTypes = ['audio/mpeg', 'audio/wav', 'audio/webm'];
        const allowedPdfType = 'application/pdf';

        if (!allowedImageTypes.includes(file.type) && !allowedAudioTypes.includes(file.type) && file.type !== allowedPdfType) {
            addMessage('doctor', 'Unsupported file type. Please upload an image, audio, or PDF.');
            fileUpload.value = ''; // Clear the input
            return;
        }

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

            // Automatically send the image with a default message
            const text = chatInput.value.trim() || "Please analyze this image.";
            const messageData = {
                text: text,
                image_path: uploadResponse.file_path,
                audio_path: null,
                generate_speech: true
            };

            const thinkingDiv = showThinking();
            try {
                const response = await fetch('/chat/message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(messageData)
                });

                if (!response.ok) {
                    throw new Error(`Failed to send message: ${response.statusText}`);
                }

                const data = await response.json();
                removeThinking(thinkingDiv);
                addMessage('user', text, uploadResponse.file_path);
                addMessage('doctor', data.response, null, data.audio, true);
            } catch (error) {
                console.error('Error sending image message:', error);
                removeThinking(thinkingDiv);
                addMessage('doctor', 'Error sending message: ' + error.message);
            } finally {
                const previewDiv = document.querySelector('.file-preview');
                if (previewDiv) previewDiv.remove();
                uploadedFile = null;
            }
        } else {
            const audioPath = uploadResponse.file_path;
            const transcription = uploadResponse.transcription;
            if (!transcription) {
                addMessage('doctor', 'Failed to transcribe audio. Please try again.');
                return;
            }
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

            addMessage('doctor', response.response, null, response.audio, true);
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
                    // Stop all tracks to release the microphone
                    stream.getTracks().forEach(track => track.stop());

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

                    if (!uploadResponse.transcription) {
                        addMessage('doctor', 'Failed to transcribe audio. Please try again.');
                        return;
                    }

                    // Add the transcribed message to the chat
                    addMessage('user', uploadResponse.transcription, null, uploadResponse.file_path);

                    // Automatically send the transcribed message to the server
                    const messageData = {
                        text: uploadResponse.transcription,
                        image_path: null,
                        audio_path: uploadResponse.file_path,
                        generate_speech: true
                    };

                    const thinkingDiv = showThinking();
                    try {
                        const response = await fetch('/chat/message', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(messageData)
                        });

                        if (!response.ok) {
                            throw new Error(`Failed to send message: ${response.statusText}`);
                        }

                        const data = await response.json();
                        removeThinking(thinkingDiv);
                        addMessage('doctor', data.response, null, data.audio, true);
                    } catch (error) {
                        console.error('Error sending transcribed message:', error);
                        removeThinking(thinkingDiv);
                        addMessage('doctor', 'Error sending message: ' + error.message);
                    }
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