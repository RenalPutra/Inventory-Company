const body = document.body;
const darkLight = document.getElementById("darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");

// Tambahkan event listener untuk tombol Sidebar
sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));
sidebarClose.addEventListener("click", () => {
  sidebar.classList.add("close", "hoverable");
});
sidebarExpand.addEventListener("click", () => {
  sidebar.classList.remove("close", "hoverable");
});
sidebar.addEventListener("mouseenter", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
});
sidebar.addEventListener("mouseleave", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
});

// Tambahkan event listener untuk tombol Dark/Light mode
darkLight.addEventListener("click", () => {
  body.classList.toggle("dark-theme");
  if (body.classList.contains("dark-theme")) {
    darkLight.classList.replace("bx-sun", "bx-moon");
    localStorage.setItem("theme", "dark-theme");
  } else {
    darkLight.classList.replace("bx-moon", "bx-sun");
    localStorage.setItem("theme", "light-theme");
  }
});

// Set tema berdasarkan local storage saat halaman dimuat
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  body.classList.add(savedTheme);
  if (savedTheme === "dark-theme") {
    darkLight.classList.replace("bx-sun", "bx-moon");
  }
}
