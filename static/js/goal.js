//degrees
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

        fetch('/get_all_goals')
            .then(response => response.json())
            .then(data => {
                const div = document.getElementById('goals');
                data.content.forEach(option => {
                    const pElement = document.createElement('p');
                    pElement.classList.add('bordered');
                    pElement.textContent = "[" + option.degreeName + " " + option.degreeLevel + "] " + option.goalCode + ": " + option.description;
                    div.appendChild(pElement);
                });
            })
            .catch(error => console.error('Error:', error));
    })
    .catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const degreeIndex = document.getElementById('degreedd').value;
    const selectedDegree = degrees[degreeIndex];
    const goalCode = document.getElementById('goalCode').value;
    const goalDesc = document.getElementById('goalDesc').value;
    
    const formData = new FormData();
    formData.append('degree', JSON.stringify(selectedDegree));
    formData.append('goalCode', goalCode);
    formData.append('goalDesc', goalDesc);
    
    fetch('/goal/form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = (data.success == 1) ? "Goal Successfully Entered" : "";
        document.getElementById('field1error').textContent = data.field1error;
        document.getElementById('field2error').textContent = data.field2error;
    })
    .catch(error => console.error('Error:', error));
});