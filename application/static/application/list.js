function deletePlant(event)
{
    event.stopPropagation();
    event.preventDefault();
    console.log("delete")
    openPopup()
}

function openPopup() {
    var popup = document.getElementById('customPopup');
    popup.style.display = 'block';
}

function closePopup() {
    var popup = document.getElementById('customPopup');
    popup.style.display = 'none';
}