//goals
var goals = [];
//courses
var courses = [];
fetch('/get_all_goals')
    .then(response => response.json())
    .then(data => {
        goals = data.content;
        const dropdown = document.getElementById('goaldd');
        data.content.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = goals.indexOf(option);
            optionElement.textContent = "[" + option.degreeName + " " + option.degreeLevel + "] " + option.goalCode;
            dropdown.appendChild(optionElement);
        });

        fetch('/get_all_courses')
            .then(response => response.json())
            .then(data => {
                courses = data.content;
                const dropdown = document.getElementById('coursedd');
                data.content.forEach(option => {
                    const optionElement = document.createElement('option');
                    optionElement.value = courses.indexOf(option);
                    optionElement.textContent = option.courseID + " " + option.courseName;
                    dropdown.appendChild(optionElement);
                });

                fetch('/get_all_goal_courses')
                    .then(response => response.json())
                    .then(data => {
                        const div = document.getElementById('degreeCourses');
                        data.content.forEach(option => {
                            const pElement = document.createElement('p');
                            pElement.classList.add('bordered');
                            pElement.textContent = "[" + option.goalCode + " " + option.degreeName + " " + option.degreeLevel + "] " + option.courseID;
                            div.appendChild(pElement);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            })
            .catch(error => console.error('Error:', error));
    })
    .catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const goalIndex = document.getElementById('goaldd').value;
    const courseIndex = document.getElementById('coursedd').value;
    const selectedGoal = goals[goalIndex];
    const selectedCourse = courses[courseIndex];
    
    const formData = new FormData();
    formData.append('goal', JSON.stringify(selectedGoal));
    formData.append('course', JSON.stringify(selectedCourse));
    
    fetch('/gcinput/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = (data.success == 1) ? "Goal-Course Successfully Linked" : "Goal-Course Already Linked";
    })
    .catch(error => console.error('Error:', error));
});