document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    document
      .querySelector("#inbox")
      .addEventListener("click", () => load_mailbox("inbox"));
    document
      .querySelector("#sent")
      .addEventListener("click", () => load_mailbox("sent"));
    document
      .querySelector("#archived")
      .addEventListener("click", () => load_mailbox("archive"));
    document.querySelector("#compose").addEventListener("click", compose_email);
    document
      .querySelector("#compose-form")
      .addEventListener("submit", send_email);
  
    // By default, load the inbox
    load_mailbox("inbox");
  
    document.querySelectorAll(".email").addEventListener("click", function () {
      load_page(document.querySelectorAll(".email").querySelector("#id").value);
    });
  });