$(document).ready(function(){
    async function logout(){
        console.log("work")
        await fetch(`/api/logout`,{method:'GET'}).then(res => {
            if (res.status===200){
                alert("로그아웃 되었습니다")
                location.href= '/'
            }else if(res.status===400){
                alert("로그아웃 실패")
            }
        })
    }

    logout();
});