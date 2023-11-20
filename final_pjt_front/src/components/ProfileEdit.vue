<template>
  <form @submit.prevent="editProfile">
    <table>
      <tbody>
        <tr>
          <th>회원번호</th>
          <td>{{ authStore.user.id }}</td>
        </tr>
        <tr>
          <th>이름</th>
          <td>
            {{ authStore.user.name || "이름을 설정해주세요" }}
          </td>
        </tr>
        <tr>
          <th>ID</th>
          <td>{{ authStore.user.username }}</td>
        </tr>
        <tr>
          <th><label for="">Email</label></th>
          <td><input type="email" v-model="editEmail" /></td>
        </tr>
        <tr>
          <th><label for="">나이</label></th>
          <td><input type="number" v-model="editAge" /></td>
        </tr>
        <tr>
          <th><label for="">현재 가진 금액</label></th>
          <td><input type="number" v-model="editAsset" /></td>
        </tr>
        <tr>
          <th><label for="">연봉</label></th>
          <td><input type="number" v-model="editSalary" /></td>
        </tr>
      </tbody>
    </table>
    <button>제출</button>
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

const emit = defineEmits(["editProfile"]);

const editProfile = function () {
  const payload = {
    // password: authStore.password,
    // username: authStore.username,
    // name: authStore.name,
    email: editEmail.value,
    age: editAge.value,
    asset: editAsset.value,
    salary: editSalary.value,
  };
  authStore.editUser(payload);

  emit("editProfile");
};
</script>

<style scoped>
th {
  padding: 20px 0 20px 0;
}

td {
  padding: 20px;
}

input {
  padding: 0;
}
</style>
