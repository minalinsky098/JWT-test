const BASE_URL = "http://127.0.0.1:8000";
const elements = {
    formtitle: null,
    form: null,
    firstNameInput: null, 
    lastNameInput: null, 
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
    elements.firstNameInput = document.querySelector("#firstname")
    elements.lastNameInput = document.querySelector("#lastname")
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
    let res = null;
    if (register){
        const {firstNameInput, lastNameInput, emailInput, passwordInput} = elements;
        const url = `${BASE_URL}/api/v1/register`;
        res = await fetch(url, {
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            }, 
            body: JSON.stringify(
                {first_name: firstNameInput.value,
                last_name: lastNameInput.value,
                password: passwordInput.value, 
                email: emailInput.value})
        });
        if (!res.ok){
            window.alert("SOMETHING WENT WRONG");
        }
        else{
            res = await res.json();
            localStorage.setItem("token", res.token)
            window.location.href = "/home"
        }
    }
    else{
        const {emailInput, passwordInput} = elements; 
        const url = `${BASE_URL}/api/v1/login`;
        res = await fetch(url,
            {
                method: "POST",
                headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email: emailInput.value, password: passwordInput.value})
            });
        if (!res.ok){
            window.alert("SOMETHING WENT WRONG");
        }
        else{
            res = await res.json();
            localStorage.setItem("token", res.token)
            window.location.href = "/home"
        }
    }
    console.log(res);
}

main()