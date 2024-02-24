document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("button-advance-clear").addEventListener("click", function(event) {
        event.preventDefault()

        document.getElementById("name").value = ""
        document.getElementById("scientific-name").value = ""
        document.getElementById("family-name").value = ""
        document.getElementById("common-name").value = ""
    })
})