$(document).ready(function(){

    const boardList = document.getElementById('boardlist')
    const boardTable = document.getElementById('boardTable')
    const tablebody = document.getElementById('table-body');

    // 게시판 목록 출력하기
    async function callBoard(){
        const response = await fetch(`/api/board`,{method:"GET"})
        const resp = await response.json()
        const res = resp['res']

        if(res.length ===0 ){
            let div = document.createElement('div');
            div.innerHTML = "게시판이 없습니다 !"
            boardList.appendChild(div)
        } else{
            for(i=0;i<res.length;i++){
                let tr = document.createElement('tr');
                tr.setAttribute('onClick',`location.href='/content/${res[i].IDX}'`)
                tr.innerHTML = `<th scope="row" boardId="${res[i].boardId}"><button id=${res[i].IDX} class="btn">${res[i].TITLE}</button></th>`

                let td2 = document.createElement('td');
                td2.innerHTML = res[i].RGS_TIME
                let td3 = document.createElement('td');
                td3.innerHTML = res[i].USR_ID
                
                tr.appendChild(td2)
                tr.appendChild(td3)
                tablebody.appendChild(tr)
            }
        }

        
    }

    // 게시판 추가하기 
    callBoard();

    const createBtn = document.getElementById('createBtn')
    const boardName = document.getElementById('boardName') //보드이름
    const id = document.getElementById('id') // 제작자 아이디

    async function createBoard(){
        data = {
            id:id.innerText,
            boardName:boardName.value
        }

        await fetch(`/api/board`,{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            if(res.status===200){
                alert("생성 완료 !")
                location.href = '/boardlist';
            }else if(res.status===400){
                alert("생성 실패 !")
                location.href = '/boardlist';
            }
        })
    }

    createBtn.onclick = function workCreate(){
        createBoard()
    }

});