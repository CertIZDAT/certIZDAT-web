document.addEventListener("DOMContentLoaded", function () {
    const projectInfoBlock = document.getElementById("project-info-id");
    const btnShow = document.getElementById("show-btn-id");
    const btnClose = document.getElementById("close-btn");
    const selectList = document.getElementById('list-of');
    const textarea = document.getElementById('site-list');
    const btnDownload = document.getElementById('download-dump');

    if (btnDownload) {
        btnDownload.addEventListener('click', download_dump);
    }

    projectInfoBlock.style.display = "none";

    const toggleProjectInfo = () => {
        projectInfoBlock.style.display = projectInfoBlock.style.display === "none" ? "block" : "none";
    };
    btnShow.addEventListener("click", toggleProjectInfo);
    btnClose.addEventListener("click", toggleProjectInfo);

    const loadData = (endpoint) => {
        fetch(`/process/${endpoint}`)
            .then(response => response.text())
            .then(data => textarea.value = data)
            .catch(error => console.error('Error loading data:', error));
    };

    if (selectList.selectedIndex !== 0) {
        loadData('gov-ca');
    }
    selectList.selectedIndex = 0;

    selectList.addEventListener('change', (event) => {
        loadData(event.target.value);
    });
});

// Setup download dump button action
function download_dump() {
    fetch('/download_dump')
        .then(response => {
            if (!response.ok) {
                throw new Error('Download failed: ' + response.status);
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'statistics.db';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        })
        .catch(error => console.error('Error downloading dump:', error));
}
