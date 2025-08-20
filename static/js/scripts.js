document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.getElementById('edit-btn');
    const editForm = document.getElementById('edit-form');
    const cancelBtn = document.getElementById('cancel-btn');
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