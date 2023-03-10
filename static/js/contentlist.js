$(document).ready(function(){
    const contentList = document.getElementById('contentlist')
    const contentTable = document.getElementById('contentTable');
    const boardId = document.getElementById('boardid');
    const tablebody = document.getElementById('table-body');

    // 게시글 목록 출력하기
    async function callContent(){
        const response = await fetch(`/api/content/${boardId.value}`,{mehtod:'GET'})
        const resp = await response.json()
        const res = resp['res']

        if(res.length ===0 ){
            let div = document.createElement('div');
            div.innerHTML = "게시글이 없습니다 !"
            contentList.appendChild(div)
        } else{
            for(i=0; i<res.length; i++){
                let tr = document.createElement('tr')
                tr.setAttribute('onClick',`location.href='/content/${boardId.value}/${res[i].IDX}'`)
                tr.innerHTML = `<td><button id=${res[i].IDX} class='btn'>${res[i].TITLE}</button></td>`
                let td2 = document.createElement('td');
                td2.innerHTML= res[i].RGS_TIME
                let td3 = document.createElement('td');
                td3.innerHTML = res[i].USR_ID
    
                tr.appendChild(td2)
                tr.appendChild(td3)
    
                tablebody.appendChild(tr)
            }
        }

    }
    //게시글 불러오기
    callContent();

    //게시글 생성하기
    const createBtn = document.getElementById('createBtn')
    const id = document.getElementById('id')
    const contentTitle = document.getElementById('contentTitle')
    const contentText = document.getElementById('contentText')

    async function createContent(){
        data = {
            boardid : boardId.value,
            id: id.innerText,
            contentTitle: contentTitle.value,
            contentText : contentText.value
        }

        await fetch(`/api/content`,{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            if(res.status===200){
                location.href =`/content/${boardId.value}`
            }else if(res.status===400){
                alert("생성 실패")
                location.href = `/content/${boardId.value}`
            }
        })
    }

    createBtn.onclick = function work(){
        createContent()
    }
});