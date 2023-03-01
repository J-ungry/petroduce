$(document).ready(function(){
    console.log('work')
    const inputId = document.getElementById('id')        //아이디 input
    const inputPw = document.getElementById('password')   //비밀번호 input
    
    const loginBtn = document.getElementById('loginBtn')        //로그인 버튼



    async function login(){
        data = {
            id : inputId.value,
            password : inputPw.value
        }
        console.log("work!!!")
        await fetch(`/api/login`,{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            if (res.status === 200){
                alert("로그인 완료 데수")
                location.href = '/boardlist';
            } else{
                alert("로그인 실패")
                location.href = '/';
            }
        })
    }

    loginBtn.onclick = function workLogin(){
        login()
    }
    
})
