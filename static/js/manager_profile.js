function managerProfileInit() {

};
managerProfileInit();

function loadStudents() {
    let url = '/student_list'
    fetch(url)
        .then(function (response) {
            return response.text();
        })
        .then(function (html) {
            let view = document.getElementById("view")
            view.innerHTML = html

            $('.table').DataTable({
                paging: false,
                info: false,
                "language": {
                    "emptyTable": "Студенты не найдены",
                    "search": "Поиск:",
                    "zeroRecords": "Нет результатов, удовлетворяющих запросу",
                }
            });
        });
}

function openStudent(id) {
    fetch("/student/" + id,
        {
            method: "GET"
        })
        .then(function (response) {
            return response.text();
        })
        .then(function (html) {
            let view = document.getElementById("view")
            view.innerHTML = html
        });
}

function editStudent(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity())
        return

    let fn = document.getElementById('first-name').value
    let ln = document.getElementById('last-name').value

    const data = {
        id: id,
        first_name: fn,
        last_name: ln
    }

    fetch("/edit_student",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) { 
            console.log(res.status)
            loadStudents()
        })
}

function deleteStudent(id) {
    fetch("/delete_student/" + id,
        {
            method: "DELETE"
        })
        .then(function (response) {
            if (response.status == 200)
                loadStudents()
        })
}