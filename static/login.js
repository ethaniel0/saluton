
function toggle(){
  let s = document.getElementById('switch');
  if (s.classList.contains('onLogin')){
    s.classList.remove('onLogin');
    s.innerHTML = `Don't have an account? <a class='text-blue-600 cursor-pointer' onclick="toggle()">Sign Up</a>`;
    document.getElementById('hpassconf').classList.add('hidden');
    document.getElementById('passConfirm').classList.add('hidden');
    document.getElementById('signin').innerHTML = "Sign In";
  }
  else {
    s.classList.add('onLogin');
    s.innerHTML = `Have an account? <a class='text-blue-600 cursor-pointer' onclick="toggle()">Log In</a>`;
    document.getElementById('hpassconf').classList.remove('hidden');
    document.getElementById('passConfirm').classList.remove('hidden');
    document.getElementById('signin').innerHTML = "Sign Up";
  }
}