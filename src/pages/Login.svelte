<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  const provider = new GoogleAuthProvider();
  const auth = getAuth();

  // 어떤 동작이 발생할때만 팝업을 띄우기 위해 함수로 만들어줌
  // then catch 구문 (promise) 말고 try catch 구문으로 작성
  const loginWighGoogle = async () => {
    try {
      // 기다렸다가 결과를 가져옴
      const result = await signInWithPopup(auth, provider);
      // credential과 token을 사용해서 새로고침시 로그인정보 유지
      // 결과에서 인증정보를 가져옴
      const credential = GoogleAuthProvider.credentialFromResult(result);
      // 그 안에 있는 토큰을 가져옴
      const token = credential.accessToken;
      // 그 안에 있는 유저정보도 가져옴
      const user = result.user;
      // console.log(user, token);
      user$.set(user);
      // 로컬스토리지에 토큰 저장
      localStorage.setItem("token", token);
    } catch (error) {
      // 에러가 있으면 에러표시
      console.error(error);
    }
  };
</script>

<div>
  <!-- 앞에 $표시를 붙여줘야 그 안에 있는 값을 볼수있음 -->
  <!-- 로그인된 상태면(저장소에 유저값이 있으면) -->
  <!-- {#if $user$}
    유저값의 사용자명을 보여줌
    <div>{$user$.displayName} 로그인됨</div>
  {/if} -->
  <div>로그인하기</div>
  <button class="login-btn" on:click={loginWighGoogle}>
    <img
      class="google-img"
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjzC2JyZDZ_RaWf0qp11K0lcvB6b6kYNMoqtZAQ9hiPZ4cTIOB"
      alt=""
    />
    <div>Google로 시작하기</div>
  </button>
</div>

<style>
  .login-btn {
    width: 200px;
    height: 50px;
    border: 1px solid gray;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    border-radius: 3px;
  }

  .google-img {
    width: 20px;
  }
</style>
