document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    fetch('/selectsemester/form', {
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
                const sectionDiv = document.createElement('div');
                sectionDiv.classList.add('bordered');

                const sectionElement = document.createElement('p');
                sectionElement.textContent = "ID: " + section.sectionID + ", Semester: " +  section.semester + " " + section.year;
                sectionDiv.appendChild(sectionElement);

                const status = section.status;
                var statusText = "";
                //switch statement to determine the status of the section
                switch (status) {
                    case "0":
                        statusText = "Never Evaluated";
                        break;
                    case "1":
                        statusText = "Fully evaluated with suggestion";
                        break;
                    case "2":
                        statusText = "Fully evaluated without suggestion";
                        break;
                    case "3":
                        statusText = "Partially evaluated with suggestion";
                        break;
                    case "4":
                        statusText = "Partially evaluated without suggestion";
                        break;
                    default:
                        statusText = "Unknown";
                }
                const evalElement = document.createElement('p');
                evalElement.textContent = "Evaluation: " + statusText;
                sectionDiv.appendChild(evalElement);

                associatedSections.appendChild(sectionDiv);
            });
        }              
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('dataForm2').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    fetch('/selectsemester/form2', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        sections = data.sections;
        const associatedSections = document.getElementById('associatedSections2');
        //clear the previous courses
        associatedSections.innerHTML = "";
        //if sections is empty, display message
        if (sections.length == 0) {
            const sectionElement = document.createElement('p');
            sectionElement.textContent = "No sections found";
            associatedSections.appendChild(sectionElement);
        } else {
            sections.forEach(section => {
                const sectionDiv = document.createElement('div');
                sectionDiv.classList.add('bordered');

                const sectionElement = document.createElement('p');
                sectionElement.textContent = "ID: " + section.sectionID + ", Semester: " +  section.semester + " " + section.year;
                sectionDiv.appendChild(sectionElement);

                const evalElement = document.createElement('p');
                evalElement.textContent = "-    Passing Percentage: " + section.percentage + "%";
                sectionDiv.appendChild(evalElement);

                associatedSections.appendChild(sectionDiv);
            });
        }              
    })
    .catch(error => console.error('Error:', error));
});