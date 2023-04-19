



let container = document.getElementById("container");

let index = 0;

function showMessage(){
    container.innerHTML = index;
    index = index + 1;
}

function retrieveMessage(){
    const res = axios.post('http://127.0.0.1:5555/show').then(result => {
        if(result.data["Status"] == 1){
            let receiver = result.data["Receiver"];
            let text = result.data["Message"];
            container.innerHTML = `Il numero ${receiver} riceve: ${text}`;
        }else{
            container.innerHTML = `<img src="iGen.png">`;
        }
        console.log(result.data["Status"]);
    });
}


window.setInterval(retrieveMessage, 2000);
