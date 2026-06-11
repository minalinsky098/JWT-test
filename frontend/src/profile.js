import { showToast, createToast } from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const elements = {
    firstNameInput: null,
    lastNameInput: null,
    form: null, 
    logout: null
}
const token = localStorage.getItem("token");
const DEV_MODE = true; //remove 

async function main(){ 
    await checkexpiry();
    createToast();

    const userStatus = window.localStorage.getItem("userstatus")
    const {firstName, lastName} = await getUserInfo();
    const user = localStorage.getItem("user");
    const toastTitle = "Login Successful!";

    elements.form = document.querySelector("form");
    elements.firstNameInput = document.querySelector("#firstNameInput");
    elements.lastNameInput = document.querySelector("#lastNameInput");
    elements.logout = document.querySelector("#logout-link")

    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
        showToast("success", toastTitle, toastMessage);
    }

    setProfileName({firstName, lastName});
    setInterval(checkexpiry, 60000)
    elements.logout.addEventListener("click", logoutHandler);
    elements.form.addEventListener("submit", updateUsername);

    window.localStorage.setItem("userstatus", "online");
}

async function updateUsername(event){
    event.preventDefault()
    const URL = BASE_URL + "/api/v1/users";
    let firstName = elements.firstNameInput.value
    let lastName = elements.lastNameInput.value
    let res = null
    let toastTitle = null;
    let toastMessage = null;

    console.log(firstName, lastName)
    console.log(`Fetching from ${URL}`)
    if (!firstName || !lastName){
        toastTitle  = "Invalid Input";
        toastMessage = "Please fill out every field!!"
        showToast("error", toastTitle, toastMessage);
        return;
    }

    res = await fetch(URL, {
        method : "PUT",
        headers : {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body : JSON.stringify({
            "first_name": firstName,
            "last_name": lastName
        })
    })

    if (!res.ok){
        toastTitle = "Update Failed";
        switch (res.status){
            case 401:
                toastMessage = "Invalid credentials, the server cannot identify you";
                break;
            case 404:
                toastMessage = "You were not found in the database";
                break;
            case 500:
                toastMessage = "Something went wrong with the server";
                break;
        }
        showToast("error", toastTitle, toastMessage);
    }
    else{
        const data = await res.json();

        firstName = data.first_name;
        lastName = data.last_name;
        toastTitle = "Update Sucessful";
        toastMessage  = `Hello ${firstName} ${lastName}`;
        console.log(data);
        showToast("success", toastTitle, toastMessage);
    }

}
function logoutHandler(){
    window.localStorage.setItem("userstatus", "offline");
}
function getTokenPayload(token){
    const payload = token.split(".")[1];
    const payloadB64 = payload.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(payload.length / 4) * 4, "=");
    return JSON.parse(atob(payloadB64));
}
function setProfileName(username){
    const {firstName, lastName} = username;
    elements.firstNameInput.value = firstName;
    elements.lastNameInput.value = lastName;
}
async function getUserInfo(){
    if (DEV_MODE) {
        return { firstName: "Dev", lastName: "User" };
    }
    let url = BASE_URL+"/api/v1/users/me";
    let res = null;
    let data = null;
    res = await fetch(url, {
        headers:{
            "Content-Type":"application/json",
            "Authorization":`Bearer ${token}`
        }
    });
    data = await res.json();
    const {first_name: firstName, last_name: lastName} = data;
    return {firstName, lastName};
}

async function checkexpiry(){
    if (DEV_MODE) {
        document.body.style.visibility = "visible";
        return;
    }
    console.log("Checking for expiry");
    const token = localStorage.getItem("token");
    if (!token) { 
        window.location.href = "/";
        window.localStorage.setItem("userstatus", "offline") 
        return; 
    }
    const payload = getTokenPayload(token);
    const isExpired = payload.exp * 1000 < Date.now();
    if (isExpired){
        window.localStorage.setItem("userstatus", "offline")
        window.location.href = "/";
        return;
    }
    else{
        document.body.style.visibility = "visible";
    }
}
main()