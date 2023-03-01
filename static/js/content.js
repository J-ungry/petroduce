$(document).ready(function(){
    console.log("work")

    const boardid = document.getElementById('boardid')
    const contentId = document.getElementById('contentId')
    const sessionId = document.getElementById('sessionId')
    let printContent = document.getElementById('printContent')
    let comm = document.querySelector('#commentBox')

    console.log(boardid)
    //게시글 출력하기
    async function callContentText(){
        const response = await fetch(`/api/content/${boardid.value}/${contentId.value}`,{method:'GET'})
        const resp = await response.json()
        const res = resp['res']

        
        printContent.innerHTML = `<div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">제목</span>
        <input type="text" id ="contentTitle" name="contentTitle" class="form-control" aria-label="Username" aria-describedby="addon-wrapping" value="${res[0].TITLE}" disable readonly>
    </div>
    <!-- <label for="contentTitle">제목 : </label>
    <input type="text" id="contentTitle" name="contentTitle" value="${res[0].TITLE}"></input> -->
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">작성자</span>
        <input class="form-control" type="text" value="${res[0].USR_ID}" aria-label="Disabled input example" disabled readonly>
    </div>
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">최종작성일</span>
        <input class="form-control" type="text" value="${res[0].RGS_TIME}" aria-label="Disabled input example" disabled readonly>
    </div>
    <div class="input-group flex-nowrap">
        <span class="input-group-text" id="addon-wrapping">내용</span>
        <input type="text" id ="contentText" name="contentText" class="form-control" aria-label="Username" aria-describedby="addon-wrapping" value="${res[0].TEXT}" disabled readonly>
    </div>`

        if(sessionId.value === res[0].USR_ID){
            console.log('work!!!')

            let div = document.createElement('div')
            div.setAttribute("class","buttons")
            let btn = document.createElement('input')
            btn.setAttribute("type","button")
            btn.setAttribute("class","btn btn-primary")
            btn.setAttribute("onclick",`location.href='/content/modify/${boardid.value}/${contentId.value}'`)
            btn.setAttribute("value","수정하기")

            div.append(btn)
            printContent.append(div)

        }

    }
    callContentText()

    //게시글 댓글 출력하기

    async function callComment(){
        const response = await fetch(`/api/comment/${contentId.value}`,{method:'GET'})
        const resp = await response.json()
        const res = resp['res']
        console.log(res)
        if(res.length===0){
            console.log("res")
            comm.innerHTML = `<div>댓글이 없어용</div>`
        }else{
            for(i=0; i<res.length; i++){

                if(sessionId.value===res[i].USR_ID){
                    console.log("수정이 가능해요")
                    comm.innerHTML += ` <div>
                    <label for="commenttext">내용 : </label>
                    <span id="commenttext" name="commenttext">${res[i].TEXT}</span>
                    <label for="commenttext">작성자 : </label>
                    <span id="commenttext" name="commenttext">${res[i].USR_ID}</span>
                    <input type="button" class='btn btn-primary' value="수정하기" id="commentModify" name="">
                    <input type="button" class='btn btn-primary' value="삭제하기" id="commentDelete" name="">
                </div>`
                }else{
                    console.log("수정이 안돼용")
                    comm.innerHTML+= ` <div>
                    <label for="commenttext">내용 : </label>
                    <span id="commenttext" name="commenttext">${res[i].TEXT}</span>
                    <label for="commenttext">작성자 : </label>
                    <span id="commenttext" name="commenttext">${res[i].USR_ID}</span>
                </div>`
                }
            }
            
            console.log('댓글이 있어용')

        }
    }
    callComment();

    console.log(boardid.value)
    console.log(contentId.value)
    //댓글 입력하기
    const inputCommentBtn = document.getElementById('inputCommentBtn')
    console.log(inputCommentBtn)

    async function inputComment(){
        const commentText = document.getElementById('commentText')
        data = {
            CNT_IDX:contentId.value,
            USR_ID:sessionId.value,
            TEXT:commentText.value
        }
        await fetch(`/api/comment`,{
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => {
            console.log(res)
            if(res.status===200){
                alert("댓글 등록 완료")
                location.href = `/content/${boardid.value}/${contentId.value}`
            }else if(res.status===400){
                alert("생성 실패")
                location.href=`/content/${boardid.value}/${contentId.value}`
            }
        })
    }

    inputCommentBtn.onclick = function postComment(){
        inputComment();
    }



});