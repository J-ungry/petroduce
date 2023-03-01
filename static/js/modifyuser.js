$(document).ready(function(){
    
    //회원 정보를 뿌려줘야하고 
    let userInfo = document.getElementById('userInfo')
    const sessionId= document.getElementById('sessionId') //아이디 가져오기

    async function callUser(){
        const response = await fetch(`/api/user/${sessionId.value}`,{method:"GET"})
        const resp = await response.json()
        const res = resp['res']

        userInfo.innerHTML = `<div class="modi-info">
        <label for="id">이메일(id)  </label>
        <span type="text" name="id" id="id">${res[0].USR_ID}</span></br>
    </div>
    <div class="modi-info">
        <label for="name">이름</label>
        <input type="text" name="name" id="name" value="${res[0].USR_NAME}">
    </div>`
    }

    callUser()
    //수정 버튼 눌렀을때 처리를 해줘야한다
    const modifyUserBtn = document.getElementById('modifyUserBtn')
    
    async function modifyUser(){
        const id = document.getElementById("id").innerText
        const newname = document.getElementById('name').value

        data = {
            id:id,
            name:newname
        }

        await fetch(`/api/user`,{
            method:"PETCH",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res =>{
            if(res.status===200){
                alert('수정 완료 !')
                location.href = `/userdetail`
            }else if(res.status===400){
                alert("수정 실패 !")
                location.href =`/userdetail`
            }
        })
    }
    modifyUserBtn.onclick = function modifyUserWork(){
        modifyUser();
    }

});