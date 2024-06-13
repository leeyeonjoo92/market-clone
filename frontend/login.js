const form = document.querySelector("#login-form");

/*---------------------------------------
 * 	로그인 (유저데이터 확인)
 */
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  // name이 password
  // sha256() : 비밀번호 암호화
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  // 요청 보내기
  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });

  // 서버에서 200이 내려왔을때 바꿔줘야함
  const data = await res.json();
  const accessToken = data.access_token;
  // 로컬스토리지에 액세스토큰 저장
  window.localStorage.setItem("token", accessToken);
  // window.sessionStorage.setItem("token", accessToken);
  alert("로그인되었습니다.");

  // 서버에서 data로 내려주는 값과 res.status는 다름
  // 서버 data값은 "200"이라는 문자열이 있는지 확인
  // res.status는 200이라는 숫자 -> 정상적으로 동작중이라는 의미
  // res.status는 main.py 서버에서 내려줌
  // if (res.status === 200) {
  //   alert("로그인에 성공했습니다!");
  //   // console.log(res.status);
  //   window.location.pathname = "/";
  // } else if (res.status === 401) {
  //   alert("id 혹은 password가 틀렸습니다.");
  // }
  // const infoDiv = document.querySelector("#info");
  // infoDiv.innerText = "로그인되었습니다";

  window.location.pathname = "/";

  // const btn = document.createElement("button");
  // btn.innerText = "상품 가져오기";
  // btn.addEventListener("click", async () => {
  //   const res = await fetch("/items", {
  //     // 로그인하고 상품가져오기 누르면 401 에러뜸
  //     // -> 로그인을 하고나면 서버는 우리가 누군지 모름
  //     // -> 헤더에 액세스토큰을 같이 넣어서 보내줘야함
  //     headers: {
  //       // Bearer라는 프리픽스를 넣어줘야함
  //       Authorization: `Bearer ${accessToken}`,
  //     },
  //   });
  //   const data = await res.json();
  //   console.log(data);
  // });
  // infoDiv.appendChild(btn);
};

form.addEventListener("submit", handleSubmit);
