window.onload = function () {
  var lis = document.getElementsByTagName("li"),
    len = lis !== null ? lis.length : 0,
    i = 0;
  for (i; i < len; i++) {
    lis[i].className += " current";
  }
};
