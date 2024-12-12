var goals = [];
var courses = [];
var degrees = [];
fetch('/get_all_degrees')
    .then(response => response.json())
    .then(data => {
        degrees = data.content;
        const dropdown = document.getElementById('degreedd');
        data.content.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = degrees.indexOf(option);
            optionElement.textContent = option.degreeName + " " + option.degreeLevel;
            dropdown.appendChild(optionElement);
        });
    })
    .catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const degreeIndex = document.getElementById('degreedd').value;
    const selectedDegree = degrees[degreeIndex];
    
    const formData = new FormData();
    formData.append('degree', JSON.stringify(selectedDegree));
    
    fetch('/selectdegree/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        courses = data.courses;
        const associatedCourses = document.getElementById('associatedCourses');
        //clear the previous courses
        associatedCourses.innerHTML = "";
        //if no courses are associated with the degree
        if (courses.length == 0) {
            const courseElement = document.createElement('p');
            courseElement.textContent = "No courses associated with this degree";
            associatedCourses.appendChild(courseElement);
        }
        courses.forEach(course => {
            const courseElement = document.createElement('p');
            courseElement.classList.add('bordered');
            courseElement.textContent = course.courseID + ", Core: " +  ((course.isCore == 1) ? "Yes" : "No");
            associatedCourses.appendChild(courseElement);
        });
        goals = data.goals;
        const associatedGoals = document.getElementById('associatedGoals');
        const goaldd = document.getElementById('goaldd');
        //clear the previous goals
        associatedGoals.innerHTML = "";
        //if no goals are associated with the degree
        if (goals.length == 0) {
            const goalElement = document.createElement('p');
            goalElement.textContent = "No goals associated with this degree";
            associatedGoals.appendChild(goalElement);
        }
        goals.forEach(goal => {
            const goalElement = document.createElement('p');
            goalElement.classList.add('bordered');
            goalElement.textContent = goal.goalCode + ", " + goal.description;
            associatedGoals.appendChild(goalElement);

            const optionElement = document.createElement('option');
            optionElement.value = goals.indexOf(goal);
            optionElement.textContent = goal.goalCode + ", " + goal.description;
            goaldd.appendChild(optionElement);
        });
        
    })
    .catch(error => console.error('Error:', error));
});

//goals
document.getElementById('dataForm2').addEventListener('submit', function(event) {
    event.preventDefault();
    const goalIndex = document.getElementById('goaldd').value;
    const selectedGoal = goals[goalIndex];
    
    const formData = new FormData();
    formData.append('goal', JSON.stringify(selectedGoal));
    
    fetch('/selectdegree/form2', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        courses = data.courses;
        const associatedCourses2 = document.getElementById('associatedCourses2');
        //clear the previous courses
        associatedCourses2.innerHTML = "";
        //if no courses are associated with the goal
        if (courses.length == 0) {
            const courseElement = document.createElement('p');
            courseElement.textContent = "No courses associated with this goal";
            associatedCourses2.appendChild(courseElement);
        } else {
            const courseElement = document.createElement('p');
            courseElement.textContent = "Courses associated with this goal:";
            associatedCourses2.appendChild(courseElement);
        }
        courses.forEach(course => {
            const courseElement = document.createElement('p');
            courseElement.classList.add('bordered');
            courseElement.textContent = course.courseID + " " +  course.courseName;
            associatedCourses2.appendChild(courseElement);
        });
    })
    .catch(error => console.error('Error:', error));
});

//sections
document.getElementById('dataForm3').addEventListener('submit', function(event) {
    event.preventDefault();
    const degreeIndex = document.getElementById('degreedd').value;
    const selectedDegree = degrees[degreeIndex];

    const formData = new FormData();
    formData.append('degree', JSON.stringify(selectedDegree));
    formData.append('startSemester', document.getElementById('startSemester').value);
    formData.append('startYear', document.getElementById('startYear').value);
    formData.append('endSemester', document.getElementById('endSemester').value);
    formData.append('endYear', document.getElementById('endYear').value);

    fetch('/selectdegree/form3', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        sections = data.sections;
        const associatedSections = document.getElementById('sections');
        //clear the previous courses
        associatedSections.innerHTML = "";
        if (sections.length == 0) {
            const sectionElement = document.createElement('p');
            sectionElement.textContent = "No matching sections found";
            associatedSections.appendChild(sectionElement);
        } else {
            sections.forEach(section => {
                const sectionElement = document.createElement('p');
                sectionElement.classList.add('bordered');
                sectionElement.textContent = section.courseID + " " + section.sectionID + ", Semester: " +  section.semester + " " + section.year + " - Instructor ID: " + section.instructorID;
                associatedSections.appendChild(sectionElement);
            });
        }    
    })
    .catch(error => console.error('Error:', error));
});