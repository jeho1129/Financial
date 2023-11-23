<template>
  <dialog @click="closeModal" ref="changePassWordDom">
    <div class="position-relative p-4 heightFull">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeSavingChangeRateDialog">
          <font-awesome-icon
            :icon="['fas', 'xmark']"
            class="closeSavingChangeRateDialog"
          />
        </button>
      </form>
      <h2 class="text-center">금리 정보 변경</h2>
      <form
        @submit.prevent="changeRate"
        class="d-flex flex-column"
        id="savingChangeRateForm"
      >
        <div
          v-for="(option, index) in savingData.savingoptions_set"
          :key="option.id"
          class="d-flex flex-column gap-2"
        >
          <h4 class="m-0">
            {{ option.save_trm }}개월 ({{ option.intr_rate_type_nm }})
          </h4>
          <div>
            <label for="normalRate">기본 금리 </label>
            <br />
            <input
              v-model.trim="savingData.savingoptions_set[index].intr_rate"
              type="number"
              style="width: 100%"
              step="0.01"
              id="save_trm"
              required
            />
          </div>
          <div>
            <label for="bestRate">우대 금리 </label>
            <br />
            <input
              v-model.trim="savingData.savingoptions_set[index].intr_rate2"
              type="number"
              style="width: 100%"
              step="0.01"
              id="bestRate"
              required
            />
          </div>
          <hr />
        </div>
        <button id="changeRateCk" class="px-4 py-2 mt-2">금리 정보 변경</button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const authStore = useAuthStore();
const changePassWordDom = ref(null);

const props = defineProps({
  savingData: Object,
});

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    changePassWordDom.value.close();
  }
};

const changeRate = () => {
  if (window.confirm("금리 정보를 변경 하시겠습니까?")) {
    const data = props.savingData.savingoptions_set.map((item) => {
      return {
        id: item.id,
        intr_rate: item.intr_rate,
        intr_rate2: item.intr_rate2,
      };
    });

    axios({
      method: "put",
      url: `${authStore.API_URL}/banking/savings/change/${props.savingData.fin_prdt_cd}/ `,
      headers: {
        Authorization: `Token ${authStore.token}`,
      },
      data: JSON.stringify({
        savingoptions_set: data,
      }),
    })
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }
};
</script>

<style scoped>
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}

dialog {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  border: 0;
  border-radius: 10px;
  padding: 0;
  height: 500px;
  width: 500px;
}

dialog::-webkit-scrollbar {
  width: 10px; /* 스크롤바의 너비 */
}

dialog::-webkit-scrollbar-thumb {
  background: lightgray; /* 스크롤바의 색상 */
  border-radius: 10px;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.move {
  top: 20px;
  right: 20px;
}

.heightFull {
  height: 100%;
}

#savingChangeRateForm {
  margin: 0 auto;
  padding: 20px 20px 0;
  border-radius: 5px;
}

#changeRateCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bolder;
  position: sticky;
  bottom: 24px;
}

#closeSavingChangeRateDialog {
  border: 0px;
  background-color: transparent;
}

.closeSavingChangeRateDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
