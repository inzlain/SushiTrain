import{_ as k}from"./_plugin-vue_export-helper.cdc0426e.js";import{f as w,o as t,c as l,a as s,j as n,t as c,d as v,b as $,F as o,e as y,g as P,h as p,T as D,k as m,i as u}from"./index.9eb82cac.js";const C={props:["name","id"],data(){return{showModal:!1}},methods:{deletePolicy(){fetch("/api/policies/"+this.id,{method:"DELETE"}).then(d=>d.json()).then(d=>{d.deleted===!0?this.$emit("afterDelete"):this.error=d.error})}}},x={key:0,class:"modal is-active"},L={class:"modal-card"},M={class:"modal-card-head"},A=s("p",{class:"modal-card-title"},"Delete Policy",-1),N={class:"modal-card-body"},T={class:"has-text-black"},V=s("br",null,null,-1),B=s("p",{class:"has-text-black"},"This will reset any paths with this policy assigned to have have no policy.",-1),E={class:"modal-card-foot"},R={class:"field is-grouped"},j={class:"control"},I={class:"control"},z=s("a",null,[s("i",{class:"fas fa-trash"})],-1),F=[z];function S(d,a,f,b,r,g){const h=w("tooltip");return t(),l(o,null,[r.showModal?(t(),l("div",x,[s("div",{class:"modal-background",onClick:a[0]||(a[0]=_=>r.showModal=!1)}),s("div",L,[s("header",M,[A,s("button",{class:"delete","aria-label":"close",onClick:a[1]||(a[1]=_=>r.showModal=!1)})]),s("section",N,[s("p",T,[n("Are you sure you want to delete "),s("strong",null,c(f.name),1),n("?")]),V,B]),s("footer",E,[s("div",R,[s("div",j,[s("button",{type:"button",class:"button is-link is-danger",onClick:a[2]||(a[2]=_=>{r.showModal=!1,g.deletePolicy()})},"Delete")]),s("div",I,[s("button",{type:"button",class:"button is-link is-success",onClick:a[3]||(a[3]=_=>r.showModal=!1)},"Cancel")])])])])])):v("",!0),s("div",null,[$((t(),l("span",{class:"icon",onClick:a[4]||(a[4]=_=>r.showModal=!0)},F)),[[h,"Delete policy",void 0,{top:!0}]])])],64)}const G=k(C,[["render",S]]),O={components:{PolicyDelete:G},data(){return{policies:[],isLoading:!0}},methods:{getPolicies(){fetch("/api/policies").then(d=>d.json()).then(d=>{this.policies=d,this.isLoading=!1})}},created(){this.getPolicies(),this.timer=setInterval(this.getPolicies,3e4)},unmounted(){clearInterval(this.timer)}},U={key:0},q=s("span",{class:"icon"},[s("i",{class:"fas fa-plus"})],-1),H=s("span",null,"Add Policy",-1),J=s("br",null,null,-1),K={class:"message-header"},Q={class:"is-size-4"},W=s("i",{class:"fas fa-shield-halved","aria-hidden":"true"},null,-1),X={class:"message-body"},Y={class:"table is-fullwidth is-hoverable has-background-primary-light"},Z=s("thead",null,[s("tr",null,[s("th",{style:{width:"15%"}},"Policy"),s("th",{style:{width:"85%"}},"Rules")])],-1),ss=s("td",null,"Geographic",-1),es={class:"tag is-danger"},ts={class:"tag is-success"},ls=s("td",null,"IP Range",-1),os={class:"tag is-danger"},is={class:"tag is-success"},ns=s("td",null,"ASN Organization",-1),as={class:"tag is-danger"},cs={class:"tag is-success"},ds=s("td",null,"User Agent",-1),rs={class:"tag is-danger"},us={class:"tag is-success"};function _s(d,a,f,b,r,g){const h=y("RouterLink"),_=y("PolicyDelete");return t(),P(D,null,{default:p(()=>[r.isLoading===!1?(t(),l("div",U,[s("div",null,[m(h,{class:"button is-link",to:"/policies/add"},{default:p(()=>[q,H]),_:1})]),J,(t(!0),l(o,null,u(r.policies,i=>(t(),l("article",{class:"message is-primary",key:i.id},[s("div",K,[s("div",null,[s("p",Q,[W,n("\xA0 "),m(h,{to:{name:"policies-edit",params:{id:i.id}}},{default:p(()=>[n(c(i.name),1)]),_:2},1032,["to"])]),s("p",null,c(i.notes),1)]),m(_,{name:i.name,id:i.id,onAfterDelete:g.getPolicies},null,8,["name","id","onAfterDelete"])]),s("div",X,[s("table",Y,[Z,s("tbody",null,[s("tr",null,[ss,s("td",null,[(t(!0),l(o,null,u(i.geographic_blocklist,e=>(t(),l(o,{key:e.id},[s("span",es,c(e.country_code),1),n(" \xA0 ")],64))),128)),(t(!0),l(o,null,u(i.geographic_allowlist,e=>(t(),l(o,{key:e.id},[s("span",ts,c(e.country_code),1),n(" \xA0 ")],64))),128))])]),s("tr",null,[ls,s("td",null,[(t(!0),l(o,null,u(i.ip_range_blocklist,e=>(t(),l(o,{key:e.id},[s("span",os,c(e.ip_range),1),n(" \xA0 ")],64))),128)),(t(!0),l(o,null,u(i.ip_range_allowlist,e=>(t(),l(o,{key:e.id},[s("span",is,c(e.ip_range),1),n(" \xA0 ")],64))),128))])]),s("tr",null,[ns,s("td",null,[(t(!0),l(o,null,u(i.asn_blocklist,e=>(t(),l(o,{key:e.id},[s("span",as,c(e.asn_org_name),1),n(" \xA0 ")],64))),128)),(t(!0),l(o,null,u(i.asn_allowlist,e=>(t(),l(o,{key:e.id},[s("span",cs,c(e.asn_org_name),1),n(" \xA0 ")],64))),128))])]),s("tr",null,[ds,s("td",null,[(t(!0),l(o,null,u(i.user_agent_blocklist,e=>(t(),l(o,{key:e.id},[s("span",rs,c(e.user_agent),1),n(" \xA0 ")],64))),128)),(t(!0),l(o,null,u(i.user_agent_allowlist,e=>(t(),l(o,{key:e.id},[s("span",us,c(e.user_agent),1),n(" \xA0 ")],64))),128))])])])])])]))),128))])):v("",!0)]),_:1})}const ps=k(O,[["render",_s]]);export{ps as default};
