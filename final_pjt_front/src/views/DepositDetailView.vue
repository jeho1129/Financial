<template>
  <div class="container my-4">
    <div v-if="deposit" class="d-flex flex-column gap-3">
      <div class="depositDetailInfo p-4">
        <h3>{{ deposit.fin_prdt_nm }}</h3>
        <p>{{ deposit.kor_co_nm }}</p>
        <p>#{{ deposit.join_way }}</p>
        <div class="d-flex gap-4">
          <div>
            <p>최고</p>
            <!-- <p>{{ deposit.depositoptions_set }}</p> -->
            <p v-for="option in deposit.depositoptions_set" :key="option.id">연 {{ option.intr_rate2 }}%</p>
          </div>
          <div>
            <p>기본</p>
            <p v-for="option in deposit.depositoptions_set" :key="option.id">
              연 {{ option.intr_rate ?? option.intr_rate2 }}% ({{ option.save_trm }}개월, 세전)
            </p>
          </div>
        </div>
        <div v-if="authStore.user">
          <button v-if="!authStore.user.financial_products || !(depositId in authStore.user.financial_products)" @click="Join" class="px-4 py-2 exChange">
            가입하기
          </button>
          <form v-else @submit.prevent="joinDeposit">
            <button class="px-4 py-2 exChange">가입취소</button>
          </form>
        </div>
      </div>
      <div class="depositDetailInfo p-4">
        <h3>이자 계산기</h3>
        <form v-if="deposit" @submit.prevent="1">
          <div>
            <label for="">예치금액</label>
            <br />
            <input type="number" v-model="amount" />
          </div>
          <!-- <p>{{ deposit.depositoptions_set }}</p> -->
          <div class="select d-flex gap-4 justify-content-center flex-wrap">
            <div
              @click="calculate(amount, option.intr_rate ?? option.intr_rate2, option.save_trm, option.intr_rate_type_nm)"
              v-for="option in deposit.depositoptions_set"
              :key="option.id"
            >
              <input type="radio" v-model="btn" :id="`select${option.id}`" name="shop" :value="option.save_trm" /><label
                :for="`select${option.id}`"
                class="py-3 d-flex flex-column gap-2"
              >
                <p class="m-0">{{ option.save_trm }}개월({{ option.intr_rate_type_nm }})</p>
                <p class="m-0">기본 {{ option.intr_rate ?? option.intr_rate2 }}%</p>
              </label>
            </div>
          </div>
          <div>
            <p class="text-center">{{ amount }}원 예금하면 총 세전 이자 {{ result }}원</p>
          </div>
        </form>
      </div>
      <div class="depositDetailInfo p-4">
        <h3>상품 정보</h3>
        <div>
          <p>가입 대상</p>
          <p>{{ deposit.join_member }}</p>
        </div>
        <hr />
        <div>
          <p>가입 방법</p>
          <p>{{ deposit.join_way }}</p>
        </div>
        <hr />
        <div>
          <p>우대조건</p>
          <p v-for="data in deposit.spcl_cnd.split('\n')" :key="data">
            {{ data }}
          </p>
        </div>
      </div>
      <div class="depositDetailInfo p-4">
        <h3>상품 리뷰</h3>
        <p>리뷰 {{ deposit.depositreviews_count }} ></p>
        <form @submit.prevent="submitComment" class="position-relative">
          <div v-if="authStore.user" class="d-flex">
            <select name="" id="" v-model="rate" class="detailDepositRate">
              <option :value="0" disabled>평점</option>
              <option :value="1">1</option>
              <option :value="2">2</option>
              <option :value="3">3</option>
              <option :value="4">4</option>
              <option :value="5">5</option>
            </select>
            <input type="text" class="detailDepositContent" placeholder="리뷰를 남겨보세요" v-model.trim="inputContent" style="border-radius: 0 5px 5px 0" />
            <button id="submitReviewBtn">
              <font-awesome-icon :icon="['fas', 'pen']" />
            </button>
          </div>
          <div v-else>
            <input
              type="text"
              class="detailDepositContent"
              placeholder="로그인 후 리뷰 작성이 가능해요"
              v-model.trim="inputContent"
              style="border-radius: 5px"
              readonly
            />
          </div>
        </form>
        <div v-for="review in deposit.depositreviews_set" :key="review.id" class="d-flex align-items-center justify-content-between my-3">
          <div>
            <p class="m-0">{{ review.user.username }}</p>
            <p>{{ review.rating }}</p>
            <p class="m-0">{{ review.content }}</p>
            <p class="m-0">
              {{
                new Date(new Date(review.created_at).getTime() + 9 * 60 * 60 * 1000).toISOString().split("T")[0] +
                " " +
                new Date(review.created_at).toTimeString().split(" ")[0]
              }}
            </p>
          </div>
          <div v-if="authStore.user">
            <div class="d-flex align-items-center gap-1" v-if="authStore.user.id === review.user.pk">
              <button id="depositEditButton" :to="{ name: 'update', params: deposit.id }">
                <font-awesome-icon :icon="['far', 'pen-to-square']" class="depositEditButton" />
              </button>
              <button @click="delComment(review.id)" id="reviewDelButton">
                <font-awesome-icon :icon="['far', 'trash-can']" class="reviewDelButton" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <DepositJoin id="moveJoinPage" :deposit="deposit" />
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import DepositJoin from "../components/DepositJoin.vue";
// period ? deposit.depositoptions_set.find((item) => item.save_trm == period).intr_rate2 : 0
const route = useRoute();
const authStore = useAuthStore();
const depositId = route.params.depositId;
const deposit = ref(null);
const rate = ref(0);
const amount = ref(0);
const result = ref(0);
const btn = ref(0);
const inputContent = ref("");

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/deposits/${depositId}/`,
  })
    .then((res) => {
      deposit.value = res.data;
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
});

const joinDeposit = () => {
  if (window.confirm("가입을 취소하시겠습니까?")) {
    axios({
      method: "post",
      url: `${authStore.API_URL}/banking/deposits/${deposit.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
    })
      .then((res) => {
        console.log(res.data.message);
        delete authStore.user.financial_products[deposit.value.fin_prdt_cd];
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

const Join = () => {
  const dialog = document.querySelector("#moveJoinPage");
  dialog.showModal();
};

const submitComment = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/banking/deposits/${depositId}/comments/`,
    data: {
      content: inputContent.value,
      rating: rate.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      deposit.value.depositreviews_set.push(res.data);
      deposit.value.depositreviews_count += 1;
      rate.value = 0;
      inputContent.value = "";
    })
    .catch((err) => {
      console.log(err);
    });
};

const delComment = (id) => {
  axios({
    method: "delete",
    url: `${authStore.API_URL}/banking/deposits/comments/${id}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then(() => {
      const idx = deposit.value.depositreviews_set.findIndex((item) => item.id === id);
      deposit.value.depositreviews_set.splice(idx, 1);
      deposit.value.depositreviews_count -= 1;
    })
    .catch((err) => {
      console.log(err);
    });
};

function calculate(principal, rate, time, method) {
  rate /= 100;
  // console.log(method);
  if (method === "단리") {
    // 예금액 * 이자율 * 기간
    console.log((principal * rate * time) / 12);
    result.value = ((principal * rate * time) / 12).toFixed();
  } else if (method === "복리") {
    // 예금액 * (1 + 이자율) ^ 기간
    result.value = principal * Math.pow(1 + rate, time / 12).toFixed() - principal;
  } else {
    result.value = 0;
  }
}
</script>

<style scoped>
.container {
  width: 700px;
}

.depositDetailInfo {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.exChange {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  width: 100%;
}

.exChange:hover {
  filter: brightness(0.9);
}

input[type="number"] {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 4px;
}

.select {
  padding: 15px 10px;
}
.select input[type="radio"] {
  display: none;
}
.select input[type="radio"] + label {
  display: inline-block;
  cursor: pointer;
  /* height: 24px; */
  width: 90px;
  border: 1px solid lightgray;
  /* line-height: 24px; */
  text-align: center;
  font-weight: bold;
  font-size: 13px;
  background-color: #fff;
  color: #333;
  border-radius: 10px;
}

.select input[type="radio"]:checked + label {
  /* background-color: #333; */
  border: 2px solid #5fb9a6;
  color: #5fb9a6;
}

.detailDepositContent {
  border: 1px solid lightgray;
  width: 100%;
  padding: 15px 10px;
}

.detailDepositRate {
  border: 1px solid lightgray;
  border-radius: 5px 0 0 5px;
  padding: 15px 10px;
}

#submitReviewBtn {
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0px;
  border: 0px;
  font-size: larger;
  background-color: transparent;
  color: #5fb9a6;
  font-weight: bold;
}

#reviewDelButton {
  border: 2px solid red;
  border-radius: 5px;
  background-color: white;
}

.reviewDelButton {
  color: red;
}
#depositEditButton {
  border: 2px solid #5fb9a6;
  border-radius: 5px;
  background-color: white;
}

.depositEditButton {
  color: #5fb9a6;
}
</style>
