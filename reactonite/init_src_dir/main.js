function toggleNavBar() {
  var navbar = document.getElementById("navbar-collapse");
  if (navbar.classList.contains("show")) {
    navbar.classList.remove("show");
  } else {
    navbar.classList.add("show");
  }
}

document
  .getElementsByClassName("navbar-toggle")[0]
  .addEventListener("click", toggleNavBar);
