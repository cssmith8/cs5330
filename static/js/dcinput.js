var degrees = [];
var courses = [];
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

                fetch('/get_all_degree_courses')
                    .then(response => response.json())
                    .then(data => {
                        const div = document.getElementById('degreeCourses');
                        data.content.forEach(option => {
                            const pElement = document.createElement('p');
                            pElement.classList.add('bordered');
                            pElement.textContent = option.degreeName + " " + option.degreeLevel + ": " + option.courseID + " (Is Core: " + option.isCore + ")";
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
    const degreeIndex = document.getElementById('degreedd').value;
    const courseIndex = document.getElementById('coursedd').value;
    const selectedDegree = degrees[degreeIndex];
    const selectedCourse = courses[courseIndex];
    const isCore = document.getElementById('isCore').checked;
    
    const formData = new FormData();
    formData.append('degree', JSON.stringify(selectedDegree));
    formData.append('course', JSON.stringify(selectedCourse));
    formData.append('isCore', isCore);
    
    fetch('/dcinput/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = (data.success == 1) ? "Degree-Course Successfully Linked" : "Degree-Course Already Linked";
    })
    .catch(error => console.error('Error:', error));
});