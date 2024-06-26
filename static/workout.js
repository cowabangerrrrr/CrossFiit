const modalController = ({ modal, btnOpen, btnClose, time = 300 }) => {
    const buttonElem = document.querySelector(btnOpen);
    const modalElem = document.querySelector(modal);

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

    const openModal = async () => {
        modalElem.style.display = "flex";
        modalElem.style.visibility = "visible";
        modalElem.style.opacity = 1;
        window.addEventListener("keydown", closeModal);
        if (btnOpen === ".st_button") {
            exercises.forEach((exerciseId) => {
                const button = document.getElementById(exerciseId);
                if (button) {
                    button.style.background = "white";
                    button.querySelector(".tick").style.opacity = "0";
                }
            });
            exercises.length = 0;
            saveButton.style.display = "none";
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
    modal: ".modalExtra",
    btnOpen: ".st_button",
    btnClose: ".closeButton",
});

document.getElementById("goToMain").addEventListener("click", () => {
    window.location.href = "/";
});

document
    .querySelector(".reboot-confirmation-dialog-button-group .yes-button")
    .addEventListener("click", () => {
        window.location.href = "workout";
    });

document
    .querySelector(".reboot-confirmation-dialog-button-group .no-button")
    .addEventListener("click", () => {
        const dialog = document.querySelector(".reboot-confirmation-dialog");
        dialog.close();
    });

document.getElementById("restart")?.addEventListener("click", () => {
    const dialog = document.querySelector(".reboot-confirmation-dialog");
    dialog.showModal();
});

function callConfirmation() {
    const dialog = document.querySelector(".confirmation-dialog-snackbar");
    dialog.showModal();

    const closeDialog = document.querySelector(
        ".close-confirmation-dialog-snackbar"
    );
    closeDialog.addEventListener("click", () => {
        dialog.close();
        showSnackbar();
    });
}

document.querySelector(".saveSerie").addEventListener("click", () => {
    const exButtons = document.querySelectorAll(".ex_button");
    const exercisesIds = [];

    exButtons.forEach((button) => {
        const modalId = button.getAttribute("data-modal-id");
        exercisesIds.push(modalId);
    });

    fetch("/save_serie", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ ids: exercisesIds }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    callConfirmation();
});

function deleteExercise(button) {
    const closeDialog = document.querySelector(".confirmation-dialog");
    const yesButton = document.querySelector(".yes-button");
    const noButton = document.querySelector(".no-button");

    button.addEventListener("click", () => {
        closeDialog.showModal();
        yesButton.addEventListener("click", () => {
            const container = button.closest(".container");
            container.remove();
            closeDialog.close();
        });
        noButton.addEventListener("click", () => closeDialog.close());
    });
}

document.querySelectorAll(".del_button").forEach(deleteExercise);

const exercises = [];
document.querySelector(".save_button").addEventListener("click", async () => {
    const exerciseContainer = document.querySelector(".exercises_container");
    const modalContainer = document.querySelector(".modal_container");
    const addButton = exerciseContainer.querySelector(".st_button");
    for (const id of exercises) {
        if (exerciseContainer.querySelector(`.ex_button[data-modal-id="${id}"]`)) 
            continue;

        const response = await fetch(`/get_exercise/${id}`);
        const exerciseData = await response.json();
        exerciseData.description = exerciseData.description.replace(/\n/g, '<br />');

        const container = document.createElement("div");
        container.className = "container";
        container.innerHTML = `
        <button class="ex_button" data-modal-id="${exerciseData.id}">
            <img src="../static/images/${exerciseData.main_photo_path}" alt="image" class="ex_image">
            <span>${exerciseData.name}</span>
        </button>
        <button class="del_button">&#10006;</button>
        `;

        const modalWindowForContainer = document.createElement("div");
        modalWindowForContainer.className = "modalExercise";
        modalWindowForContainer.id = `modal${exerciseData.id}`;
        modalWindowForContainer.innerHTML = `
        <div class="modalMain">
            <div class="header">
            <h2 class="modalTitle">${exerciseData.name}</h2>
                <button class="closeButton">&#10006;</button>
            </div>
            <img src="../static/images/${exerciseData.second_photo_path}" alt="default-img">

            <div class="descriptionContainer">
                <h3>Правила выполнения</h3>
                <pre>${exerciseData.description}</pre>
            </div>
        </div>
        `;
        exerciseContainer.insertBefore(container, addButton);
        modalContainer.appendChild(modalWindowForContainer);

        modalController({
            modal: `#modal${exerciseData.id}`,
            btnOpen: `.ex_button[data-modal-id="${exerciseData.id}"]`,
            btnClose: ".closeButton",
        });
        deleteExercise(container.querySelector(".del_button"));
    }
});

const saveButton = document.querySelector(".save_button");
document.querySelectorAll(".extraExerciseButton").forEach((button) => {
    button.addEventListener("click", () => {
        const id = button.id;
        if (exercises.includes(id)) {
            const ind = exercises.indexOf(id);
            exercises.splice(ind, 1);
            button.style.background = "white";
            button.querySelector(".tick").style.opacity = "0";
        } else {
            exercises.push(id);
            button.style.background = "rgb(164, 164, 164)";
            button.querySelector(".tick").style.opacity = "1";
        }
        saveButton.style.display = exercises.length > 0 ? "block" : "none";
    });
});

saveButton.addEventListener("click", () => {
    const modalExtra = document.querySelector(".modalExtra");
    modalExtra.style.display = "none";
    showSnackbar('snackbarAddExercise');
});

function showSnackbar(id='snackbar') {
    const snackbar = document.getElementById(id);
    snackbar.className = "show";
    setTimeout(function () {
        snackbar.className = snackbar.className.replace("show", "");
    }, 3000);
}
