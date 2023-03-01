$(document).ready(function(){
    const newpwBtn = document.getElementById('newpwBtn')
    const id = document.getElementById('id')
    async function newPassword(){
        const newpw = document.getElementById('password')

        var regExpPw = /(?=.*\d{1,50})(?=.*[~`!@#$%\^&*()-+=]{1,50})(?=.*[a-zA-Z]{2,50}).{8,50}$/;

        if(regExpPw.test(newpw.value)==false){
            alert("비밀번호는 8자리이상, 영문 2자리이상 숫자, 특수문자를 사용해주세요")
        }else{
            data = {
                pw : newpw.value,
                id : id.value
            }

            await fetch(`/api/user/password`,{
                method:"PETCH",
                headers:{
                    'Content-Type':'application/json'
                },
                body: JSON.stringify(data)
            }).then(res => {
                if(res.status===200){
                    alert("수정 완료 ! 다시 로그인하세요")
                    location.href = `/`
                }else if(res.status===400){
                    alert("수정 실패 !")
                    location.href=`/password/2/${id.value}`
                }
            })
        }
    }
    newpwBtn.onclick = function changePw(){
        newPassword();
    }
});
