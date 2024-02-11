document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    document
      .querySelector("#dashboard")
      .addEventListener("click", () => load_dashboard());
    document
      .querySelector("#create")
      .addEventListener("click", () => load_create());
    document
      .querySelector("#dashboard-plant-list")
      .addEventListener("click", () => load_plant_list());
    document
      .querySelector("#dashboard-letter-index-list")
      .addEventListener("click", () => load_letter_index_list());
    document
      .querySelector("#dashboard-family-index-list")
      .addEventListener("click", () => load_family_index_list());
  
    // By default, load the inbox
    load_dashboard();
    load_plant_list()
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

function load_plant_list(){
  document.querySelector("#plant-list-view").style.display = "block";
  document.querySelector("#letter-index-list-view").style.display = "none";
  document.querySelector("#family-index-list-view").style.display = "none";
}

function load_letter_index_list(){
  document.querySelector("#plant-list-view").style.display = "none";
  document.querySelector("#letter-index-list-view").style.display = "block";
  document.querySelector("#family-index-list-view").style.display = "none";
}

function load_family_index_list()
{
  document.querySelector("#plant-list-view").style.display = "none";
  document.querySelector("#letter-index-list-view").style.display = "none";
  document.querySelector("#family-index-list-view").style.display = "block";
}