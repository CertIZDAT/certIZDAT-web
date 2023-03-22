// Set behavior for the project info button
document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("show-btn-id");
    var project_info_block = document.getElementById("project-info-id");
    project_info_block.style.display = "none";
    btn.addEventListener("click", function () {
        var project_info_block = document.getElementById("project-info-id");
        if (project_info_block.style.display === "none") {
            btn.style.backgroundColor = "#FF0000";
            project_info_block.style.display = "block";
        } else {
            btn.style.backgroundColor = "#FFE5E5";
            project_info_block.style.display = "none";
        }
    });
});

// Setup download dump button action
function download_dump() {
    // Send a fetch request to the /download_dump endpoint
    fetch('/download_dump')
        .then(response => response.blob())
        .then(blob => {
            // Create a new Blob object with the file data and create a download link
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'statistics.db';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
};

// Setup download list of the sites with Russian Trusted CA button action
function download_ca_list() {
    // Send a fetch request to the /download_dump endpoint
    fetch('/download_ca_list')
        .then(response => response.blob())
        .then(blob => {
            // Create a new Blob object with the file data and create a download link
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'CA_list.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
};

// Setup download list of the sites with self signed certificate button action
function download_self_sign_list() {
    // Send a fetch request to the /download_dump endpoint
    fetch('/download_self_sign_list')
        .then(response => response.blob())
        .then(blob => {
            // Create a new Blob object with the file data and create a download link
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'self_sign_list.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
};
