document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.getElementByClass('edit-btn');
    const editForm = document.getElementByClass('edit-form');
    const cancelBtn = document.getElementByClass('cancel-btn');
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            editForm.style.display = 'block';
            editBtn.style.display = 'none';
        });
    }
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            editForm.style.display = 'none';
            editBtn.style.display = 'inline-block';
        });
    }
});