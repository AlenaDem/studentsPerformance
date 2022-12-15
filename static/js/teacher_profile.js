
const profile_state = {
    year: 2020,
    semester: 1,
    disciplineId: -1,
    groupId: -1,
    studentId: -1,
    grade: -1,
}

function init() {
    let yearSelectedBtn = document.getElementById("year-selected-btn");
    yearSelectedBtn.addEventListener("click", dateSelected);

    document.getElementById("select-semester").addEventListener("change", hideAll);
    document.getElementById("group-grades").style.display = "none";
};
init();

function hideAll() {
    document.getElementById("discipline-form").style.display = "none";
    document.getElementById("group-form").style.display = "none";
    document.getElementById("student-form").style.display = "none";
    document.getElementById("grade-form").style.display = "none";
    document.getElementById("group-grades").style.display = "none";
}

function dateSelected() {
    hideAll();
    profile_state.year = document.getElementById("input-year").value;
    semesterElement = document.getElementById("select-semester");
    profile_state.semester = semesterElement.options[semesterElement.selectedIndex].value;

    let url = '/disciplines_by_date?' + new URLSearchParams({
        year: profile_state.year,
        semester: profile_state.semester
    })

    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(fillDisciplines);
}

function fillSelect(select, data) {
    let newSelect = document.createElement('select');
    option = document.createElement('option');
    option.setAttribute('id', -1);
    option.appendChild(document.createTextNode("-"));
    newSelect.appendChild(option);

    for (let id in data) {
        option = document.createElement('option');
        option.setAttribute('id', id);
        option.appendChild(document.createTextNode(data[id]));
        newSelect.appendChild(option);
    }

    select.innerHTML = newSelect.innerHTML;
}

function fillDisciplines(disciplines) {
    let select = document.getElementById("discipline-select");
    select.removeEventListener("change", disciplineSelected);
    fillSelect(select, disciplines);
    select.addEventListener("change", disciplineSelected);

    document.getElementById("discipline-form").style.display = "block";
}

function disciplineSelected() {
    document.getElementById("group-grades").style.display = "none";

    let select = document.getElementById("discipline-select");
    let selectedId = select.options[select.options.selectedIndex].id;

    if (selectedId == -1) {
        document.getElementById("group-form").style.display = "none";
        document.getElementById("student-form").style.display = "none";
        document.getElementById("grade-form").style.display = "none";
        return
    }

    profile_state.disciplineId = selectedId;

    let url = '/discipline-groups?' + new URLSearchParams({
        discipline_id: profile_state.disciplineId,
        year: profile_state.year,
        semester: profile_state.semester
    })

    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(fillGroups);
}

function fillGroups(groups) {
    let select = document.getElementById("group-select");
    select.removeEventListener("change", groupSelected);
    fillSelect(select, groups);
    select.addEventListener("change", groupSelected);

    document.getElementById("group-form").style.display = "block";
}

function groupSelected() {
    let select = document.getElementById("group-select");
    let selectedId = select.options[select.options.selectedIndex].id;

    if (selectedId == -1) {
        document.getElementById("student-form").style.display = "none";
        document.getElementById("grade-form").style.display = "none";
        document.getElementById("group-grades").style.display = "none";
        return
    }

    profile_state.groupId = selectedId;
    loadGroupGrades();

    url = '/group-students?' + new URLSearchParams({
        group_id: profile_state.groupId
    })
    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(fillStudents);
}

function loadGroupGrades() {
    let url = '/load_group_grades?' + new URLSearchParams({
        group_id: profile_state.groupId,
        discipline_id: profile_state.disciplineId,
        year: profile_state.year,
        semester: profile_state.semester
    })

    fetch(url)
        .then(function (response) {
            return response.text();
        }).then(function (data) {
            let gradesBlock = document.getElementById("group-grades")
            gradesBlock.innerHTML = data
            gradesBlock.style.display = "block";
        });
}

function fillStudents(students) {
    let select = document.getElementById("student-select");
    select.removeEventListener("change", studentSelected);
    fillSelect(select, students);
    select.addEventListener("change", studentSelected);

    document.getElementById("student-form").style.display = "block";
}

function studentSelected() {
    let select = document.getElementById("student-select");
    let selectedId = select.options[select.options.selectedIndex].id;

    if (selectedId == -1) {
        document.getElementById("grade-form").style.display = "none";
        return
    }

    profile_state.studentId = selectedId;

    document.getElementById("grade-form").style.display = "block";
    document.getElementById("grade-btn").style.display = "block";
    document.getElementById("grade-btn").addEventListener("click", addGrade)
}

function addGrade() {
    let select = document.getElementById("grade-select");
    profile_state.grade = select.options[select.options.selectedIndex].value;

    fetch("/add_grade",
        {
            method: "POST",
            body: JSON.stringify(profile_state)
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            loadGroupGrades();
        })
}