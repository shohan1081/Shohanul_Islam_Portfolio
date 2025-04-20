document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.querySelector("#hamburger");
    const menu = document.querySelector("#menu");
  
    hamburger.addEventListener("click", () => {
      menu.classList.toggle("hidden");
      hamburger.classList.toggle("bg-white");
    });
  });
  
  function showTab(tab) {
    document
      .querySelectorAll(".tab-content")
      .forEach((el) => el.classList.add("hidden"));
    document
      .querySelectorAll(".tab-btn")
      .forEach((el) => el.classList.remove("border-blue-500"));
    document.getElementById(tab).classList.remove("hidden");
    document.getElementById(tab + "-tab").classList.add("border-blue-500");
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    showTab("skill");
  });
  