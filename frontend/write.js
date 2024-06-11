const form = document.getElementById("write-form");

/*************************************
 * 	데이터 보내기
 */
const handleSubmitForm = async (event) => {
  event.preventDefault();

  const body = new FormData(form);
  // append("name(컬럼명)", 값)
  // utc 시간 : 세계시각기준으로 보냄
  body.append("insertAt", new Date().getTime());

  // try 안에 있는 로직을 시도해보다가
  try {
    const res = await fetch("/items", {
      method: "POST",
      // 자바스크립트 내장객체 중 폼데이터
      // body: new FormData(form),
      // body: body,
      body,
    });
    // console.log("제출 완료했습니다.");
    const data = await res.json();
    // 글쓰기가 정상적으로 완료되면 루트페이지로 이동
    if (data === "200") window.location.pathname = "/";
    // 에러가 발생하면 이 로직을 실행
  } catch (e) {
    // 콘솔에 에러 띄우기
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);
