/*******************************************
 * 	서버에서 데이터 받아서 페이지 만들기
 ******************************************/
/*-----------------------------------
 *	시간 함수
 * 	(현재시간과 작성시간 차이)
 */
const calcTime = (timestamp) => {
  // 세계시간 +9시간 해서 한국시간으로 계산됨
  // 세계시간으로 맞추기 위해 9시간 빼기
  // 9*60*60*1000 -> 9시간*60분*60초*밀리세컨드
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const minute = time.getMinutes();
  const second = time.getSeconds();

  if (hour > 0) return `${hour}시간 전`;
  else if (minute > 0) return `${minute}분 전`;
  else if (second > 0) return `${second}초 전`;
  else "방금 전";
};

/*-----------------------------------
 *	blob타입 이미지 이미지형식으로
 */

/*-----------------------------------
 *	데이터 렌더링하기
 */
const renderData = (data) => {
  const main = document.querySelector("main");

  // 최신글이 위로 올라오게
  // reverse() -> 배열을 뒤집어 주는 메소드
  data.reverse().forEach(async (obj) => {
    // console.log(obj);
    const div = document.createElement("div");
    div.className = "item-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    // 블롭 타입으로 바꿔줌
    const blob = await res.blob();
    // URL 객체에 블롭타입을 url로 바꿔주는 메소드 사용
    const url = URL.createObjectURL(blob);
    img.src = url;

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "item-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "item-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);
    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);
    main.append(div);
  });
};

/*-----------------------------------
 *	데이터 받기
 */
const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  // console.log(data);
  renderData(data);
};

fetchList();
