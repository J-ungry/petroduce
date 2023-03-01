$(document).ready(function(){
    const boardid = document.getElementById('boardid')
    const contentId = document.getElementById('contentId')
    const sessionId = document.getElementById('sessionId')
    let printContent = document.getElementById('printContent')

    //우선 출력해주고
    async function printContentText(){
        const response = await fetch(`/api/content/${boardid.value}/${contentId.value}`,{method:'GET'})
        const resp = await response.json()
        const res = resp['res']

        printContent.innerHTML = ` <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">제목</span>
        <input type="text" id ="contentTitle" name="contentTitle" class="form-control" aria-label="Username" aria-describedby="addon-wrapping" value="${res[0].TITLE}">
    </div>
    <!-- <label for="contentTitle">제목 : </label>
    <input type="text" id="contentTitle" name="contentTitle" value="${res[0].TITLE}"></input> -->
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">작성자</span>
        <input class="form-control" type="text" placeholder="${res[0].USR_ID}" aria-label="Disabled input example" disabled readonly>
    </div>
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">최종작성일</span>
        <input class="form-control" type="text" placeholder="${res[0].RGS_TIME}" aria-label="Disabled input example" disabled readonly>
    </div>
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">내용</span>
        <input type="text" id ="contentText" name="contentText" class="form-control" aria-label="Username" aria-describedby="addon-wrapping" value="${res[0].TEXT}">
    </div>
`
    }

    printContentText()

    //수정내용 보내는거랑
    const modifyContentBtn = document.getElementById('modifyContent')

    async function modifyContent(){
        const contentTitle = document.getElementById('contentTitle')
        const contentText = document.getElementById('contentText')
        // const now = new Date();

        data = {
            contentTitle:contentTitle.value,
            contentText:contentText.value
        }

        await fetch(`/api/content/${boardid.value}/${contentId.value}`,{
            method:"PETCH",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            if(res.status===200){
                location.href = `/content/${boardid.value}/${contentId.value}`
            }else if(res.status===400){
                alert("수정 실패 !")
                location.href = `/content/${boardid.value}/${contentId.value}`
            }

        })


    }
    modifyContentBtn.onclick = function modifyWork(){
        modifyContent();
    }

    //삭제하기
    const deleteContentBtn = document.getElementById('deleteContent')

    async function deleteContent(){
        await fetch(`/api/content/${boardid.value}/${contentId.value}`,{
            method:'DELETE'
        }).then(res => {
            if(res.status===200){
                alert('삭제 완료')
                location.href=`/content/${boardid.value}`
            }else if(res.status===400){
                alert('삭제 실패 !')
                location.href=`/content/${boardid.value}/${contentId.value}`
            }
        })
    }

    deleteContentBtn.onclick = function deleteWork(){
        deleteContent()
    }
})
// onclick="/api/content/${boardid}/${contentId}"