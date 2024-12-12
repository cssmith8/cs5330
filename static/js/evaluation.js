//instructors
var instructors = [];
var evaluations = [];
var selectedEvaluation = null;
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
    const semester = document.getElementById('semester').value;
    const year = document.getElementById('year').value;
    
    const formData = new FormData();
    formData.append('instructor', JSON.stringify(selectedInstructor));
    formData.append('semester', semester);
    formData.append('year', year);
    
    fetch('/evaluation/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        evaluations = data.evaluations;
        const associatedSections = document.getElementById('associatedSections');
        //clear the previous courses
        associatedSections.innerHTML = "";
        //if sections is empty, display message
        if (evaluations.length == 0) {
            const sectionElement = document.createElement('p');
            sectionElement.textContent = "No sections with any goals found";
            associatedSections.appendChild(sectionElement);
        } else {
            
            evaluations.forEach(e => {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'bordered';

                const sectionElement = document.createElement('p');
                sectionElement.textContent = e.courseID + ": " + e.sectionID + " - " + e.goalCode + " " + e.degreeName + " " + e.degreeLevel;
                sectionDiv.appendChild(sectionElement);

                //button that will allow the user to edit the evaluation
                const editButton = document.createElement('button');
                editButton.textContent = "Edit Evaluation";
                editButton.addEventListener('click', function() {
                    document.getElementById('editResult').innerHTML = "";
                    document.getElementById('evalType').value = e.evaluationType || "";
                    document.getElementById('aamount').value = e.A >= 0 ? e.A : "";
                    document.getElementById('bamount').value = e.B >= 0 ? e.B : "";
                    document.getElementById('camount').value = e.C >= 0 ? e.C : "";
                    document.getElementById('famount').value = e.F >= 0 ? e.F : "";
                    document.getElementById('improvement').value = e.improvementSuggestion || "";
                    selectedEvaluation = e;
                    document.getElementById('currentlyEditing').textContent = "Currently editing evaluation for section " + e.sectionID;
                    document.querySelector('#editForm button[type="submit"]').disabled = false;
                });
                sectionDiv.appendChild(editButton);

                associatedSections.appendChild(sectionDiv);

                //add these evaluations to the dropdown for duplication
                const evalFromDropdown = document.getElementById('evalFrom');
                const evalToDropdown = document.getElementById('evalTo');
                const evalFromOption = document.createElement('option');
                evalFromOption.value = evaluations.indexOf(e);
                evalFromOption.textContent = e.courseID + " " + e.sectionID + " " + e.goalCode;
                evalFromDropdown.appendChild(evalFromOption);
                const evalToOption = document.createElement('option');
                evalToOption.value = evaluations.indexOf(e);
                evalToOption.textContent = e.courseID + " " + e.sectionID + " " + e.goalCode;
                evalToDropdown.appendChild(evalToOption);

            });
        }    
        document.querySelector('#duplicateForm button[type="submit"]').disabled = false;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('editForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('sectionID', selectedEvaluation.sectionID);
    formData.append('courseID', selectedEvaluation.courseID);
    formData.append('semester', selectedEvaluation.semester);
    formData.append('year', selectedEvaluation.year);
    formData.append('goalCode', selectedEvaluation.goalCode);
    formData.append('degreeName', selectedEvaluation.degreeName);
    formData.append('degreeLevel', selectedEvaluation.degreeLevel);
    formData.append('evaluationType', document.getElementById('evalType').value);
    formData.append('A', document.getElementById('aamount').value);
    formData.append('B', document.getElementById('bamount').value);
    formData.append('C', document.getElementById('camount').value);
    formData.append('F', document.getElementById('famount').value);
    formData.append('improvementSuggestion', document.getElementById('improvement').value);

    fetch('/evaluation/edit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('editResult').textContent = "Evaluation updated successfully";
        } else {
            document.getElementById('editResult').textContent = "";
        }
        document.getElementById('field1error').textContent = data.field1error;
        document.getElementById('field2error').textContent = data.field2error;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('duplicateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    const evalFromIndex = document.getElementById('evalFrom').value;
    const evalToIndex = document.getElementById('evalTo').value;
    formData.append('evalFrom', JSON.stringify(evaluations[evalFromIndex]));
    formData.append('evalTo', JSON.stringify(evaluations[evalToIndex]));

    fetch('/evaluation/duplicate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('duplicateResult').textContent = "Evaluation duplicated successfully";
        } else {
            document.getElementById('duplicateResult').textContent = "Error duplicating evaluation";
        }
    })
    .catch(error => console.error('Error:', error));
});