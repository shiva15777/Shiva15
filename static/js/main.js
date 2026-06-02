// Global state
const state = {
    currentFile: null,
    currentFilePath: null,
    analysisData: null,
    syncData: null,
    processedPath: null
};

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const analyzeBtn = document.getElementById('analyzeBtn');
const syncBtn = document.getElementById('syncBtn');
const processBtn = document.getElementById('processBtn');
const exportBtn = document.getElementById('exportBtn');
const lyricsInput = document.getElementById('lyricsInput');
const normalizeCheckbox = document.getElementById('normalizeCheckbox');
const loudnessInput = document.getElementById('loudnessInput');
const compressCheckbox = document.getElementById('compressCheckbox');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const errorMessage = document.getElementById('errorMessage');
const successMessage = document.getElementById('successMessage');

// Helper functions
function showLoading(message = 'Processing...') {
    loadingText.textContent = message;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 5000);
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
    // Scroll to section
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// Upload handling
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragging');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragging');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragging');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    state.currentFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatBytes(file.size);
    fileInfo.style.display = 'block';
    
    uploadAudio();
}

async function uploadAudio() {
    showLoading('Uploading audio...');
    
    const formData = new FormData();
    formData.append('file', state.currentFile);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        state.currentFilePath = data.filepath;
        showSuccess('Audio uploaded successfully!');
        hideLoading();
        
        // Show next sections
        showSection('analyze-section');
        
    } catch (error) {
        hideLoading();
        showError('Upload failed: ' + error.message);
    }
}

// Analyze
analyzeBtn.addEventListener('click', analyzeAudio);

async function analyzeAudio() {
    if (!state.currentFilePath) {
        showError('No file uploaded');
        return;
    }
    
    showLoading('Analyzing audio...');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: state.currentFilePath
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        state.analysisData = data.analysis;
        displayAnalysis(data.analysis);
        hideLoading();
        showSuccess('Audio analyzed successfully!');
        
        // Show lyrics section
        showSection('lyrics-section');
        
    } catch (error) {
        hideLoading();
        showError('Analysis failed: ' + error.message);
    }
}

function displayAnalysis(analysis) {
    const analysisResults = document.getElementById('analysisResults');
    const analysisData = document.getElementById('analysisData');
    
    analysisData.innerHTML = `
        <div><strong>Duration:</strong> ${analysis.duration.toFixed(2)}s</div>
        <div><strong>Sample Rate:</strong> ${analysis.sample_rate} Hz</div>
        <div><strong>Tempo (BPM):</strong> ${analysis.tempo.toFixed(2)}</div>
        <div><strong>Detected Beats:</strong> ${analysis.beats_count}</div>
        <div><strong>Spectral Centroid:</strong> ${analysis.spectral_centroid_mean.toFixed(0)} Hz</div>
        <div><strong>Zero Crossing Rate:</strong> ${analysis.zero_crossing_rate_mean.toFixed(4)}</div>
        <div><strong>RMS Energy:</strong> ${analysis.rms_energy_mean.toFixed(4)}</div>
    `;
    
    analysisResults.style.display = 'block';
}

// Sync Lyrics
syncBtn.addEventListener('click', syncLyrics);

async function syncLyrics() {
    const lyricsText = lyricsInput.value.trim();
    
    if (!lyricsText) {
        showError('Please enter lyrics');
        return;
    }
    
    showLoading('Syncing lyrics to beats...');
    
    try {
        const response = await fetch('/api/sync-lyrics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: state.currentFilePath,
                lyrics: lyricsText
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Sync failed');
        }
        
        state.syncData = data.sync_data;
        displaySyncData(data.sync_data);
        hideLoading();
        showSuccess('Lyrics synced successfully!');
        
        // Show master section
        showSection('master-section');
        
    } catch (error) {
        hideLoading();
        showError('Lyrics sync failed: ' + error.message);
    }
}

function displaySyncData(syncData) {
    const syncResults = document.getElementById('syncResults');
    const syncDataDiv = document.getElementById('syncData');
    
    syncDataDiv.innerHTML = syncData.map(item => `
        <div>
            <strong>Line ${item.line_index + 1}:</strong> ${item.text}
            <br>
            <small>Time: ${item.start_time.toFixed(2)}s - ${item.end_time.toFixed(2)}s (${item.duration.toFixed(2)}s)</small>
        </div>
    `).join('');
    
    syncResults.style.display = 'block';
}

// Process/Master
processBtn.addEventListener('click', processAudio);

async function processAudio() {
    showLoading('Mastering audio...');
    
    const normalize = normalizeCheckbox.checked;
    const loudness = parseFloat(loudnessInput.value);
    const compress = compressCheckbox.checked;
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: state.currentFilePath,
                normalize,
                loudness,
                compress
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Processing failed');
        }
        
        state.processedPath = data.output_path;
        hideLoading();
        showSuccess('Audio mastered successfully!');
        
        // Show export section
        showSection('export-section');
        
    } catch (error) {
        hideLoading();
        showError('Audio processing failed: ' + error.message);
    }
}

// Export
exportBtn.addEventListener('click', exportAudio);

async function exportAudio() {
    showLoading('Exporting as MP3...');
    
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filepath: state.processedPath || state.currentFilePath
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Export failed');
        }
        
        hideLoading();
        displayExportResult(data);
        showSuccess('Audio exported successfully!');
        
    } catch (error) {
        hideLoading();
        showError('Export failed: ' + error.message);
    }
}

function displayExportResult(data) {
    const exportResults = document.getElementById('exportResults');
    const downloadLink = document.getElementById('downloadLink');
    
    downloadLink.href = data.download_url;
    downloadLink.textContent = `⬇️ Download ${data.output_filename}`;
    
    exportResults.style.display = 'block';
}

// Show initial section
showSection('upload-section');