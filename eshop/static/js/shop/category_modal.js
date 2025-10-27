
const categoryForm = document.getElementById("add_category");
const categoryModalEl = document.getElementById("categoryModal");
const categoryModal = new bootstrap.Modal('#categoryModal');
const alertMessages = document.getElementById("alertMessages");

const modalTitle = categoryModalEl.querySelector(".modal-title");
const categoryIdInput = document.getElementById("id_category_id");
const categoryNameInput = document.getElementById("id_category_name");
const categoryBtn = document.getElementById("category_btn");
const btnAdd = document.getElementById("btnAddCategory");
const categoryTable = document.getElementById("categoryTable");

// Open modal for adding
btnAdd.addEventListener("click", () => {
modalTitle.textContent = "Add category";
categoryForm.action = "/admin/category/add/";
categoryIdInput.value = "";
categoryNameInput.value = "";
categoryBtn.innerHTML = "Add category";
alertMessages.innerHTML = "";
});

// Open form for editing
document.querySelectorAll(".btn-edit-category").forEach((button) => {
button.addEventListener("click", () => {
    const categoryId = button.dataset.id;
    const categoryName = button.dataset.name;

    modalTitle.textContent = "Edit category";
    categoryForm.action = `/admin/category/update/${categoryId}/`;
    categoryIdInput.value = categoryId;
    categoryNameInput.value = categoryName;
    categoryBtn.innerHTML = "Update category";
    alertMessages.innerHTML = "";

    categoryModal.show();
});
});

// Send form
categoryForm.addEventListener("submit", (event) => {
event.preventDefault();
event.stopPropagation();

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
        // Update table line
        const row = categoryTable.querySelector(`.btn-edit-category[data-id='${categoryIdInput.value}']`)
            .closest("tr");
        if (row) {
            row.querySelector(".text-start a").textContent = data.category_name;
            row.querySelector(".btn-edit-category").dataset.name = data.category_name;
        }
        } else {
        // Add new row
        const currentRows = categoryTable.querySelectorAll("tr").length;
        if (currentRows >= 30) {
            categoryModal.hide();
            return;
        }
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td class="text-start">
            <a href="/shop/category/${data.category_id}/" class="text-decoration-none text-dark">
                ${data.category_name}
            </a>
            </td>
            <td>0</td>
            <td>0</td>
            <td>
            <div class="btn-group">
                <button type="button" class="btn btn-primary btn-sm rounded me-2 btn-edit-category"
                        data-id="${data.category_id}"
                        data-name="${data.category_name}"
                        data-bs-toggle="modal"
                        data-bs-target="#categoryModal">
                <i class="bi bi-pencil"></i> Update
                </button>
                <form action="/admin/category/delete/${data.category_id}/" method="post"
                    onsubmit="return confirm('Are you sure you want to delete category: ${data.category_name}?');">
                <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                <button type="submit" class="btn btn-danger btn-sm rounded">
                    <i class="bi bi-trash"></i> Delete
                </button>
                </form>
            </div>
            </td>
        `;
        categoryTable.appendChild(newRow);

        // Add handler to the new edit button
        const newEditBtn = newRow.querySelector(".btn-edit-category");
        newEditBtn.addEventListener("click", () => {
            modalTitle.textContent = "Edit category";
            categoryForm.action = `/admin/category/update/${data.category_id}/`;
            categoryIdInput.value = data.category_id;
            categoryNameInput.value = data.category_name;
            categoryBtn.innerHTML = "Update category";
            alertMessages.innerHTML = "";
            categoryModal.show();
        });
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