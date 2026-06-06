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
    toast.addEventListener('transitionend', ()=>{toast.classList.remove('show')}, { once: true })
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