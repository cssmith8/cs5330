//instructors
var instructors = [];
//courses
var courses = [];
fetch('/get_all_instructors')
    .then(response => response.json())
    .then(data => {
        instructors = data.content;
        const dropdown = document.getElementById('instructordd');
        data.content.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = instructors.indexOf(option);
            optionElement.textContent = "[" + option.instructorID + "] " + option.instructorName;
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

                fetch('/get_all_sections')
                    .then(response => response.json())
                    .then(data => {
                        const div = document.getElementById('degreeCourses');
                        data.content.forEach(option => {
                            const pElement = document.createElement('p');
                            pElement.classList.add('bordered');
                            pElement.textContent = option.courseID + " " + option.sectionID + ": " +  option.semester + " " + option.year + " (" + option.numStudents + " students) - Instructor ID: " + option.instructorID
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
    const instructorIndex = document.getElementById('instructordd').value;
    const courseIndex = document.getElementById('coursedd').value;
    const selectedInstructor = instructors[instructorIndex];
    const selectedCourse = courses[courseIndex];
    const sectionID = document.getElementById('sectionID').value;
    const semester = document.getElementById('semester').value;
    const year = document.getElementById('year').value;
    const numStudents = document.getElementById('numStudents').value;
    
    const formData = new FormData();
    formData.append('instructor', JSON.stringify(selectedInstructor));
    formData.append('course', JSON.stringify(selectedCourse));
    formData.append('sectionID', sectionID);
    formData.append('semester', semester);
    formData.append('year', year);
    formData.append('numStudents', numStudents);
    
    fetch('/section/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = (data.success == 1) ? "Section Successfully Added" : "Error";
        document.getElementById('field1error').textContent = data.field1error;
        document.getElementById('field2error').textContent = data.field2error;
        document.getElementById('field3error').textContent = data.field3error;
    })
    .catch(error => console.error('Error:', error));
});