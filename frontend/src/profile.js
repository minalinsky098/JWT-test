import { showToast, createToast } from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const DEV_MODE = false; //remove 
async function main(){ 
    await checkexpiry();
    createToast();
    const userStatus = window.localStorage.getItem("userstatus")
    const {firstName, lastName} = await getUserInfo();
    const user = localStorage.getItem("user");
    const toastTitle = "Login Successful!";
    const firstNameInput = document.querySelector("#firstNameInput");
    const lastNameInput = document.querySelector("#lastNameInput");
    const logout = document.querySelector("#logout-link")
    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
            showToast("success", toastTitle, toastMessage);
    }
    setProfileName(firstNameInput, lastNameInput, {firstName, lastName});
    setInterval(checkexpiry, 60000)
    logout.addEventListener("click", logoutHandler);

    window.localStorage.setItem("userstatus", "online");
}
function logoutHandler(){
    window.localStorage.setItem("userstatus", "offline");
}
function getTokenPayload(token){
    const payload = token.split(".")[1];
    const payloadB64 = payload.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(payload.length / 4) * 4, "=");
    return JSON.parse(atob(payloadB64));
}
function setProfileName(firstNameInput, lastNameInput, username){
    const {firstName, lastName} = username;
    firstNameInput.value = firstName;
    lastNameInput.value = lastName;
}
async function getUserInfo(){
    if (DEV_MODE) {
        return { firstName: "Dev", lastName: "User" };
    }
    let url = BASE_URL+"/api/v1/users/me";
    let res = null;
    let data = null;
    const token = localStorage.getItem("token");
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