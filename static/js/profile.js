fetch('/profile-data')
      .then(function (response) {
          return response.json();
      }).then(function (data) {
          let years = data["years"]
          console.log(years)
      });

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