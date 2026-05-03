const BASE_URL = "http://127.0.0.1:8000";
async function main(){ 
    await checkexpiry()
    setInterval(await checkexpiry, 60000);

}
function getTokenPayload(token){
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
}
async function checkexpiry(){
    const token = localStorage.getItem("token");
    const payload = getTokenPayload(token);
    const isExpired = payload.exp * 1000 < Date.now();
    console.log("check for expiry")
    if (isExpired){
        window.location.href = "/";
        return;
    }
    else{
        document.body.style.visibility = "visible";
    }
}
main()