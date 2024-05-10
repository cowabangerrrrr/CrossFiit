function handleCloseButton() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: none;');
    dialog.close();
}

document.body.querySelector('[class="adding-button"]')
    .addEventListener('click', () => {
        const dialog = document.body.querySelector('dialog');
        dialog.setAttribute('style', 
        `display: flex;
        flex-direction: column;`);
        dialog.showModal();
    });

document.querySelector('[class="close-window-adding-exercise"]')
    .addEventListener('click', handleCloseButton);

document.querySelector('[class="done-button"]')
    .addEventListener('click', handleCloseButton);


