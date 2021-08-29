var socket = io();
socket.on('connect', parts => {
  if (!parts) return;
  console.log(parts);
  let {texts, senders} = parts;
  for (let i = 0; i < texts.length; i++) makeText(senders[i] == 's', texts[i]);
});

let typing = document.getElementById('typing');
typing.addEventListener('keydown', e => {
  console.log('keydown', e.keyCode);
  if (e.keyCode == 13){
    socket.emit('newMessage', typing.value);
    typing.value = '';
  }
});

socket.on('message', parts => {
  makeText(parts.sent, parts.text);
})

function makeText(sent, text){
  let texts = document.getElementById('texts');
  texts.innerHTML += `<p class="text self-${sent ? 'end' : 'start'} p-6 rounded-2xl text-xl bg-${sent ? 'blue-300' : 'gray-300'} mb-1" ${sent ? '' : 'style="background-color: #f59e9b"'}>${text}</p>`;
  texts.scrollIntoView({ behavior: "smooth", block: "end" });
}

