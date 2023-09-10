import{D as k}from"./datetime.ba57e231.js";import{f as y,o as l,c as n,a as e,j as _,t as d,d as h,b as c,F as g,e as D,g as U,h as C,T,n as v,p,i as x,v as f,k as M}from"./index.eecb294c.js";import{_ as w}from"./_plugin-vue_export-helper.cdc0426e.js";const S={props:["username","user_id"],data(){return{showModal:!1}},methods:{deleteUser(){fetch("/api/users/"+this.user_id,{method:"DELETE"}).then(i=>i.json()).then(i=>{i.deleted===!0?this.$emit("afterDelete"):this.error=i.error})}}},L={key:0,class:"modal is-active has-text-left"},N={class:"modal-card"},O={class:"modal-card-head"},F=e("p",{class:"modal-card-title"},"Delete User",-1),V={class:"modal-card-body"},j={class:"has-text-black"},A={class:"modal-card-foot"},I={class:"field is-grouped"},E={class:"control"},B={class:"control"},R=e("a",null,[e("i",{class:"fas fa-trash has-text-black"})],-1),q=[R];function P(i,s,m,b,t,r){const u=y("tooltip");return l(),n(g,null,[t.showModal?(l(),n("div",L,[e("div",{class:"modal-background",onClick:s[0]||(s[0]=a=>t.showModal=!1)}),e("div",N,[e("header",O,[F,e("button",{class:"delete","aria-label":"close",onClick:s[1]||(s[1]=a=>t.showModal=!1)})]),e("section",V,[e("p",j,[_("Are you sure you want to delete "),e("strong",null,d(m.username),1),_("?")])]),e("footer",A,[e("div",I,[e("div",E,[e("button",{type:"button",class:"button is-link is-danger",onClick:s[2]||(s[2]=a=>{t.showModal=!1,r.deleteUser()})},"Delete")]),e("div",B,[e("button",{type:"button",class:"button is-link is-success",onClick:s[3]||(s[3]=a=>t.showModal=!1)},"Cancel")])])])])])):h("",!0),e("div",null,[c((l(),n("span",{class:"icon",onClick:s[4]||(s[4]=a=>t.showModal=!0)},q)),[[u,"Delete user",void 0,{top:!0}]])])],64)}const z=w(S,[["render",P]]),J={components:{UserDelete:z},computed:{DateTime(){return k}},data(){return{users:[],delivery_hostname:"",delivery_port:"",delivery_path:"",selected_tab:"users",new_username:"",new_password:"",isLoading:!0,error:""}},methods:{getSettings(){fetch("/api/settings/").then(i=>i.json()).then(i=>{this.delivery_hostname=i.delivery_hostname,this.delivery_port=i.delivery_port,this.delivery_path=i.delivery_path})},getUsers(){fetch("/api/users").then(i=>i.json()).then(i=>{this.users=i.users,this.isLoading=!1})},addUser(){const i=JSON.stringify({username:this.new_username,password:this.new_password});fetch("/api/users",{method:"POST",body:i}).then(s=>s.json()).then(s=>{s.created===!0?(this.getUsers(),this.new_username="",this.new_password=""):(this.error=s.error,window.scrollTo(0,0))})}},created(){this.getSettings(),this.getUsers()}},G={key:0},H={key:0,class:"message is-danger"},K=e("div",{class:"message-header"},[e("p",null,"Error")],-1),Q={class:"message-body"},W={class:"box"},X=e("h1",{class:"title"},"Settings",-1),Y={class:"tabs"},Z=e("a",null,"Users",-1),$=[Z],ee=e("a",null,"Configuration",-1),se=[ee],te={class:"content"},oe={class:"table is-fullwidth is-hoverable"},ie=e("thead",null,[e("tr",null,[e("th",{style:{width:"20%"}},"Username"),e("th",{style:{width:"5%"}},"Admin"),e("th",{style:{width:"20%"}},"Created"),e("th",{style:{width:"20%"}},"Last Login"),e("th",{style:{width:"20%"}},"Last Failed Login"),e("th",{style:{width:"10%"}},"Failed Logins"),e("th",{style:{width:"5%"}},"Delete")])],-1),le={class:"has-text-centered"},ne={key:0,class:"icon"},re=e("i",{class:"fas fa-circle-check","aria-hidden":"true"},null,-1),de=[re],ae={key:0},ce={key:1},_e={key:2},he={key:3},ue={key:4,class:"has-text-centered"},me={key:5},ve=e("br",null,null,-1),pe=e("h1",{class:"title is-4"},"Add New User",-1),fe={class:"tile is-ancestor"},ye={class:"tile is-parent is-4"},ge={class:"tile is-child"},we={class:"field"},be=e("label",{class:"label"},"Username",-1),ke={class:"control"},De={class:"tile is-ancestor"},Ue={class:"tile is-parent is-4"},Ce={class:"tile is-child"},Te={class:"field"},xe=e("label",{class:"label"},"Password",-1),Me={class:"control"},Se={class:"field is-grouped"},Le={class:"control"},Ne=e("span",{class:"icon"},[e("i",{class:"fas fa-plus"})],-1),Oe=e("span",null,"Add User",-1),Fe=[Ne,Oe],Ve=e("strong",null,"Delivery URL: ",-1);function je(i,s,m,b,t,r){const u=D("UserDelete"),a=y("tooltip");return l(),U(T,null,{default:C(()=>[t.isLoading===!1?(l(),n("div",G,[t.error?(l(),n("article",H,[K,e("div",Q,d(t.error),1)])):h("",!0),e("div",W,[X,e("div",Y,[e("ul",null,[e("li",{class:v({"is-active":t.selected_tab==="users"}),onClick:s[0]||(s[0]=o=>t.selected_tab="users")},$,2),e("li",{class:v({"is-active":t.selected_tab==="configuration"}),onClick:s[1]||(s[1]=o=>t.selected_tab="configuration")},se,2)])]),e("div",te,[c(e("div",null,[e("table",oe,[ie,e("tbody",null,[(l(!0),n(g,null,x(t.users,o=>(l(),n("tr",{key:o.id},[e("td",null,d(o.username),1),e("td",le,[o.admin===!0?(l(),n("span",ne,de)):h("",!0)]),c((l(),n("td",null,[_(d(r.DateTime.fromISO(o.created).toFormat("yyyy-MM-dd hh:mm:ss")),1)])),[[a,r.DateTime.fromISO(o.created).toRelative(),void 0,{top:!0}]]),o.last_successful_login?c((l(),n("td",ae,[_(d(r.DateTime.fromISO(o.last_successful_login).toFormat("yyyy-MM-dd hh:mm:ss")),1)])),[[a,r.DateTime.fromISO(o.last_successful_login).toRelative(),void 0,{top:!0}]]):(l(),n("td",ce,"Never")),o.last_failed_login?c((l(),n("td",_e,[_(d(r.DateTime.fromISO(o.last_failed_login).toFormat("yyyy-MM-dd hh:mm:ss")),1)])),[[a,r.DateTime.fromISO(o.last_failed_login).toRelative(),void 0,{top:!0}]]):(l(),n("td",he,"Never")),e("td",null,d(o.failed_login_count),1),t.users.length>1?(l(),n("td",ue,[M(u,{user_id:o.id,username:o.username,onAfterDelete:r.getUsers},null,8,["user_id","username","onAfterDelete"])])):(l(),n("td",me))]))),128))])]),ve,pe,e("div",null,[e("div",fe,[e("div",ye,[e("div",ge,[e("div",we,[be,e("div",ke,[c(e("input",{class:"input",type:"text",placeholder:"user","onUpdate:modelValue":s[2]||(s[2]=o=>t.new_username=o),required:""},null,512),[[f,t.new_username]])])])])])]),e("div",De,[e("div",Ue,[e("div",Ce,[e("div",Te,[xe,e("div",Me,[c(e("input",{class:"input",type:"password",placeholder:"********","onUpdate:modelValue":s[3]||(s[3]=o=>t.new_password=o),required:""},null,512),[[f,t.new_password]])])])])])]),e("div",Se,[e("div",Le,[e("button",{class:"button is-link",type:"submit",onClick:s[4]||(s[4]=(...o)=>r.addUser&&r.addUser(...o))},Fe)])])])],512),[[p,t.selected_tab==="users"]]),c(e("div",null,[e("p",null,[Ve,_(" https://"+d(t.delivery_hostname)+":"+d(t.delivery_port)+d(t.delivery_path),1)])],512),[[p,t.selected_tab==="configuration"]])])])])):h("",!0)]),_:1})}const Be=w(J,[["render",je]]);export{Be as default};