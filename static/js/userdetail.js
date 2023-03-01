$(document).ready(function(){
    console.log('work')
    //회원 탈퇴하기
    const deleteUserBtn = document.getElementById('deleteUser')
    const id = document.getElementById('id')


    async function deleteUser(){
        console.log('work')
        console.log(id.value)
        await fetch(`/api/user/${id.value}`,{
            method:"DELETE"
        }).then(res => {
            if(res.status===200){
                alert("회원 탈퇴 되었습니다")
                location.href=`/`
            }else if(res.status===400){
                alert('회원 탈퇴에 실패했습니다')
                location.href=`/userdetail`
            }
        })
    }
    deleteUserBtn.onclick = function deleteUserWork(){
        deleteUser()
    }
});