(function(){
    const dropArea = document.querySelector('#dropArea');
    const uploadButton = document.querySelector('#uploadButton');
    const fileInput = document.querySelector('#fileInput');
    async function handleDragOver(event) {
        event.preventDefault();
        // event.dataTransfer.dropEffect = 'copy';
        dropArea.classList.add('dragover');
    }

    async function handleDrop(event) {
        event.preventDefault();
        dropArea.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            handleUploadedFiles(files);
            fileInput.files = event.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    }

    function handleFileInputChange(event) {
        // fileInput.files
        handleUploadedFiles(fileInput.files);
    }
    async function handleUploadedFiles(files) {
        if (files.length > 0) {
            console.log('files', files)
            let fileNames = Object.keys(files).map(key => files[key].name).join(', ');
            dropArea.textContent = `File(s) selected: ${fileNames}`;
        } else {
            dropArea.textContent = 'Drag & Drop file here or click to select';
        }
    }
    async function init() {
        dropArea.addEventListener('dragover', handleDragOver);
        dropArea.addEventListener('drop', handleDrop);
        uploadButton.addEventListener('click', uploadFiles);
        fileInput.addEventListener('change', handleFileInputChange);
    }

    function getFileExtension(fileName) {
        const extension = fileName.split('.').pop();
        return extension;
    }
    function isExtensionImage(fileType) {
        return ['jpg', 'jpeg', 'png', 'gif', 'heic'].includes(fileType.toLowerCase());
    }
    function isExtensionAudio(fileType){
        return ['mp3', 'wav', 'ogg', 'm4a'].includes(fileType);
    }
    function createFormData(files) {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            if (isExtensionImage(getFileExtension(files[i].name))) {
                formData.append('image', files[i]);
            }
            if (isExtensionAudio(getFileExtension(files[i].name))) {
                formData.append('audio', files[i]);
            }
        }
        return formData;
    }
    async function uploadFiles() {
        const fileInput = document.getElementById('fileInput');
        const file1 = fileInput.files[0];
        const file2 = fileInput.files[1];

        if (!file1 || !file2) {
            alert('Please select a file.');
            return;
        }

        // const formData = new FormData();
        // formData.append('file1', file1);
        // formData.append('file2', file2);
        const formData = createFormData(fileInput.files);

        let response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        })
        
        if (response.ok) {
            alert('File uploaded successfully!');
        } else {
            alert('File upload failed.');
        }
        let data = await response.json();
        console.log('resp data', data);
    }
    init();
})();