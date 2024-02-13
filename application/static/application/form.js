// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelector('#compose-form')
//     .addEventListener("submit", create)
// })

// function create(event)
// {
//     event.preventDefault()

//     let fromData = new FormData(this)

//     // let familyNameList = []
//     // let commonNameList  = []
//     // let qrImageList = []
//     // let plantImageList = []

//     // let name = document.getElementById("name").value
//     // let scientificName = document.getElementById("scientific-name").value
//     // let familyNames = document.querySelectorAll(".family-name")
//     // let commonNames = document.querySelectorAll(".common-name")
//     // let use = document.getElementById("use").value
//     // let characteristic = document.getElementById("characteristic").value
//     // let distribution = document.getElementById("distribution").value
//     // let habitat = document.getElementById("habitat").value
//     // let location = document.getElementById("location").value
//     // let reference = document.getElementById("reference").value
//     // let qrImages = document.getElementById("qr-input")
//     // let plantImages = document.getElementById("image-input")

//     // const files = plantImages.files

//     // const promises = Array.from(files).map(file => readAndSendFile(file));

//     // for(let i = 0; i < familyNames.length; i++)
//     // {
//     //     familyNameList.push(familyNames[i].value)
//     // }

//     // for(let i = 0; i < commonNames.length; i++)
//     // {
//     //     commonNameList.push(commonNames[i].value)
//     // }

//     // for(let i = 0; i < qrImages.files.length; i++)
//     // {
//     //     qrImageList.push(qrImages.files[i])
//     // }

//     // for(let i = 0; i < plantImages.files.length; i++)
//     // {
//     //     plantImageList.push(plantImages.files[i])
//     // }

//     // console.log(plantImageList)

//     fetch('create', {
//         method : "POST",
//         body: FormData
//         // JSON.stringify({
//         //     name : name,
//         //     scientificName : scientificName,
//         //     familyNameList : familyNameList,
//         //     commonNameList : commonNameList,
//         //     use : use,
//         //     characteristic : characteristic,
//         //     distribution : distribution,
//         //     habitat : habitat,
//         //     location : location,
//         //     reference : reference,
//         //     qrImageList : qrImageList,
//         //     plantImageList : plantImageList
//         // })
//     })
//     .then(response => {
//         if (response.ok) {
//             console.log('Item create successfully');
//         } else {
//             console.error('Failed to delete item');
//         }
//     })

// }

function deleteImage(id)
{
    let container = document.querySelector(`.plant-image-${id}`)
    let parent = container.parentNode
    parent.removeChild(container)

    fetch(`deleteImage/${id}`, {
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

function deleteQR(id)
{
    let container = document.querySelector(`.qr-image-${id}`)

    let parent = container.parentNode
    parent.removeChild(container)

    fetch(`deleteQR/${id}`, {
        method : 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (response.ok) {
            console.log('Item deleted successfully');
        } else {
            console.error('Failed to delete item');
        }
    })
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function addName(event, inputContainer, deleteButtonID, name)
{
    event.preventDefault();

    let container = document.getElementById(inputContainer)
    let input = document.createElement('input')
    input.type = "text"
    input.className = "form-control multipleInput"
    input.name = name

    container.appendChild(input)

    let numberOfChildren = container.children.length
    console.log(numberOfChildren)

    if (numberOfChildren > 2)
    {
        let deleteName = document.getElementById(deleteButtonID)
        deleteName.style.display = 'block'
    }  
}

function deleteName(event, inputContainer, deleteButtonID)
{
    event.preventDefault();

    let container = document.getElementById(inputContainer)

    let lastChild = container.lastChild
    container.removeChild(lastChild)

    let numberOfChildren = container.children.length
    console.log(numberOfChildren)

    if (numberOfChildren == 2)
    {
        let deleteName = document.getElementById(deleteButtonID)
        deleteName.style.display = 'none'
    }
}

function displayFileNames(containerElement, inputElement)
{
    let input = document.getElementById(inputElement)
    let fileContainer = document.getElementById(containerElement)

    fileContainer.innerHTML = '';

    for (let i = 0; i < input.files.length; i++)
    {
        let imageContainer = document.createElement("div")
        let name = document.createElement('p')
        let deleteButton = document.createElement('button')
        let icon = document.createElement('i')

        icon.className = "fa-solid fa-xmark"
        deleteButton.appendChild(icon)

        imageContainer.className = "container-file-item"

        name.className = "mt-1"
        name.textContent = input.files[i].name

        deleteButton.className = "btn btn-primary btn-sm ms-1"
        deleteButton.type = "button";

        let currentContainer = containerElement
        let currentInput = inputElement

        deleteButton.onclick = deleteHandler(i, currentContainer , currentInput)

        imageContainer.appendChild(name)
        imageContainer.appendChild(deleteButton)

        fileContainer.appendChild(imageContainer)
    }
}

function deleteHandler(index, containerElement , inputElement)
{ 
    return function()
    {
        let fileContainer = document.getElementById(inputElement)
        let fileList = Array.from(fileContainer.files)
    
        fileList.splice(index, 1)
    
        let newFileList = new DataTransfer();
    
        fileList.forEach(function(file){
            newFileList.items.add(file)
        })
    
        fileContainer.files = newFileList.files
    
        displayFileNames(containerElement , inputElement)
    }
}

