/* The rows of a class page's Usage table (html-multi/browser/browser_classinfo.html),
   built from USAGE, which usage.js next to the pages defines (usage_js() in
   viz_html_multi.py): a group of rows for each class in the table's data-groups, its
   name, then its properties. Written once rather than repeated on every class page
   (backlog #21). */

(function() {
  var data = window.USAGE;
  var table = document.getElementById("usage-table");
  if (!data || !table) return;
  var escape = function(s) {
    return String(s).replace(/[&<>"']/g, function(c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
    });
  };
  var link = function(page, title, qname, css) {
    return '<a title="' + escape(qname) + '" href="' + escape(page) + '.html" class="' + css + '">' +
      escape(title) + '</a>';
  };
  var html = "";
  table.getAttribute("data-groups").split(" ").forEach(function(id) {
    var group = data.groups[id];
    if (!group) return;
    html += '<tr class="table-inheritanceinfo"><th colspan="4" class="treeinfo">' +
      '<span class="label label-default">From class ' +
      link(group[2], group[0], group[1], "fromclass_link") + '</span></th></tr>';
    group[3].forEach(function(pid) {
      var p = data.props[pid];
      if (!p) return;
      var ranges = p[5].length ? p[5].map(function(r) {
        return r[0] != null ? link(r[0], r[1], r[2], "rdfclass") : "<i>" + escape(r[1]) + "</i>";
      }).join(" ") : "<i>owl:Thing</i>";
      html += '<tr><td class="firsttd">' + link(p[2], p[0], p[1], "propcolor") + '</td>' +
        '<td class="secondtd"><i>' + escape(p[3] || "") + '</i></td>' +
        '<td class="thirdtd"><span>' + escape(p[4]) + '</span></td>' +
        '<td class="fourthtd">' + ranges + '</td></tr>';
    });
  });
  table.querySelector("tbody").insertAdjacentHTML("beforeend", html);
})();
