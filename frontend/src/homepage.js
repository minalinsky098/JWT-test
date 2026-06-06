import { showToast, createToast } from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const DEV_MODE = true; //remove 
async function main(){ 
    await checkexpiry();
    const {firstName, lastName} = await getUserInfo();
    const user = localStorage.getItem("user");
    const toastTitle = "Login Successful!";
    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";
    toastMessage+= ` ${firstName} ${lastName}`;
    createToast();
    showToast("success", toastTitle, toastMessage);
    setInterval(checkexpiry, 60000)
}
function getTokenPayload(token){
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
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
    const token = localStorage.getItem("token");
    if (!token) { window.location.href = "/"; return; }
    const payload = getTokenPayload(token);
    const isExpired = payload.exp * 1000 < Date.now();
    if (isExpired){
        window.location.href = "/";
        return;
    }
    else{
        document.body.style.visibility = "visible";
    }
}
main()