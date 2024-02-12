function deletePlant(event, plantID)
{
    event.stopPropagation();
    event.preventDefault();
    openPopup(plantID)
}

function openPopup(plantID) {
    let popup = document.getElementById('customPopup');
    let confirm = document.getElementById('confirm')

    popup.style.display = 'block';
    confirm.setAttribute('data-plant-id', plantID);
}

function closePopup() {
    var popup = document.getElementById('customPopup');
    popup.style.display = 'none';
}

function confirmDelete()
{ 
    let popup = document.getElementById('customPopup');
    let id = document.getElementById("confirm").getAttribute("data-plant-id");
    const csrfToken = getCookie('csrftoken')

    popup.style.display = 'none';

    fetch(`deletePlant/${id}`, {
        method : 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (response.ok) {
            console.log('Item deleted successfully');
            location.reload();
        } else {
            console.error('Failed to delete item');
        }
    })
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}