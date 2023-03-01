$(document).ready(function(){
    //비밀번호 가입자 정보 확인하고 일치하면 비밀번호 바꾸기 페이지로 넘겨주기
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    
    async function checkUserInfo(){
        const userid = document.getElementById('id');
        const username = document.getElementById('name');

        data = {
            id:userid.value,
            name:username.value
        }

        await fetch(`/api/user/password`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            if(res.status === 200){
                location.href=`/password/2/${userid.value}`
            }else if(res.status ===400){
                alert("이메일, 이름을 다시 확인해주세요")
                location.href=`/password/1`
            }
        })
    }
    changePasswordBtn.onclick = function checkInfo(){
        checkUserInfo();
    }
});