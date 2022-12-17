
$(document).ready(function () {
    $('.table').DataTable({
        paging: false,
        info: false,
        "language": {
          "emptyTable": "За данный семестр оценки отсутствуют",
          "search": "Поиск:",
          "zeroRecords": "Нет результатов, удовлетворяющих запросу",
        }
    });

});