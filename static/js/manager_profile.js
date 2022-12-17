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

function openStudentForEdit(id) {
    fetch("/edit_student_form/" + id,
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

    let fn = document.getElementById('first-name-input').value
    let ln = document.getElementById('last-name-input').value
    let patronymic = document.getElementById('patronymic-input').value
    let year = document.getElementById('year-input').value
    let groupId = document.getElementById('group-select').value

    const data = {
        id: id,
        first_name: fn,
        last_name: ln,
        patronymic: patronymic,
        year: year,
        group_id: groupId
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

function openStudentForCreate() {
    fetch("/create_student_form",
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

function createStudent() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity())
        return

    let fn = document.getElementById('first-name-input').value
    let ln = document.getElementById('last-name-input').value
    let patronymic = document.getElementById('patronymic-input').value
    let year = document.getElementById('year-input').value
    let groupId = document.getElementById('group-select').value

    let login = document.getElementById('login-input').value
    let password = document.getElementById('pass-input').value

    const data = {
        first_name: fn,
        last_name: ln,
        patronymic: patronymic,
        year: year,
        group_id: groupId,
        login: login,
        password: password
    }

    fetch("/create_student",
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