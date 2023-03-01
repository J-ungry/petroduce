$(document).ready(function(){
    const inputId = document.getElementById('id')        //아이디 input
    const inputPw = document.getElementById('password')   //비밀번호 input
    const inputName = document.getElementById('name')    //이름 input
    
    const signupBtn = document.getElementById('signupBtn')        //회원가입 버튼



    async function signup(){
        var email = inputId.value
        var exptext = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;
        var regExpPw = /(?=.*\d{1,50})(?=.*[~`!@#$%\^&*()-+=]{1,50})(?=.*[a-zA-Z]{2,50}).{8,50}$/;

        if(exptext.test(email)==false){
            alert("아이디를 이메일 형식으로 작성해주세요")
        } else if(regExpPw.test(inputPw.value)==false){
            alert("비밀번호는 8자리이상, 영문 2자리이상 숫자, 특수문자를 사용해주세요")
        }else{
            data = {
                id : inputId.value,
                password : inputPw.value,
                name: inputName.value
            }
            await fetch(`/api/signup`,{
                method:"POST",
                headers:{
                    'Content-Type':'application/json'
                },
                body: JSON.stringify(data)
            }).then(res => {
                if (res.status === 200){
                    alert("회원가입 완료")
                    location.href = '/';
                } else{
                    alert("동일한 아이디가 존재합니다")
                }
            })
        }


    }

    signupBtn.onclick = function workSignup(){
        signup()
    }

    const checkId = document.getElementById('checkId');

    async function checkUsersId(){
        var exptext = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;

        data = {
            USR_ID : inputId.value
        }

        const response = await fetch(`/api/user`,{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
        const resp = await response.json() 
        const res = resp['res']
        const count = res[0]['COUNT(*)']

        if (count===0){
            if(exptext.test(inputId.value)==false){
                alert("이메일 형식의 아이디를 사용해주세요")
            }else{
                alert("사용 가능한 아이디 입니다")
            }

        }else{
            alert("이미 사용중인 아이디입니다")
        }
    }

    checkId.onclick = function checkUserId(){
        checkUsersId();
    }

    
})
