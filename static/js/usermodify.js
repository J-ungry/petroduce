$(document).ready(function(){
    const apibtn = document.getElementById('apibtn');
    const nowid = document.getElementById('nowid').value;


    console.log(nowid)
    console.log(newid)


    async function modify(nowid){
        const newid = document.getElementById('newid').value;
        const newpw = document.getElementById('newpw').value;
        const newname = document.getElementById('newname').value;

        const data = {
            newid:newid,
            newpw:newpw,
            newname:newname
        }

        const response = await fetch(`/api/user/modify/${nowid}`,
        {method:"PUT",
        headers: {"Content-Type": "application/json"},
        body:JSON.stringify(data)}).then(window.location.href='/userdetail')
        console.log(response)
    }
    apibtn.onclick = function getApi(){
        modify(nowid)
    }

});