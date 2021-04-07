var selectedRow = null


var datalist = document.getElementById('date-datalist');
var fragment = document.createDocumentFragment();

var myGrades = ['10%', '20%'];

// Prepare the option elements to be rendered.
myGrades.forEach(function(car) {
  var option = document.createElement('option');
  var text = document.createTextNode(car);

  option.value = car;
  option.appendChild(text);
  fragment.appendChild(option);
});


// Append all of them to DOM.
datalist.appendChild(fragment);

function onFormSubmit() {
    if (validate()) {
        var formData = readFormData();
        if (selectedRow == null)
            insertNewRecord(formData);
        else
            updateRecord(formData);
        resetForm();
    }
}

function readFormData() {
    var formData = {};
    formData["Assessment"] = document.getElementById("Assessment").value;
    formData["weight"] = document.getElementById("weight").value;
    formData["date"] = document.getElementById("date").value;
    return formData;
}

function insertNewRecord(data) {
    var table = document.getElementById("employeeList").getElementsByTagName('tbody')[0];
    var newRow = table.insertRow(table.length);
    cell1 = newRow.insertCell(0);
    cell1.innerHTML = data.Assessment;
    cell2 = newRow.insertCell(1);
    cell2.innerHTML = data.weight;
    cell3 = newRow.insertCell(2);
    cell3.innerHTML = data.date;
    cell4 = newRow.insertCell(3);
    cell4.innerHTML = '<a onClick="onEdit(this)">Edit</a><a onClick="onDelete(this)">Delete</a>';
}

function resetForm() {
    document.getElementById("Assessment").value = "";
    document.getElementById("weight").value = "";
    document.getElementById("date").value = "";
    selectedRow = null;
}

function onEdit(td) {
    selectedRow = td.parentElement.parentElement;
    document.getElementById("Assessment").value = selectedRow.cells[0].innerHTML;
    document.getElementById("weight").value = selectedRow.cells[1].innerHTML;
    document.getElementById("date").value = selectedRow.cells[2].innerHTML;
}
function updateRecord(formData) {
    selectedRow.cells[0].innerHTML = formData.Assessment;
    selectedRow.cells[1].innerHTML = formData.weight;
    selectedRow.cells[2].innerHTML = formData.date;
}

function onDelete(td) {

    row = td.parentElement.parentElement;
    document.getElementById("employeeList").deleteRow(row.rowIndex);
    resetForm();
}
function validate() {
    isValid = true;
    if (document.getElementById("Assessment").value == "") {
        isValid = false;
        document.getElementById("AssessmentValidationError").classList.remove("hide");
    } else {
        isValid = true;
        if (!document.getElementById("AssessmentValidationError").classList.contains("hide"))
            document.getElementById("AssessmentValidationError").classList.add("hide");
    }
    return isValid;
}