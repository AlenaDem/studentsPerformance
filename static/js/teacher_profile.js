
const groupGradeMode = {
    GRADES: 0,
    UNDERACHIEVING: 1
}

const profile_state = {
    year: 2020,
    semester: 1,
    disciplineId: -1,
    groupId: -1,
    studentId: -1,
    grade: -1,
    mode: groupGradeMode.GRADES
}

function init() {
    let yearSelectedBtn = document.getElementById("year-selected-btn");
    yearSelectedBtn.addEventListener("click", dateSelected);

    document.getElementById("select-semester").addEventListener("change", hideAll);
    document.getElementById("group-grades").style.display = "none";

    setGroupGradesMode(groupGradeMode.GRADES)
    setGradesBlockEnabled(false)
};
init();

function setGroupGradesMode(mode) {
    if (mode == groupGradeMode.UNDERACHIEVING) {
        profile_state.mode = mode
        document.getElementById("group-grades-block").style.display = "none";
        document.getElementById("underachieving-block").style.display = "block";
    }
    else if (mode == groupGradeMode.GRADES) {
        profile_state.mode = mode
        document.getElementById("group-grades-block").style.display = "block";
        document.getElementById("underachieving-block").style.display = "none";
    }
}

function setGradesBlockEnabled(enable) {
    if (enable)
        document.getElementById("group-grades").style.display = "block";
    else
        document.getElementById("group-grades").style.display = "none";
}

function showUnderachievingStudents() {
    setGroupGradesMode(groupGradeMode.UNDERACHIEVING)
}

function showGrades() {
    setGroupGradesMode(groupGradeMode.GRADES)
}

function hideAll() {
    document.getElementById("discipline-form").style.display = "none";
    document.getElementById("group-form").style.display = "none";
    document.getElementById("student-form").style.display = "none";
    document.getElementById("grade-form").style.display = "none";
    document.getElementById("group-grades").style.display = "none";
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
  }

  function validateGrade(inputID) {
    const input = document.getElementById(inputID);
    const validityState = input.validity;
  
    if (validityState.valueMissing) {
      input.setCustomValidity('Пожалуйста, заполните поле');
    } else if (validityState.rangeUnderflow) {
      input.setCustomValidity('Введите значение от 1');
    } else if (validityState.rangeOverflow) {
      input.setCustomValidity('Введите год до 5');
    } else if (validityState.stepMismatch) {
        input.setCustomValidity('Максимально доступная точность 0.01');
    } 
    else {
      input.setCustomValidity('');
    }
  }

function dateSelected() {
    let form = document.getElementById('edit-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }
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
    document.getElementById("student-form").style.display = "none";
    document.getElementById("grade-form").style.display = "none";

    let select = document.getElementById("discipline-select");
    let selectedId = select.options[select.options.selectedIndex].id;

    if (selectedId == -1) {
        document.getElementById("group-form").style.display = "none";
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
    document.getElementById("grade-form").style.display = "none";
    document.getElementById("group-grades").style.display = "none";

    let select = document.getElementById("group-select");
    let selectedId = select.options[select.options.selectedIndex].id;

    if (selectedId == -1) {
        document.getElementById("student-form").style.display = "none";
        return
    }

    profile_state.groupId = selectedId;
    loadGroupGrades();
    loadUnderachievingStudents();

    url = '/group-students?' + new URLSearchParams({
        group_id: profile_state.groupId
    })
    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(fillStudents);
}

function loadUnderachievingStudents() {
    let form = document.getElementById('underachieving-form')
    if (!form.checkValidity()) {
        form.reportValidity()
        return
    }

    let grade = document.getElementById('grade-input').value
    let url = '/load_underachieving_students?' + new URLSearchParams({
        group_id: profile_state.groupId,
        grade: grade,
        discipline_id: profile_state.disciplineId,
        year: profile_state.year,
        semester: profile_state.semester
    })

    fetch(url)
        .then(function (response) {
            return response.text();
        }).then(function (data) {
            let gradesBlock = document.getElementById("underachieving-content")
            gradesBlock.innerHTML = data
            setGradesBlockEnabled(true);
        });
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
            let gradesBlock = document.getElementById("group-grades-block")
            gradesBlock.innerHTML = data
            setGradesBlockEnabled(true);
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
            loadUnderachievingStudents();
        })
}