//instructors
var instructors = [];
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
    })
    .catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const instructorIndex = document.getElementById('instructordd').value;
    const selectedInstructor = instructors[instructorIndex];
    
    const formData = new FormData();
    formData.append('instructor', JSON.stringify(selectedInstructor));
    formData.append('startSemester', document.getElementById('startSemester').value);
    formData.append('startYear', document.getElementById('startYear').value);
    formData.append('endSemester', document.getElementById('endSemester').value);
    formData.append('endYear', document.getElementById('endYear').value);
    
    fetch('/selectinstructor/form', {
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