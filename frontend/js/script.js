// Set behavior for the project info button
document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("show-btn-id");
    let project_info_block = document.getElementById("project-info-id");
    project_info_block.style.display = "none";
    btn.addEventListener("click", function () {
        let project_info_block = document.getElementById("project-info-id");
        if (project_info_block.style.display === "none") {
            project_info_block.style.display = "block";
        } else {
            project_info_block.style.display = "none";
        }
    });

    const close_btn = document.getElementById("close-btn");
    close_btn.addEventListener("click", function () {
        let project_info_block = document.getElementById("project-info-id");
        project_info_block.style.display = "none";
    });

    // Set the selected index to -1 on page load
    const list_of_select = document.getElementById('list-of');
    // Fetch data from the server for the default index
    if (list_of_select.selectedIndex != 0) {
        fetch("/process/gov-ca")
            .then(response => response.text())
            .then(data => {
                textarea.value = data;
            })
            .catch(error => console.error(error));
    }
    list_of_select.selectedIndex = 0;

    // Set '#list-of' on change action
    const select = document.getElementById('list-of');
    const textarea = document.getElementById('site-list');

    select.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        const url = `/process/${selectedValue}`;

        fetch(url)
            .then(response => response.text())
            .then(data => {
                textarea.value = data;
            })
            .catch(error => console.error(error));
    });
});

// Setup download dump button action
function download_dump() {
    // Send a fetch request to the /download_dump endpoint
    fetch('/download_dump')
        .then(response => response.blob())
        .then(blob => {
            // Create a new Blob object with the file data and create a download link
            const url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'statistics.db';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
}
