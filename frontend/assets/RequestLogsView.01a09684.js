import{P as w,v as b}from"./vue-debounce.min.6e53b092.js";import{D as q}from"./datetime.ba57e231.js";import{e as _,f as h,o,g as D,h as p,T as L,c as i,a as e,b as n,v as m,j as r,F as g,i as V,k as v,t as a,d as f}from"./index.9eb82cac.js";import{_ as T}from"./_plugin-vue_export-helper.cdc0426e.js";import"./_commonjsHelpers.f037b798.js";const R={computed:{DateTime(){return q}},components:{Paginate:w},data(){return{logs:[],page:1,page_count:1,results_count:0,limit:15,query:"",export_download:"",export_rows:1e3,isLoading:!0}},methods:{updateFilter(){this.page=1,this.getLogs()},getLogs(){fetch("/api/requests?page="+this.page+"&limit="+this.limit+"&query="+this.query).then(c=>c.json()).then(c=>{this.logs=c.results,this.page_count=c.page_count,this.results_count=c.results_count,this.isLoading=!1})}},directives:{debounce:b.exports.vue3Debounce({lock:!0})},created(){this.getLogs()}},F={key:0},N={class:"box"},P=e("h1",{class:"title"},"Request Logs",-1),S={class:"tile is-ancestor"},B={class:"tile is-parent is-6"},C={class:"tile is-child"},U={class:"field"},A=e("label",{class:"label"},"Search",-1),E={class:"control"},I={class:"tile is-parent is-3"},M={class:"tile is-child"},j={class:"field"},O=e("label",{class:"label"},"Export Rows To CSV",-1),H={class:"control"},z=["href"],G=e("span",{class:"icon"},[e("i",{class:"fas fa-file-export"})],-1),J=e("span",null,"Export",-1),K=[G,J],Q={class:"table is-fullwidth is-hoverable"},W=e("thead",null,[e("tr",null,[e("th",{style:{width:"16%"}},"Date"),e("th",{style:{width:"15%"}},"Hostname"),e("th",{style:{width:"20%"}},"Path"),e("th",{style:{width:"15%"}},"IP Address"),e("th",{style:{width:"24%"}},"User Agent"),e("th",{style:{width:"5%"}},"Allowed"),e("th",{style:{width:"5%"}},"Details")])],-1),X={key:0,class:"is-truncated"},Y={key:1,class:"is-truncated has-text-danger"},Z={class:"is-truncated"},$={class:"is-truncated"},ee={class:"has-text-centered"},te={class:"icon"},se={key:0,class:"fas fa-circle-check has-text-success","aria-hidden":"true"},oe={key:1,class:"fas fa-circle-xmark has-text-danger","aria-hidden":"true"},ie={class:"has-text-centered"},ne=e("span",{class:"icon"},[e("i",{class:"fas fa-circle-info"})],-1),ae=e("span",null,"View",-1),re={class:"pagination is-centered",role:"navigation","aria-label":"pagination"},le={class:"columns is-centered"};function ce(c,d,de,ue,s,u){const x=_("RouterLink"),y=_("paginate"),k=h("debounce"),l=h("tooltip");return o(),D(L,null,{default:p(()=>[s.isLoading===!1?(o(),i("div",F,[e("div",N,[P,e("div",S,[e("div",B,[e("div",C,[e("div",U,[A,e("div",E,[n(e("input",{class:"input",type:"text","onUpdate:modelValue":d[0]||(d[0]=t=>s.query=t),placeholder:"example.com"},null,512),[[m,s.query],[k,u.updateFilter,"250ms"]])])])])]),e("div",I,[e("div",M,[e("div",j,[O,e("div",H,[n(e("input",{class:"input",type:"text",placeholder:"1000","onUpdate:modelValue":d[1]||(d[1]=t=>s.export_rows=t),style:{"max-width":"25%"},maxlength:"10"},null,512),[[m,s.export_rows]]),r(" \xA0 "),e("a",{class:"button is-link is-outlined",href:"/api/requests?&limit="+s.export_rows+"&query="+s.query+"&export=1"},K,8,z)])])])])]),e("table",Q,[W,e("tbody",null,[(o(!0),i(g,null,V(s.logs,t=>n((o(),i("tr",{key:t.id},[n((o(),i("td",null,[r(a(u.DateTime.fromISO(t.datetime).toFormat("yyyy-MM-dd hh:mm:ss")),1)])),[[l,t.datetime,void 0,{top:!0}]]),t.redirector_hostname?n((o(),i("td",X,[r(a(t.redirector_hostname),1)])),[[l,t.redirector_hostname,void 0,{top:!0}]]):n((o(),i("td",Y,[r(a(t.request_hostname),1)])),[[l,t.redirector_hostname,void 0,{top:!0}]]),n((o(),i("td",Z,[r(a(t.redirector_path),1)])),[[l,t.redirector_path,void 0,{top:!0}]]),n((o(),i("td",null,[r(a(t.request_ip)+" ",1),t.request_country_code?(o(),i(g,{key:0},[r("("+a(t.request_country_code)+")",1)],64)):f("",!0)])),[[l,t.request_asn_org_name,void 0,{top:!0}]]),n((o(),i("td",$,[r(a(t.request_user_agent),1)])),[[l,t.request_user_agent,void 0,{top:!0}]]),e("td",ee,[e("span",te,[t.allowed===!0?(o(),i("i",se)):(o(),i("i",oe))])]),e("td",ie,[v(x,{class:"button is-link is-outlined",to:{name:"request-log",params:{id:t.id}}},{default:p(()=>[ne,ae]),_:2},1032,["to"])])])),[[l,u.DateTime.fromISO(t.datetime).toRelative(),void 0,{left:!0}]])),128))])]),e("nav",re,[v(y,{modelValue:s.page,"onUpdate:modelValue":d[2]||(d[2]=t=>s.page=t),"page-count":s.page_count,"click-handler":u.getLogs,"prev-text":"Previous","next-text":"Next","container-class":"pagination-list","page-link-class":"pagination-link","prev-link-class":"pagination-previous","next-link-class":"pagination-next","active-class":"is-current","disabled-class":"is-disabled","break-view-link-class":"pagination-ellipsis","no-li-surround":!0},null,8,["modelValue","page-count","click-handler"])]),e("div",le,[e("p",null,"(showing "+a(s.logs.length)+" of "+a(s.results_count)+" total results)",1)])])])):f("",!0)]),_:1})}const ve=T(R,[["render",ce]]);export{ve as default};
