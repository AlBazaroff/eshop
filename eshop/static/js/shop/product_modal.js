const category_selector = document.getElementById("id_category");
const categoryForm = document.getElementById("add_category");
const categoryModalEl = document.getElementById("categoryModal");
const categoryModal = new bootstrap.Modal('#categoryModal');
const alertMessages = document.getElementById("alertMessages");

const modalTitle = categoryModalEl.querySelector(".modal-title");
const categoryIdInput = document.getElementById("id_category_id");
const categoryNameInput = document.getElementById("id_category_name");

const btnAdd = document.getElementById("btnAddCategory");
const btnEdit = document.getElementById("btnEditCategory");
const categoryBtn = document.getElementById("category_btn");

// add category
btnAdd.addEventListener("click", () => {
modalTitle.textContent = "Add category";
categoryForm.action = "/admin/category/add/";
categoryIdInput.value = "";
categoryNameInput.value = "";
categoryBtn.innerHTML = "Add category"
alertMessages.innerHTML = "";
});

// update category
btnEdit.addEventListener("click", () => {
const selectedOption = category_selector.options[category_selector.selectedIndex];
if (!selectedOption || !selectedOption.value) {
    alert("Please select a category to edit.");
    return;
}

const categoryId = selectedOption.value;
const categoryName = selectedOption.text;

modalTitle.textContent = "Edit category";
categoryForm.action = `/admin/category/update/${categoryId}/`;
categoryIdInput.value = categoryId;
categoryNameInput.value = categoryName;
categoryBtn.innerHTML = "Update category"
alertMessages.innerHTML = "";
categoryModal.show();
});

// --- отправка формы ---
categoryForm.addEventListener("submit", (event) => {
event.preventDefault();
const formData = new FormData(categoryForm);

fetch(categoryForm.action, {
    method: "POST",
    body: formData,
})
    .then((response) => response.json())
    .then((data) => {
    alertMessages.innerHTML = "";
    if (data.success) {
        if (categoryIdInput.value) {
        // update existing category
        const option = [...category_selector.options].find(
            (opt) => opt.value === categoryIdInput.value
        );
        if (option) option.text = data.category_name;
        } else {
        // add new category
        const new_op = document.createElement("option");
        new_op.value = data.category_id;
        new_op.textContent = data.category_name;
        category_selector.appendChild(new_op);
        }

        categoryModal.hide();
    } else {
        const msg = document.createElement("div");
        msg.classList.add("alert", "alert-danger");
        msg.innerHTML = data.error;
        alertMessages.appendChild(msg);
    }
    })
    .catch((error) => {
    alertMessages.innerHTML = "";
    const msg = document.createElement("div");
    msg.classList.add("alert", "alert-danger");
    msg.innerHTML = error.message || "Error while saving category";
    alertMessages.appendChild(msg);
    });
});