function is_valid(li) {
  if (li.className.indexOf("toctree-l1") != -1) return true;
  if (li.className.indexOf("toctree-l2") != -1) return true;
  return false;
}

window.onload = function () {
  var lis = document.getElementsByTagName("li"),
    len = lis !== null ? lis.length : 0,
    i = 0;
  for (i; i < len; i++) {
    if (is_valid(lis[i])) lis[i].className += " current";
  }
  fetch(
    "https://raw.githubusercontent.com/reactonite/reactonite.github.io/master/versions.json"
  )
    .then((response) => response.json())
    .then((json) => {
      var sideNav = document.getElementsByClassName("wy-menu-vertical")[0];
      var versionTitle = document.createElement("p");
      versionTitle.className = "caption";
      versionTitle.innerHTML =
        "<span class='caption-text'>Docs Versions:</span>";
      sideNav.appendChild(versionTitle);
      var listUl = document.createElement("ul");
      listUl.style =
        "background: #c9c9c9; padding: 10px 0; font-weight: 400; font-size: 90%";
      var listElements = "";
      json.forEach((element) => {
        listElements +=
          '<li><a style="color: #404040; background: #c9c9c9;" href="/' +
          element +
          '/index.html">' +
          element +
          "</a></li>";
      });
      listUl.innerHTML = listElements;
      sideNav.appendChild(listUl);
    });
};
