function disciplineSelected() {
    let select = document.getElementById("exampleSelect1")
    console.log(select.options[select.options.selectedIndex].id)

    fetch("/discipline-groups")
      .then(function (response) {
          return response.json();
      }).then(function (data) {
        console.log(data)
      });
}