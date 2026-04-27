const BASE_URL = "http://127.0.0.1:8000";
const elements = {
    formtitle: null,
    form: null,
    firstnameInput: null, 
    lastnameInput: null, 
    emailInput: null,
    passwordInput: null,
    firstNameGroup: null,
    lastNameGroup: null,
    registerButton: null,
    submitButton: null
}

let register = false;

function main(){
    elements.formtitle = document.querySelector("#title");
    elements.form = document.querySelector("form");
    elements.firstnameInput = document.querySelector("#firstname")
    elements.lastnameInput = document.querySelector("#lastname")
    elements.emailInput = document.querySelector("#email");
    elements.passwordInput = document.querySelector("#password");
    elements.registerButton = document.querySelector("#register");
    elements.firstNameGroup = document.querySelector("#firstName-group");
    elements.lastNameGroup = document.querySelector("#lastName-group");
    elements.submitButton = document.querySelector("#submit");

    elements.form.addEventListener("submit", onSubmit);
    elements.registerButton.addEventListener("click", switchRegister);
}

function switchRegister(event){
    const {formtitle, firstNameGroup, lastNameGroup, submitButton, registerButton} = elements;
    register = !register;
    if (register){
        formtitle.textContent = "Register";
        firstNameGroup.style.display = "flex";
        lastNameGroup.style.display = "flex";
        submitButton.textContent = "Register";
        registerButton.textContent = "Have an account?"
    }
    else{
        formtitle.textContent = "Login";
        firstNameGroup.style.display = "none";
        lastNameGroup.style.display = "none";
        submitButton.textContent = "Login";
        registerButton.textContent = "Don't have an account?"
    }
}

async function onSubmit(event){
    event.preventDefault();
    if (register){
        const {emailInput, passwordInput} = elements

    }
    else{
        const {emailInput, passwordInput} = elements
        res = await fetch(BASE_URL);
        res = await res.json();
        console.log(res);
    }
}

main()