// Automatically fade and remove alert after 3 seconds
setTimeout(function() {
  const alertBox = document.querySelector('.alert');
  if (alertBox) {
    alertBox.style.opacity = '0';
    setTimeout(() => alertBox.remove(), 500);
  }
}, 3000);

let deleteUrl = null;

    function openDeleteModal(button) {
      deleteUrl = button.getAttribute("data-url");
      document.getElementById("deleteModal").style.display = "flex";
      document.getElementById("confirm-delete").onclick = confirmDelete;
    }

    function closeDeleteModal() {
      document.getElementById("deleteModal").style.display = "none";
    }

    function showFlashMessage(msg) {
      const flashBox = document.getElementById('flash-message');
      flashBox.textContent = msg;
      flashBox.style.display = 'block';
      flashBox.style.opacity = '1';

      setTimeout(() => {
        flashBox.style.opacity = '0';
        setTimeout(() => {
          flashBox.style.display = 'none';
        }, 500);
      }, 3000);
    }

    function confirmDelete() {
      if (deleteUrl !== null) {
        fetch(deleteUrl, {
          method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showFlashMessage(data.message);
            closeDeleteModal();
            const updateId = deleteUrl.split('/').pop();
            const element = document.getElementById('update-' + updateId);
            if (element) element.remove();
          } else {
            showFlashMessage('Error: ' + data.message);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          showFlashMessage('Unexpected error occurred');
        });
      }
    }