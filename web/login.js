let login = document.getElementById("login");
let signup = document.getElementById("signup");
let slide = document.getElementById("slide");
let signinForm = document.querySelector(".signin-form");
let signupForm = document.querySelector(".signup-form");

document.getElementById("login").addEventListener("click", () =>
{
  slide.classList.add("slide-left");
  slide.classList.remove("slide-right");
  signinForm.style.zIndex = "2";
  signinForm.style.opacity = "1";
});

signup.addEventListener("click", () => {
  slide.classList.add("slide-right");
  slide.classList.remove("slide-left");
  signinForm.style.zIndex = "-1";
  signinForm.style.opacity = "0";
});
function checker(form)
{
  if(form.passw.value!=form.cpassw.value){
    alert("Password and the confirmation donot match. Please verify it!!");
  }
}
function check(form)/*function to check userid & password*/
{
 /*the following code checkes whether the entered userid and password are matching*/
 if(form.userid.value == "anish@gmail.com" && form.pswrd.value == "test" ||form.userid.value == "aravindpusuluri10@gmail.com" && form.pswrd.value == "test")
  {
    generateNewPage()/*opens the target page while Id & password matches*/
  }
 else
 {
   alert("Invalid Credentials, Please try again")/*displays error message*/
  }
}
