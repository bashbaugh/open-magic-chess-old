(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["new"],{2871:function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-dialog",{staticClass:"new-dialog",attrs:{visible:!0,title:"Create New Game",width:"50%","before-close":function(){return e.$router.push("/")}}},[a("div",{directives:[{name:"loading",rawName:"v-loading",value:e.$store.state.loading,expression:"$store.state.loading"}],attrs:{"element-loading-background":"rgba(0, 0, 0, 0.2)","element-loading-text":e.$store.state.loadingText}},[a("el-select",{attrs:{placeholder:"Select game type"},model:{value:e.value,callback:function(t){e.value=t},expression:"value"}},e._l(e.options,function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})}),1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){return e.$router.push("/")}}},[e._v("Cancel")]),a("el-button",{attrs:{type:"success",disabled:e.$store.state.loading},on:{click:e.startGame,"update:disabled":function(t){return e.$set(e.$store.state,"loading",t)}}},[e._v("Start new game")])],1)])],1)},n=[],o={name:"NewGame",data:function(){return{}},methods:{startGame:function(){}}},s=o,r=a("2877"),i=Object(r["a"])(s,l,n,!1,null,null,null);t["default"]=i.exports}}]);
//# sourceMappingURL=new.34521df5.js.map