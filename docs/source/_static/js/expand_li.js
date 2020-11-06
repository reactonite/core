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
};
