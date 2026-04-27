function main(){
    const form = document.querySelector("form");
    const emailInput = document.querySelector("#email");
    const passwordInput = document.querySelector("#password")
    form.addEventListener("submit", function(e){onSubmit(e, emailInput, passwordInput)})
    console.log("Hello world");
}




function onSubmit(event, email, password){
    event.preventDefault();
    console.log(email.value, password.value);
}

main()