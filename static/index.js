document.querySelector(".generating-button").addEventListener("click", () => window.location.href = "workout");

document.querySelector(".history-button").addEventListener("click", () => window.location.href = "saved_workout");

function handleCloseButton() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: none;');
    dialog.close();
}

function changeGridLayout() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: block;')
    dialog.showModal();
}

document.body.querySelector('.adding-button')
    .addEventListener('click', changeGridLayout);

document.querySelector('.close-window-adding-exercise')
    .addEventListener('click', handleCloseButton);

const defaultFotoPath = 'static/images/default-foto-download.png';
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.adding-exercise');
    const dialog = document.querySelector('.window-adding-exercise');
    const confirmationDialog = document.querySelector('.confirmation-dialog');
    const addButton = document.querySelector('.adding-button');
    const closeButton = document.querySelector('.close-window-adding-exercise');
    const mainFotoInput = document.getElementById('main-foto');
    const instructionFotoInput = document.getElementById('instruction-foto');
    const mainFotoImg = document.querySelector('.load-main-foto img');
    const instructionFotoImg = document.querySelector('.load-instructions-foto img');
    const closeConfirmation = document.querySelector('.close-confirmation-dialog');

    const data = {};

    addButton.addEventListener('click', () => dialog.showModal());

    closeButton.addEventListener('click', () => {
        form.reset();
        mainFotoImg.src = defaultFotoPath;
        instructionFotoImg.src = defaultFotoPath;
        dialog.close();
    });

    closeConfirmation.addEventListener('click', () => confirmationDialog.close());

    const handleFileUpload = (input, imgElement, key) => {
        input.addEventListener('change', () => {
            const file = input.files[0];
            const reader = new FileReader();

            reader.onload = () => {
                data[key] = reader.result;
                imgElement.src = reader.result;
                console.log(data);
            };

            if (file) {
                reader.readAsDataURL(file);
            }
        });
    };

    handleFileUpload(mainFotoInput, mainFotoImg, 'mainFoto');
    handleFileUpload(instructionFotoInput, instructionFotoImg, 'instructionFoto');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch('/upload_exercise', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                confirmationDialog.showModal();
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }

        form.reset();
        mainFotoImg.src = defaultFotoPath;
        instructionFotoImg.src = defaultFotoPath;
        dialog.close();
    });
});

function showSnackbar() {
    const snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    setTimeout(() => snackbar.className = snackbar.className.replace("show", ""), 3000);
}

window.onload = function() {
    if (showSavedSnackbar) {
        showSnackbar();
    }
}
