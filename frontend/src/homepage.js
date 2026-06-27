import { showToast, createToast, set_cache, get_cache, check_TTL, cacheTTL, get_favorite_cache, add_favorite_cache, remove_favorite_cache} from "./utils.js";
const BASE_URL = `http://127.0.0.1:8000`;
const DEV_MODE = true; //remove 
const elements = {
    logout: null,
    main : null,
    sentinel : null
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
    elements.sentinel = document.querySelector("#sentinel")

    let favorites = get_favorite_cache();
    let cats = get_cache();
    if (check_TTL()){
        cats = await getCats();
        cacheTTL();
    }
    cats = normalize_entires(favorites, cats); 
    set_cache(cats);
    await displayCats(cats);
    const observer = new IntersectionObserver(handleIntersection, {
    root: null,          // null = the browser viewport. Could be a scrollable div instead.
    rootMargin: "100%", // expands the root's box for intersection purposes
    threshold: 0          // fire as soon as even 1px of the target is visible
    });
    observer.observe(elements.sentinel);

    let toastMessage = (user==="register")?"Welcome user":"Welcome back user";

    toastMessage+= ` ${firstName} ${lastName}`;

    if (userStatus!=="online"){
        showToast("success", toastTitle, toastMessage);
    }

    elements.logout.addEventListener("click", logoutHandler);
    setInterval(checkexpiry, 60000)

    window.localStorage.setItem("userstatus", "online")
}
async function handleIntersection(entries){
  const entry = entries[0];
  if (entry.isIntersecting) {
    console.log("im fired")
    let cats = convert_to_object(await getCats());
    let shownCats = get_cache();
    console.log(cats)
    cats = normalize_entires(cats,shownCats);
    console.log(cats);
    await displayCats(cats); // need to normalize entries
    set_cache(cats);
  }
}
function convert_to_object(catlist){
    let converted_obj = {};
    catlist.forEach((cat)=>{
        converted_obj[`${cat.id}`] = {"img":cat.url,"description":cat.description,"title": cat.breed};
    })
    return converted_obj;
}
function normalize_entires(entry, catlist){ // entry should be an object not array
    let normalized_list = [];
    for(const[id, value] of Object.entries(entry)){
        normalized_list.push({"id":id, "url":value.img,"description":value.description,"breed":value.title});
    }
    for (const cat of catlist) {
        if (cat.id in entry) {
            continue; 
        }
        normalized_list.push(cat);
    }
    return normalized_list;
}
function favorites_initial(){
    const {main} = elements;
    const articles = main.querySelectorAll("article");
    articles.forEach((article, index)=>{
        const imgId = article.querySelector("img").id;
        const heartButton = article.querySelector("button");
        if (imgId in get_favorite_cache()){
            heartButton.setAttribute('aria-pressed', true);
        }
    })
}
async function displayCats(cats){
    const { main, sentinel } = elements;

    const currentindex = main.childElementCount-1;

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
        heartButton.id = `button${index+currentindex}`;
        heartButton.addEventListener('click',(e)=>(buttonHandler(e, `${index+currentindex}`)));
        heartButton.setAttribute('aria-pressed', false);
        hearticon.src = "frontend/images/heartlogo.png";
        hearticon.classList.add("button-icon");
        description.textContent = cat.description;

        article.append(title, img, heartButton, description);
        article.id = `card${index+currentindex}`;
        main.insertBefore(article, sentinel);
    }) 
    favorites_initial();
}
function buttonHandler(e, index){
    console.log(`button${index} was clicked`)
    const article = document.querySelector(`#card${index}`);
    const title = article.querySelector("h3").textContent;
    const img = article.querySelector("img").src;
    const id = article.querySelector("img").id;
    const description = article.querySelector("p").textContent;
    const button = e.currentTarget;
    if(JSON.parse(button.getAttribute('aria-pressed'))){ //if its pressed/favorited, remove it
        remove_favorite_cache(id);
    }
    else{
    add_favorite_cache(id,{"title":title, "img":img,"description": description});
    }
    button.setAttribute('aria-pressed', !JSON.parse(button.getAttribute('aria-pressed')));//swaps the value for aria-pressed
    let favorites = get_favorite_cache();
    console.log(favorites);
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