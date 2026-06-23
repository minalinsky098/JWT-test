import { showToast, createToast } from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const DEV_MODE = true; //remove 
const elements = {
    logout: null
}

async function main(){ 
    await checkexpiry();
    await getCats();
    createToast();

    const userStatus = window.localStorage.getItem("userstatus")
    const {firstName, lastName} = await getUserInfo();
    const user = localStorage.getItem("user");
    const toastTitle = "Login Successful!";

    elements.logout = document.querySelector("#logout-link");

    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
            showToast("success", toastTitle, toastMessage);
    }

    elements.logout.addEventListener("click", logoutHandler);
    setInterval(checkexpiry, 60000)

    window.localStorage.setItem("userstatus", "online")
}
async function getCats(){
    const fetch_url = BASE_URL+"/api/v1/users/fetch";
    const token = localStorage.getItem("token");
    let res = await fetch(fetch_url, {
        headers:{
        "Authorization": `Bearer ${token}`
        }
    })
    let data = await res.json();
    console.log(res);
    console.log(data);
}

function logoutHandler(){
    window.localStorage.setItem("userstatus", "offline");
    window.localStorage.removeItem("token")
    window.location.href = "/";
}
function getTokenPayload(token){
    const payload = token.split(".")[1];
    const payloadB64 = payload.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(payload.length / 4) * 4, "=");
    return JSON.parse(atob(payloadB64));
}
async function getUserInfo(){
    console.log("Checking for expiry");
    let url = BASE_URL+"/api/v1/users/me";
    let res = null;
    let data = null;
    const token = localStorage.getItem("token");
    res = await fetch(url, {
        headers:{
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