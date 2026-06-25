export function showToast(type, toastTitle, toastMessage = ""){
    const toast = document.querySelector('.toast');
    if (type==="success"){
        toast.style.borderColor = "#24e50a";
    }
    else if(type ==="error"){
        toast.style.borderColor = "#e50a0a";
    }
    const title = toast.querySelector('h1');
    const message = toast.querySelector('p');
    title.textContent = toastTitle;
    message.textContent = toastMessage;
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    setTimeout(() => {
    toast.classList.remove('show');
    toast.addEventListener('transitionend', ()=>{toast.classList.remove('show')}, { once: true })
    }, 3000); 
}

export function createToast(){
    const toast = document.createElement('div');
    const message = document.createElement('p');
    const title = document.createElement('h1')
    toast.appendChild(title);
    toast.appendChild(message);
    document.body.appendChild(toast);
    toast.classList.add('toast');
}

export function set_cache(catlist){
    if (!Array.isArray(catlist)) return;
    localStorage.setItem("cats", JSON.stringify(catlist))
}

export function get_cache(){
    const cats = localStorage.getItem("cats");
    return (cats == "undefined") ? null : JSON.parse(cats);
}

export function get_favorite_cache(){
    if (!("favorites" in localStorage)){
        localStorage.setItem("favorites", JSON.stringify({}));
    }
    return JSON.parse(localStorage.getItem("favorites"));
}
export function add_favorite_cache(catid, catinfo){
    const favorites = JSON.parse(localStorage.getItem("favorites"));
    favorites[catid] = catinfo;
    localStorage.setItem("favorites", JSON.stringify(favorites));
}

export function cacheTTL(){
    const now = Date.now()
    localStorage.setItem("TTL", now);
}

export function check_TTL(){
    const now = Date.now();
    let ttl = localStorage.getItem("TTL");
    if (now>parseInt(ttl)+300000) return true;
    return false;
}