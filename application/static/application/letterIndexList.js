document.addEventListener("DOMContentLoaded", function () {
    generateThaiAlphabetButtons();
    generateAlphabetButtons();
    checkButton();
});

function generateAlphabetButtons() {
    var buttonContainer = document.getElementById('eng-button-container')
    
    createButtons(buttonContainer, 65 ,90)
}

function generateThaiAlphabetButtons() {
    var buttonContainer = document.getElementById('thai-button-container');

    createButtons(buttonContainer, 0xE01 , 0xE2E)
}

function createButtons(buttonContainer, min , max)
{
    for (var i = min; i <= max; i++) { // ASCII values for 'a' to 'z'
        let letter = String.fromCharCode(i)
        let button = document.createElement('a')
        let indexList = document.getElementById('button-container').getAttribute('data-django-variable')
        button.textContent = letter;
  
        let charlist = []
  
        if (indexList != "all")
        {
          if (indexList.length == 1)
          {
              charlist.push(indexList)
          }
          else
          {
              charlist = indexList.split('+')
          }
        }
  
        if (charlist.includes(letter))
        {
          button.className = 'btn btn-success mr-2 m-1' // Bootstrap button styling
        }
        else
        {
          button.className = 'btn btn-primary mr-2 m-1' // Bootstrap button styling
        }
       
        button.addEventListener("click", function () {
          if(charlist.includes(letter))
          {
              if(charlist.length == 1)
              {
                  button.href = "all"
              }
              else
              {
                  let newList = charlist.filter(function(element) {
                      return element !== letter
                  })
                  newList.sort()
                  button.href = newList.join('+')
              }
          }
          else
          {
              if(charlist.length == 0)
              {
                  button.href = letter
              }
              else
              {
                  charlist.push(letter)
                  charlist.sort()
                  charlist = charlist.join('+')
                  button.href = charlist
              }
          }
        })
  
        buttonContainer.appendChild(button)
      }
}