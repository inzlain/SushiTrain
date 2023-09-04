import{r as u,e as m,o as l,g as v,h as p,T as k,c as n,a as e,t as g,d as c,b as d,v as r,q as y,j as a,n as f,s as x,F as w,i as V,u as _,k as C}from"./index.1e99d4f4.js";import{_ as T}from"./_plugin-vue_export-helper.cdc0426e.js";const q={data(){return{policies:[],hostname:"",https:"yes",port:"443",host_header:"",notes:"",headers:"",default_policy_id:null,default_logging:!0,default_logging_request_body:!0,default_logging_response_body:!0,selected_tab:"policy",isLoading:!0,error:""}},methods:{getRedirector(){this.$route.params.id>0?fetch("/api/redirectors/"+this.$route.params.id).then(i=>i.json()).then(i=>{this.hostname=i.hostname,this.host_header=i.host_header,this.notes=i.notes,this.headers=i.headers,this.port=i.port,this.https=i.https,this.default_policy_id=i.default_policy_id,this.default_logging=i.default_logging,this.default_logging_request_body=i.default_logging_request_body,this.default_logging_response_body=i.default_logging_response_body,this.isLoading=!1}):this.isLoading=!1},addRedirector(){const i=JSON.stringify({hostname:this.hostname,host_header:this.host_header,notes:this.notes,headers:this.headers,port:this.port,https:this.https,default_policy_id:this.default_policy_id,default_logging:this.default_logging,default_logging_request_body:this.default_logging_request_body,default_logging_response_body:this.default_logging_response_body});fetch("/api/redirectors",{method:"POST",body:i}).then(s=>s.json()).then(s=>{s.created===!0?u.push("/redirectors"):(this.error=s.error,window.scrollTo(0,0))})},editRedirector(){const i=JSON.stringify({hostname:this.hostname,host_header:this.host_header,notes:this.notes,headers:this.headers,port:this.port,https:this.https,default_policy_id:this.default_policy_id,default_logging:this.default_logging,default_logging_request_body:this.default_logging_request_body,default_logging_response_body:this.default_logging_response_body});fetch("/api/redirectors/"+this.$route.params.id,{method:"PUT",body:i}).then(s=>s.json()).then(s=>{s.modified===!0?u.push("/redirectors"):(this.error=s.error,window.scrollTo(0,0))})},getPolicies(){fetch("/api/policies?list=1").then(i=>i.json()).then(i=>{this.policies=i})}},created(){this.getPolicies(),this.getRedirector()}},L={key:0},P={key:0,class:"message is-danger"},R=e("div",{class:"message-header"},[e("p",null,"Error")],-1),U={class:"message-body"},S={class:"box"},N={key:0,class:"title"},j={key:1,class:"title"},D={class:"tile is-ancestor"},H={class:"tile is-parent is-6"},E={class:"tile is-child"},B={class:"field"},M=e("label",{class:"label"},"Hostname",-1),O={class:"control"},F={class:"tile is-parent is-6"},J={class:"tile is-child"},z={class:"field"},A=e("label",{class:"label"},"Notes",-1),G={class:"control"},I={class:"tile is-ancestor"},K={class:"tile is-parent is-3"},Q={class:"tile is-child"},W={class:"field"},X=e("label",{class:"label"},"Host Header (i.e. domain fronting)",-1),Y={class:"control"},Z={class:"tile is-parent is-1"},$={class:"tile is-child"},ee={class:"field"},se=e("label",{class:"label"},"Port",-1),te={class:"control"},oe={class:"tile is-parent is-2"},ie={class:"tile is-child"},le={class:"field"},ne=e("label",{class:"label"},"Protocol",-1),de={class:"control"},ae={class:"radio"},re={class:"radio"},ce={class:"message is-primary"},_e=e("div",{class:"message-header"},"Headers",-1),he={class:"message-body"},ue=e("p",null,"These headers will be automatically applied to every path under this redirector, as well to 404 responses for non-existent paths that are requested. Each individual path also has it's own headers that can be configured in addition to these redirector-wide headers. Path level headers take precedence over these headers and will overwrite them.",-1),pe=e("br",null,null,-1),ge={class:"field"},ye={class:"message is-primary"},fe=e("div",{class:"message-header"},"Default Path Settings",-1),be={class:"message-body"},me={class:"tabs"},ve={key:0,class:"has-text-primary-dark",style:{"text-decoration":"none"}},ke=e("strong",null,"Policy",-1),xe=[ke],we={key:1,class:"has-text-primary",style:{"text-decoration":"none"}},Ve={key:0,class:"has-text-primary-dark",style:{"text-decoration":"none"}},Ce=e("strong",null,"Logging",-1),Te=[Ce],qe={key:1,class:"has-text-primary",style:{"text-decoration":"none"}},Le={key:0},Pe=e("p",null,"This is the default policy that will be applied to newly created paths under this redirector. Changing this setting won't affect the policy setting of any existing paths.",-1),Re=e("br",null,null,-1),Ue={class:"field"},Se=e("label",{class:"label"},"Select Default Policy",-1),Ne={class:"control"},je={class:"select"},De=e("option",{value:"null"},"None",-1),He=["value"],Ee={key:1},Be=e("p",null,"This is the default log retention configuration that will be applied to newly created paths under this redirector. Changing this setting won't affect the log retention configuration of any existing paths.",-1),Me=e("br",null,null,-1),Oe={class:"field"},Fe=e("label",{class:"label"},"Default Logging Configuration",-1),Je={class:"checkbox"},ze=e("br",null,null,-1),Ae={class:"checkbox"},Ge=e("br",null,null,-1),Ie={class:"checkbox"},Ke={class:"field is-grouped"},Qe={class:"control"},We=e("span",{class:"icon"},[e("i",{class:"fas fa-circle-check"})],-1),Xe=e("span",null,"Save",-1),Ye=[We,Xe],Ze=e("span",{class:"icon"},[e("i",{class:"fas fa-circle-check"})],-1),$e=e("span",null,"Save",-1),es=[Ze,$e],ss={class:"control"},ts=e("span",{class:"icon"},[e("i",{class:"fas fa-circle-xmark"})],-1),os=e("span",null,"Cancel",-1);function is(i,s,ls,ns,t,h){const b=m("RouterLink");return l(),v(k,null,{default:p(()=>[t.isLoading===!1?(l(),n("div",L,[t.error?(l(),n("article",P,[R,e("div",U,g(t.error),1)])):c("",!0),e("div",S,[i.$route.params.id?(l(),n("h1",N,"Edit Redirector")):(l(),n("h1",j,"Add Redirector")),e("div",D,[e("div",H,[e("div",E,[e("div",B,[M,e("div",O,[d(e("input",{class:"input",type:"text","onUpdate:modelValue":s[0]||(s[0]=o=>t.hostname=o),placeholder:"example.com",required:""},null,512),[[r,t.hostname]])])])])]),e("div",F,[e("div",J,[e("div",z,[A,e("div",G,[d(e("input",{class:"input",type:"text","onUpdate:modelValue":s[1]||(s[1]=o=>t.notes=o),placeholder:"Delivery of phishing payloads"},null,512),[[r,t.notes]])])])])])]),e("div",I,[e("div",K,[e("div",Q,[e("div",W,[X,e("div",Y,[d(e("input",{class:"input",type:"text","onUpdate:modelValue":s[2]||(s[2]=o=>t.host_header=o),placeholder:"yourname.cdn.com"},null,512),[[r,t.host_header]])])])])]),e("div",Z,[e("div",$,[e("div",ee,[se,e("div",te,[d(e("input",{class:"input",type:"text","onUpdate:modelValue":s[3]||(s[3]=o=>t.port=o),placeholder:"443"},null,512),[[r,t.port]])])])])]),e("div",oe,[e("div",ie,[e("div",le,[ne,e("div",de,[e("label",ae,[d(e("input",{type:"radio",name:"https",value:"yes","onUpdate:modelValue":s[4]||(s[4]=o=>t.https=o)},null,512),[[y,t.https]]),a(" HTTPS ")]),e("label",re,[d(e("input",{type:"radio",name:"https",value:"no","onUpdate:modelValue":s[5]||(s[5]=o=>t.https=o)},null,512),[[y,t.https]]),a(" HTTP ")])])])])])]),e("article",ce,[_e,e("div",he,[ue,pe,e("div",ge,[d(e("textarea",{class:"textarea","onUpdate:modelValue":s[6]||(s[6]=o=>t.headers=o),placeholder:`Server: nginx
Cache-Control: no-cache`,rows:"4"},null,512),[[r,t.headers]])])])]),e("article",ye,[fe,e("div",be,[e("div",me,[e("ul",null,[e("li",{class:f({"is-active":t.selected_tab==="policy"}),onClick:s[7]||(s[7]=o=>t.selected_tab="policy")},[t.selected_tab==="policy"?(l(),n("a",ve,xe)):(l(),n("a",we,"Policy"))],2),e("li",{class:f({"is-active":t.selected_tab==="logging"}),onClick:s[8]||(s[8]=o=>t.selected_tab="logging")},[t.selected_tab==="logging"?(l(),n("a",Ve,Te)):(l(),n("a",qe,"Logging"))],2)])]),t.selected_tab==="policy"?(l(),n("div",Le,[Pe,Re,e("div",Ue,[Se,e("div",Ne,[e("div",je,[d(e("select",{class:"is-truncated-select-option","onUpdate:modelValue":s[9]||(s[9]=o=>t.default_policy_id=o)},[De,(l(!0),n(w,null,V(t.policies,o=>(l(),n("option",{key:o.id,value:o.id},g(o.name),9,He))),128))],512),[[x,t.default_policy_id]])])])])])):c("",!0),t.selected_tab==="logging"?(l(),n("div",Ee,[Be,Me,e("div",Oe,[Fe,e("label",Je,[d(e("input",{type:"checkbox","onUpdate:modelValue":s[10]||(s[10]=o=>t.default_logging=o)},null,512),[[_,t.default_logging]]),a(" Logging enabled ")]),ze,a("\xA0\xA0\xA0\xA0 "),e("label",Ae,[d(e("input",{type:"checkbox","onUpdate:modelValue":s[11]||(s[11]=o=>t.default_logging_request_body=o)},null,512),[[_,t.default_logging_request_body]]),a(" Log request body ")]),Ge,a("\xA0\xA0\xA0\xA0 "),e("label",Ie,[d(e("input",{type:"checkbox","onUpdate:modelValue":s[12]||(s[12]=o=>t.default_logging_response_body=o)},null,512),[[_,t.default_logging_response_body]]),a(" Log response body ")])])])):c("",!0)])]),e("div",Ke,[e("div",Qe,[i.$route.params.id?(l(),n("button",{key:0,class:"button is-link",type:"submit",onClick:s[13]||(s[13]=o=>h.editRedirector())},Ye)):(l(),n("button",{key:1,class:"button is-link",type:"submit",onClick:s[14]||(s[14]=o=>h.addRedirector())},es))]),e("div",ss,[C(b,{class:"button is-link is-light",to:"/redirectors"},{default:p(()=>[ts,os]),_:1})])])])])):c("",!0)]),_:1})}const rs=T(q,[["render",is]]);export{rs as default};
