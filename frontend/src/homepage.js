import { showToast, createToast, set_cache, get_cache, check_TTL, cacheTTL, get_favorite_cache, add_favorite_cache} from "./utils.js";
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

    let favorites = get_favorite_cache();
    console.log(favorites);
    let cats = get_cache()
    if (cats == null || cats == "undefined" || check_TTL()){
        cats = await getCats();
        set_cache(cats);
        cacheTTL();
    }
    await displayCats(cats);

    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
            showToast("success", toastTitle, toastMessage);
    }

    elements.logout.addEventListener("click", logoutHandler);
    setInterval(checkexpiry, 60000)

    window.localStorage.setItem("userstatus", "online")
}
async function displayCats(cats){
    const { main } = elements;

    cats.forEach((cat, index)=>{
        const article = document.createElement("article");
        let title = document.createElement("h3");
        let img = document.createElement("img");
        let heartButton = document.createElement("button");
        let hearticon = document.createElement("img");
        let description = document.createElement("p");

        title.textContent = cat.breed;
        img.src = cat.url;
        img.classList.add("cat-icon");
        img.id = cat.id;
        heartButton.appendChild(hearticon);
        heartButton.id = `button${index}`;
        heartButton.addEventListener('click',(e)=>(buttonHandler(e, `${index}`)));
        hearticon.src = "frontend/images/heartlogo.png";
        hearticon.classList.add("button-icon");
        description.textContent = cat.description;

        article.append(title, img, heartButton, description);
        article.id = `card${index}`;
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
    if (!res.ok){
        let toastTitle = "Error";
        let toastMessage = null;
        switch (res.status){
            case 401:
                toastMessage = "Invalid credentials, please restart your session";
                break;
            case 404:
                toastMessage = "You might have logged in without registering, please register first before using this app";
                break;
            case 500:
                toastMessage = "An error has occured please contact the developer";
                break;
            case 502:
                toastMessage = "There seems to be an issue with Cat API, please wait for a few minutes before trying again";
                break;
        }
        showToast("error", toastTitle, toastMessage);
        return;
    }
    const data = await res.json();
    return data.cats
}
function buttonHandler(e, index){
    console.log(`button${index} was clicked`)
    const article = document.querySelector(`#card${index}`);
    const title = article.querySelector("h3").textContent;
    const img = article.querySelector("img").src;
    const id = article.querySelector("img").id;
    const description = article.querySelector("p").textContent;
    console.log(title, img, id, description);
    if(id in get_favorite_cache()){
        console.log("already favorited");
        return;
    }
    add_favorite_cache(id,{"title":title, "img":img,"description": description});
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