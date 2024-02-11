document.addEventListener("DOMContentLoaded", function () {
    generateThaiAlphabetButtons();
    generateAlphabetButtons();
    getData();
});

function getData()
{

}

function generateAlphabetButtons() {
    var buttonContainer = document.getElementById('eng-button-container');

    for (var i = 97; i <= 122; i++) { // ASCII values for 'a' to 'z'
      var letter = String.fromCharCode(i);
      var button = document.createElement('button');
      button.textContent = letter;
      button.className = 'btn btn-primary mr-2 m-1'; // Bootstrap button styling

      button.addEventListener('click', function()
      {
        toggleButtonColor(this);
      });

      buttonContainer.appendChild(button);
    }
}

function generateThaiAlphabetButtons() {
    var buttonContainer = document.getElementById('thai-button-container');

    for (var i = 0xE01; i <= 0xE2E; i++) { // Unicode values for 'ก' to 'ฮ'
      var letter = String.fromCharCode(i);
      var button = document.createElement('button');
      button.textContent = letter;
      button.className = 'btn btn-primary mr-2 m-1'; // Bootstrap button styling

      button.addEventListener('click', function()
      {
        toggleButtonColor(this);
      });

      buttonContainer.appendChild(button);
    }
}

function toggleButtonColor(button)
{
  button.classList.toggle('btn-primary');
  button.classList.toggle('btn-success');
}
