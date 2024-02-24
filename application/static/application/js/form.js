function deleteImage(dataBack, dataFront)
{
    let frontImage = document.getElementById(dataFront)
    let frontImageParent = frontImage.parentNode
    frontImageParent.removeChild(frontImage)

    let backImage = document.getElementById(dataBack)
    let backImageParent = backImage.parentNode
    backImageParent.removeChild(backImage)
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

    if (numberOfChildren >= 2)
    {
        let deleteName = document.getElementById(deleteButtonID)
        deleteName.style.display = 'block'
    }  
}

function deleteName(event, inputContainer, deleteButtonID)
{
    event.preventDefault();

    let container = document.getElementById(inputContainer)
    let lastChild = container.lastElementChild
    
    container.removeChild(lastChild)

    let numberOfChildren = container.children.length
    console.log(numberOfChildren)

    if (numberOfChildren == 3)
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

        imageContainer.className = "container-file-item"

        name.className = "mt-1 create-label"
        name.textContent = input.files[i].name

        deleteButton.className = "btn btn-primary btn-sm ms-1 delete-button"
        deleteButton.type = "button";
        deleteButton.innerHTML = "ลบรูปภาพ"

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

