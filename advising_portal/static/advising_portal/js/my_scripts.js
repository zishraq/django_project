function table_search(colspan) {
    var input, filter, table, tr, td, i, text_value;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        if (i === 0) {
            continue;
        }
        td = tr[i].getElementsByTagName("td")[0];

        if (td && td.colSpan !== colspan) {
            text_value = td.textContent || td.innerText;
            if (text_value.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
