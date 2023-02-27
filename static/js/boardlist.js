
$(document).ready(function(){
    console.log('work')
    const boardTable = document.getElementById('boardlist')
    const board = document.querySelector('#boardTable')
    console.log(boardTable)
    
    
    //게시판 목록 출력 함수
    async function callBoardList(){
        const response  = await fetch(`/api/board`)
        const resp = await response.json();
        console.log(resp)
        
        for(i=0; i<resp.length;i++){
            console.log(resp[i].boardName)
            let tr = document.createElement('tr');
            tr.innerHTML = `<td onclick='location.href="/api/contentlist/${resp[i].boardId}"'>${resp[i].boardName}</td>`

            // let td1 = document.createElement('td');
            // td1.innerHTML = resp[i].boardname
            // td1.onclick = `location.href="/api/content/${resp[i].boardid}"`

            let td2 = document.createElement('td');
            td2.innerHTML = resp[i].boardDate
            let td3 = document.createElement('td');
            td3.innerHTML = resp[i].id
    
            // tr.appendChild(td1);
            tr.appendChild(td2);
            tr.appendChild(td3);
    
            console.log(tr)
            boardTable.appendChild(tr);
            
        }
    }
    
    callBoardList();
});

