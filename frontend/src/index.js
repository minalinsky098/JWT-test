const BASE_URL = "http://127.0.0.1:8000";
const elements = {
    formtitle: null,
    form: null,
    emailInput: null,
    passwordInput: null,
    firstNameGroup: null,
    lastNameGroup: null,
    registerButton: null,
    submitButton: null
}

let register = true;

function main(){
    elements.formtitle = document.querySelector("#title");
    elements.form = document.querySelector("form");
    elements.emailInput = document.querySelector("#email");
    elements.passwordInput = document.querySelector("#password");
    elements.registerButton = document.querySelector("#register");
    elements.firstNameGroup = document.querySelector("#firstName-group");
    elements.lastNameGroup = document.querySelector("#lastName-group");
    elements.submitButton = document.querySelector("#submit");

    elements.form.addEventListener("submit", onSubmit);
    elements.registerButton.addEventListener("click", switchRegister);
    console.log("Hello world");
}

function switchRegister(event){
    const {formtitle, firstNameGroup, lastNameGroup, submitButton, registerButton} = elements;
    console.log("switch", register);
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
    register = !register;
}

async function onSubmit(event){
    event.preventDefault();
    const {emailInput, passwordInput} = elements
    console.log(email.value, password.value);
    res = await fetch(BASE_URL);
    res = await res.json();
    console.log(res);
}

main()