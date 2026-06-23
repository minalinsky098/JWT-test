import { showToast, createToast } from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const DEV_MODE = true; //remove 
const elements = {
    logout: null,
    main : null
}

async function main(){ 
    await checkexpiry();

    createToast();

    const userStatus = window.localStorage.getItem("userstatus")
    const {firstName, lastName} = await getUserInfo();
    const user = localStorage.getItem("user");
    const toastTitle = "Login Successful!";

    elements.logout = document.querySelector("#logout-link");
    elements.main = document.querySelector("main");
    await displayCats();

    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
            showToast("success", toastTitle, toastMessage);
    }

    elements.logout.addEventListener("click", logoutHandler);
    setInterval(checkexpiry, 60000)

    window.localStorage.setItem("userstatus", "online")
}
async function displayCats(){
    const { main } = elements;
    const cats = await getCats();
    console.log(main);
    console.log(cats);

    cats.forEach((cat)=>{
        console.log(cat.breed, cat.url, cat.description)
        const article = document.createElement("article");
        let title = document.createElement("h3");
        let img = document.createElement("img");
        let description = document.createElement("p");
        title.textContent = cat.breed
        img.src = cat.url
        description.textContent = cat.description
        article.append(title, img, description)
        main.appendChild(article);
    }) 
}
async function getCats(){
    const fetch_url = BASE_URL+"/api/v1/users/fetch";
    const token = localStorage.getItem("token");
    const res = await fetch(fetch_url, {
        headers:{
        "Authorization": `Bearer ${token}`
        }
    })
    const data = await res.json();
    return data.cats
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