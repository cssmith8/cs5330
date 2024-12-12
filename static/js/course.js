//degrees
fetch('/get_all_courses')
.then(response => response.json())
.then(data => {
    const div = document.getElementById('courses');
    data.content.forEach(option => {
        const pElement = document.createElement('p');
        pElement.classList.add('bordered');
        pElement.textContent = option.courseID + ": " + option.courseName;
        div.appendChild(pElement);
    });
})
.catch(error => console.error('Error:', error));

document.getElementById('dataForm').addEventListener('submit', function(event) {
event.preventDefault();
const formData = new FormData(event.target);
fetch('/course/form', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    document.getElementById('result').textContent = (data.success == 1) ? "Course Successfully Entered" : "";
    document.getElementById('field1error').textContent = data.field1error;
    document.getElementById('field2error').textContent = data.field2error;
})
.catch(error => console.error('Error:', error));
});