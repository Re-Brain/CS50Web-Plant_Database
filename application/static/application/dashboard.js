document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    document
      .querySelector("#dashboard")
      .addEventListener("click", () => load_dashboard());
    document
      .querySelector("#create")
      .addEventListener("click", () => load_create());
  
    // By default, load the inbox
    load_dashboard();
  });

function load_dashboard() {
    // Show compose view and hide other views
    document.querySelector("#dashboard-view").style.display = "block";
    document.querySelector("#create-view").style.display = "none";
}

function load_create() {
    // Show compose view and hide other views
    document.querySelector("#dashboard-view").style.display = "none";
    document.querySelector("#create-view").style.display = "block";
}