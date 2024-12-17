export function authUser(email, password){
    let a = email+password
    return a.length;
}
export function regUser(email, password){
    return (email+password).length > 0
}
export function getHistoryList(){
    let history = JSON.parse(localStorage.getItem('history'))
    if(history == null) return [];
    let output = []
    for(let i = 0; i < history.length; i++){
        let el = {history_id: i, user_prompt: history[i].user_prompt};  
        output.push(el)
    }
    return output
}
export function getHistoryElement(history_id){
    return JSON.parse(localStorage.getItem('history'))[history_id]
}



export async function sendPrompt(obj){
    localStorage.setItem('ip', 'http://192.168.31.243:8000');
    let ip = localStorage.getItem('ip')
    console.log(ip)
    return await fetch(ip, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(obj)
    }).then(el => el.json()).then(text => {
        console.log(text)
        return {
        user_prompt: obj.text,
        ai_answer: text?.received_data.slice(26,text?.received_data.length -2),
    }}).then(el => {
        let history = JSON.parse(localStorage.getItem('history'))
        console.log(history)
        if(history == null) history = [];
        history.push(el)
        localStorage.setItem('history', JSON.stringify(history))
    })
}
