//degrees
fetch('/get_all_degrees')
.then(response => response.json())
.then(data => {
    const div = document.getElementById('degrees');
    data.content.forEach(option => {
        const pElement = document.createElement('p');
        pElement.classList.add('bordered');
        pElement.textContent = option.degreeName + " " + option.degreeLevel;
        div.appendChild(pElement);
    });
})
.catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
event.preventDefault();
const formData = new FormData(event.target);
fetch('/degree/form', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    document.getElementById('result').textContent = (data.success == 1) ? "Degree Successfully Entered" : "";
    document.getElementById('field1error').textContent = data.field1error;
    document.getElementById('field2error').textContent = data.field2error;
})
.catch(error => console.error('Error:', error));
});