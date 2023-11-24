<template>
  <form class="defaultMyProfile p-4" @submit.prevent="editProfile">
    <div class="d-flex justify-content-between">
      <h4>기본 정보 수정</h4>
      <button class="p-2" id="moveProfile">수정하기</button>
      <!-- <button v-else @click="dddd" class="p-2" id="moveProfile">수정하기</button> -->
    </div>
    <div class="d-flex align-items-center gap-4">
      <img src="../assets/profile.jpg" alt="" />
      <p class="m-0">{{ authStore.user.name || "admin" }}</p>
    </div>
    <hr />
    <table>
      <tbody>
        <tr>
          <th>아이디</th>
          <td>{{ authStore.user.username }}</td>
        </tr>
        <tr>
          <th>이메일</th>
          <td><input type="email" v-model.trim="editEmail" min="0" /></td>
        </tr>
        <tr>
          <th>비밀번호</th>
          <td style="font-size: 10px" class="d-flex gap-1"><font-awesome-icon v-for="a in 6" :key="a" :icon="['fas', 'circle']" /></td>
        </tr>
        <tr>
          <th>나이</th>
          <td><input type="number" v-model.trim="editAge" min="0" /></td>
        </tr>
        <tr>
          <th>직업</th>
          <td>
            <select v-model.trim="editJob">
              <option value="" disabled>직업 선택하기</option>
              <option
                :value="data"
                style="width: 100%"
                v-for="data in ['공무원', '변호사', '의사', '회사원', '엔지니어', '개발자', '교수', '간호사']"
                :key="data"
              >
                {{ data }}
              </option>
            </select>
          </td>
        </tr>
        <tr>
          <th>자산</th>
          <td><input type="number" v-model.trim="editAsset" min="0" /></td>
        </tr>
        <tr>
          <th>연봉</th>
          <td><input type="number" v-model.trim="editSalary" min="0" /></td>
        </tr>
      </tbody>
    </table>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

const editEmail = ref(authStore.user.email);
const editAge = ref(authStore.user.age);
const editAsset = ref(authStore.user.asset);
const editSalary = ref(authStore.user.salary);
const editJob = ref(authStore.user.job);

const emit = defineEmits(["editProfile"]);

const editProfile = function () {
  if (window.confirm("회원정보를 수정하시겠습니까?")) {
    const payload = {
      // password: authStore.password,
      // username: authStore.username,
      // name: authStore.name,
      email: editEmail.value,
      age: editAge.value,
      asset: editAsset.value,
      salary: editSalary.value,
      job: editJob.value,
    };

    console.log(payload);
    authStore.editUser(payload);
  }
  emit("editProfile");
};
</script>

<style scoped>
.defaultMyProfile {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

#moveProfile {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

#moveProfile:hover {
  filter: brightness(0.9);
}

img {
  width: 60px;
  border-radius: 50%;
}

td {
  padding: 10px;
}

input,
select {
  padding: 0 0 0 10px;
  width: 200px;
  border: 1px solid lightgray;
  border-radius: 5px;
}
</style>
