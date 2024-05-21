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
            }, time);

            window.removeEventListener("keydown", closeModal);
        }
    };

    const openModal = async () => {
        modalElem.style.visibility = "visible";
        modalElem.style.opacity = 1;
        window.addEventListener("keydown", closeModal);
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


const exercisesIdsToAdd = [1, 2, 22];
const addExercisesButton = document.querySelector('.addExercisesButton');
addExercisesButton.addEventListener('click', async () => {
    const exerciseContainer = document.querySelector('.exercises_container');
    const addButton = exerciseContainer.querySelector('.st_button');
    for (const id of exercisesIdsToAdd) {
        const a = exerciseContainer.querySelector(`.ex_button[data-modal-id="${id}"]`);
        if (a) {
            continue;
        }

        const response = await fetch(`/get_exercise/${id}`);
        const exerciseData = await response.json();

        const container = document.createElement('div');
        container.className = 'container';
        container.innerHTML = 
        `
        <div class="container">
            <button class="ex_button" data-modal-id="${exerciseData.id}">
                <img src="../static/images/${exerciseData.main_photo_path}" alt="image" class="ex_image">
                <span>${exerciseData.name}</span>
            </button>
            <button class="del_button">
                <img src="../static/images/delete.png" alt="image" class="del_img">
            </button>
        </div>
        `;
        exerciseContainer.insertBefore(container, addButton);
    }
});