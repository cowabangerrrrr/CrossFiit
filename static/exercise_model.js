const modalController = ({ modal, btnOpen, btnClose, time = 300 }) => {
    const buttonElem = document.querySelector(btnOpen);
    const modalElem = document.querySelector(modal);
    modalElem.style.cssText = `
    display: flex;
    visibility: hidden;
    opacity: 0;
    transition: opacity 300ms ease-in-out;
  `;

    const closeModal = (event) => {
        const target = event.target;

        if (
            target === modalElem ||
            (btnClose && target.closest(`${modal} .closeButton`)) ||
            event.code === "Escape"
        ) {
            modalElem.style.opacity = 0;

            setTimeout(() => {
                modalElem.style.visibility = "hidden";
                modalElem.style.display = "none";
            }, time);

            window.removeEventListener("keydown", closeModal);
        }
    };

    const openModal = () => {
        modalElem.style.display = "flex";
        modalElem.style.visibility = "visible";
        modalElem.style.opacity = 1;
        window.addEventListener("keydown", closeModal);
        if (btnOpen === '.st_button'){
            exercises.forEach(exerciseId => {
                const button = document.getElementById(exerciseId);
                if (button) {
                    button.style.background = 'white';
                }
            });
            exercises.length = 0;
            saveButton.style.display = 'none';
        }
    };

    buttonElem.addEventListener("click", openModal);

    modalElem.addEventListener("click", closeModal);
};

document.querySelectorAll(".ex_button").forEach((button) => {
    const modalId = button.dataset.modalId;
    modalController({
        modal: `#modal${modalId}`,
        btnOpen: `.ex_button[data-modal-id="${modalId}"]`,
        btnClose: ".closeButton",
    });
});

modalController({
    modal: '.modalExtra',
    btnOpen: '.st_button',
    btnClose: ".closeButton",
});

document.getElementById("goToMain").addEventListener("click", () => {
    window.location.href = "/";
});

document.getElementById("restart").addEventListener("click", () => {
    window.location.href = "workout";
});

document.querySelectorAll(".del_button").forEach((button) => {
    button.addEventListener("click", () => {
        const confirmDelete = confirm("Вы действительно хотите удалить упражнение?");
        if (confirmDelete) {
            const container = button.closest(".container");
            container.remove();
        }
    });
});


const exercises = [];
const extraExerciseButtons = document.querySelectorAll('.extraExerciseButton');
const saveButton = document.querySelector('.save_button');

extraExerciseButtons.forEach(button => {
    button.addEventListener('click', () => {
        const id = button.id;
        if (exercises.includes(id)) {
            const ind = exercises.indexOf(id);
            exercises.splice(ind, 1);
            button.style.background = 'white';
        } else {
            exercises.push(id);
            button.style.background = '#393939';
        }
        saveButton.style.display = exercises.length > 0 ? 'block' : 'none';
    });
});

saveButton.addEventListener('click', () => {
    console.log(exercises);
    const modalExtra = document.querySelector('.modalExtra');
    modalExtra.style.display = 'none';
});