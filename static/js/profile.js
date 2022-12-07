fetch('/profile-data')
      .then(function (response) {
          return response.json();
      }).then(function (data) {
          let years = data["years"]
          console.log(years)
      });