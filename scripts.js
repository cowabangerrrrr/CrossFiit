function handleCloseButton() {
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: none;');
    dialog.close();
}

function changeGridLayout() {
    const form = document.body.querySelector('form');
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
        form.setAttribute('style',
        `display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: 30px 30px 0.5fr 1fr 0.25fr;
        row-gap: 10px;
        column-gap: 10px;
        grid-template-areas:
            "name name name"
            "selector selector selector"
            "first-explanatory-note second-explanatory-note third-explanatory-note"
            "first-download-block second-download-block description-block"
            ". done-button .";`);
    }
    const dialog = document.body.querySelector('dialog');
    dialog.setAttribute('style', 'display: block;')
    dialog.showModal();
}

function handleFormSubmit(event) {
    event.preventDefault();
    const data = serializeForm(event.target);
    
}

function serializeForm(formNode) {
    // const { elements } = formNode;
    // const data = Array.from(elements)
    //   .filter((item) => !!item.name)
    //   .map((element) => {
    //     const { name, value } = element;
  
    //     return { name, value }
    //   });
    const data = new FormData(formNode);
    console.log(Array.from(data.entries()));

  }
  
  

document.body.querySelector('[class="adding-button"]')
    .addEventListener('click', () => changeGridLayout());

document.querySelector('[class="close-window-adding-exercise"]')
    .addEventListener('click', handleCloseButton);

const form = document.querySelector('.adding-exercise');
form.addEventListener('click', handleFormSubmit);

window.addEventListener('resize', changeGridLayout);