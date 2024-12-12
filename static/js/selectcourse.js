//courses
var courses = [];
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
    })
    .catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const courseIndex = document.getElementById('coursedd').value;
    const selectedCourse = courses[courseIndex];
    
    const formData = new FormData();
    formData.append('course', JSON.stringify(selectedCourse));
    formData.append('startSemester', document.getElementById('startSemester').value);
    formData.append('startYear', document.getElementById('startYear').value);
    formData.append('endSemester', document.getElementById('endSemester').value);
    formData.append('endYear', document.getElementById('endYear').value);
    
    fetch('/selectcourse/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        sections = data.sections;
        const associatedSections = document.getElementById('associatedSections');
        //clear the previous courses
        associatedSections.innerHTML = "";
        //if sections is empty, display message
        if (sections.length == 0) {
            const sectionElement = document.createElement('p');
            sectionElement.textContent = "No sections found";
            associatedSections.appendChild(sectionElement);
        } else {
            sections.forEach(section => {
                const sectionElement = document.createElement('p');
                sectionElement.classList.add('bordered');
                sectionElement.textContent = "ID: " + section.sectionID + ", Semester: " +  section.semester + " " + section.year;
                associatedSections.appendChild(sectionElement);
            });
        }              
    })
    .catch(error => console.error('Error:', error));
});