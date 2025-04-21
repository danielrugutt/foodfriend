const listSelect = document.getElementById("list_select");
const nameInputBox = document.getElementById('name_input_box');

function updateNameDisplay() {
    if (listSelect.value === 'new') {
        nameInputBox.style.display = 'inline-block';
    } else {
        nameInputBox.style.display = 'none';
    }
}

listSelect.addEventListener('change', updateNameDisplay);
updateNameDisplay();
