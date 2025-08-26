document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-btn').forEach(function(editBtn) {
        editBtn.addEventListener('click', function() {
            const container = editBtn.closest('.editable-block');
            const form = container.querySelector('.edit-form');
            if (form) {
                form.style.display = 'block';
                editBtn.style.display = 'none';
            }
        });
    });

    document.querySelectorAll('.cancel-btn').forEach(function(cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            const container = cancelBtn.closest('.editable-block');
            const form = container.querySelector('.edit-form');
            const editBtn = container.querySelector('.edit-btn');
            if (form && editBtn) {
                form.style.display = 'none';
                editBtn.style.display = 'inline-block';
            }
        });
    });
        // AJAX отправка формы
    document.querySelectorAll('.edit-form').forEach(function(editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(editForm);
            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const container = editForm.closest('.editable-block');
                if (data.success) {
                    // Найти ближайший блок с контентом и заменить его содержимое
                    const contentBlock = container.querySelector('.page-content-block');
                    if (contentBlock) {
                        contentBlock.innerHTML = data.content;
                    }
                    editForm.style.display = 'none';
                    const editBtn = container.querySelector('.edit-btn');
                    if (editBtn) editBtn.style.display = 'inline-block';
                } else if (data.errors) {
                    alert("Ошибка при сохранении контента. Пожалуйста, проверьте форму.");
                }
            });
        });
    });
});