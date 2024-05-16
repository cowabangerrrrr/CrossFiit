function handleCloseButton() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: none;');
    dialog.close();
}

function changeGridLayout() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: block;')
    dialog.showModal();
    return;
    if (window.innerWidth <= 450){
        form.setAttribute('style',
        `display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 30px 30px 0.25fr 1fr 0.25fr 1fr 0.25fr 0.5fr;
        row-gap: 10px;
        column-gap: 10px;
        grid-template-areas:
            "name"
            "selector"
            "first-explanatory-note"
            "first-download-block"
            "second-explanatory-note"
            "second-download-block"
            "third-explanatory-note"
            "description-block"
            "done-button";`);
    } else {
    }
    // const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: block;')
    dialog.showModal();
}
  
  

document.body.querySelector('[class="adding-button"]')
    .addEventListener('click', changeGridLayout);

document.querySelector('[class="close-window-adding-exercise"]')
    .addEventListener('click', handleCloseButton);

document.addEventListener('DOMContentLoaded', () => {
    const mainFotoInput = document.getElementById('main-foto');
    const instructionFotoInput = document.getElementById('instruction-foto');
    const mainFotoImg = document.querySelector('.load-main-foto img');
    const instructionFotoImg = document.querySelector('.load-instructions-foto img');
    let data = {};

    const handleFileUpload = (input, imgElement, key) => {
        input.addEventListener('change', () => {
            const file = input.files[0];
            const reader = new FileReader();

            reader.onload = (e) => {
                data[key] = e.target.result;
                imgElement.src = e.target.result;
                console.log(data);
            };

            if (file) {
                reader.readAsDataURL(file);
            }
        });
    };

    handleFileUpload(mainFotoInput, mainFotoImg, 'mainFoto');
    handleFileUpload(instructionFotoInput, instructionFotoImg, 'instructionFoto');
});


document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form[name="form-for-adding-exercise"]');
    const dialog = document.querySelector('dialog.window-adding-exercise');
    const addButton = document.querySelector('.adding-button');
    const closeButton = document.querySelector('.close-window-adding-exercise');
    const mainFotoInput = document.getElementById('main-foto');
    const instructionFotoInput = document.getElementById('instruction-foto');
    const mainFotoImg = document.querySelector('.load-main-foto img');
    const instructionFotoImg = document.querySelector('.load-instructions-foto img');
    let data = {};

    // Open the dialog
    addButton.addEventListener('click', () => {
        dialog.showModal();
    });

    // Close the dialog and reset the form
    closeButton.addEventListener('click', () => {
        form.reset();
        mainFotoImg.src = '/images/default-foto-download.png'; // Reset to default image
        instructionFotoImg.src = '/images/default-foto-download.png'; // Reset to default image
        dialog.close();
    });

    // Handle file upload and preview
    const handleFileUpload = (input, imgElement, key) => {
        input.addEventListener('change', () => {
            const file = input.files[0];
            const reader = new FileReader();

            reader.onload = (e) => {
                data[key] = e.target.result;
                imgElement.src = e.target.result;
                console.log(data);
            };

            if (file) {
                reader.readAsDataURL(file);
            }
        });
    };

    handleFileUpload(mainFotoInput, mainFotoImg, 'mainFoto');
    handleFileUpload(instructionFotoInput, instructionFotoImg, 'instructionFoto');

    // Handle form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        // Convert form data to JSON
        const json = {};
        formData.forEach((value, key) => {
            if (value instanceof File) {
                json[key] = value.name; // Store file name (you might want to handle file uploads separately)
            } else {
                json[key] = value;
            }
        });

        // Example: sending the files and JSON data to the server
        const fileData = new FormData();
        fileData.append('main-foto', formData.get('main-foto'));
        fileData.append('instruction-foto', formData.get('instruction-foto'));
        fileData.append('json', JSON.stringify(json));

        try {
            const response = await fetch('/your-server-endpoint', { // тут будет путь до сервера
                method: 'POST',
                body: fileData,
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Success:', result);
                form.reset(); // Reset form after successful submission
                mainFotoImg.src = '/images/default-foto-download.png'; // Reset to default image
                instructionFotoImg.src = '/images/default-foto-download.png'; // Reset to default image
                dialog.close(); // Close dialog on success
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
