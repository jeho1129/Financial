<template>
  <div>
    <div id="map" class="position-relative">
      <div class="z-3 aaa">
        <div style="position: sticky" class="top-0" id="bankSearch">
          <div id="bankSearchTitle">은행 찾기</div>
          <div class="d-flex flex-column p-3 gap-3">
            <select v-model="state">
              <option value="">지역 전체</option>
              <option v-for="city in Object.keys(cities)">
                {{ city }}
              </option>
            </select>
            <select v-model="city">
              <option value="">시/군/구 전체</option>
              <option v-for="city in cities[state]" :key="city">
                {{ city }}
              </option>
            </select>
            <button @click="geo">검색</button>
            <!-- <select value="">
        <option value="" >지역선택하기</option>
        <option
          v-for="bank in Array.from(new Set(bankCategory))"
          :key="bank"
          name=""
          id=""
        >
          {{ bank }}
        </option>
      </select> -->
          </div>
          <hr class="m-0" />
        </div>
        <div v-for="bank in bankList" class="m-3" @click="aaa(bank.x, bank.y, bank)">
          <p>{{ bank.place_name }}</p>
          <p>{{ bank.address_name }}</p>
          <p>{{ bank.phone || "전화번호 없음" }}</p>
          <hr />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const state = ref("");
const city = ref("");
const geocoder = ref("");
const bankCategory = ref([]);
const bankList = ref([]);

const ma = ref(126.879717024296);
const la = ref(35.2091686314065);

const cities = {
  서울특별시: [
    "종로구",
    "중구",
    "용산구",
    "성동구",
    "광진구",
    "동대문구",
    "중랑구",
    "성북구",
    "강북구",
    "도봉구",
    "노원구",
    "은평구",
    "서대문구",
    "마포구",
    "양천구",
    "강서구",
    "구로구",
    "금천구",
    "영등포구",
    "동작구",
    "관악구",
    "서초구",
    "강남구",
    "송파구",
    "강동구",
  ],
  세종특별자치시: ["세종시"],
  부산광역시: [
    "중구",
    "서구",
    "동구",
    "영도구",
    "부산진구",
    "동래구",
    "남구",
    "북구",
    "해운대구",
    "사하구",
    "금정구",
    "강서구",
    "연제구",
    "수영구",
    "사상구",
    "기장군",
  ],
  대구광역시: ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"],
  인천광역시: ["중구", "동구", "미추홀구", "연수구", "남동구", "부평구", "계양구", "서구", "강화군", "옹진군"],
  광주광역시: ["동구", "서구", "남구", "북구", "광산구"],
  대전광역시: ["동구", "중구", "서구", "유성구", "대덕구"],
  울산광역시: ["중구", "남구", "동구", "북구", "울주군"],
  경기도: [
    "고양시",
    "수원시",
    "용인시",
    "과천시",
    "광명시",
    "광주시",
    "구리시",
    "군포시",
    "김포시",
    "남양주시",
    "동두천시",
    "부천시",
    "성남시",
    "시흥시",
    "안산시",
    "안성시",
    "안양시",
    "양주시",
    "여주시",
    "오산시",
    "의왕시",
    "의정부시",
    "이천시",
    "파주시",
    "평택시",
    "포천시",
    "하남시",
    "화성시",
    "가평군",
    "양평군",
    "연천군",
  ],
  강원도: [
    "강릉시",
    "동해시",
    "삼척시",
    "속초시",
    "원주시",
    "춘천시",
    "태백시",
    "고성군",
    "양구군",
    "양양군",
    "영월군",
    "인제군",
    "정선군",
    "철원군",
    "평창군",
    "홍청군",
    "화천군",
    "횡성군",
  ],
  충청북도: ["제천시", "청주시", "충주시", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "증평군", "진천군"],
  충청남도: [
    "계룡시",
    "공주시",
    "논산시",
    "당진시",
    "보령시",
    "서산시",
    "아산시",
    "천안시",
    "금산군",
    "부여군",
    "서천군",
    "예산군",
    "청양군",
    "태안군",
    "홍성군",
  ],
  전라북도: ["군산시", "김제시", "남원시", "익산시", "전주시", "정읍시", "고창군", "무주군", "부안군", "순창군", "완주군", "임실군", "장수군", "진안군"],
  전라남도: [
    "광양시",
    "나주시",
    "목포시",
    "순천시",
    "여수시",
    "강진군",
    "고흥군",
    "곡성군",
    "구례군",
    "담양군",
    "무안군",
    "보성군",
    "신안군",
    "영광군",
    "영암군",
    "완도군",
    "장성군",
    "장흥군",
    "진도군",
    "함평군",
    "해남군",
    "화순군",
  ],
  경상북도: [
    "경산시",
    "경주시",
    "구미시",
    "김천시",
    "문경시",
    "상주시",
    "안동시",
    "영주시",
    "영천시",
    "포항시",
    "고령군",
    "군위군",
    "봉화군",
    "성주군",
    "영덕군",
    "영양군",
    "예천군",
    "울릉군",
    "울진군",
    "의성군",
    "청도군",
    "청송군",
    "칠곡군",
  ],
  경상남도: [
    "창원시",
    "거제시",
    "김해시",
    "밀양시",
    "사천시",
    "양산시",
    "진주시",
    "통영시",
    "거창군",
    "고성군",
    "남해군",
    "산청군",
    "의령군",
    "창녕군",
    "하동군",
    "함안군",
    "함양군",
    "합천군",
  ],
  제주특별자치도: ["서귀포시", "제주시"],
};

let map = null;
let infowindow = null;
let ps = null;
const markers = ref([]);
let infowindows = ref([]);

const initMap = () => {
  const container = document.getElementById("map");
  geocoder.value = new kakao.maps.services.Geocoder();
  const options = {
    center: new kakao.maps.LatLng(la.value, ma.value),
    level: 3,
  };
  // 지도 객체를 등록합니다.
  // 지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
  map = new kakao.maps.Map(container, options);

  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
  ps = new kakao.maps.services.Places(map);
  ps.categorySearch("BK9", placesSearchCB, { useMapBounds: true });
};

// // 키워드 검색 완료 시 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
  if (status === kakao.maps.services.Status.OK) {
    bankList.value = [];
    for (let i = 0; i < data.length; i++) {
      if (data[i].category_name.split(" > ")[3] !== "ATM") {
        displayMarker(data[i]);
        bankList.value.push(data[i]);
        bankCategory.value.push(data[i].category_name.split(" > ")[3]);
      }
    }
  }
}

// // 지도에 마커를 표시하는 함수입니다
function displayMarker(place) {
  // 마커를 생성하고 지도에 표시합니다
  var marker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(place.y, place.x),
  });

  markers.value.push(marker);
  // console.log(marker);

  //   // 마커에 클릭이벤트를 등록합니다
  kakao.maps.event.addListener(marker, "click", function () {
    // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
    infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + "</div>");
    infowindow.open(map, marker);
    infowindows.value.push(infowindow);
  });

  kakao.maps.event.addListener(marker, "click", function () {
    removeInfowindow();
    removeMarker();
    map.setCenter(new kakao.maps.LatLng(place.y, place.x));
    map.setLevel();
    ps = new kakao.maps.services.Places(map);
    ps.categorySearch("BK9", placesSearchCB, { useMapBounds: true });
    infowindow.open(map, marker);
  });

  kakao.maps.event.addListener(map, "click", function () {
    infowindow.close();
  });
}

const aaa = (x, y, marker) => {
  var coords = new kakao.maps.LatLng(y, x);
  la.value = coords.La;
  ma.value = coords.Ma;
  removeInfowindow();
  map.setCenter(new kakao.maps.LatLng(ma.value, la.value));
};

onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap();

    // console.log("if b", infowindow);
  } else {
    const script = document.createElement("script");
    /* global kakao */
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=41e58afe859c2949686e1c1b46012a3f&libraries=services`;
    document.head.appendChild(script);
    script.onload = () => {
      kakao.maps.load(initMap);
    };
  }
});

const removeMarker = () => {
  for (let i = 0; i < markers.value.length; i++) {
    markers.value[i].setMap(null);
  }
  markers.value = [];
};

const removeInfowindow = () => {
  for (var i = 0; i < infowindows.value.length; i++) {
    infowindows.value[i].close();
  }
};

const geo = () => {
  if (city.value && state.value) {
    geocoder.value.addressSearch(`${state.value} ${city.value}`, function (result, status) {
      // 정상적으로 검색이 완료됐으면
      if (status === kakao.maps.services.Status.OK) {
        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
        la.value = coords.La;
        ma.value = coords.Ma;
        removeMarker();
        removeInfowindow();
        map.setCenter(new kakao.maps.LatLng(ma.value, la.value));
        map.setLevel(3);

        infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
        ps = new kakao.maps.services.Places(map);
        ps.categorySearch("BK9", placesSearchCB, { useMapBounds: true });
      }
    });
  } else {
    removeMarker();
    removeInfowindow();
    map.setLevel();
    // infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    ps = new kakao.maps.services.Places(map);
    ps.categorySearch("BK9", placesSearchCB, { useMapBounds: true });
  }

  city.value = "";
  state.value = "";
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 90vh;
}

.aaa {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.8);
  width: 330px;
  border-radius: 10px;
  top: 20px;
  bottom: 20px;
  left: 20px;
  overflow: auto;
}

.aaa::-webkit-scrollbar {
  width: 10px; /* 스크롤바의 너비 */
}

.aaa::-webkit-scrollbar-thumb {
  background: lightgray; /* 스크롤바의 색상 */
  border-radius: 10px;
}

#bankSearchTitle {
  background-color: #5fb9a6;
  text-align: center;
  padding: 20px;
  border-radius: 10px;
  font-weight: bolder;
}

#bankSearch {
  background-color: white;
  opacity: 1;
}

select {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 4px;
  /* box-sizing: border-box; */
}

button {
  color: #5fb9a6;
  background-color: white;
  border: 1px solid #5fb9a6;
  padding: 5px;
  border-radius: 10px;
  font-weight: bolder;
}
</style>
