function managerProfileInit() {

};
managerProfileInit();

function hideStatus() {
    let holder = document.getElementById("status-holder")
    if (!holder)
        return
    holder.style.display = "none"
}

function setSuccess(msg) {
    let holder = document.getElementById("status-holder")
    if (!holder)
        return
    holder.innerHTML = '<div class="alert alert-success">\n<strong>Успешно!</strong> ' + msg + '\n</div>'
    holder.style.display = "block"
}

function setError(msg) {
    let holder = document.getElementById("status-holder")
    if (!holder)
        return
    holder.innerHTML = '<div class="alert alert-warning">\n<strong>Ошибка!</strong> ' + msg + '\n</div>'
    holder.style.display = "block"
}

//
// Студенты
//
function loadStudents() {
    hideStatus()

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

function validateYear(inputID) {
    const input = document.getElementById(inputID);
    const validityState = input.validity;
  
    if (validityState.valueMissing) {
      input.setCustomValidity('Пожалуйста, заполните год');
    } else if (validityState.rangeUnderflow) {
      input.setCustomValidity('Введите год от 2000');
    } else if (validityState.rangeOverflow) {
      input.setCustomValidity('Введите год до 2022');
    } else {
      input.setCustomValidity('');
    }
  
    input.reportValidity();
}

function validateText(inputID) {
    const input = document.getElementById(inputID);
    const validityState = input.validity;
  
    if (validityState.valueMissing) {
      input.setCustomValidity('Пожалуйста, заполните поле');
    } else if (validityState.patternMismatch || validityState.rangeOverflow || validityState.rangeUnderflow || validityState.tooLong || validityState.tooShort || validityState.typeMismatch || validityState.badInput) {
      input.setCustomValidity('Пожалуйста, введите корректное значение для поля');
    } else {
      input.setCustomValidity('');
    }
  
    input.reportValidity();
}

function editStudent(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

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
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

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
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

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
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadStudents()
        })
}

function deleteStudent(id) {
    fetch("/delete_student/" + id,
        {
            method: "DELETE"
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadStudents()
        })
}


//
// Преподаватели
//
function loadTeachers() {
    hideStatus()

    let url = '/teacher_list'
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
                    "emptyTable": "Преподаватели не найдены",
                    "search": "Поиск:",
                    "zeroRecords": "Нет результатов, удовлетворяющих запросу",
                }
            });
        });
}

function openTeacherForEdit(id) {
    fetch("/edit_teacher_form/" + id,
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

function editTeacher(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let fn = document.getElementById('first-name-input').value
    let ln = document.getElementById('last-name-input').value
    let patronymic = document.getElementById('patronymic-input').value

    const data = {
        id: id,
        first_name: fn,
        last_name: ln,
        patronymic: patronymic,
    }

    fetch("/edit_teacher",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadTeachers()
        })
}

function openTeacherForCreate() {
    fetch("/create_teacher_form",
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

function createTeacher() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let fn = document.getElementById('first-name-input').value
    let ln = document.getElementById('last-name-input').value
    let patronymic = document.getElementById('patronymic-input').value

    let login = document.getElementById('login-input').value
    let password = document.getElementById('pass-input').value

    const data = {
        first_name: fn,
        last_name: ln,
        patronymic: patronymic,
        login: login,
        password: password
    }

    fetch("/create_teacher",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadTeachers()
        })
}


//
// Специальности
//
function loadSpecialities() {
    hideStatus()

    let url = '/speciality_list'
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
                    "emptyTable": "Специальности не найдены",
                    "search": "Поиск:",
                    "zeroRecords": "Нет результатов, удовлетворяющих запросу",
                }
            });
        });
}

function openSpecialityForEdit(id) {
    fetch("/edit_speciality_form/" + id,
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

function editSpeciality(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value

    const data = {
        id: id,
        name: name
    }

    fetch("/edit_speciality",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadSpecialities()
        })
}

function openSpecialityForCreate() {
    fetch("/create_speciality_form",
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

function createSpeciality() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value

    const data = {
        name: name
    }

    fetch("/create_speciality",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadSpecialities()
        })
}


//
// Дисциплины
//
function loadDisciplines() {
    hideStatus()

    let url = '/discipline_list'
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
                    "emptyTable": "Дисциплины не найдены",
                    "search": "Поиск:",
                    "zeroRecords": "Нет результатов, удовлетворяющих запросу",
                }
            });
        });
}

function openDisciplineForEdit(id) {
    fetch("/edit_discipline_form/" + id,
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

function editDiscipline(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value

    const data = {
        id: id,
        name: name
    }

    fetch("/edit_discipline",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadDisciplines()
        })
}

function openDisciplineForCreate() {
    fetch("/create_discipline_form",
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

function createDiscipline() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value

    const data = {
        name: name
    }

    fetch("/create_discipline",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadDisciplines()
        })
}


//
// Группы
//
function loadGroups() {
    hideStatus()

    let url = '/group_list'
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
                    "emptyTable": "Группы не найдены",
                    "search": "Поиск:",
                    "zeroRecords": "Нет результатов, удовлетворяющих запросу",
                }
            });
        });
}

function openGroupForEdit(id) {
    fetch("/edit_group_form/" + id,
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

function editGroup(id) {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value
    let course = document.getElementById('course-input').value
    let specId = document.getElementById('spec-select').value

    const data = {
        id: id,
        name: name,
        course: course,
        spec_id: specId
    }

    fetch("/edit_group",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadGroups()
        })
}

function openGroupForCreate() {
    fetch("/create_group_form",
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

function createGroup() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let name = document.getElementById('name-input').value
    let course = document.getElementById('course-input').value
    let specId = document.getElementById('spec-select').value

    const data = {
        name: name,
        course: course,
        spec_id: specId
    }

    fetch("/create_group",
        {
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(function (res) {
            if (res.ok)
                res.text().then(msg => setSuccess(msg))
            else
                res.text().then(msg => setError(msg))

            loadGroups()
        })
}
