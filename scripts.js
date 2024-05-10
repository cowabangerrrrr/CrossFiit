function handleCloseButton() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: none;');
    dialog.close();
}

document.body.querySelector('[class="adding-button"]')
    .addEventListener('click', () => {
        const dialog = document.body.querySelector('dialog');
        dialog.setAttribute('style', 
        `display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: 40px 30px 30px 0.5fr 1fr 0.25fr;
        row-gap: 10px;
        column-gap: 10px;
        grid-template-areas:
            "header header header"
            "name name name"
            "selector selector selector"
            "first-explanatory-note second-explanatory-note third-explanatory-note"
            "first-download-block second-download-block description-block"
            ". done-button .";`);
        dialog.showModal();
    });

document.querySelector('[class="close-window-adding-exercise"]')
    .addEventListener('click', handleCloseButton);

document.querySelector('[class="done-button"]')
    .addEventListener('click', handleCloseButton);


