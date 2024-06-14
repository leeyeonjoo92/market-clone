<script>
  import Router from "svelte-spa-router";
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    getAuth,
    GoogleAuthProvider,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import Loading from "./pages/Loading.svelte";
  import Mypage from "./pages/Mypage.svelte";

  // const provider = new GoogleAuthProvider();
  // provider.addScope("https://www.googleapis.com/auth/contacts.readonly");

  // let login = false;

  // 로그인돼있을때 새로고침하면 로그인페이지가 잠깐보였다가 넘어감
  // 처음 로딩됐을때는 true값을 가지고있다가
  let isLoading = true;

  const auth = getAuth();

  const checkLogin = async () => {
    const token = localStorage.getItem("token");
    // 토큰이 없으면 아무동작도 하지 않음
    // 처음 로딩된 이후에는 false로 바꿔줌
    if (!token) return (isLoading = false);

    // credential(idToken, access token) -> id토큰 없으니까 null로 넘겨줌
    // 토큰을 바탕으로 인증을 진행
    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);
    // 유저정보를 가져옴
    const user = result.user;
    // 유저스토어에 업데이트
    user$.set(user);
    // 처음 로딩된 이후에는 false로 바꿔줌
    isLoading = false;
  };

  const routes = {
    "/": Main,
    // "/login": Login,
    "/signup": Signup,
    "/write": Write,
    "/my": Mypage,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loading />
  <!-- 로그인 안돼있으면 (유저스토어에 값이 없으면) -->
{:else if !$user$}
  <!-- 로그인페이지 보여주고 -->
  <Login />
  <!-- 로그인돼있으면 (유저스토어에 값이 있으면) -->
{:else}
  <!-- router 보여주기 -->
  <Router {routes} />
{/if}
