import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const token = ref(null);
    const API_URL = "http://127.0.0.1:8000";
    const user = ref(null);

    const isAuthenticated = computed(() => {
      return token.value === null ? false : true;
    });

    const router = useRouter();

    const checkUser = () => {
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/ `,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          user.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const editUser = (payload) => {
      const di = {};
      for (const key in payload) {
        if (payload[key]) {
          di[key] = payload[key];
        }
      }
      axios({
        method: "put",
        url: `${API_URL}/accounts/user/ `,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: di,
      })
        .then((res) => {
          user.value.age = res.data.age;
          user.value.email = res.data.email;
          user.value.asset = res.data.asset;
          user.value.salary = res.data.salary;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const signUp = function (payload) {
      const di = {};
      for (const key in payload) {
        if (payload[key]) {
          di[key] = payload[key];
        }
      }

      // const { username, password1, password2, email, name, age, salary, asset } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        data: di,
      })
        .then((res) => {
          console.log("회원가입이 완료되었습니다.");
          // logIn({ username, password: password1 });
        })
        .catch((err) => {
          console.log(err);
        });
      console.log(payload);
    };

    const logIn = function (payload) {
      const { username, password } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key;
          const dialog = document.querySelector("#moveLogInPage");
          dialog.close();
          checkUser();
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
        .then((res) => {
          router.push({ name: "home" });
          token.value = null;
          user.value = null;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return { token, signUp, logIn, isAuthenticated, logOut, user, API_URL, editUser };
  },
  { persist: true }
);
