
async function run(){
 let g=document.getElementById('goal').value
 let r=await fetch('/agent/run',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({
   model:'sonar-large',
   messages:[{role:'user',content:g}]
  })
 })
 let j=await r.json()
 let out=''
 j.forEach(x=>{
  out+=`\nSTEP: ${x.task}\nMODEL: ${x.model}\n${x.output}\n`
 })
 document.getElementById('out').innerText=out
}
