let copy =document.querySelector('.copy')


const clipboard = new ClipboardJS(".btn");

clipboard.on('success',(e)=>{
    copy.textContent='Copied!'
    setTimeout(()=>{
       copy.textContent = "Copy";
    },3000)

})
