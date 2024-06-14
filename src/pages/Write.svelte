<script>
  import Nav from "../components/Nav.svelte";
  // import { getDatabase, ref, set } from "firebase/database";
  import { getDatabase, ref, push } from "firebase/database";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";

  // 추후에 수정될거기 때문에 let
  let title;
  let price;
  let description;
  let place;
  let files;

  /*---------------------------------
		이미지 업로드 / 다운로드
	----------------------------------*/
  const db = getDatabase();
  const storage = getStorage();

  function writeUserData(imgUrl) {
    // db정보 가져옴
    // set으로 하면 제목이 중복되고 나머지 내용이 다르다면
    // 값이 추가되는게 아니라 업데이트됨
    push(ref(db, "items/"), {
      title: title,
      price: price,
      description: description,
      place: place,
      insertAt: new Date().getTime(),
      imgUrl: imgUrl,
    });
    // 안쓰는 문법임 (귀찮은 ux)
    alert("글쓰기가 완료되었습니다.");
    // 글쓰기 완료 버튼 클릭시 메인으로 이동
    window.location.hash = "/";
  }

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    // 이미지 업로드
    const res = await uploadBytes(imgRef, file);
    // 이미지 다운로드
    // -> 실시간 데이터베이스에 이미지 url 정보도 같이 넣기위해
    const url = await getDownloadURL(imgRef);
    // 지금 이미지 용량이 너무 큰데 이미지 최적화는 과제로 해보기
    return url;
  };

  const handleSubmit = async () => {
    // 업로드된 파일의 url을 받아와서
    const url = await uploadFile();
    // 유저데이터에 url 업데이트
    writeUserData(url);
  };
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <!-- 칼럼 이름과 맞춰줘야 편함 -->
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <!-- bind:value={} -> 이 안에 있는 값을 쟤랑 연동시켜라 -->
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">글쓰기 완료</button>
  </div>
</form>

<Nav location="write" />

<style>
  /* 파일 안에 있는 클래스에만 적용됨 */
  .write-button {
    background-color: tomato;
    margin: 10px;
    border-radius: 10px;
    padding: 5px 12px;
    color: white;
    cursor: pointer;
  }
</style>
