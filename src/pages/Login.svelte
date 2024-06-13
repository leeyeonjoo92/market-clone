<!-- signup 이라는 api로 폼을 보냄 -->
<!-- POST 방식으로 보냄 -->
<form id="login-form" action="/login" method="POST">
  <div>로그인하기</div>
  <div>
    <label for="id">아이디</label>
    <input type="text" id="id" name="id" required />
  </div>
  <div>
    <label for="password">패스워드</label>
    <input type="password" id="password" name="password" required />
  </div>
  <div>
    <button type="submit">로그인</button>
  </div>
  <div id="info"></div>
</form>
