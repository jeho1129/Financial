import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";
import { onMounted, ref } from "vue";
import Chart from "./Chart.vue";

export default (() => {
const __VLS_setup = async () => {
const authStore = useAuthStore();
const depositStore = useDepositStore();
const savingStore = useSavingStore();
const router = useRouter();

const findDeposit = ref([]);
const findSaving = ref([]);
const totalProduct = ref([]);

const moveProductDetail = (id) => {
router.push({ name: "depositDetail", params: { depositId: id } });
};

onMounted(() => {
console.logs(authStore.user);
// if (
//   authStore.user.financial_products &&
//   Object.keys(authStore.user.financial_products)
// ) {
//   totalProduct.value = authStore.user.financial_products;
//   findDeposit.value = depositStore.deposit.filter((item) =>
//     Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd)
//   );
//   console.log(findDeposit.value);
//   findSaving.value = savingStore.saving.filter((item) =>
//     Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd)
//   );
// }
});
const __VLS_publicComponent = (await import('vue')).defineComponent({
setup() {
return {};
},
});

const __VLS_componentsOption = {};

let __VLS_name!: 'CkJoinProduct';
function __VLS_template() {
let __VLS_ctx!: InstanceType<import('./__VLS_types.js').PickNotAny<typeof __VLS_publicComponent, new () => {}>> & InstanceType<import('./__VLS_types.js').PickNotAny<typeof __VLS_internalComponent, new () => {}>> & {};
/* Components */
let __VLS_localComponents!: NonNullable<typeof __VLS_internalComponent extends { components: infer C; } ? C : {}> & typeof __VLS_componentsOption & typeof __VLS_ctx;
let __VLS_otherComponents!: typeof __VLS_localComponents & import('./__VLS_types.js').GlobalComponents;
let __VLS_own!: import('./__VLS_types.js').SelfComponent<typeof __VLS_name, typeof __VLS_internalComponent & typeof __VLS_publicComponent & (new () => { $slots: typeof __VLS_slots; }) >;
let __VLS_components!: typeof __VLS_otherComponents & Omit<typeof __VLS_own, keyof typeof __VLS_otherComponents>;
/* Style Scoped */
type __VLS_StyleScopedClasses = {} &
{ 'defaultMyProfile'?: boolean; } &
{ 'searchProduct'?: boolean; } &
{ 'searchProduct'?: boolean; };
let __VLS_styleScopedClasses!: __VLS_StyleScopedClasses | keyof __VLS_StyleScopedClasses | (keyof __VLS_StyleScopedClasses)[];
/* CSS variable injection */
/* CSS variable injection end */
let __VLS_templateComponents!: {} &
import('./__VLS_types.js').WithComponent<'Chart', typeof __VLS_components, 'Chart'>;
__VLS_components.Chart;
// @ts-ignore
[Chart,];
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { class: ("defaultMyProfile p-4"), };
{
({} as JSX.IntrinsicElements).h4;
({} as JSX.IntrinsicElements).h4;
(__VLS_x as JSX.IntrinsicElements)['h4'] = { style: ({}), };
}
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { class: ("d-flex justify-content-between"), };
}
{
({} as JSX.IntrinsicElements).hr;
(__VLS_x as JSX.IntrinsicElements)['hr'] = {};
}
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = {};
{
({} as JSX.IntrinsicElements).h4;
({} as JSX.IntrinsicElements).h4;
(__VLS_x as JSX.IntrinsicElements)['h4'] = {};
}
if (!__VLS_ctx.findDeposit.length) {
// @ts-ignore
[findDeposit,];
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = {};
}
}
else {
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { id: ("searchProducts"), };
for (const [info] of (await import('./__VLS_types.js')).getVForSourceType(__VLS_ctx.findDeposit)) {
// @ts-ignore
[findDeposit,];
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { class: ("searchProduct"), };
type __VLS_0 = JSX.IntrinsicElements['div'];
const __VLS_1: import('./__VLS_types.js').EventObject<typeof undefined, 'click', {}, __VLS_0['onClick']> = {
click: $event => {
__VLS_ctx.moveProductDetail(info.fin_prdt_cd);
}
};
// @ts-ignore
[moveProductDetail,];
{
({} as JSX.IntrinsicElements).p;
({} as JSX.IntrinsicElements).p;
(__VLS_x as JSX.IntrinsicElements)['p'] = {};
(info.fin_prdt_nm);
}
{
({} as JSX.IntrinsicElements).p;
({} as JSX.IntrinsicElements).p;
(__VLS_x as JSX.IntrinsicElements)['p'] = {};
(info.kor_co_nm);
}
}
}
}
}
}
{
({} as JSX.IntrinsicElements).hr;
(__VLS_x as JSX.IntrinsicElements)['hr'] = {};
}
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = {};
{
({} as JSX.IntrinsicElements).h4;
({} as JSX.IntrinsicElements).h4;
(__VLS_x as JSX.IntrinsicElements)['h4'] = {};
}
if (!__VLS_ctx.findSaving.length) {
// @ts-ignore
[findSaving,];
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = {};
}
}
else {
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { id: ("searchProducts"), };
for (const [info] of (await import('./__VLS_types.js')).getVForSourceType(__VLS_ctx.findSaving)) {
// @ts-ignore
[findSaving,];
{
({} as JSX.IntrinsicElements).div;
({} as JSX.IntrinsicElements).div;
(__VLS_x as JSX.IntrinsicElements)['div'] = { class: ("searchProduct"), };
type __VLS_2 = JSX.IntrinsicElements['div'];
const __VLS_3: import('./__VLS_types.js').EventObject<typeof undefined, 'click', {}, __VLS_2['onClick']> = {
click: $event => {
__VLS_ctx.moveProductDetail(info.fin_prdt_cd);
}
};
// @ts-ignore
[moveProductDetail,];
{
({} as JSX.IntrinsicElements).p;
({} as JSX.IntrinsicElements).p;
(__VLS_x as JSX.IntrinsicElements)['p'] = {};
(info.fin_prdt_nm);
}
{
({} as JSX.IntrinsicElements).p;
({} as JSX.IntrinsicElements).p;
(__VLS_x as JSX.IntrinsicElements)['p'] = {};
(info.kor_co_nm);
}
}
}
}
}
}
{
(__VLS_x as import('./__VLS_types.js').ComponentProps<typeof __VLS_templateComponents.Chart>) = {};
}
}
if (typeof __VLS_styleScopedClasses === 'object' && !Array.isArray(__VLS_styleScopedClasses)) {
__VLS_styleScopedClasses['defaultMyProfile'];
__VLS_styleScopedClasses['p-4'];
__VLS_styleScopedClasses['d-flex'];
__VLS_styleScopedClasses['justify-content-between'];
__VLS_styleScopedClasses['searchProduct'];
__VLS_styleScopedClasses['searchProduct'];
}
declare var __VLS_slots: {};
return __VLS_slots;
}
const __VLS_internalComponent = (await import('vue')).defineComponent({
setup() {
return {
Chart: Chart,
findDeposit: findDeposit,
findSaving: findSaving,
moveProductDetail: moveProductDetail,
};
},
});
return {} as typeof __VLS_publicComponent;
};
return {} as typeof __VLS_setup extends () => Promise<infer T> ? T : never;
})({} as any);
