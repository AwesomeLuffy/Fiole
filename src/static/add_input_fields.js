let counter_da = 1;

const PATTERN_REGEX_DA = "^[0-9]{9,12}$";

const PATTERN_REGEX_NAME = "^[a-zA-ZÀ-ÿ\\-\\s]{1,40}$";

const LIST_ACCEPT_FILES = ".jpg,.jpeg,.png";


/**
 * This function has to be called when the user click on the button "Ajouter un champ"
 * It can be only used for the form in "add_people.html"
 */
function addFields() {
    /*
    * Create the necessaries div to add the new fields
    * */
    // <div class="form-group">
    let divFormGroup = returnDiv("form-group", "", "formGroup" + counter_da);

    // <div class="d-flex">
    let divFlex = returnDiv("d-flex");

    // <div class="d-inline-block">
    let divInline0 = returnDiv("d-inline-block");

    let divInline1 = returnDiv("d-inline-block", "margin-left: 1%");

    let divInline2 = returnDiv("d-inline-block", "margin-left: 1%");

    let divInline3 = returnDiv("d-inline-block", "margin-left: 1%");

    let divInline4 = returnDiv("d-inline-block", "margin-left: 1%");

    let divInline5 = returnDiv("d-inline-block", "margin-left: 1%");

    let divSwitch = returnDiv("form-check form-switch", "padding-top: 75%");

    /*
    * Create the buttonDelete depends on the counter_da
    *
     */
    let buttonDelete = returnButton("&#10060;",
        "margin-top: 75%;",
        "btn btn-outline-danger",
        "deleteLine(this.parentNode.parentNode.parentNode.id)");

    /*
    * Create the labelDA depends on the counter_da
    * */
    // <label for="inputDA" class="form-label mt-4">Numéro de DA</label>
    let labelDA = returnLabel("inputDA" + counter_da, "Numéro de DA");

    /*
    * Create the daInput depends on the counter_da
    * */
    // <input type="text" class="form-control" id="inputDA" placeholder="Ex. 200010101">
    let daInput = returnInput("text", "inputDA" + counter_da, true, "Ex. 200010101", "", PATTERN_REGEX_DA);

    /*
    * Create the labelFile depends on the counter_da
    * */
    // <label for="formFile" class="form-label mt-4">Default file input example</label>
    let labelFile = returnLabel("formFile" + counter_da, "Fichier");

    /*
    * Create the fileInput depends on the counter_da
    * */
    // <input class="form-control" type="file" id="formFile">
    let fileInput = returnInput("file", "formFile" + counter_da, true);
    fileInput.setAttribute("accept", LIST_ACCEPT_FILES);

    /*
    * Create the labelName depends on the counter_da
     */
    // <label for="inputName" class="form-label mt-4">Nom</label>
    let labelName = returnLabel("inputName" + counter_da, "Nom");

    /*
    * Create the nameInput depends on the counter_da
    */
    // <input type="text" class="form-control" id="inputName" placeholder="Ex. Dupont">
    let nameInput = returnInput("text", "inputName" + counter_da, true, "Ex. Dupont", "", PATTERN_REGEX_NAME);

    /*
    * Create the labelSurname depends on the counter_da
     */
    // <label for="inputFName" class="form-label mt-4">Prénom</label>
    let labelSurname = returnLabel("inputFName" + counter_da, "Prénom");

    /*
    * Create the surnameInput depends on the counter_da
    */
    // <input type="text" class="form-control" id="inputFName" placeholder="Ex. Jean">
    let surnameInput = returnInput("text", "inputFName" + counter_da, true, "Ex. Jean", "", PATTERN_REGEX_NAME);

    /*
    * Create the checkbox depends on the counter_da
     */
    // <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
    let checkbox = returnInput("checkbox", "flexSwitchCheckAccess" + counter_da, "", "", "form-check-input");

    /*
    * Create the labelCheckbox depends on the counter_da
     */
    // <label class="form-check-label" for="flexSwitchCheckDefault">Accès</label>
    let labelCheckbox = returnLabel("flexSwitchCheckAccess" + counter_da, "Accès", "form-check-label");


    /* Set the elements in the right order (same structure as the html file :
    *
    *           <div>
                    <div>
                        <div>
                            <label></label>
                            <input>
                        </div>
                        <div>
                            <label></label>
                            <input>
                        </div>
                    </div>
                </div>
    * */
    //Div for the buttonDelete
    divInline0.appendChild(buttonDelete);

    // Div for the DA
    divInline1.appendChild(labelDA);
    divInline1.appendChild(daInput);

    //Div for the file
    divInline2.appendChild(labelFile);
    divInline2.appendChild(fileInput);

    //Div for the name
    divInline3.appendChild(labelName);
    divInline3.appendChild(nameInput);

    //Div for the surname
    divInline4.appendChild(labelSurname);
    divInline4.appendChild(surnameInput);

    //Div for the switch (form-check form-switch)
    divSwitch.appendChild(checkbox);
    divSwitch.appendChild(labelCheckbox);

    //Div for the switch (d-inline-block)
    divInline5.appendChild(divSwitch);

    //Div for the d-flex
    divFlex.appendChild(divInline0);
    divFlex.appendChild(divInline1);
    divFlex.appendChild(divInline2);
    divFlex.appendChild(divInline3);
    divFlex.appendChild(divInline4);
    divFlex.appendChild(divInline5);

    //Div for the form-group
    divFormGroup.appendChild(divFlex);

    //Append the divFormGroup to the divFieldsFormStudent
    document.getElementById("divFieldsFormStudent").appendChild(divFormGroup);

    counter_da++;
}

// Create a div with a class and a style
function returnInput(type, name, required = true, placeholder = "", clazz = "", regex = "") {
    let input = document.createElement("input");
    input.setAttribute("type", type);

    if (clazz !== "") {
        input.setAttribute("class", clazz);
    } else {
        input.setAttribute("class", "form-control");
    }

    input.setAttribute("name", name);

    if (placeholder !== "") {
        input.setAttribute("placeholder", placeholder);
    }

    if (required) {
        input.setAttribute("required", "");
    }

    if (regex !== "") {
        input.setAttribute("pattern", regex);
    }


    return input;
}

function returnButton(value, style, clazz, action) {
    let button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute("onclick", action);
    button.setAttribute("class", clazz);
    button.setAttribute("style", style);
    button.innerHTML = value;
    return button;
}

// Create a label with a for and a text
function returnLabel(forName, text, clazz = "") {
    let label = document.createElement("label");
    label.setAttribute("for", forName);
    if (clazz !== "") {
        label.setAttribute("class", clazz);
    } else {
        label.setAttribute("class", "form-label mt-4");
    }

    label.innerHTML = text;

    return label;
}

// Create a div with a class and a style
function returnDiv(classDiv, style = "", id = "") {
    let div = document.createElement("div");
    div.setAttribute("class", classDiv);
    if (id !== "") {
        div.setAttribute("id", id);
    }
    if (style !== "") {
        div.setAttribute("style", style);
    }

    return div;
}

// Function to delete a line
function deleteLine(formGroupNumber) {
    let divFieldsFormStudent = document.getElementById("divFieldsFormStudent");
    let divFormGroup = document.getElementById(formGroupNumber);

    divFieldsFormStudent.removeChild(divFormGroup);

}