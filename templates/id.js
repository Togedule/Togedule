function submit(){
  var form = document.forms['form']; // 取得 name 屬性為 form 的表單
  var username = form.elements.id.value("username").value;
  var password = form.elements.id.value("password").value;

  postData("http://127.0.0.1:5500/result/",username)
  postData("http://127.0.0.1:5500/result/",password)

  .then(form=>{
    console.log(form);
  })
}
