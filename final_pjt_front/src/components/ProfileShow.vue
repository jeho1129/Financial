<template>
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
        <th>Email</th>
        <td>{{ authStore.user.email || "이메일을 설정해주세요" }}</td>
      </tr>
      <tr>
        <th>나이</th>
        <td>{{ authStore.user.age || "나이를 설정해주세요" }}</td>
      </tr>
      <tr>
        <th>현재 가진 금액</th>
        <td>{{ authStore.user.asset || "금액을 설정해주세요" }}</td>
      </tr>
      <tr>
        <th>연봉</th>
        <td>{{ authStore.user.salary || "금액을 설정해주세요" }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
</script>

<style scoped>
th {
  padding: 20px 0 20px 0;
}

td {
  padding: 20px;
}
</style>
