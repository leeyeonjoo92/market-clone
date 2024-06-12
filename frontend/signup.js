const form = document.querySelector("#signup-form");

/*---------------------------------------
 * 	비밀번호 확인 함수
 */
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

/*---------------------------------------
 * 	회원가입 (비밀번호 암호화)
 */
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // console.log(sha256("hi"));
  // name이 password
  // sha256() : 비밀번호 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);
  // console.log(formData.get("password"));

  const div = document.querySelector("#info");

  // 비밀번호 확인했더니 true면
  if (checkPassword()) {
    // 요청 보내기
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });

    // 서버에서 200이 내려왔을때 바꿔줘야함
    const data = await res.json();

    if (data === "200") {
      // div.innerText = "회원가입에 성공했습니다!";
      // div.style.color = "blue";
      // 바로 로그인 페이지로 넘어가지 않게 alert창 추가
      alert("회원 가입에 성공했습니다.");
      // 로그인페이지로 이동
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
