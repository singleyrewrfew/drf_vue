import{_ as bt,n as Ae,o as Kt,a2 as Zt,j as D,c as j,r as X,b as Ve,a as N,K as Jt,t as Oe,N as Qt,s as De,u as Ne,d as I,w as Y,W as At,E as F,h as et,X as Be,k as Ye,p as ut,f as ct,J as Ht,aj as Fe,z as He,a5 as We,U as dt}from"./index-BfWl2eKD.js";import{a as Wt}from"./index-CclmsIXI.js";import{D as Ue}from"./DeleteButton-BdToVfUj.js";function je(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}var Tt={exports:{}},Xe=Tt.exports,Ut;function qe(){return Ut||(Ut=1,(function(e,t){(function(n,o){e.exports=o()})(Xe,function(){function n(l){return(n=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(d){return typeof d}:function(d){return d&&typeof Symbol=="function"&&d.constructor===Symbol&&d!==Symbol.prototype?"symbol":typeof d})(l)}var o=Object.prototype.toString,r=function(l){if(l===void 0)return"undefined";if(l===null)return"null";var d=n(l);if(d==="boolean")return"boolean";if(d==="string")return"string";if(d==="number")return"number";if(d==="symbol")return"symbol";if(d==="function")return(function(u){return i(u)==="GeneratorFunction"})(l)?"generatorfunction":"function";if((function(u){return Array.isArray?Array.isArray(u):u instanceof Array})(l))return"array";if((function(u){return u.constructor&&typeof u.constructor.isBuffer=="function"?u.constructor.isBuffer(u):!1})(l))return"buffer";if((function(u){try{if(typeof u.length=="number"&&typeof u.callee=="function")return!0}catch(h){if(h.message.indexOf("callee")!==-1)return!0}return!1})(l))return"arguments";if((function(u){return u instanceof Date||typeof u.toDateString=="function"&&typeof u.getDate=="function"&&typeof u.setDate=="function"})(l))return"date";if((function(u){return u instanceof Error||typeof u.message=="string"&&u.constructor&&typeof u.constructor.stackTraceLimit=="number"})(l))return"error";if((function(u){return u instanceof RegExp||typeof u.flags=="string"&&typeof u.ignoreCase=="boolean"&&typeof u.multiline=="boolean"&&typeof u.global=="boolean"})(l))return"regexp";switch(i(l)){case"Symbol":return"symbol";case"Promise":return"promise";case"WeakMap":return"weakmap";case"WeakSet":return"weakset";case"Map":return"map";case"Set":return"set";case"Int8Array":return"int8array";case"Uint8Array":return"uint8array";case"Uint8ClampedArray":return"uint8clampedarray";case"Int16Array":return"int16array";case"Uint16Array":return"uint16array";case"Int32Array":return"int32array";case"Uint32Array":return"uint32array";case"Float32Array":return"float32array";case"Float64Array":return"float64array"}if((function(u){return typeof u.throw=="function"&&typeof u.return=="function"&&typeof u.next=="function"})(l))return"generator";switch(d=o.call(l)){case"[object Object]":return"object";case"[object Map Iterator]":return"mapiterator";case"[object Set Iterator]":return"setiterator";case"[object String Iterator]":return"stringiterator";case"[object Array Iterator]":return"arrayiterator"}return d.slice(8,-1).toLowerCase().replace(/\s/g,"")};function i(l){return l.constructor?l.constructor.name:null}function a(l,d){var u=2<arguments.length&&arguments[2]!==void 0?arguments[2]:["option"];return s(l,d,u),c(l,d,u),(function(h,m,f){var y=r(m),b=r(h);if(y==="object"){if(b!=="object")throw new Error("[Type Error]: '".concat(f.join("."),"' require 'object' type, but got '").concat(b,"'"));Object.keys(m).forEach(function(C){var z=h[C],E=m[C],$=f.slice();$.push(C),s(z,E,$),c(z,E,$),a(z,E,$)})}if(y==="array"){if(b!=="array")throw new Error("[Type Error]: '".concat(f.join("."),"' require 'array' type, but got '").concat(b,"'"));h.forEach(function(C,z){var E=h[z],$=m[z]||m[0],S=f.slice();S.push(z),s(E,$,S),c(E,$,S),a(E,$,S)})}})(l,d,u),l}function s(l,d,u){if(r(d)==="string"){var h=r(l);if(d[0]==="?"&&(d=d.slice(1)+"|undefined"),!(-1<d.indexOf("|")?d.split("|").map(function(m){return m.toLowerCase().trim()}).filter(Boolean).some(function(m){return h===m}):d.toLowerCase().trim()===h))throw new Error("[Type Error]: '".concat(u.join("."),"' require '").concat(d,"' type, but got '").concat(h,"'"))}}function c(l,d,u){if(r(d)==="function"){var h=d(l,r(l),u);if(h!==!0){var m=r(h);throw m==="string"?new Error(h):m==="error"?h:new Error("[Validator Error]: The scheme for '".concat(u.join("."),"' validator require return true, but got '").concat(h,"'"))}}}return a.kindOf=r,a})})(Tt)),Tt.exports}var Ge=qe();const mt=je(Ge),Ot="5.4.0",gt={properties:["audioTracks","autoplay","buffered","controller","controls","crossOrigin","currentSrc","currentTime","defaultMuted","defaultPlaybackRate","duration","ended","error","loop","mediaGroup","muted","networkState","paused","playbackRate","played","preload","readyState","seekable","seeking","src","startDate","textTracks","videoTracks","volume"],methods:["addTextTrack","canPlayType","load","play","pause"],events:["abort","canplay","canplaythrough","durationchange","emptied","ended","error","loadeddata","loadedmetadata","loadstart","pause","play","playing","progress","ratechange","seeked","seeking","stalled","suspend","timeupdate","volumechange","waiting"],prototypes:["width","height","videoWidth","videoHeight","poster","webkitDecodedFrameCount","webkitDroppedFrameCount","playsInline","webkitSupportsFullscreen","webkitDisplayingFullscreen","onenterpictureinpicture","onleavepictureinpicture","disablePictureInPicture","cancelVideoFrameCallback","requestVideoFrameCallback","getVideoPlaybackQuality","requestPictureInPicture","webkitEnterFullScreen","webkitEnterFullscreen","webkitExitFullScreen","webkitExitFullscreen"]},wt=globalThis?.CUSTOM_USER_AGENT??(typeof navigator<"u"?navigator.userAgent:""),te=/^(?:(?!chrome|android).)*safari/i.test(wt),ee=/iPad|iPhone|iPod/i.test(wt)&&!window.MSStream,ne=ee||wt.includes("Macintosh")&&navigator.maxTouchPoints>=1,L=/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(wt)||ne,St=typeof window<"u"&&typeof document<"u";function H(e,t=document){return t.querySelector(e)}function xt(e,t=document){return Array.from(t.querySelectorAll(e))}function k(e,t){return e.classList.add(t)}function A(e,t){return e.classList.remove(t)}function Q(e,t){return e.classList.contains(t)}function g(e,t){return t instanceof Element?e.appendChild(t):e.insertAdjacentHTML("beforeend",String(t)),e.lastElementChild||e.lastChild}function zt(e){return e.parentNode.removeChild(e)}function p(e,t,n){return e.style[t]=n,e}function Mt(e,t){for(const n in t)p(e,n,t[n]);return e}function Ke(e,t,n=!0){const o=window.getComputedStyle(e,null).getPropertyValue(t);return n?Number.parseFloat(o):o}function oe(e){return Array.from(e.parentElement.children).filter(t=>t!==e)}function G(e,t){oe(e).forEach(n=>A(n,t)),k(e,t)}function tt(e,t,n="top"){L||(e.setAttribute("aria-label",t),k(e,"hint--rounded"),k(e,`hint--${n}`))}function Dt(e,t=0){const n=e.getBoundingClientRect(),o=window.innerHeight||document.documentElement.clientHeight,r=window.innerWidth||document.documentElement.clientWidth,i=n.top-t<=o&&n.top+n.height+t>=0,a=n.left-t<=r+t&&n.left+n.width+t>=0;return i&&a}function lt(e,t){return Bt(e).includes(t)}function Nt(e,t){return t.parentNode.replaceChild(e,t),e}function P(e){return document.createElement(e)}function re(e="",t=""){const n=P("i");return k(n,"art-icon"),k(n,`art-icon-${e}`),g(n,t),n}function ie(e,t){let n=document.getElementById(e);n||(n=document.createElement("style"),n.id=e,document.readyState==="loading"?document.addEventListener("DOMContentLoaded",()=>{document.head.appendChild(n)}):(document.head||document.documentElement).appendChild(n)),n.textContent=t}function ae(){const e=document.createElement("div");return e.style.display="flex",e.style.display==="flex"}function K(e){return e.getBoundingClientRect()}function se(e,t){return new Promise((n,o)=>{const r=new Image;r.onload=function(){if(!t||t===1)n(r);else{const i=document.createElement("canvas"),a=i.getContext("2d");i.width=r.width*t,i.height=r.height*t,a.drawImage(r,0,0,i.width,i.height),i.toBlob(s=>{const c=URL.createObjectURL(s),l=new Image;l.onload=function(){n(l)},l.onerror=function(){URL.revokeObjectURL(c),o(new Error(`Image load failed: ${e}`))},l.src=c})}},r.onerror=function(){o(new Error(`Image load failed: ${e}`))},r.src=e})}function Bt(e){if(e.composedPath)return e.composedPath();const t=[];let n=e.target;for(;n;)t.push(n),n=n.parentNode;return!t.includes(window)&&window!==void 0&&t.push(window),t}class le extends Error{constructor(t,n){super(t),typeof Error.captureStackTrace=="function"&&Error.captureStackTrace(this,n||this.constructor),this.name="ArtPlayerError"}}function U(e,t){if(!e)throw new le(t);return e}function yt(e){return e.includes("?")?yt(e.split("?")[0]):e.includes("#")?yt(e.split("#")[0]):e.trim().toLowerCase().split(".").pop()}function ce(e,t){const n=document.createElement("a");n.style.display="none",n.href=e,n.download=t,document.body.appendChild(n),n.click(),document.body.removeChild(n)}function W(e,t,n){return Math.max(Math.min(e,Math.max(t,n)),Math.min(t,n))}function _t(e){return e.charAt(0).toUpperCase()+e.slice(1)}function Z(e){if(!e)return"00:00";const t=i=>i<10?`0${i}`:String(i),n=Math.floor(e/3600),o=Math.floor((e-n*3600)/60),r=Math.floor(e-n*3600-o*60);return(n>0?[n,o,r]:[o,r]).map(t).join(":")}function de(e){return e.replace(/[&<>'"]/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[t]||t)}function Ze(e){const t={"&amp;":"&","&lt;":"<","&gt;":">","&#39;":"'","&quot;":'"'},n=new RegExp(`(${Object.keys(t).join("|")})`,"g");return e.replace(n,o=>t[o]||o)}const v=Object.defineProperty,{hasOwnProperty:Je}=Object.prototype;function vt(e,t){return Je.call(e,t)}function pe(e,t){return Object.getOwnPropertyDescriptor(e,t)}function Lt(...e){const t=n=>n&&typeof n=="object"&&!Array.isArray(n);return e.reduce((n,o)=>(Object.keys(o).forEach(r=>{const i=n[r],a=o[r];Array.isArray(i)&&Array.isArray(a)?n[r]=i.concat(...a):t(i)&&t(a)?n[r]=Lt(i,a):n[r]=a}),n),{})}function Qe(e){return e.replace(/(\d\d:\d\d:\d\d)[,.](\d+)/g,(t,n,o)=>{let r=o.slice(0,3);return o.length===1&&(r=`${o}00`),o.length===2&&(r=`${o}0`),`${n},${r}`})}function ue(e){return`WEBVTT \r
\r
`.concat(Qe(e).replace(/\{\\([ibu])\}/g,"</$1>").replace(/\{\\([ibu])1\}/g,"<$1>").replace(/\{([ibu])\}/g,"<$1>").replace(/\{\/([ibu])\}/g,"</$1>").replace(/(\d\d:\d\d:\d\d),(\d\d\d)/g,"$1.$2").replace(/\{[\s\S]*?\}/g,"").concat(`\r
\r
`))}function Ct(e){return URL.createObjectURL(new Blob([e],{type:"text/vtt"}))}function he(e){const t=new RegExp("Dialogue:\\s\\d,(\\d+:\\d\\d:\\d\\d.\\d\\d),(\\d+:\\d\\d:\\d\\d.\\d\\d),([^,]*),([^,]*),(?:[^,]*,){4}([\\s\\S]*)$","i");function n(o=""){return o.split(/[:.]/).map((r,i,a)=>{if(i===a.length-1){if(r.length===1)return`.${r}00`;if(r.length===2)return`.${r}0`}else if(r.length===1)return(i===0?"0":":0")+r;return i===0?r:i===a.length-1?`.${r}`:`:${r}`}).join("")}return`WEBVTT

${e.split(/\r?\n/).map(o=>{const r=o.match(t);return r?{start:n(r[1].trim()),end:n(r[2].trim()),text:r[5].replace(/\{[\s\S]*?\}/g,"").replace(/(\\N)/g,`
`).trim().split(/\r?\n/).map(i=>i.trim()).join(`
`)}:null}).filter(o=>o).map((o,r)=>o?`${r+1}
${o.start} --> ${o.end}
${o.text}`:"").filter(o=>o.trim()).join(`

`)}`}function pt(e=0){return new Promise(t=>setTimeout(t,e))}function fe(e,t){let n;return function(...o){const r=()=>(n=null,e.apply(this,o));clearTimeout(n),n=setTimeout(r,t)}}function me(e,t){let n=!1;return function(...o){n||(e.apply(this,o),n=!0,setTimeout(()=>{n=!1},t))}}const tn=Object.freeze(Object.defineProperty({__proto__:null,ArtPlayerError:le,addClass:k,append:g,assToVtt:he,capitalize:_t,clamp:W,createElement:P,debounce:fe,def:v,download:ce,errorHandle:U,escape:de,get:pe,getComposedPath:Bt,getExt:yt,getIcon:re,getRect:K,getStyle:Ke,has:vt,hasClass:Q,includeFromEvent:lt,inverseClass:G,isBrowser:St,isIOS:ee,isIOS13:ne,isInViewport:Dt,isMobile:L,isSafari:te,loadImg:se,mergeDeep:Lt,query:H,queryAll:xt,remove:zt,removeClass:A,replaceElement:Nt,secondToTime:Z,setStyle:p,setStyleText:ie,setStyles:Mt,siblings:oe,sleep:pt,srtToVtt:ue,supportsFlex:ae,throttle:me,tooltip:tt,unescape:Ze,userAgent:wt,vttToBlob:Ct},Symbol.toStringTag,{value:"Module"})),jt="array",M="boolean",O="string",q="number",st="object",nt="function";function ge(e,t,n){return U(t===O||t===q||e instanceof Element,`${n.join(".")} require '${O}' or 'Element' type`)}const ht={html:ge,disable:`?${M}`,name:`?${O}`,index:`?${q}`,style:`?${st}`,click:`?${nt}`,mounted:`?${nt}`,tooltip:`?${O}|${q}`,width:`?${q}`,selector:`?${jt}`,onSelect:`?${nt}`,switch:`?${M}`,onSwitch:`?${nt}`,range:`?${jt}`,onRange:`?${nt}`,onChange:`?${nt}`},Vt={id:O,container:ge,url:O,poster:O,type:O,theme:O,lang:O,volume:q,isLive:M,muted:M,autoplay:M,autoSize:M,autoMini:M,loop:M,flip:M,playbackRate:M,aspectRatio:M,screenshot:M,setting:M,hotkey:M,pip:M,mutex:M,backdrop:M,fullscreen:M,fullscreenWeb:M,subtitleOffset:M,miniProgressBar:M,useSSR:M,playsInline:M,lock:M,gesture:M,fastForward:M,autoPlayback:M,autoOrientation:M,airplay:M,proxy:`?${nt}`,plugins:[nt],layers:[ht],contextmenu:[ht],settings:[ht],controls:[{...ht,position:(e,t,n)=>{const o=["top","left","right"];return U(o.includes(e),`${n.join(".")} only accept ${o.toString()} as parameters`)}}],quality:[{default:`?${M}`,html:O,url:O}],highlight:[{time:q,text:O}],thumbnails:{url:O,number:q,column:q,width:q,height:q,scale:q},subtitle:{url:O,name:O,type:O,style:st,escape:M,encoding:O,onVttLoad:nt},moreVideoAttr:st,i18n:st,icons:st,cssVar:st,customType:st};class it{constructor(t){this.id=0,this.art=t,this.cache=new Map,this.add=this.add.bind(this),this.remove=this.remove.bind(this),this.update=this.update.bind(this)}get show(){return Q(this.art.template.$player,`art-${this.name}-show`)}set show(t){const{$player:n}=this.art.template,o=`art-${this.name}-show`;t?k(n,o):A(n,o),this.art.emit(this.name,t)}toggle(){this.show=!this.show}add(t){const n=typeof t=="function"?t(this.art):t;if(n.html=n.html||"",mt(n,ht),!this.$parent||!this.name||n.disable)return;const o=n.name||`${this.name}${this.id}`;U(!this.cache.has(o),`Can't add an existing [${o}] to the [${this.name}]`),this.id+=1;const r=P("div");k(r,`art-${this.name}`),k(r,`art-${this.name}-${o}`);const i=Array.from(this.$parent.children);r.dataset.index=n.index||this.id;const a=i.find(c=>Number(c.dataset.index)>=Number(r.dataset.index));a?a.insertAdjacentElement("beforebegin",r):g(this.$parent,r),n.html&&g(r,n.html),n.style&&Mt(r,n.style),n.tooltip&&tt(r,n.tooltip);const s=[];if(n.click){const c=this.art.events.proxy(r,"click",l=>{l.preventDefault(),n.click.call(this.art,this,l)});s.push(c)}return n.selector&&["left","right"].includes(n.position)&&this.selector(n,r,s),this[o]=r,this.cache.set(o,{$ref:r,events:s,option:n}),n.mounted&&n.mounted.call(this.art,r),r}remove(t){U(this.cache.has(t),`Can't find [${t}] from the [${this.name}]`);const n=this.cache.get(t);n.option.beforeUnmount&&n.option.beforeUnmount.call(this.art,n.$ref);for(const o of n.events)this.art.events.remove(o);this.cache.delete(t),delete this[t],zt(n.$ref)}update(t){if(this.cache.has(t.name)){const n=this.cache.get(t.name);t=Object.assign(n.option,t),this.remove(t.name)}return this.add(t)}}function en(e){return t=>{const{i18n:n,constructor:{ASPECT_RATIO:o}}=t,r=o.map(i=>`<span data-value="${i}">${i==="default"?n.get("Default"):i}</span>`).join("");return{...e,html:`${n.get("Aspect Ratio")}: ${r}`,click:(i,a)=>{const{value:s}=a.target.dataset;s&&(t.aspectRatio=s,i.show=!1)},mounted:i=>{const a=H('[data-value="default"]',i);a&&G(a,"art-current"),t.on("aspectRatio",s=>{const c=xt("span",i).find(l=>l.dataset.value===s);c&&G(c,"art-current")})}}}}function nn(e){return t=>({...e,html:t.i18n.get("Close"),click:n=>{n.show=!1}})}function on(e){return t=>{const{i18n:n,constructor:{FLIP:o}}=t,r=o.map(i=>`<span data-value="${i}">${n.get(_t(i))}</span>`).join("");return{...e,html:`${n.get("Video Flip")}: ${r}`,click:(i,a)=>{const{value:s}=a.target.dataset;s&&(t.flip=s.toLowerCase(),i.show=!1)},mounted:i=>{const a=H('[data-value="normal"]',i);a&&G(a,"art-current"),t.on("flip",s=>{const c=xt("span",i).find(l=>l.dataset.value===s);c&&G(c,"art-current")})}}}}function rn(e){return t=>({...e,html:t.i18n.get("Video Info"),click:n=>{t.info.show=!0,n.show=!1}})}function an(e){return t=>{const{i18n:n,constructor:{PLAYBACK_RATE:o}}=t,r=o.map(i=>`<span data-value="${i}">${i===1?n.get("Normal"):i.toFixed(1)}</span>`).join("");return{...e,html:`${n.get("Play Speed")}: ${r}`,click:(i,a)=>{const{value:s}=a.target.dataset;s&&(t.playbackRate=Number(s),i.show=!1)},mounted:i=>{const a=H('[data-value="1"]',i);a&&G(a,"art-current"),t.on("video:ratechange",()=>{const s=xt("span",i).find(c=>Number(c.dataset.value)===t.playbackRate);s&&G(s,"art-current")})}}}}function sn(e){const t=St?location.href:"";return{...e,html:`<a href="https://artplayer.org?ref=${encodeURIComponent(t)}" target="_blank" style="width:100%;">ArtPlayer ${Ot}</a>`}}class ln extends it{constructor(t){super(t),this.name="contextmenu",this.$parent=t.template.$contextmenu,L||this.init()}init(){const{option:t,proxy:n,template:{$player:o,$contextmenu:r}}=this.art;t.playbackRate&&this.add(an({name:"playbackRate",index:10})),t.aspectRatio&&this.add(en({name:"aspectRatio",index:20})),t.flip&&this.add(on({name:"flip",index:30})),this.add(rn({name:"info",index:40})),this.add(sn({name:"version",index:50})),this.add(nn({name:"close",index:60}));for(let i=0;i<t.contextmenu.length;i++)this.add(t.contextmenu[i]);n(o,"contextmenu",i=>{if(!this.art.constructor.CONTEXTMENU)return;i.preventDefault(),this.show=!0;const a=i.clientX,s=i.clientY,{height:c,width:l,left:d,top:u}=K(o),{height:h,width:m}=K(r);let f=a-d,y=s-u;a+m>d+l&&(f=l-m),s+h>u+c&&(y=c-h),Mt(r,{top:`${y}px`,left:`${f}px`})}),n(o,"click",i=>{lt(i,r)||(this.show=!1)}),this.art.on("blur",()=>{this.show=!1})}}function cn(e){return t=>({...e,tooltip:t.i18n.get("AirPlay"),mounted:n=>{const{proxy:o,icons:r}=t;g(n,r.airplay),o(n,"click",()=>t.airplay())}})}function dn(e){return t=>({...e,tooltip:t.i18n.get("Fullscreen"),mounted:n=>{const{proxy:o,icons:r,i18n:i}=t,a=g(n,r.fullscreenOn),s=g(n,r.fullscreenOff);p(s,"display","none"),o(n,"click",()=>{t.fullscreen=!t.fullscreen}),t.on("fullscreen",c=>{c?(tt(n,i.get("Exit Fullscreen")),p(a,"display","none"),p(s,"display","inline-flex")):(tt(n,i.get("Fullscreen")),p(a,"display","inline-flex"),p(s,"display","none"))})}})}function pn(e){return t=>({...e,tooltip:t.i18n.get("Web Fullscreen"),mounted:n=>{const{proxy:o,icons:r,i18n:i}=t,a=g(n,r.fullscreenWebOn),s=g(n,r.fullscreenWebOff);p(s,"display","none"),o(n,"click",()=>{t.fullscreenWeb=!t.fullscreenWeb}),t.on("fullscreenWeb",c=>{c?(tt(n,i.get("Exit Web Fullscreen")),p(a,"display","none"),p(s,"display","inline-flex")):(tt(n,i.get("Web Fullscreen")),p(a,"display","inline-flex"),p(s,"display","none"))})}})}function un(e){return t=>({...e,tooltip:t.i18n.get("PIP Mode"),mounted:n=>{const{proxy:o,icons:r,i18n:i}=t;g(n,r.pip),o(n,"click",()=>{t.pip=!t.pip}),t.on("pip",a=>{tt(n,i.get(a?"Exit PIP Mode":"PIP Mode"))})}})}function hn(e){return t=>({...e,mounted:n=>{const{proxy:o,icons:r,i18n:i}=t,a=g(n,r.play),s=g(n,r.pause);tt(a,i.get("Play")),tt(s,i.get("Pause")),o(a,"click",()=>{t.play()}),o(s,"click",()=>{t.pause()});function c(){p(a,"display","flex"),p(s,"display","none")}function l(){p(a,"display","none"),p(s,"display","flex")}t.playing?l():c(),t.on("video:playing",()=>{l()}),t.on("video:pause",()=>{c()})}})}function ft(e,t){const{$progress:n}=e.template,{left:o}=K(n),r=L?t.touches[0].clientX:t.clientX,i=W(r-o,0,n.clientWidth),a=i/n.clientWidth*e.duration,s=Z(a),c=W(i/n.clientWidth,0,1);return{second:a,time:s,width:i,percentage:c}}function ve(e,t){if(e.isRotate){const n=t.touches[0].clientY/e.height,o=n*e.duration;e.emit("setBar","played",n,t),e.seek=o}else{const{second:n,percentage:o}=ft(e,t);e.emit("setBar","played",o,t),e.seek=n}}function fn(e){return t=>{const{icons:n,option:o,proxy:r}=t,{$player:i,$progress:a}=t.template;return{...e,html:`
                <div class="art-control-progress-inner">
                    <div class="art-progress-hover"></div>
                    <div class="art-progress-loaded"></div>
                    <div class="art-progress-played"></div>
                    <div class="art-progress-highlight"></div>
                    <div class="art-progress-indicator"></div>
                    <div class="art-progress-tip">00:00</div>
                </div>
            `,mounted:s=>{let c=null,l=!1;const d=H(".art-progress-hover",s),u=H(".art-progress-loaded",s),h=H(".art-progress-played",s),m=H(".art-progress-highlight",s),f=H(".art-progress-indicator",s),y=H(".art-progress-tip",s);n.indicator?g(f,n.indicator):p(f,"backgroundColor","var(--art-theme)");function b($){const{width:S}=ft(t,$),{text:_}=$.target.dataset;y.textContent=_;const B=y.clientWidth;S<=B/2?p(y,"left",0):S>s.clientWidth-B/2?p(y,"left",`${s.clientWidth-B}px`):p(y,"left",`${S-B/2}px`)}function C($,S){const{width:_,time:B}=S||ft(t,$);y.textContent=B||"00:00";const ot=y.clientWidth;_<=ot/2?p(y,"left",0):_>s.clientWidth-ot/2?p(y,"left",`${s.clientWidth-ot}px`):p(y,"left",`${_-ot/2}px`)}function z(){m.textContent="";for(let $=0;$<o.highlight.length;$++){const S=o.highlight[$],_=W(S.time,0,t.duration)/t.duration*100,B=`<span data-text="${S.text}" data-time="${S.time}" style="left: ${_}%"></span>`;g(m,B)}}function E($,S,_){const B=$==="played"&&_&&L;if($==="loaded"&&p(u,"width",`${S*100}%`),$==="hover"&&(p(d,"width",`${S*100}%`),lt(_,m)?b(_):C(_),S===0?A(i,"art-progress-hover"):k(i,"art-progress-hover")),$==="played"&&(p(h,"width",`${S*100}%`),p(f,"left",`${S*100}%`)),B){k(i,"art-progress-hover");const ot=s.clientWidth*S,It=Z(S*t.duration);C(_,{width:ot,time:It}),clearTimeout(c),c=setTimeout(()=>{A(i,"art-progress-hover")},500)}}t.on("setBar",E),t.on("video:loadedmetadata",z),t.constructor.USE_RAF?t.on("raf",()=>{t.emit("setBar","played",t.played),t.emit("setBar","loaded",t.loaded)}):(t.on("video:timeupdate",()=>{t.emit("setBar","played",t.played)}),t.on("video:progress",()=>{t.emit("setBar","loaded",t.loaded)}),t.on("video:ended",()=>{t.emit("setBar","played",1)})),t.emit("setBar","loaded",t.loaded||0),L||(r(a,"click",$=>{$.target!==f&&ve(t,$)}),r(a,"mousemove",$=>{const{percentage:S}=ft(t,$);t.emit("setBar","hover",S,$)}),r(a,"mouseleave",$=>{t.emit("setBar","hover",0,$)}),r(a,"mousedown",$=>{l=$.button===0}),t.on("document:mousemove",$=>{if(l){const{second:S,percentage:_}=ft(t,$);t.emit("setBar","played",_,$),t.seek=S}}),t.on("document:mouseup",()=>{l&&(l=!1)}))}}}}function mn(e){return t=>({...e,tooltip:t.i18n.get("Screenshot"),mounted:n=>{const{proxy:o,icons:r}=t;g(n,r.screenshot),o(n,"click",()=>{t.screenshot()})}})}function gn(e){return t=>({...e,tooltip:t.i18n.get("Show Setting"),mounted:n=>{const{proxy:o,icons:r,i18n:i}=t;g(n,r.setting),o(n,"click",()=>{t.setting.toggle(),t.setting.resize()}),t.on("setting",a=>{tt(n,i.get(a?"Hide Setting":"Show Setting"))})}})}function vn(e){return t=>({...e,style:L?{fontSize:"12px",padding:"0 5px"}:{cursor:"auto",padding:"0 10px"},mounted:n=>{function o(){const i=`${Z(t.currentTime)} / ${Z(t.duration)}`;i!==n.textContent&&(n.textContent=i)}o();const r=["video:loadedmetadata","video:timeupdate","video:progress"];for(let i=0;i<r.length;i++)t.on(r[i],o)}})}function yn(e){return t=>({...e,mounted:n=>{const{proxy:o,icons:r}=t,i=g(n,r.volume),a=g(n,r.volumeClose),s=g(n,'<div class="art-volume-panel"></div>'),c=g(s,'<div class="art-volume-inner"></div>'),l=g(c,'<div class="art-volume-val"></div>'),d=g(c,'<div class="art-volume-slider"></div>'),u=g(d,'<div class="art-volume-handle"></div>'),h=g(u,'<div class="art-volume-loaded"></div>'),m=g(d,'<div class="art-volume-indicator"></div>');function f(b){const{top:C,height:z}=K(d);return 1-(b.clientY-C)/z}function y(){if(t.muted||t.volume===0)p(i,"display","none"),p(a,"display","flex"),p(m,"top","100%"),p(h,"top","100%"),l.textContent=0;else{const b=t.volume*100;p(i,"display","flex"),p(a,"display","none"),p(m,"top",`${100-b}%`),p(h,"top",`${100-b}%`),l.textContent=Math.floor(b)}}if(y(),t.on("video:volumechange",y),o(i,"click",()=>{t.muted=!0}),o(a,"click",()=>{t.muted=!1}),L)p(s,"display","none");else{let b=!1;o(d,"mousedown",C=>{b=C.button===0,t.volume=f(C)}),t.on("document:mousemove",C=>{b&&(t.muted=!1,t.volume=f(C))}),t.on("document:mouseup",()=>{b&&(b=!1)})}}})}class bn extends it{constructor(t){super(t),this.isHover=!1,this.name="control",this.timer=Date.now();const{constructor:n}=t,{$player:o,$bottom:r}=this.art.template;t.on("mousemove",()=>{L||(this.show=!0)}),t.on("click",()=>{L?this.toggle():this.show=!0}),t.on("document:mousemove",i=>{this.isHover=lt(i,r)}),t.on("video:timeupdate",()=>{!t.setting.show&&!this.isHover&&!t.isInput&&t.playing&&this.show&&Date.now()-this.timer>=n.CONTROL_HIDE_TIME&&(this.show=!1)}),t.on("control",i=>{i?(A(o,"art-hide-cursor"),k(o,"art-hover"),this.timer=Date.now()):(k(o,"art-hide-cursor"),A(o,"art-hover"))}),this.init()}init(){const{option:t}=this.art;t.isLive||this.add(fn({name:"progress",position:"top",index:10})),this.add({name:"thumbnails",position:"top",index:20}),this.add(hn({name:"playAndPause",position:"left",index:10})),this.add(yn({name:"volume",position:"left",index:20})),t.isLive||this.add(vn({name:"time",position:"left",index:30})),t.quality.length&&pt().then(()=>{this.art.quality=t.quality}),t.screenshot&&!L&&this.add(mn({name:"screenshot",position:"right",index:20})),t.setting&&this.add(gn({name:"setting",position:"right",index:30})),t.pip&&this.add(un({name:"pip",position:"right",index:40})),t.airplay&&window.WebKitPlaybackTargetAvailabilityEvent&&this.add(cn({name:"airplay",position:"right",index:50})),t.fullscreenWeb&&this.add(pn({name:"fullscreenWeb",position:"right",index:60})),t.fullscreen&&this.add(dn({name:"fullscreen",position:"right",index:70}));for(let n=0;n<t.controls.length;n++)this.add(t.controls[n])}add(t){const n=typeof t=="function"?t(this.art):t,{$progress:o,$controlsLeft:r,$controlsRight:i}=this.art.template;switch(n.position){case"top":this.$parent=o;break;case"left":this.$parent=r;break;case"right":this.$parent=i;break;default:U(!1,"Control option.position must one of 'top', 'left', 'right'");break}super.add(n)}check(t){if(t){t.$control_value.innerHTML=t.html;for(let n=0;n<t.$control_option.length;n++){const o=t.$control_option[n];o.default=o===t,o.default&&G(o.$control_item,"art-current")}}}selector(t,n,o){const{proxy:r}=this.art.events;k(n,"art-control-selector");const i=P("div");k(i,"art-selector-value"),g(i,t.html),n.textContent="",g(n,i);const a=P("div");k(a,"art-selector-list"),g(n,a);for(let c=0;c<t.selector.length;c++){const l=t.selector[c],d=P("div");k(d,"art-selector-item"),l.default&&k(d,"art-current"),d.dataset.index=c,d.dataset.value=l.value,d.innerHTML=l.html,g(a,d),v(l,"$control_option",{get:()=>t.selector}),v(l,"$control_item",{get:()=>d}),v(l,"$control_value",{get:()=>i})}const s=r(a,"click",async c=>{const l=Bt(c),d=t.selector.find(u=>u.$control_item===l.find(h=>u.$control_item===h));this.check(d),t.onSelect&&(i.innerHTML=await t.onSelect.call(this.art,d,d.$control_item,c))});o.push(s)}}function wn(e,t){const{constructor:n,template:{$player:o,$video:r}}=e;function i(s){lt(s,o)?(e.isInput=s.target.tagName==="INPUT",e.isFocus=!0,e.emit("focus",s)):(e.isInput=!1,e.isFocus=!1,e.emit("blur",s))}e.on("document:click",i),e.on("document:contextmenu",i);let a=[];t.proxy(r,"click",s=>{const c=Date.now();a.push(c);const{MOBILE_CLICK_PLAY:l,DBCLICK_TIME:d,MOBILE_DBCLICK_PLAY:u,DBCLICK_FULLSCREEN:h}=n,m=a.filter(f=>c-f<=d);switch(m.length){case 1:e.emit("click",s),L?!e.isLock&&l&&e.toggle():e.toggle(),a=m;break;case 2:e.emit("dblclick",s),L?!e.isLock&&u&&e.toggle():h&&(e.fullscreen=!e.fullscreen),a=[];break;default:a=[]}})}function xn(e,t){return Math.atan2(t,e)*180/Math.PI}function kn(e,t,n,o){const r=t-o,i=n-e;let a=0;if(Math.abs(i)<2&&Math.abs(r)<2)return a;const s=xn(i,r);return s>=-45&&s<45?a=4:s>=45&&s<135?a=1:s>=-135&&s<-45?a=2:(s>=135&&s<=180||s>=-180&&s<-135)&&(a=3),a}function $n(e,t){if(L&&!e.option.isLive){const{$video:n,$progress:o}=e.template;let r=null,i=!1,a=0,s=0,c=0;const l=h=>{if(h.touches.length===1&&!e.isLock){r===o&&ve(e,h),i=!0;const{pageX:m,pageY:f}=h.touches[0];a=m,s=f,c=e.currentTime}},d=h=>{if(h.touches.length===1&&i&&e.duration){const{pageX:m,pageY:f}=h.touches[0],y=kn(a,s,m,f),b=[3,4].includes(y),C=[1,2].includes(y);if(b&&!e.isRotate||C&&e.isRotate){const E=W((m-a)/e.width,-1,1),$=W((f-s)/e.height,-1,1),S=e.isRotate?$:E,_=r===n?e.constructor.TOUCH_MOVE_RATIO:1,B=W(c+e.duration*S*_,0,e.duration);e.seek=B,e.emit("setBar","played",W(B/e.duration,0,1),h),e.notice.show=`${Z(B)} / ${Z(e.duration)}`}}},u=()=>{i&&(a=0,s=0,c=0,i=!1,r=null)};e.option.gesture&&(t.proxy(n,"touchstart",h=>{r=n,l(h)}),t.proxy(n,"touchmove",d)),t.proxy(o,"touchstart",h=>{r=o,l(h)}),t.proxy(o,"touchmove",d),e.on("document:touchend",u)}}function Tn(e,t){const n=["click","mouseup","keydown","touchend","touchmove","mousemove","pointerup","contextmenu","pointermove","visibilitychange","webkitfullscreenchange"],o=["resize","scroll","orientationchange"],r=[];function i(a={}){for(let c=0;c<r.length;c++)t.remove(r[c]);r.length=0;const{$player:s}=e.template;n.forEach(c=>{const l=a.document||s.ownerDocument||document,d=t.proxy(l,c,u=>{e.emit(`document:${c}`,u)});r.push(d)}),o.forEach(c=>{const l=a.window||s.ownerDocument?.defaultView||window,d=t.proxy(l,c,u=>{e.emit(`window:${c}`,u)});r.push(d)})}i(),t.bindGlobalEvents=i}function Cn(e,t){const{$player:n}=e.template;t.hover(n,o=>{k(n,"art-hover"),e.emit("hover",!0,o)},o=>{A(n,"art-hover"),e.emit("hover",!1,o)})}function En(e,t){const{$player:n}=e.template;t.proxy(n,"mousemove",o=>{e.emit("mousemove",o)})}function Sn(e,t){const{option:n,constructor:o}=e;e.on("resize",()=>{const{aspectRatio:i,notice:a}=e;e.state==="standard"&&n.autoSize&&e.autoSize(),e.aspectRatio=i,a.show=""});const r=fe(()=>e.emit("resize"),o.RESIZE_TIME);e.on("window:orientationchange",()=>r()),e.on("window:resize",()=>r()),screen&&screen.orientation&&screen.orientation.onchange&&t.proxy(screen.orientation,"change",()=>r())}function zn(e){if(e.constructor.USE_RAF){let t=null;(function n(){e.playing&&e.emit("raf"),e.isDestroy||(t=requestAnimationFrame(n))})(),e.on("destroy",()=>{cancelAnimationFrame(t)})}}function Mn(e){const{option:t,constructor:n,template:{$container:o}}=e,r=me(()=>{e.emit("view",Dt(o,n.SCROLL_GAP))},n.SCROLL_TIME);e.on("window:scroll",()=>r()),e.on("view",i=>{t.autoMini&&(e.mini=!i)})}class _n{constructor(t){this.destroyEvents=new Set,this.proxy=this.proxy.bind(this),this.hover=this.hover.bind(this),wn(t,this),Cn(t,this),En(t,this),Sn(t,this),$n(t,this),Mn(t),Tn(t,this),zn(t)}proxy(t,n,o,r={}){if(Array.isArray(n))return n.map(a=>this.proxy(t,a,o,r));t.addEventListener(n,o,r);const i=()=>t.removeEventListener(n,o,r);return this.destroyEvents.add(i),i}hover(t,n,o){n&&this.proxy(t,"mouseenter",n),o&&this.proxy(t,"mouseleave",o)}remove(t){if(this.destroyEvents.has(t))try{t()}catch(n){console.warn("Failed to remove event listener:",n)}finally{this.destroyEvents.delete(t)}}destroy(){for(const t of this.destroyEvents)try{t()}catch(n){console.warn("Failed to destroy event listener:",n)}this.destroyEvents.clear()}}class Ln{constructor(t){this.art=t,this.keys={},L||this.init()}init(){const{constructor:t}=this.art;this.art.option.hotkey&&(this.add("Escape",()=>{this.art.fullscreenWeb&&(this.art.fullscreenWeb=!1)}),this.add("Space",()=>{this.art.toggle()}),this.add("ArrowLeft",()=>{this.art.backward=t.SEEK_STEP}),this.add("ArrowUp",()=>{this.art.volume+=t.VOLUME_STEP}),this.add("ArrowRight",()=>{this.art.forward=t.SEEK_STEP}),this.add("ArrowDown",()=>{this.art.volume-=t.VOLUME_STEP})),this.art.on("document:keydown",n=>{if(this.art.isFocus){const o=document.activeElement.tagName.toUpperCase(),r=document.activeElement.getAttribute("contenteditable");if(o!=="INPUT"&&o!=="TEXTAREA"&&r!==""&&r!=="true"&&!n.altKey&&!n.ctrlKey&&!n.metaKey&&!n.shiftKey){const i=this.keys[n.code];if(i){n.preventDefault();for(let a=0;a<i.length;a++)i[a].call(this.art,n);this.art.emit("hotkey",n)}}}this.art.emit("keydown",n)})}add(t,n){return this.keys[t]?this.keys[t].includes(n)||this.keys[t].push(n):this.keys[t]=[n],this}remove(t,n){if(this.keys[t]){const o=this.keys[t].indexOf(n);o!==-1&&this.keys[t].splice(o,1),this.keys[t].length===0&&delete this.keys[t]}return this}}const ye={"Video Info":"统计信息",Close:"关闭","Video Load Failed":"加载失败",Volume:"音量",Play:"播放",Pause:"暂停",Rate:"速度",Mute:"静音","Video Flip":"画面翻转",Horizontal:"水平",Vertical:"垂直",Reconnect:"重新连接","Show Setting":"显示设置","Hide Setting":"隐藏设置",Screenshot:"截图","Play Speed":"播放速度","Aspect Ratio":"画面比例",Default:"默认",Normal:"正常",Open:"打开","Switch Video":"切换","Switch Subtitle":"切换字幕",Fullscreen:"全屏","Exit Fullscreen":"退出全屏","Web Fullscreen":"网页全屏","Exit Web Fullscreen":"退出网页全屏","Mini Player":"迷你播放器","PIP Mode":"开启画中画","Exit PIP Mode":"退出画中画","PIP Not Supported":"不支持画中画","Fullscreen Not Supported":"不支持全屏","Subtitle Offset":"字幕偏移","Last Seen":"上次看到","Jump Play":"跳转播放",AirPlay:"隔空播放","AirPlay Not Available":"隔空播放不可用"};typeof window<"u"&&(window["artplayer-i18n-zh-cn"]=ye);class In{constructor(t){this.art=t,this.languages={"zh-cn":ye},this.language={},this.update(t.option.i18n)}init(){const t=this.art.option.lang.toLowerCase();this.language=this.languages[t]||{}}get(t){return this.language[t]||t}update(t){this.languages=Lt(this.languages,t),this.init()}}const Pn=`<svg width="18px" height="18px" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
    <g>
        <path d="M16,1 L2,1 C1.447,1 1,1.447 1,2 L1,12 C1,12.553 1.447,13 2,13 L5,13 L5,11 L3,11 L3,3 L15,3 L15,11 L13,11 L13,13 L16,13 C16.553,13 17,12.553 17,12 L17,2 C17,1.447 16.553,1 16,1 L16,1 Z"></path>
        <polygon points="4 17 14 17 9 11"></polygon>
    </g>
</svg>
`,Rn=`<svg xmlns="http://www.w3.org/2000/svg" height="32" width="32" version="1.1" viewBox="0 0 32 32">
    <path d="M 19.41,20.09 14.83,15.5 19.41,10.91 18,9.5 l -6,6 6,6 z" />
</svg>`,An=`<svg xmlns="http://www.w3.org/2000/svg" height="32" width="32" version="1.1" viewBox="0 0 32 32">
    <path d="m 12.59,20.34 4.58,-4.59 -4.58,-4.59 1.41,-1.41 6,6 -6,6 z" />
</svg>`,Vn='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 88" preserveAspectRatio="xMidYMid meet" style="width: 100%; height: 100%; transform: translate3d(0px, 0px, 0px);"><defs><clipPath id="__lottie_element_216"><rect width="88" height="88" x="0" y="0"></rect></clipPath></defs><g clip-path="url(#__lottie_element_216)"><g transform="matrix(1,0,0,1,44,44)" opacity="1" style="display: block;"><g opacity="1" transform="matrix(1,0,0,1,0,0)"><path fill-opacity="1" d=" M12.437999725341797,-12.70199966430664 C12.437999725341797,-12.70199966430664 9.618000030517578,-9.881999969482422 9.618000030517578,-9.881999969482422 C8.82800006866455,-9.092000007629395 8.82800006866455,-7.831999778747559 9.618000030517578,-7.052000045776367 C9.618000030517578,-7.052000045776367 16.687999725341797,0.017999999225139618 16.687999725341797,0.017999999225139618 C16.687999725341797,0.017999999225139618 9.618000030517578,7.0879998207092285 9.618000030517578,7.0879998207092285 C8.82800006866455,7.877999782562256 8.82800006866455,9.137999534606934 9.618000030517578,9.918000221252441 C9.618000030517578,9.918000221252441 12.437999725341797,12.748000144958496 12.437999725341797,12.748000144958496 C13.227999687194824,13.527999877929688 14.48799991607666,13.527999877929688 15.267999649047852,12.748000144958496 C15.267999649047852,12.748000144958496 26.58799934387207,1.437999963760376 26.58799934387207,1.437999963760376 C27.368000030517578,0.6579999923706055 27.368000030517578,-0.6119999885559082 26.58799934387207,-1.3919999599456787 C26.58799934387207,-1.3919999599456787 15.267999649047852,-12.70199966430664 15.267999649047852,-12.70199966430664 C14.48799991607666,-13.491999626159668 13.227999687194824,-13.491999626159668 12.437999725341797,-12.70199966430664z M-12.442000389099121,-12.70199966430664 C-13.182000160217285,-13.442000389099121 -14.362000465393066,-13.482000350952148 -15.142000198364258,-12.821999549865723 C-15.142000198364258,-12.821999549865723 -15.272000312805176,-12.70199966430664 -15.272000312805176,-12.70199966430664 C-15.272000312805176,-12.70199966430664 -26.582000732421875,-1.3919999599456787 -26.582000732421875,-1.3919999599456787 C-27.32200050354004,-0.6520000100135803 -27.36199951171875,0.5180000066757202 -26.70199966430664,1.3079999685287476 C-26.70199966430664,1.3079999685287476 -26.582000732421875,1.437999963760376 -26.582000732421875,1.437999963760376 C-26.582000732421875,1.437999963760376 -15.272000312805176,12.748000144958496 -15.272000312805176,12.748000144958496 C-14.531999588012695,13.48799991607666 -13.362000465393066,13.527999877929688 -12.571999549865723,12.868000030517578 C-12.571999549865723,12.868000030517578 -12.442000389099121,12.748000144958496 -12.442000389099121,12.748000144958496 C-12.442000389099121,12.748000144958496 -9.612000465393066,9.918000221252441 -9.612000465393066,9.918000221252441 C-8.871999740600586,9.178000450134277 -8.831999778747559,8.008000373840332 -9.501999855041504,7.2179999351501465 C-9.501999855041504,7.2179999351501465 -9.612000465393066,7.0879998207092285 -9.612000465393066,7.0879998207092285 C-9.612000465393066,7.0879998207092285 -16.68199920654297,0.017999999225139618 -16.68199920654297,0.017999999225139618 C-16.68199920654297,0.017999999225139618 -9.612000465393066,-7.052000045776367 -9.612000465393066,-7.052000045776367 C-8.871999740600586,-7.791999816894531 -8.831999778747559,-8.961999893188477 -9.501999855041504,-9.751999855041504 C-9.501999855041504,-9.751999855041504 -9.612000465393066,-9.881999969482422 -9.612000465393066,-9.881999969482422 C-9.612000465393066,-9.881999969482422 -12.442000389099121,-12.70199966430664 -12.442000389099121,-12.70199966430664z M28,-28 C32.41999816894531,-28 36,-24.420000076293945 36,-20 C36,-20 36,20 36,20 C36,24.420000076293945 32.41999816894531,28 28,28 C28,28 -28,28 -28,28 C-32.41999816894531,28 -36,24.420000076293945 -36,20 C-36,20 -36,-20 -36,-20 C-36,-24.420000076293945 -32.41999816894531,-28 -28,-28 C-28,-28 28,-28 28,-28z" data-darkreader-inline-fill="" style="--darkreader-inline-fill:#a8a6a4;"></path></g></g></g></svg>',On=`<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 24 24" style="width: 100%; height: 100%;">
<path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" />
</svg>`,Dn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1655876154826" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="22" height="22">
<path d="M571.733333 512l268.8-268.8c17.066667-17.066667 17.066667-42.666667 0-59.733333-17.066667-17.066667-42.666667-17.066667-59.733333 0L512 452.266667 243.2 183.466667c-17.066667-17.066667-42.666667-17.066667-59.733333 0-17.066667 17.066667-17.066667 42.666667 0 59.733333L452.266667 512 183.466667 780.8c-17.066667 17.066667-17.066667 42.666667 0 59.733333 8.533333 8.533333 19.2 12.8 29.866666 12.8s21.333333-4.266667 29.866667-12.8L512 571.733333l268.8 268.8c8.533333 8.533333 19.2 12.8 29.866667 12.8s21.333333-4.266667 29.866666-12.8c17.066667-17.066667 17.066667-42.666667 0-59.733333L571.733333 512z" p-id="2131">
</path>
</svg>`,Nn='<svg height="24" viewBox="0 0 24 24" width="24"><path d="M15,17h6v1h-6V17z M11,17H3v1h8v2h1v-2v-1v-2h-1V17z M14,8h1V6V5V3h-1v2H3v1h11V8z            M18,5v1h3V5H18z M6,14h1v-2v-1V9H6v2H3v1 h3V14z M10,12h11v-1H10V12z" data-darkreader-inline-fill="" style="--darkreader-inline-fill:#a8a6a4;"></path></svg>',Bn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1652850026663" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2749" xmlns:xlink="http://www.w3.org/1999/xlink" width="50" height="50">
<path d="M593.8176 168.5504l356.00384 595.21024c26.15296 43.74528 10.73152 99.7376-34.44736 125.05088-14.39744 8.06912-30.72 12.30848-47.37024 12.30848H155.97568C103.75168 901.12 61.44 860.16 61.44 809.61536c0-16.09728 4.38272-31.92832 12.71808-45.8752L430.16192 168.5504c26.17344-43.7248 84.00896-58.65472 129.20832-33.34144a93.0816 93.0816 0 0 1 34.44736 33.34144zM512 819.2a61.44 61.44 0 1 0 0-122.88 61.44 61.44 0 0 0 0 122.88z m0-512a72.31488 72.31488 0 0 0-71.76192 81.3056l25.72288 205.7216a46.40768 46.40768 0 0 0 92.07808 0l25.72288-205.74208A72.31488 72.31488 0 0 0 512 307.2z" p-id="2750">
</path>
</svg>`,Yn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1652445277062" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24">
<path d="M554.666667 810.666667v85.333333h-85.333334v-85.333333h85.333334zM170.666667 178.005333a42.666667 42.666667 0 0 1 34.986666 18.218667l203.904 291.328a42.666667 42.666667 0 0 1 0 48.896l-203.946666 291.328A42.666667 42.666667 0 0 1 128 803.328V220.672a42.666667 42.666667 0 0 1 42.666667-42.666667z m682.666666 0a42.666667 42.666667 0 0 1 42.368 37.717334l0.298667 4.949333v582.656a42.666667 42.666667 0 0 1-74.24 28.629333l-3.413333-4.181333-203.904-291.328a42.666667 42.666667 0 0 1-3.029334-43.861333l3.029334-5.034667 203.946666-291.328A42.666667 42.666667 0 0 1 853.333333 178.005333zM554.666667 640v85.333333h-85.333334v-85.333333h85.333334zM196.266667 319.104V716.8L335.957333 512 196.309333 319.104zM554.666667 469.333333v85.333334h-85.333334v-85.333334h85.333334z m0-170.666666v85.333333h-85.333334V298.666667h85.333334z m0-170.666667v85.333333h-85.333334V128h85.333334z">
</path>
</svg>
`,Fn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="22" height="22" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M768 298.666667h170.666667v85.333333h-256V128h85.333333v170.666667zM341.333333 384H85.333333V298.666667h170.666667V128h85.333333v256z m426.666667 341.333333v170.666667h-85.333333v-256h256v85.333333h-170.666667zM341.333333 640v256H256v-170.666667H85.333333v-85.333333h256z" />
</svg>
`,Hn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="22" height="22" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M625.777778 256h142.222222V398.222222h113.777778V142.222222H625.777778v113.777778zM256 398.222222V256H398.222222v-113.777778H142.222222V398.222222h113.777778zM768 625.777778v142.222222H625.777778v113.777778h256V625.777778h-113.777778zM398.222222 768H256V625.777778h-113.777778v256H398.222222v-113.777778z" />
</svg>
`,Wn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="18" height="18" viewBox="0 0 1152 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M1075.2 0H76.8A76.8 76.8 0 0 0 0 76.8v870.4A76.8 76.8 0 0 0 76.8 1024h998.4a76.8 76.8 0 0 0 76.8-76.8V76.8A76.8 76.8 0 0 0 1075.2 0zM1024 128v768H128V128h896zM896 512a64 64 0 0 1 7.488 127.552L896 640h-128v128a64 64 0 0 1-56.512 63.552L704 832a64 64 0 0 1-63.552-56.512L640 768V582.592c0-34.496 25.024-66.112 61.632-70.208L709.632 512H896zM256 512a64 64 0 0 1-7.488-127.552L256 384h128V256a64 64 0 0 1 56.512-63.552L448 192a64 64 0 0 1 63.552 56.512L512 256v185.408c0 34.432-25.024 66.112-61.632 70.144L442.368 512H256z" />
</svg>
`,Un=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="18" height="18" viewBox="0 0 1152 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
<path d="M1075.2 0H76.8A76.8 76.8 0 0 0 0 76.8v870.4A76.8 76.8 0 0 0 76.8 1024h998.4a76.8 76.8 0 0 0 76.8-76.8V76.8A76.8 76.8 0 0 0 1075.2 0zM1024 128v768H128V128h896zM448 192a64 64 0 0 1 7.488 127.552L448 320H320v128a64 64 0 0 1-56.512 63.552L256 512a64 64 0 0 1-63.552-56.512L192 448V262.592c0-34.432 25.024-66.112 61.632-70.144L261.632 192H448zM704 832a64 64 0 0 1-7.488-127.552L704 704h128V576a64 64 0 0 1 56.512-63.552L896 512a64 64 0 0 1 63.552 56.512L960 576v185.408c0 34.496-25.024 66.112-61.632 70.208l-8 0.384H704z" />
</svg>
`,jn=`<svg xmlns="http://www.w3.org/2000/svg" width="50px" height="50px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" class="uil-default">
  <rect x="0" y="0" width="100" height="100" fill="none" class="bk"/>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(0 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-1s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(30 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.9166666666666666s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(60 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.8333333333333334s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(90 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.75s" repeatCount="indefinite"/></rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(120 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.6666666666666666s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(150 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.5833333333333334s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(180 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.5s" repeatCount="indefinite"/></rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(210 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.4166666666666667s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(240 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.3333333333333333s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(270 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.25s" repeatCount="indefinite"/></rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(300 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.16666666666666666s" repeatCount="indefinite"/>
  </rect>
  <rect x="47" y="40" width="6" height="20" rx="5" ry="5" transform="rotate(330 50 50) translate(0 -30)">
    <animate attributeName="opacity" from="1" to="0" dur="1s" begin="-0.08333333333333333s" repeatCount="indefinite"/>
  </rect>
</svg>`,Xn=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1650612139149" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20" height="20">
<path d="M298.666667 426.666667V341.333333a213.333333 213.333333 0 1 1 426.666666 0v85.333334h42.666667a85.333333 85.333333 0 0 1 85.333333 85.333333v256a85.333333 85.333333 0 0 1-85.333333 85.333333H256a85.333333 85.333333 0 0 1-85.333333-85.333333v-256a85.333333 85.333333 0 0 1 85.333333-85.333333h42.666667z m213.333333-213.333334a128 128 0 0 0-128 128v85.333334h256V341.333333a128 128 0 0 0-128-128z"></path>
</svg>
`,qn=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 22 22">
    <path d="M7 3a2 2 0 0 0-2 2v12a2 2 0 1 0 4 0V5a2 2 0 0 0-2-2zM15 3a2 2 0 0 0-2 2v12a2 2 0 1 0 4 0V5a2 2 0 0 0-2-2z"></path>
</svg>`,Gn=`<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="22" height="22">
<path d="M844.8 219.648h-665.6c-6.144 0-10.24 4.608-10.24 10.752v563.2c0 5.632 4.096 10.24 10.24 10.24h256v92.16h-256a102.4 102.4 0 0 1-102.4-102.4v-563.2c0-56.832 45.568-102.4 102.4-102.4h665.6a102.4 102.4 0 0 1 102.4 102.4v204.8h-92.16v-204.8c0-6.144-4.608-10.752-10.24-10.752zM614.4 588.8c-28.672 0-51.2 22.528-51.2 51.2v204.8c0 28.16 22.528 51.2 51.2 51.2h281.6c28.16 0 51.2-23.04 51.2-51.2v-204.8c0-28.672-23.04-51.2-51.2-51.2H614.4z"></path>
</svg>`,Kn=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 22 22">
  <path d="M17.982 9.275L8.06 3.27A2.013 2.013 0 0 0 5 4.994v12.011a2.017 2.017 0 0 0 3.06 1.725l9.922-6.005a2.017 2.017 0 0 0 0-3.45z"></path>
</svg>`,Zn='<svg height="24" viewBox="0 0 24 24" width="24"><path d="M10,8v8l6-4L10,8L10,8z M6.3,5L5.7,4.2C7.2,3,9,2.2,11,2l0.1,1C9.3,3.2,7.7,3.9,6.3,5z            M5,6.3L4.2,5.7C3,7.2,2.2,9,2,11 l1,.1C3.2,9.3,3.9,7.7,5,6.3z            M5,17.7c-1.1-1.4-1.8-3.1-2-4.8L2,13c0.2,2,1,3.8,2.2,5.4L5,17.7z            M11.1,21c-1.8-0.2-3.4-0.9-4.8-2 l-0.6,.8C7.2,21,9,21.8,11,22L11.1,21z            M22,12c0-5.2-3.9-9.4-9-10l-0.1,1c4.6,.5,8.1,4.3,8.1,9s-3.5,8.5-8.1,9l0.1,1 C18.2,21.5,22,17.2,22,12z" data-darkreader-inline-fill="" style="--darkreader-inline-fill:#a8a6a4;"></path></svg>',Jn=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 50 50">
	<path d="M 19.402344 6 C 17.019531 6 14.96875 7.679688 14.5 10.011719 L 14.097656 12 L 9 12 C 6.238281 12 4 14.238281 4 17 L 4 38 C 4 40.761719 6.238281 43 9 43 L 41 43 C 43.761719 43 46 40.761719 46 38 L 46 17 C 46 14.238281 43.761719 12 41 12 L 35.902344 12 L 35.5 10.011719 C 35.03125 7.679688 32.980469 6 30.597656 6 Z M 25 17 C 30.519531 17 35 21.480469 35 27 C 35 32.519531 30.519531 37 25 37 C 19.480469 37 15 32.519531 15 27 C 15 21.480469 19.480469 17 25 17 Z M 25 19 C 20.589844 19 17 22.589844 17 27 C 17 31.410156 20.589844 35 25 35 C 29.410156 35 33 31.410156 33 27 C 33 22.589844 29.410156 19 25 19 Z "/>
</svg>
`,Qn=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 22 22">
    <circle cx="11" cy="11" r="2"></circle>
    <path d="M19.164 8.861L17.6 8.6a6.978 6.978 0 0 0-1.186-2.099l.574-1.533a1 1 0 0 0-.436-1.217l-1.997-1.153a1.001 1.001 0 0 0-1.272.23l-1.008 1.225a7.04 7.04 0 0 0-2.55.001L8.716 2.829a1 1 0 0 0-1.272-.23L5.447 3.751a1 1 0 0 0-.436 1.217l.574 1.533A6.997 6.997 0 0 0 4.4 8.6l-1.564.261A.999.999 0 0 0 2 9.847v2.306c0 .489.353.906.836.986l1.613.269a7 7 0 0 0 1.228 2.075l-.558 1.487a1 1 0 0 0 .436 1.217l1.997 1.153c.423.244.961.147 1.272-.23l1.04-1.263a7.089 7.089 0 0 0 2.272 0l1.04 1.263a1 1 0 0 0 1.272.23l1.997-1.153a1 1 0 0 0 .436-1.217l-.557-1.487c.521-.61.94-1.31 1.228-2.075l1.613-.269a.999.999 0 0 0 .835-.986V9.847a.999.999 0 0 0-.836-.986zM11 15a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"></path>
</svg>`,to=`<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24">
<path d="M9.5 9.325v5.35q0 .575.525.875t1.025-.05l4.15-2.65q.475-.3.475-.85t-.475-.85L11.05 8.5q-.5-.35-1.025-.05t-.525.875ZM12 22q-2.075 0-3.9-.788t-3.175-2.137q-1.35-1.35-2.137-3.175T2 12q0-2.075.788-3.9t2.137-3.175q1.35-1.35 3.175-2.137T12 2q2.075 0 3.9.788t3.175 2.137q1.35 1.35 2.138 3.175T22 12q0 2.075-.788 3.9t-2.137 3.175q-1.35 1.35-3.175 2.138T12 22Z"/>
</svg>
`,eo=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="26" height="26" viewBox="0 0 1740 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <path d="M511.8976 1024h670.5152c282.4192-0.4096 511.1808-229.4784 511.1808-511.8976 0-282.4192-228.7616-511.488-511.1808-511.8976H511.8976C229.4784 0.6144 0.7168 229.6832 0.7168 512.1024c0 282.4192 228.7616 511.488 511.1808 511.8976zM511.3344 48.64A464.5888 464.5888 0 1 1 48.0256 513.024 463.872 463.872 0 0 1 511.3344 48.4352V48.64z" />
</svg>
`,no=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg class="icon" width="26" height="26" viewBox="0 0 1664 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <path fill="#648FFC" d="M1152 0H512a512 512 0 0 0 0 1024h640a512 512 0 0 0 0-1024z m0 960a448 448 0 1 1 448-448 448 448 0 0 1-448 448z"  />
</svg>`,oo=`<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1650612464266" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="20" height="20"><path d="M666.752 194.517333L617.386667 268.629333A128 128 0 0 0 384 341.333333l0.042667 85.333334h384a85.333333 85.333333 0 0 1 85.333333 85.333333v256a85.333333 85.333333 0 0 1-85.333333 85.333333H256a85.333333 85.333333 0 0 1-85.333333-85.333333v-256a85.333333 85.333333 0 0 1 85.333333-85.333333h42.666667V341.333333a213.333333 213.333333 0 0 1 368.085333-146.816z"></path></svg>
`,ro=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 22 22">
    <path d="M15 11a3.998 3.998 0 0 0-2-3.465v2.636l1.865 1.865A4.02 4.02 0 0 0 15 11z"></path>
    <path d="M13.583 5.583A5.998 5.998 0 0 1 17 11a6 6 0 0 1-.585 2.587l1.477 1.477a8.001 8.001 0 0 0-3.446-11.286 1 1 0 0 0-.863 1.805zM18.778 18.778l-2.121-2.121-1.414-1.414-1.415-1.415L13 13l-2-2-3.889-3.889-3.889-3.889a.999.999 0 1 0-1.414 1.414L5.172 8H5a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h1l4.188 3.35a.5.5 0 0 0 .812-.39v-3.131l2.587 2.587-.01.005a1 1 0 0 0 .86 1.806c.215-.102.424-.214.627-.333l2.3 2.3a1.001 1.001 0 0 0 1.414-1.416zM11 5.04a.5.5 0 0 0-.813-.39L8.682 5.854 11 8.172V5.04z"></path>
</svg>`,io=`<svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 22 22">
    <path d="M10.188 4.65L6 8H5a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h1l4.188 3.35a.5.5 0 0 0 .812-.39V5.04a.498.498 0 0 0-.812-.39zM14.446 3.778a1 1 0 0 0-.862 1.804 6.002 6.002 0 0 1-.007 10.838 1 1 0 0 0 .86 1.806A8.001 8.001 0 0 0 19 11a8.001 8.001 0 0 0-4.554-7.222z"></path>
    <path d="M15 11a3.998 3.998 0 0 0-2-3.465v6.93A3.998 3.998 0 0 0 15 11z"></path>
</svg>`;class ao{constructor(t){const n={loading:jn,state:to,play:Kn,pause:qn,check:On,volume:io,volumeClose:ro,screenshot:Jn,setting:Qn,pip:Gn,arrowLeft:Rn,arrowRight:An,playbackRate:Zn,aspectRatio:Vn,config:Nn,lock:Xn,flip:Yn,unlock:oo,fullscreenOff:Fn,fullscreenOn:Hn,fullscreenWebOff:Wn,fullscreenWebOn:Un,switchOn:no,switchOff:eo,error:Bn,close:Dn,airplay:Pn,...t.option.icons};for(const o in n)v(this,o,{get:()=>re(o,n[o])})}}class so extends it{constructor(t){super(t),this.name="info",L||this.init()}init(){const{proxy:t,constructor:n,template:{$infoPanel:o,$infoClose:r,$video:i}}=this.art;t(r,"click",()=>{this.show=!1});let a=null;const s=xt("[data-video]",o)||[];this.art.on("destroy",()=>clearTimeout(a));function c(){for(let l=0;l<s.length;l++){const d=s[l],u=i[d.dataset.video],h=typeof u=="number"?u.toFixed(2):u;d.textContent!==h&&(d.textContent=h)}a=setTimeout(c,n.INFO_LOOP_TIME)}c()}}class lo extends it{constructor(t){super(t);const{option:n,template:{$layer:o}}=t;this.name="layer",this.$parent=o;for(let r=0;r<n.layers.length;r++)this.add(n.layers[r])}}class co extends it{constructor(t){super(t),this.name="loading",g(t.template.$loading,t.icons.loading)}}class po extends it{constructor(t){super(t),this.name="mask";const{template:n,icons:o,events:r}=t,i=g(n.$state,o.state),a=g(n.$state,o.error);p(a,"display","none"),t.on("destroy",()=>{p(i,"display","none"),p(a,"display",null)}),r.proxy(n.$state,"click",()=>t.play())}}class uo{constructor(t){this.art=t,this.timer=null,t.on("destroy",()=>this.destroy())}destroy(){this.timer&&(clearTimeout(this.timer),this.timer=null)}set show(t){const{constructor:n,template:{$player:o,$noticeInner:r}}=this.art;t?(r.textContent=t instanceof Error?t.message.trim():t,k(o,"art-notice-show"),clearTimeout(this.timer),this.timer=setTimeout(()=>{r.textContent="",A(o,"art-notice-show")},n.NOTICE_TIME)):A(o,"art-notice-show")}get show(){const{template:{$player:t}}=this.art;return t.classList.contains("art-notice-show")}}function ho(e){const{i18n:t,notice:n,proxy:o,template:{$video:r}}=e;let i=!0;window.WebKitPlaybackTargetAvailabilityEvent&&r.webkitShowPlaybackTargetPicker?o(r,"webkitplaybacktargetavailabilitychanged",a=>{switch(a.availability){case"available":i=!0;break;case"not-available":i=!1;break}}):i=!1,v(e,"airplay",{value(){i?(r.webkitShowPlaybackTargetPicker(),e.emit("airplay")):n.show=t.get("AirPlay Not Available")}})}function fo(e){const{i18n:t,notice:n,template:{$video:o,$player:r}}=e;v(e,"aspectRatio",{get(){return r.dataset.aspectRatio||"default"},set(i){if(i||(i="default"),i==="default")p(o,"width",null),p(o,"height",null),p(o,"margin",null),delete r.dataset.aspectRatio;else{const a=i.split(":").map(Number),{clientWidth:s,clientHeight:c}=r,l=s/c,d=a[0]/a[1];l>d?(p(o,"width",`${d*c}px`),p(o,"height","100%"),p(o,"margin","0 auto")):(p(o,"width","100%"),p(o,"height",`${s/d}px`),p(o,"margin","auto 0")),r.dataset.aspectRatio=i}n.show=`${t.get("Aspect Ratio")}: ${i==="default"?t.get("Default"):i}`,e.emit("aspectRatio",i)}})}function mo(e){const{template:{$video:t}}=e;v(e,"attr",{value(n,o){if(o===void 0)return t[n];t[n]=o}})}function go(e){const{template:{$container:t,$video:n}}=e;v(e,"autoHeight",{value(){const{clientWidth:o}=t,{videoHeight:r,videoWidth:i}=n,a=r*(o/i);p(t,"height",`${a}px`),e.emit("autoHeight",a)}})}function vo(e){const{$container:t,$player:n,$video:o}=e.template;v(e,"autoSize",{value(){const{videoWidth:r,videoHeight:i}=o,{width:a,height:s}=K(t),c=r/i;if(a/s>c){const d=s*c/a*100;p(n,"width",`${d}%`),p(n,"height","100%")}else{const d=a/c/s*100;p(n,"width","100%"),p(n,"height",`${d}%`)}e.emit("autoSize",{width:e.width,height:e.height})}})}function yo(e){const{$player:t}=e.template;v(e,"cssVar",{value(n,o){return o?t.style.setProperty(n,o):getComputedStyle(t).getPropertyValue(n)}})}function bo(e){const{$video:t}=e.template;v(e,"currentTime",{get:()=>t.currentTime||0,set:n=>{n=Number.parseFloat(n),!Number.isNaN(n)&&(t.currentTime=W(n,0,e.duration))}})}function wo(e){v(e,"duration",{get:()=>{const{duration:t}=e.template.$video;return t===1/0?0:t||0}})}function xo(e){const{i18n:t,notice:n,option:o,constructor:r,proxy:i,template:{$player:a,$video:s,$poster:c}}=e;let l=0;for(let d=0;d<gt.events.length;d++)i(s,gt.events[d],u=>{e.emit(`video:${u.type}`,u)});e.on("video:canplay",()=>{l=0,e.loading.show=!1}),e.once("video:canplay",()=>{e.loading.show=!1,e.controls.show=!0,e.mask.show=!0,e.isReady=!0,e.emit("ready")}),e.on("video:ended",()=>{o.loop?(e.seek=0,e.play(),e.controls.show=!1,e.mask.show=!1):(e.controls.show=!0,e.mask.show=!0)}),e.on("video:error",async d=>{l<r.RECONNECT_TIME_MAX?(await pt(r.RECONNECT_SLEEP_TIME),l+=1,e.url=o.url,n.show=`${t.get("Reconnect")}: ${l}`,e.emit("error",d,l)):(e.mask.show=!0,e.loading.show=!1,e.controls.show=!0,k(a,"art-error"),await pt(r.RECONNECT_SLEEP_TIME),n.show=t.get("Video Load Failed"))}),e.on("video:loadedmetadata",()=>{e.emit("resize"),L&&(e.loading.show=!1,e.controls.show=!0,e.mask.show=!0)}),e.on("video:loadstart",()=>{e.loading.show=!0,e.mask.show=!1,e.controls.show=!0}),e.on("video:pause",()=>{e.controls.show=!0,e.mask.show=!0}),e.on("video:play",()=>{e.mask.show=!1,p(c,"display","none")}),e.on("video:playing",()=>{e.mask.show=!1}),e.on("video:progress",()=>{e.playing&&(e.loading.show=!1)}),e.on("video:seeked",()=>{e.loading.show=!1,e.mask.show=!0}),e.on("video:seeking",()=>{e.loading.show=!0,e.mask.show=!1}),e.on("video:timeupdate",()=>{e.mask.show=!1}),e.on("video:waiting",()=>{e.loading.show=!0,e.mask.show=!1})}function ko(e){const{template:{$player:t},i18n:n,notice:o}=e;v(e,"flip",{get(){return t.dataset.flip||"normal"},set(r){r||(r="normal"),r==="normal"?delete t.dataset.flip:t.dataset.flip=r,o.show=`${n.get("Video Flip")}: ${n.get(_t(r))}`,e.emit("flip",r)}})}const Xt=[["requestFullscreen","exitFullscreen","fullscreenElement","fullscreenEnabled","fullscreenchange","fullscreenerror"],["webkitRequestFullscreen","webkitExitFullscreen","webkitFullscreenElement","webkitFullscreenEnabled","webkitfullscreenchange","webkitfullscreenerror"],["webkitRequestFullScreen","webkitCancelFullScreen","webkitCurrentFullScreenElement","webkitCancelFullScreen","webkitfullscreenchange","webkitfullscreenerror"],["mozRequestFullScreen","mozCancelFullScreen","mozFullScreenElement","mozFullScreenEnabled","mozfullscreenchange","mozfullscreenerror"],["msRequestFullscreen","msExitFullscreen","msFullscreenElement","msFullscreenEnabled","MSFullscreenChange","MSFullscreenError"]],rt=(()=>{if(typeof document>"u")return!1;const e=Xt[0],t={};for(const n of Xt)if(n[1]in document){for(const[r,i]of n.entries())t[e[r]]=i;return t}return!1})(),qt={change:rt.fullscreenchange,error:rt.fullscreenerror},R={request(e=document.documentElement,t){return new Promise((n,o)=>{const r=()=>{R.off("change",r),n()};R.on("change",r);const i=e[rt.requestFullscreen](t);i instanceof Promise&&i.then(r).catch(o)})},exit(){return new Promise((e,t)=>{if(!R.isFullscreen){e();return}const n=()=>{R.off("change",n),e()};R.on("change",n);const o=document[rt.exitFullscreen]();o instanceof Promise&&o.then(n).catch(t)})},toggle(e,t){return R.isFullscreen?R.exit():R.request(e,t)},onchange(e){R.on("change",e)},onerror(e){R.on("error",e)},on(e,t){const n=qt[e];n&&document.addEventListener(n,t,!1)},off(e,t){const n=qt[e];n&&document.removeEventListener(n,t,!1)},raw:rt};Object.defineProperties(R,{isFullscreen:{get:()=>!!document[rt.fullscreenElement]},element:{enumerable:!0,get:()=>document[rt.fullscreenElement]},isEnabled:{enumerable:!0,get:()=>!!document[rt.fullscreenEnabled]}});function $o(e){const{i18n:t,notice:n,template:{$video:o,$player:r}}=e,i=s=>{R.on("change",()=>{s.emit("fullscreen",R.isFullscreen),R.isFullscreen?(s.state="fullscreen",k(r,"art-fullscreen")):A(r,"art-fullscreen"),s.emit("resize")}),R.on("error",c=>{s.emit("fullscreenError",c)}),v(s,"fullscreen",{get(){return R.isFullscreen},async set(c){c?await R.request(r):await R.exit()}})},a=s=>{s.on("document:webkitfullscreenchange",()=>{s.emit("fullscreen",s.fullscreen),s.emit("resize")}),v(s,"fullscreen",{get(){return document.fullscreenElement===o},set(c){c?(s.state="fullscreen",o.webkitEnterFullscreen()):o.webkitExitFullscreen()}})};e.once("video:loadedmetadata",()=>{R.isEnabled?i(e):o.webkitSupportsFullscreen?a(e):v(e,"fullscreen",{get(){return!1},set(){n.show=t.get("Fullscreen Not Supported")}}),v(e,"fullscreen",pe(e,"fullscreen"))})}function To(e){const{constructor:t,template:{$container:n,$player:o}}=e;let r="";v(e,"fullscreenWeb",{get(){return Q(o,"art-fullscreen-web")},set(i){i?(r=o.style.cssText,t.FULLSCREEN_WEB_IN_BODY&&g(document.body,o),e.state="fullscreenWeb",p(o,"width","100%"),p(o,"height","100%"),k(o,"art-fullscreen-web"),e.emit("fullscreenWeb",!0)):(t.FULLSCREEN_WEB_IN_BODY&&g(n,o),r&&(o.style.cssText=r,r=""),A(o,"art-fullscreen-web"),e.emit("fullscreenWeb",!1)),e.emit("resize")}})}function Co(e){const{$video:t}=e.template;v(e,"loaded",{get:()=>e.loadedTime/t.duration}),v(e,"loadedTime",{get:()=>t.buffered.length?t.buffered.end(t.buffered.length-1):0})}function Eo(e){const{icons:t,proxy:n,storage:o,template:{$player:r,$video:i}}=e;let a=!1,s=0,c=0;function l(){const{$mini:m}=e.template;m&&(A(r,"art-mini"),p(m,"display","none"),r.prepend(i),e.emit("mini",!1))}function d(m,f){e.playing?(p(m,"display","none"),p(f,"display","flex")):(p(m,"display","flex"),p(f,"display","none"))}function u(){const{$mini:m}=e.template;if(m)return g(m,i),p(m,"display","flex");{const f=P("div");k(f,"art-mini-popup"),g(document.body,f),e.template.$mini=f,g(f,i);const y=g(f,'<div class="art-mini-close"></div>');g(y,t.close),n(y,"click",l);const b=g(f,'<div class="art-mini-state"></div>'),C=g(b,t.play),z=g(b,t.pause);return n(C,"click",()=>e.play()),n(z,"click",()=>e.pause()),d(C,z),e.on("video:playing",()=>d(C,z)),e.on("video:pause",()=>d(C,z)),e.on("video:timeupdate",()=>d(C,z)),n(f,"mousedown",E=>{a=E.button===0,s=E.pageX,c=E.pageY}),e.on("document:mousemove",E=>{if(a){k(f,"art-mini-dragging");const $=E.pageX-s,S=E.pageY-c;p(f,"transform",`translate(${$}px, ${S}px)`)}}),e.on("document:mouseup",()=>{if(a){a=!1,A(f,"art-mini-dragging");const E=K(f);o.set("left",E.left),o.set("top",E.top),p(f,"left",`${E.left}px`),p(f,"top",`${E.top}px`),p(f,"transform",null)}}),f}}function h(){const{$mini:m}=e.template,f=K(m),y=window.innerHeight-f.height-50,b=window.innerWidth-f.width-50;o.set("top",y),o.set("left",b),p(m,"top",`${y}px`),p(m,"left",`${b}px`)}v(e,"mini",{get(){return Q(r,"art-mini")},set(m){if(m){e.state="mini",k(r,"art-mini");const f=u(),y=o.get("top"),b=o.get("left");typeof y=="number"&&typeof b=="number"?(p(f,"top",`${y}px`),p(f,"left",`${b}px`),Dt(f)||h()):h(),e.emit("mini",!0)}else l()}})}function So(e){const{option:t,storage:n,template:{$video:o,$poster:r}}=e;for(const a in t.moreVideoAttr)e.attr(a,t.moreVideoAttr[a]);t.muted&&(e.muted=t.muted),t.volume&&(o.volume=W(t.volume,0,1));const i=n.get("volume");typeof i=="number"&&(o.volume=W(i,0,1)),t.poster&&p(r,"backgroundImage",`url(${t.poster})`),t.autoplay&&(o.autoplay=t.autoplay),t.playsInline&&(o.playsInline=!0,o["webkit-playsinline"]=!0),t.theme&&(t.cssVar["--art-theme"]=t.theme);for(const a in t.cssVar)e.cssVar(a,t.cssVar[a]);e.url=t.url}function zo(e){const{template:{$video:t},i18n:n,notice:o}=e;v(e,"pause",{value(){const r=t.pause();return o.show=n.get("Pause"),e.emit("pause"),r}})}function Mo(e){const{template:{$video:t},proxy:n,notice:o}=e;t.disablePictureInPicture=!1,v(e,"pip",{get(){return document.pictureInPictureElement},set(r){r?(e.state="pip",t.requestPictureInPicture().catch(i=>{throw o.show=i,i})):document.exitPictureInPicture().catch(i=>{throw o.show=i,i})}}),n(t,"enterpictureinpicture",()=>{e.emit("pip",!0)}),n(t,"leavepictureinpicture",()=>{e.emit("pip",!1)})}function _o(e){const{$video:t}=e.template;t.webkitSetPresentationMode("inline"),v(e,"pip",{get(){return t.webkitPresentationMode==="picture-in-picture"},set(n){n?(e.state="pip",t.webkitSetPresentationMode("picture-in-picture"),e.emit("pip",!0)):(t.webkitSetPresentationMode("inline"),e.emit("pip",!1))}})}function Lo(e){const{i18n:t,notice:n,template:{$video:o}}=e;document.pictureInPictureEnabled?Mo(e):o.webkitSupportsPresentationMode?_o(e):v(e,"pip",{get(){return!1},set(){n.show=t.get("PIP Not Supported")}})}function Io(e){const{template:{$video:t},i18n:n,notice:o}=e;v(e,"playbackRate",{get(){return t.playbackRate},set(r){if(r){if(r===t.playbackRate)return;t.playbackRate=r,o.show=`${n.get("Rate")}: ${r===1?n.get("Normal"):`${r}x`}`}else e.playbackRate=1}})}function Po(e){v(e,"played",{get:()=>e.currentTime/e.duration})}function Ro(e){const{$video:t}=e.template;v(e,"playing",{get:()=>typeof t.playing=="boolean"?t.playing:t.currentTime>0&&!t.paused&&!t.ended&&t.readyState>2})}function Ao(e){const{i18n:t,notice:n,option:o,constructor:{instances:r},template:{$video:i}}=e;v(e,"play",{async value(){const a=await i.play();if(n.show=t.get("Play"),e.emit("play"),o.mutex)for(let s=0;s<r.length;s++){const c=r[s];c!==e&&c.pause()}return a}})}function Vo(e){const{template:{$poster:t}}=e;v(e,"poster",{get:()=>{try{return t.style.backgroundImage.match(/"(.*)"/)[1]}catch{return""}},set(n){p(t,"backgroundImage",`url(${n})`)}})}function Oo(e){v(e,"quality",{set(t){const{controls:n,notice:o,i18n:r}=e,i=t.find(a=>a.default)||t[0];n.update({name:"quality",position:"right",index:10,style:{marginRight:"10px"},html:i?.html||"",selector:t,async onSelect(a){return await e.switchQuality(a.url),o.show=`${r.get("Switch Video")}: ${a.html}`,a.html}})}})}function Do(e){v(e,"rect",{get:()=>K(e.template.$player)});const t=["bottom","height","left","right","top","width"];for(let n=0;n<t.length;n++){const o=t[n];v(e,o,{get:()=>e.rect[o]})}v(e,"x",{get:()=>e.left+window.pageXOffset}),v(e,"y",{get:()=>e.top+window.pageYOffset})}function No(e){const{notice:t,template:{$video:n}}=e,o=P("canvas");v(e,"getDataURL",{value:()=>new Promise((r,i)=>{try{o.width=n.videoWidth,o.height=n.videoHeight,o.getContext("2d").drawImage(n,0,0),r(o.toDataURL("image/png"))}catch(a){t.show=a,i(a)}})}),v(e,"getBlobUrl",{value:()=>new Promise((r,i)=>{try{o.width=n.videoWidth,o.height=n.videoHeight,o.getContext("2d").drawImage(n,0,0),o.toBlob(a=>{r(URL.createObjectURL(a))})}catch(a){t.show=a,i(a)}})}),v(e,"screenshot",{value:async r=>{const i=await e.getDataURL(),a=r||`artplayer_${Z(n.currentTime)}`;return ce(i,`${a}.png`),e.emit("screenshot",i),i}})}function Bo(e){const{notice:t}=e;v(e,"seek",{set(n){e.currentTime=n,e.duration&&(t.show=`${Z(e.currentTime)} / ${Z(e.duration)}`),e.emit("seek",e.currentTime,n)}}),v(e,"forward",{set(n){e.seek=e.currentTime+n}}),v(e,"backward",{set(n){e.seek=e.currentTime-n}})}function Yo(e){const t=["mini","pip","fullscreen","fullscreenWeb"];v(e,"state",{get:()=>t.find(n=>e[n])||"standard",set(n){for(let o=0;o<t.length;o++){const r=t[o];r!==n&&e[r]&&(e[r]=!1)}}})}function Fo(e){const{notice:t,i18n:n,template:o}=e;v(e,"subtitleOffset",{get(){return o.$track?.offset||0},set(r){const{cues:i}=e.subtitle;if(!o.$track||i.length===0)return;const a=W(r,-10,10);o.$track.offset=a;for(let s=0;s<i.length;s++){const c=i[s];c.originalStartTime=c.originalStartTime??c.startTime,c.originalEndTime=c.originalEndTime??c.endTime,c.startTime=W(c.originalStartTime+a,0,e.duration),c.endTime=W(c.originalEndTime+a,0,e.duration)}e.subtitle.update(),t.show=`${n.get("Subtitle Offset")}: ${r}s`,e.emit("subtitleOffset",r)}})}function Ho(e){function t(n,o){return new Promise((r,i)=>{if(n===e.url){r();return}const{playing:a,aspectRatio:s,playbackRate:c}=e;e.pause(),e.url=n,e.notice.show="";const l={};l.error=d=>{e.off("video:canplay",l.canplay),e.off("video:loadedmetadata",l.metadata),i(d)},l.metadata=()=>{e.currentTime=o},l.canplay=async()=>{e.off("video:error",l.error),e.playbackRate=c,e.aspectRatio=s,a&&await e.play(),e.notice.show="",r()},e.once("video:error",l.error),e.once("video:loadedmetadata",l.metadata),e.once("video:canplay",l.canplay)})}v(e,"switchQuality",{value:n=>t(n,e.currentTime)}),v(e,"switchUrl",{value:n=>t(n,0)}),v(e,"switch",{set:e.switchUrl})}function Wo(e){v(e,"theme",{get(){return e.cssVar("--art-theme")},set(t){e.cssVar("--art-theme",t)}})}function Uo(e){const{option:t,template:{$progress:n,$video:o}}=e;let r=null,i=!1,a=null;function s(){clearTimeout(r),r=null,i=!1,a=null}function c(l){const d=e.controls?.thumbnails;if(!d)return;const{number:u,column:h,width:m,height:f,scale:y}=t.thumbnails,b=m*y||a.naturalWidth/h,C=f*y||b/(o.videoWidth/o.videoHeight),z=n.clientWidth/u,E=Math.floor(l/z),$=Math.ceil(E/h)-1,S=E%h||h-1;p(d,"backgroundImage",`url(${a.src})`),p(d,"height",`${C}px`),p(d,"width",`${b}px`),p(d,"backgroundPosition",`-${S*b}px -${$*C}px`),l<=b/2?p(d,"left",0):l>n.clientWidth-b/2?p(d,"left",`${n.clientWidth-b}px`):p(d,"left",`${l-b/2}px`)}e.on("setBar",async(l,d,u)=>{const h=e.controls?.thumbnails,{url:m,scale:f}=t.thumbnails;if(!h||!m)return;if(l==="hover"||l==="played"&&u&&L){if(!a&&!i&&(i=!0,a=await se(m,f),i=!1),!a)return;const b=n.clientWidth*d;b>0&&b<n.clientWidth&&c(b)}}),v(e,"thumbnails",{get(){return e.option.thumbnails},set(l){l.url&&!e.option.isLive&&(e.option.thumbnails=l,s())}})}function jo(e){v(e,"toggle",{value(){return e.playing?e.pause():e.play()}})}function Xo(e){v(e,"type",{get(){return e.option.type},set(t){e.option.type=t}})}function qo(e){const{option:t,template:{$video:n}}=e;v(e,"url",{get(){return n.src},async set(o){if(o){const r=e.url,i=t.type||yt(o),a=t.customType[i];i&&a?(await pt(),e.loading.show=!0,a.call(e,n,o,e)):(URL.revokeObjectURL(r),n.src=o),r!==e.url&&(e.option.url=o,e.isReady&&r&&e.once("video:canplay",()=>{e.emit("restart",o)}))}else await pt(),e.loading.show=!0}})}function Go(e){const{template:{$video:t},i18n:n,notice:o,storage:r}=e;v(e,"volume",{get:()=>t.volume||0,set:i=>{t.volume=W(i,0,1),o.show=`${n.get("Volume")}: ${Number.parseInt(t.volume*100,10)}`,t.volume!==0&&r.set("volume",t.volume)}}),v(e,"muted",{get:()=>t.muted,set:i=>{t.muted=i,e.emit("muted",i)}})}class Ko{constructor(t){qo(t),mo(t),Ao(t),zo(t),jo(t),Bo(t),Go(t),bo(t),wo(t),Ho(t),Io(t),fo(t),No(t),$o(t),To(t),Lo(t),Co(t),Po(t),Ro(t),vo(t),Do(t),ko(t),Eo(t),Vo(t),go(t),yo(t),Wo(t),Xo(t),Yo(t),Fo(t),ho(t),Oo(t),Uo(t),xo(t),So(t)}}function Zo(e){const{notice:t,constructor:n,template:{$player:o,$video:r}}=e,i="art-auto-orientation",a="art-auto-orientation-fullscreen";let s=!1;function c(){const u=document.documentElement.clientWidth,h=document.documentElement.clientHeight;p(o,"width",`${h}px`),p(o,"height",`${u}px`),p(o,"transform-origin","0 0"),p(o,"transform",`rotate(90deg) translate(0, -${u}px)`),k(o,i),e.isRotate=!0,e.emit("resize")}function l(){p(o,"width",""),p(o,"height",""),p(o,"transform-origin",""),p(o,"transform",""),A(o,i),e.isRotate=!1,e.emit("resize")}function d(){const{videoWidth:u,videoHeight:h}=r,m=document.documentElement.clientWidth,f=document.documentElement.clientHeight;return u>h&&m<f||u<h&&m>f}return e.on("fullscreenWeb",u=>{if(u){if(d()){const h=Number(n.AUTO_ORIENTATION_TIME??0);setTimeout(()=>{e.fullscreenWeb&&!Q(o,i)&&c()},h)}}else Q(o,i)&&l()}),e.on("fullscreen",async u=>{const h=!!screen?.orientation?.lock;if(u){if(h&&d())try{const f=screen.orientation.type.startsWith("portrait")?"landscape":"portrait";await screen.orientation.lock(f),s=!0,k(o,a)}catch(m){s=!1,t.show=m}}else if(Q(o,a)&&A(o,a),h&&s){try{screen.orientation.unlock()}catch{}s=!1}}),{name:"autoOrientation",get state(){return Q(o,i)}}}function Jo(e){const{i18n:t,icons:n,storage:o,constructor:r,proxy:i,template:{$poster:a}}=e,s=e.layers.add({name:"auto-playback",html:`
            <div class="art-auto-playback-close"></div>
            <div class="art-auto-playback-last"></div>
            <div class="art-auto-playback-jump"></div>
        `}),c=H(".art-auto-playback-last",s),l=H(".art-auto-playback-jump",s),d=H(".art-auto-playback-close",s);g(d,n.close);let u=null;e.on("video:timeupdate",()=>{if(e.playing){const m=o.get("times")||{},f=Object.keys(m);f.length>r.AUTO_PLAYBACK_MAX&&delete m[f[0]],m[e.option.id||e.option.url]=e.currentTime,o.set("times",m)}});function h(){const f=(o.get("times")||{})[e.option.id||e.option.url];clearTimeout(u),p(s,"display","none"),f&&f>=r.AUTO_PLAYBACK_MIN&&(p(s,"display","flex"),c.textContent=`${t.get("Last Seen")} ${Z(f)}`,l.textContent=t.get("Jump Play"),i(d,"click",()=>{p(s,"display","none")}),i(l,"click",()=>{e.seek=f,e.play(),p(a,"display","none"),p(s,"display","none")}),e.once("video:timeupdate",()=>{u=setTimeout(()=>{p(s,"display","none")},r.AUTO_PLAYBACK_TIMEOUT)}))}return e.on("ready",h),e.on("restart",h),{name:"auto-playback",get times(){return o.get("times")||{}},clear(){return o.del("times")},delete(m){const f=o.get("times")||{};return delete f[m],o.set("times",f),f}}}function Qo(e){const{constructor:t,proxy:n,template:{$player:o,$video:r}}=e;let i=null,a=!1,s=1;const c=d=>{d.touches.length===1&&e.playing&&!e.isLock&&(i=setTimeout(()=>{a=!0,s=e.playbackRate,e.playbackRate=t.FAST_FORWARD_VALUE,k(o,"art-fast-forward")},t.FAST_FORWARD_TIME))},l=()=>{clearTimeout(i),a&&(a=!1,e.playbackRate=s,A(o,"art-fast-forward"))};return n(r,"touchstart",c),e.on("document:touchmove",l),e.on("document:touchend",l),{name:"fastForward",get state(){return Q(o,"art-fast-forward")}}}function tr(e){const{layers:t,icons:n,template:{$player:o}}=e;function r(){return Q(o,"art-lock")}function i(){k(o,"art-lock"),e.isLock=!0,e.emit("lock",!0)}function a(){A(o,"art-lock"),e.isLock=!1,e.emit("lock",!1)}return t.add({name:"lock",mounted(s){const c=g(s,n.lock),l=g(s,n.unlock);p(c,"display","none"),e.on("lock",d=>{d?(p(c,"display","inline-flex"),p(l,"display","none")):(p(c,"display","none"),p(l,"display","inline-flex"))})},click(){r()?a():i()}}),{name:"lock",get state(){return r()},set state(s){s?i():a()}}}function er(e){return e.on("control",t=>{t?A(e.template.$player,"art-mini-progress-bar"):k(e.template.$player,"art-mini-progress-bar")}),{name:"mini-progress-bar"}}class nr{constructor(t){this.art=t,this.id=0;const{option:n}=t;n.miniProgressBar&&!n.isLive&&this.add(er),n.lock&&L&&this.add(tr),n.autoPlayback&&!n.isLive&&this.add(Jo),n.autoOrientation&&L&&this.add(Zo),n.fastForward&&L&&!n.isLive&&this.add(Qo);for(let o=0;o<n.plugins.length;o++)this.add(n.plugins[o])}add(t){this.id+=1;const n=t.call(this.art,this.art);return n instanceof Promise?n.then(o=>this.next(t,o)):this.next(t,n)}next(t,n){const o=n&&n.name||t.name||`plugin${this.id}`;return U(!vt(this,o),`Cannot add a plugin that already has the same name: ${o}`),v(this,o,{value:n}),this}}function or(e){const{i18n:t,icons:n,constructor:{SETTING_ITEM_WIDTH:o,ASPECT_RATIO:r}}=e;function i(s){return s==="default"?t.get("Default"):s}function a(){const s=e.setting.find(`aspect-ratio-${e.aspectRatio}`);e.setting.check(s)}return{width:o,name:"aspect-ratio",html:t.get("Aspect Ratio"),icon:n.aspectRatio,tooltip:i(e.aspectRatio),selector:r.map(s=>({value:s,name:`aspect-ratio-${s}`,default:s===e.aspectRatio,html:i(s)})),onSelect(s){return e.aspectRatio=s.value,s.html},mounted:()=>{a(),e.on("aspectRatio",()=>a())}}}function rr(e){const{i18n:t,icons:n,constructor:{SETTING_ITEM_WIDTH:o,FLIP:r}}=e;function i(s){return t.get(_t(s))}function a(){const s=e.setting.find(`flip-${e.flip}`);e.setting.check(s)}return{width:o,name:"flip",html:t.get("Video Flip"),tooltip:i(e.flip),icon:n.flip,selector:r.map(s=>({value:s,name:`flip-${s}`,default:s===e.flip,html:i(s)})),onSelect(s){return e.flip=s.value,s.html},mounted:()=>{a(),e.on("flip",()=>a())}}}function ir(e){const{i18n:t,icons:n,constructor:{SETTING_ITEM_WIDTH:o,PLAYBACK_RATE:r}}=e;function i(s){return s===1?t.get("Normal"):s.toFixed(1)}function a(){const s=e.setting.find(`playback-rate-${e.playbackRate}`);e.setting.check(s)}return{width:o,name:"playback-rate",html:t.get("Play Speed"),tooltip:i(e.playbackRate),icon:n.playbackRate,selector:r.map(s=>({value:s,name:`playback-rate-${s}`,default:s===e.playbackRate,html:i(s)})),onSelect(s){return e.playbackRate=s.value,s.html},mounted:()=>{a(),e.on("video:ratechange",()=>a())}}}function ar(e){const{i18n:t,icons:n,constructor:o}=e;return{width:o.SETTING_ITEM_WIDTH,name:"subtitle-offset",html:t.get("Subtitle Offset"),icon:n.subtitle,tooltip:"0s",range:[0,-10,10,.1],onChange(r){return e.subtitleOffset=r.range[0],`${r.range[0]}s`},mounted:(r,i)=>{e.on("subtitleOffset",a=>{i.$range.value=a,i.tooltip=`${a}s`})}}}class sr extends it{constructor(t){super(t);const{option:n,controls:o,template:{$setting:r}}=t;this.name="setting",this.$parent=r,this.id=0,this.active=null,this.cache=new Map,this.option=[...this.builtin,...n.settings],n.setting&&(this.format(),this.render(),t.on("blur",()=>{this.show&&(this.show=!1,this.render())}),t.on("focus",i=>{const a=lt(i,o.setting),s=lt(i,this.$parent);this.show&&!a&&!s&&(this.show=!1,this.render())}),t.on("resize",()=>this.resize()))}get builtin(){const t=[],{option:n}=this.art;return n.playbackRate&&t.push(ir(this.art)),n.aspectRatio&&t.push(or(this.art)),n.flip&&t.push(rr(this.art)),n.subtitleOffset&&t.push(ar(this.art)),t}traverse(t,n=this.option){for(let o=0;o<n.length;o++){const r=n[o];t(r),r.selector?.length&&this.traverse(t,r.selector)}}check(t){t&&(t.$parent.tooltip=t.html,this.traverse(n=>{n.default=n===t,n.default&&n.$item&&G(n.$item,"art-current")},t.$option),this.render(t.$parents))}format(t=this.option,n,o,r=[]){for(let i=0;i<t.length;i++){const a=t[i];if(a?.name?(U(!r.includes(a.name),`The [${a.name}] already exists in [setting]`),r.push(a.name)):a.name=`setting-${this.id++}`,!a.$formatted){v(a,"$parent",{get:()=>n}),v(a,"$parents",{get:()=>o}),v(a,"$option",{get:()=>t});const s=[];v(a,"$events",{get:()=>s}),v(a,"$formatted",{get:()=>!0})}this.format(a.selector||[],a,t,r)}this.option=t}find(t=""){let n=null;return this.traverse(o=>{o.name===t&&(n=o)}),n}resize(){const{controls:t,constructor:{SETTING_WIDTH:n,SETTING_ITEM_HEIGHT:o},template:{$player:r,$setting:i}}=this.art;if(t.setting&&this.show){const a=this.active[0]?.$parent?.width||n,{left:s,width:c}=K(t.setting),{left:l,width:d}=K(r),u=s-l+c/2-a/2,h=this.active===this.option?this.active.length*o:(this.active.length+1)*o;if(p(i,"height",`${h}px`),p(i,"width",`${a}px`),this.art.isRotate||L)return;u+a>d?(p(i,"left",null),p(i,"right",null)):(p(i,"left",`${u}px`),p(i,"right","auto"))}}inactivate(t){for(let n=0;n<t.$events.length;n++)this.art.events.remove(t.$events[n]);t.$events.length=0}remove(t){const n=this.find(t);U(n,`Can't find [${t}] in the [setting]`);const o=n.$option.indexOf(n);n.$option.splice(o,1),this.inactivate(n),n.$item&&zt(n.$item),this.render()}update(t){const n=this.find(t.name);return n?(this.inactivate(n),Object.assign(n,t),this.format(),this.createItem(n,!0),this.render(),n):this.add(t)}add(t,n=this.option){return n.push(t),this.format(),this.createItem(t),this.render(),t}createHeader(t){if(!this.cache.has(t.$option))return;const n=this.cache.get(t.$option),{proxy:o,icons:{arrowLeft:r},constructor:{SETTING_ITEM_HEIGHT:i}}=this.art,a=P("div");p(a,"height",`${i}px`),k(a,"art-setting-item"),k(a,"art-setting-item-back");const s=g(a,'<div class="art-setting-item-left"></div>'),c=P("div");k(c,"art-setting-item-left-icon"),g(c,r),g(s,c),g(s,t.$parent.html);const l=o(a,"click",()=>this.render(t.$parents));t.$parent.$events.push(l),g(n,a)}createItem(t,n=!1){if(!this.cache.has(t.$option))return;const o=this.cache.get(t.$option),r=t.$item;let i="selector";vt(t,"switch")&&(i="switch"),vt(t,"range")&&(i="range"),vt(t,"onClick")&&(i="button");const{icons:a,proxy:s,constructor:c}=this.art,l=P("div");k(l,"art-setting-item"),p(l,"height",`${c.SETTING_ITEM_HEIGHT}px`),l.dataset.name=t.name||"",l.dataset.value=t.value||"";const d=g(l,'<div class="art-setting-item-left"></div>'),u=g(l,'<div class="art-setting-item-right"></div>'),h=P("div");switch(k(h,"art-setting-item-left-icon"),i){case"button":case"switch":case"range":g(h,t.icon||a.config);break;case"selector":t.selector?.length?g(h,t.icon||a.config):g(h,a.check);break}g(d,h),v(t,"$icon",{configurable:!0,get:()=>h}),v(t,"icon",{configurable:!0,get(){return h.innerHTML},set(y){h.innerHTML="",g(h,y)}});const m=P("div");k(m,"art-setting-item-left-text"),g(m,t.html||""),g(d,m),v(t,"$html",{configurable:!0,get:()=>m}),v(t,"html",{configurable:!0,get(){return m.innerHTML},set(y){m.innerHTML="",g(m,y)}});const f=P("div");switch(k(f,"art-setting-item-right-tooltip"),g(f,t.tooltip||""),g(u,f),v(t,"$tooltip",{configurable:!0,get:()=>f}),v(t,"tooltip",{configurable:!0,get(){return f.innerHTML},set(y){f.innerHTML="",g(f,y)}}),i){case"switch":{const y=P("div");k(y,"art-setting-item-right-icon");const b=g(y,a.switchOn),C=g(y,a.switchOff);p(t.switch?C:b,"display","none"),g(u,y),v(t,"$switch",{configurable:!0,get:()=>y});let z=t.switch;v(t,"switch",{configurable:!0,get:()=>z,set(E){z=E,E?(p(C,"display","none"),p(b,"display",null)):(p(C,"display",null),p(b,"display","none"))}});break}case"range":{const y=P("div");k(y,"art-setting-item-right-icon");const b=g(y,'<input type="range">');b.value=t.range[0],b.min=t.range[1],b.max=t.range[2],b.step=t.range[3],k(b,"art-setting-range"),g(u,y),v(t,"$range",{configurable:!0,get:()=>b});let C=[...t.range];v(t,"range",{configurable:!0,get:()=>C,set(z){C=[...z],b.value=z[0],b.min=z[1],b.max=z[2],b.step=z[3]}})}break;case"selector":if(t.selector?.length){const y=P("div");k(y,"art-setting-item-right-icon"),g(y,a.arrowRight),g(u,y)}break}switch(i){case"switch":{if(t.onSwitch){const y=s(l,"click",async b=>{t.switch=await t.onSwitch.call(this.art,t,l,b)});t.$events.push(y)}break}case"range":{if(t.$range){if(t.onRange){const y=s(t.$range,"change",async b=>{t.range[0]=t.$range.valueAsNumber,t.tooltip=await t.onRange.call(this.art,t,l,b)});t.$events.push(y)}if(t.onChange){const y=s(t.$range,"input",async b=>{t.range[0]=t.$range.valueAsNumber,t.tooltip=await t.onChange.call(this.art,t,l,b)});t.$events.push(y)}}break}case"selector":{const y=s(l,"click",async b=>{t.selector?.length?this.render(t.selector):(this.check(t),t.$parent.onSelect&&(t.$parent.tooltip=await t.$parent.onSelect.call(this.art,t,l,b)))});t.$events.push(y),t.default&&k(l,"art-current")}break;case"button":if(t.onClick){const y=s(l,"click",async b=>{t.tooltip=await t.onClick.call(this.art,t,l,b)});t.$events.push(y)}break}v(t,"$item",{configurable:!0,get:()=>l}),n?Nt(l,r):g(o,l),t.mounted&&setTimeout(()=>t.mounted.call(this.art,t.$item,t),0)}render(t=this.option){if(this.active=t,this.cache.has(t)){const n=this.cache.get(t);G(n,"art-current")}else{const n=P("div");this.cache.set(t,n),k(n,"art-setting-panel"),g(this.$parent,n),G(n,"art-current"),t[0]?.$parent&&this.createHeader(t[0]);for(let o=0;o<t.length;o++)this.createItem(t[o])}this.resize()}}class lr{constructor(){this.name="artplayer_settings",this.settings={}}get(t){try{const n=JSON.parse(window.localStorage.getItem(this.name))||{};return t?n[t]:n}catch{return t?this.settings[t]:this.settings}}set(t,n){try{const o=Object.assign({},this.get(),{[t]:n});window.localStorage.setItem(this.name,JSON.stringify(o))}catch{this.settings[t]=n}}del(t){try{const n=this.get();delete n[t],window.localStorage.setItem(this.name,JSON.stringify(n))}catch{delete this.settings[t]}}clear(){try{window.localStorage.removeItem(this.name)}catch{this.settings={}}}}const be=`.art-video-player {
  --art-theme: #f00;
  --art-font-color: #fff;
  --art-background-color: #000;
  --art-text-shadow-color: rgba(0, 0, 0, 0.5);
  --art-transition-duration: 0.2s;
  --art-padding: 10px;
  --art-border-radius: 3px;
  --art-progress-height: 6px;
  --art-progress-color: rgba(255, 255, 255, 0.25);
  --art-progress-top-gap: 10px;
  --art-hover-color: rgba(255, 255, 255, 0.25);
  --art-loaded-color: rgba(255, 255, 255, 0.25);
  --art-state-size: 80px;
  --art-state-opacity: 0.8;
  --art-bottom-height: 100px;
  --art-bottom-offset: 20px;
  --art-bottom-gap: 5px;
  --art-highlight-width: 8px;
  --art-highlight-color: rgba(255, 255, 255, 0.5);
  --art-control-height: 46px;
  --art-control-opacity: 0.75;
  --art-control-icon-size: 36px;
  --art-control-icon-scale: 1.1;
  --art-volume-height: 120px;
  --art-volume-handle-size: 14px;
  --art-lock-size: 36px;
  --art-indicator-scale: 0;
  --art-indicator-size: 16px;
  --art-fullscreen-web-index: 9999;
  --art-settings-icon-size: 24px;
  --art-settings-max-height: 300px;
  --art-selector-max-height: 300px;
  --art-contextmenus-min-width: 250px;
  --art-subtitle-font-size: 20px;
  --art-subtitle-gap: 5px;
  --art-subtitle-bottom: 15px;
  --art-subtitle-border: #000;
  --art-widget-background: rgba(0, 0, 0, 0.85);
  --art-tip-background: rgba(0, 0, 0, 0.7);
  --art-scrollbar-size: 4px;
  --art-scrollbar-background: rgba(255, 255, 255, 0.25);
  --art-scrollbar-background-hover: rgba(255, 255, 255, 0.5);
  --art-mini-progress-height: 2px;
}
.art-bg-cover {
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
}
.art-bottom-gradient {
  background-image: linear-gradient(to top, #000, rgba(0, 0, 0, 0.4), transparent);
  background-repeat: repeat-x;
  background-position: center bottom;
}
.art-backdrop-filter {
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
  background-color: rgba(0, 0, 0, 0.75) !important;
}
.art-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.art-video-player {
  position: relative;
  margin: 0 auto;
  width: 100%;
  height: 100%;
  outline: 0;
  zoom: 1;
  padding: 0;
  text-align: left;
  direction: ltr;
  font-size: 14px;
  line-height: 1.3;
  user-select: none;
  box-sizing: border-box;
  color: var(--art-font-color);
  background-color: var(--art-background-color);
  text-shadow: 0 0 2px var(--art-text-shadow-color);
  font-family: PingFang SC, Helvetica Neue, Microsoft YaHei, Roboto, Arial, sans-serif;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  -ms-touch-action: manipulation;
  touch-action: manipulation;
  -ms-high-contrast-adjust: none;
}
.art-video-player *,
.art-video-player *::before,
.art-video-player *::after {
  box-sizing: border-box;
}
.art-video-player ::-webkit-scrollbar {
  width: var(--art-scrollbar-size);
  height: var(--art-scrollbar-size);
}
.art-video-player ::-webkit-scrollbar-thumb {
  background-color: var(--art-scrollbar-background);
}
.art-video-player ::-webkit-scrollbar-thumb:hover {
  background-color: var(--art-scrollbar-background-hover);
}
.art-video-player img {
  max-width: 100%;
  vertical-align: top;
}
.art-video-player svg {
  fill: var(--art-font-color);
}
.art-video-player a {
  color: var(--art-font-color);
  text-decoration: none;
}
.art-icon {
  line-height: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.art-video-player.art-backdrop .art-contextmenus,
.art-video-player.art-backdrop .art-info,
.art-video-player.art-backdrop .art-settings,
.art-video-player.art-backdrop .art-layer-auto-playback,
.art-video-player.art-backdrop .art-selector-list,
.art-video-player.art-backdrop .art-volume-inner {
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
  background-color: rgba(0, 0, 0, 0.75) !important;
}
.art-video {
  position: absolute;
  inset: 0;
  z-index: 10;
  width: 100%;
  height: 100%;
}
.art-poster {
  position: absolute;
  inset: 0;
  z-index: 11;
  width: 100%;
  height: 100%;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  pointer-events: none;
}
.art-video-player .art-subtitle {
  display: none;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: absolute;
  z-index: 20;
  width: 100%;
  padding: 0 5%;
  text-align: center;
  pointer-events: none;
  gap: var(--art-subtitle-gap);
  bottom: var(--art-subtitle-bottom);
  font-size: var(--art-subtitle-font-size);
  transition: bottom var(--art-transition-duration) ease;
  text-shadow: var(--art-subtitle-border) 1px 0 1px, var(--art-subtitle-border) 0 1px 1px, var(--art-subtitle-border) -1px 0 1px, var(--art-subtitle-border) 0 -1px 1px, var(--art-subtitle-border) 1px 1px 1px, var(--art-subtitle-border) -1px -1px 1px, var(--art-subtitle-border) 1px -1px 1px, var(--art-subtitle-border) -1px 1px 1px;
}
.art-video-player.art-subtitle-show .art-subtitle {
  display: flex;
}
.art-video-player.art-control-show .art-subtitle {
  bottom: calc(var(--art-control-height) + var(--art-subtitle-bottom));
}
.art-danmuku {
  position: absolute;
  inset: 0;
  z-index: 30;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}
.art-video-player .art-layers {
  position: absolute;
  inset: 0;
  z-index: 40;
  width: 100%;
  height: 100%;
  display: none;
  pointer-events: none;
}
.art-video-player .art-layers .art-layer {
  pointer-events: auto;
}
.art-video-player.art-layer-show .art-layers {
  display: flex;
}
.art-video-player .art-mask {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  inset: 0;
  z-index: 50;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.art-video-player .art-mask .art-state {
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transform: scale(2);
  width: var(--art-state-size);
  height: var(--art-state-size);
  transition: all var(--art-transition-duration) ease;
}
.art-video-player.art-mask-show .art-state {
  pointer-events: auto;
  opacity: var(--art-state-opacity);
  transform: scale(1);
}
.art-video-player.art-loading-show .art-state {
  display: none;
}
.art-video-player .art-loading {
  display: none;
  justify-content: center;
  align-items: center;
  position: absolute;
  inset: 0;
  z-index: 70;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.art-video-player.art-loading-show .art-loading {
  display: flex;
}
.art-video-player.art-loading-show .art-mask {
  display: none;
}
.art-video-player .art-bottom {
  position: absolute;
  inset: 0;
  z-index: 60;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  padding: 0 var(--art-padding);
  transition: all var(--art-transition-duration) ease;
  background-size: 100% var(--art-bottom-height);
  background-image: linear-gradient(to top, #000, rgba(0, 0, 0, 0.4), transparent);
  background-repeat: repeat-x;
  background-position: center bottom;
}
.art-video-player .art-bottom .art-controls,
.art-video-player .art-bottom .art-progress {
  transform: translateY(var(--art-bottom-offset));
  transition: transform var(--art-transition-duration) ease;
}
.art-video-player.art-control-show .art-bottom,
.art-video-player.art-hover .art-bottom {
  opacity: 1;
}
.art-video-player.art-control-show .art-bottom .art-controls,
.art-video-player.art-hover .art-bottom .art-controls,
.art-video-player.art-control-show .art-bottom .art-progress,
.art-video-player.art-hover .art-bottom .art-progress {
  transform: translateY(0);
}
.art-bottom .art-progress {
  position: relative;
  z-index: 0;
  cursor: pointer;
  pointer-events: auto;
  padding-top: var(--art-progress-top-gap);
  padding-bottom: var(--art-bottom-gap);
}
.art-bottom .art-progress .art-control-progress {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: var(--art-progress-height);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner {
  display: flex;
  align-items: center;
  position: relative;
  height: 50%;
  width: 100%;
  transition: height var(--art-transition-duration) ease;
  background-color: var(--art-progress-color);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-hover {
  position: absolute;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  width: 0%;
  background-color: var(--art-hover-color);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-loaded {
  position: absolute;
  inset: 0;
  z-index: 10;
  width: 100%;
  height: 100%;
  width: 0%;
  background-color: var(--art-loaded-color);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-played {
  position: absolute;
  inset: 0;
  z-index: 20;
  width: 100%;
  height: 100%;
  width: 0%;
  background-color: var(--art-theme);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-highlight {
  position: absolute;
  inset: 0;
  z-index: 30;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-highlight span {
  position: absolute;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  right: auto;
  pointer-events: auto;
  width: var(--art-highlight-width) !important;
  transform: translateX(calc(var(--art-highlight-width) / -2));
  background-color: var(--art-highlight-color);
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  z-index: 40;
  left: 0;
  border-radius: 50%;
  width: var(--art-indicator-size);
  height: var(--art-indicator-size);
  transform: scale(var(--art-indicator-scale));
  margin-left: calc(var(--art-indicator-size) / -2);
  transition: transform var(--art-transition-duration) ease;
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-indicator .art-icon {
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-indicator:hover {
  transform: scale(1.2) !important;
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-indicator:active {
  transform: scale(1) !important;
}
.art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-tip {
  transform-origin: bottom center;
  transform: scale(0.5);
  opacity: 0;
  position: absolute;
  z-index: 50;
  top: -25px;
  left: 0;
  padding: 3px 5px;
  line-height: 1;
  font-size: 12px;
  border-radius: var(--art-border-radius);
  white-space: nowrap;
  background-color: var(--art-tip-background);
  transition: transform var(--art-transition-duration) ease, opacity var(--art-transition-duration) ease;
}
.art-bottom .art-progress .art-control-thumbnails {
  transform-origin: bottom center;
  transform: scale(0.5);
  opacity: 0;
  position: absolute;
  bottom: calc(var(--art-bottom-gap) + 10px);
  left: 0;
  border-radius: var(--art-border-radius);
  pointer-events: none;
  background-color: var(--art-widget-background);
  transition: transform var(--art-transition-duration) ease, opacity var(--art-transition-duration) ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2), 0 1px 2px -1px rgba(0, 0, 0, 0.2);
}
.art-bottom .art-progress:hover .art-control-progress .art-control-progress-inner {
  height: 100%;
}
.art-bottom:hover .art-progress .art-control-progress .art-control-progress-inner .art-progress-indicator {
  transform: scale(1);
}
.art-progress-hover .art-bottom .art-progress .art-control-progress .art-control-progress-inner .art-progress-tip,
.art-progress-hover .art-bottom .art-progress .art-control-thumbnails {
  transform: scale(1);
  opacity: 1;
}
.art-video-player .art-controls {
  position: relative;
  z-index: 10;
  pointer-events: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--art-control-height);
}
.art-video-player .art-controls .art-controls-left,
.art-video-player .art-controls .art-controls-right {
  display: flex;
  height: 100%;
}
.art-video-player .art-controls .art-controls-center {
  display: none;
  justify-content: center;
  align-items: center;
  flex: 1;
  height: 100%;
  padding: 0 10px;
}
.art-video-player .art-controls .art-controls-right {
  justify-content: flex-end;
}
.art-video-player .art-controls .art-control {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  cursor: pointer;
  white-space: nowrap;
  opacity: var(--art-control-opacity);
  min-height: var(--art-control-height);
  min-width: var(--art-control-height);
  transition: opacity var(--art-transition-duration) ease;
}
.art-video-player .art-controls .art-control .art-icon {
  height: var(--art-control-icon-size);
  width: var(--art-control-icon-size);
  transform: scale(var(--art-control-icon-scale));
  transition: transform var(--art-transition-duration) ease;
}
.art-video-player .art-controls .art-control .art-icon:active {
  transform: scale(calc(var(--art-control-icon-scale) * 0.8));
}
.art-video-player .art-controls .art-control:hover {
  opacity: 1;
}
.art-control-volume {
  position: relative;
}
.art-control-volume .art-volume-panel {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  left: 0;
  right: 0;
  padding: 0 5px;
  font-size: 12px;
  text-align: center;
  cursor: default;
  opacity: 0;
  transform: translateY(10px);
  pointer-events: none;
  bottom: var(--art-control-height);
  width: var(--art-control-height);
  height: var(--art-volume-height);
  transition: all var(--art-transition-duration) ease;
}
.art-control-volume .art-volume-panel .art-volume-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  height: 100%;
  width: 100%;
  padding: 10px 0 12px;
  border-radius: var(--art-border-radius);
  background-color: var(--art-widget-background);
}
.art-control-volume .art-volume-panel .art-volume-inner .art-volume-slider {
  flex: 1;
  width: 100%;
  display: flex;
  cursor: pointer;
  position: relative;
  justify-content: center;
}
.art-control-volume .art-volume-panel .art-volume-inner .art-volume-slider .art-volume-handle {
  position: relative;
  display: flex;
  justify-content: center;
  width: 2px;
  border-radius: var(--art-border-radius);
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.25);
}
.art-control-volume .art-volume-panel .art-volume-inner .art-volume-slider .art-volume-handle .art-volume-loaded {
  position: absolute;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  background-color: var(--art-theme);
}
.art-control-volume .art-volume-panel .art-volume-inner .art-volume-slider .art-volume-indicator {
  position: absolute;
  width: var(--art-volume-handle-size);
  height: var(--art-volume-handle-size);
  margin-top: calc(var(--art-volume-handle-size) / -2);
  flex-shrink: 0;
  transform: scale(1);
  border-radius: 100%;
  background-color: var(--art-theme);
  transition: transform var(--art-transition-duration) ease;
}
.art-control-volume .art-volume-panel .art-volume-inner .art-volume-slider:active .art-volume-indicator {
  transform: scale(0.9);
}
.art-control-volume:hover .art-volume-panel {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
.art-video-player .art-notice {
  display: none;
  position: absolute;
  inset: 0;
  z-index: 80;
  width: 100%;
  height: 100%;
  height: auto;
  bottom: auto;
  padding: var(--art-padding);
  pointer-events: none;
}
.art-video-player .art-notice .art-notice-inner {
  display: inline-flex;
  padding: 5px;
  line-height: 1;
  border-radius: var(--art-border-radius);
  background-color: var(--art-tip-background);
}
.art-video-player.art-notice-show .art-notice {
  display: flex;
}
.art-video-player .art-contextmenus {
  display: none;
  flex-direction: column;
  position: absolute;
  z-index: 120;
  padding: 5px 0;
  border-radius: var(--art-border-radius);
  font-size: 12px;
  background-color: var(--art-widget-background);
  min-width: var(--art-contextmenus-min-width);
}
.art-video-player .art-contextmenus .art-contextmenu {
  cursor: pointer;
  display: flex;
  padding: 10px 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.art-video-player .art-contextmenus .art-contextmenu span {
  padding: 0 8px;
}
.art-video-player .art-contextmenus .art-contextmenu span:hover,
.art-video-player .art-contextmenus .art-contextmenu span.art-current {
  color: var(--art-theme);
}
.art-video-player .art-contextmenus .art-contextmenu:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.art-video-player .art-contextmenus .art-contextmenu:last-child {
  border-bottom: none;
}
.art-video-player.art-contextmenu-show .art-contextmenus {
  display: flex;
}
.art-video-player .art-settings {
  display: none;
  flex-direction: column;
  position: absolute;
  z-index: 90;
  left: auto;
  overflow-y: auto;
  overflow-x: hidden;
  border-radius: var(--art-border-radius);
  max-height: var(--art-settings-max-height);
  right: var(--art-padding);
  bottom: var(--art-control-height);
  transition: all var(--art-transition-duration) ease;
  background-color: var(--art-widget-background);
}
.art-video-player .art-settings .art-setting-panel {
  display: none;
  flex-direction: column;
}
.art-video-player .art-settings .art-setting-panel.art-current {
  display: flex;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5px;
  cursor: pointer;
  overflow: hidden;
  transition: background-color var(--art-transition-duration) ease;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.art-video-player .art-settings .art-setting-panel .art-setting-item.art-current {
  color: var(--art-theme);
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-icon-check {
  visibility: hidden;
  height: 15px;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item.art-current .art-icon-check {
  visibility: visible;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-left {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  gap: 5px;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-left .art-setting-item-left-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  height: var(--art-settings-icon-size);
  width: var(--art-settings-icon-size);
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-right {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-right .art-setting-item-right-tooltip {
  white-space: nowrap;
  color: rgba(255, 255, 255, 0.5);
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-right .art-setting-item-right-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 32px;
  height: 24px;
}
.art-video-player .art-settings .art-setting-panel .art-setting-item .art-setting-item-right .art-setting-range {
  height: 3px;
  width: 80px;
  outline: none;
  appearance: none;
  background-color: rgba(255, 255, 255, 0.2);
}
.art-video-player .art-settings .art-setting-panel .art-setting-item-back {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.art-video-player.art-setting-show .art-settings {
  display: flex;
}
.art-video-player .art-info {
  display: none;
  position: absolute;
  left: var(--art-padding);
  top: var(--art-padding);
  z-index: 100;
  padding: 10px;
  font-size: 12px;
  border-radius: var(--art-border-radius);
  background-color: var(--art-widget-background);
}
.art-video-player .art-info .art-info-panel {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.art-video-player .art-info .art-info-panel .art-info-item {
  display: flex;
  align-items: center;
  gap: 5px;
}
.art-video-player .art-info .art-info-panel .art-info-item .art-info-title {
  width: 100px;
  text-align: right;
}
.art-video-player .art-info .art-info-panel .art-info-item .art-info-content {
  width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  user-select: all;
}
.art-video-player .art-info .art-info-close {
  position: absolute;
  top: 5px;
  right: 5px;
  cursor: pointer;
}
.art-video-player.art-info-show .art-info {
  display: flex;
}
.art-hide-cursor * {
  cursor: none !important;
}
.art-video-player[data-aspect-ratio] {
  overflow: hidden;
}
.art-video-player[data-aspect-ratio] .art-video {
  object-fit: fill;
  box-sizing: content-box;
}
.art-fullscreen {
  --art-progress-height: 8px;
  --art-indicator-size: 20px;
  --art-control-height: 60px;
  --art-control-icon-scale: 1.3;
}
.art-fullscreen-web {
  --art-progress-height: 8px;
  --art-indicator-size: 20px;
  --art-control-height: 60px;
  --art-control-icon-scale: 1.3;
  position: fixed;
  inset: 0;
  z-index: var(--art-fullscreen-web-index);
  width: 100%;
  height: 100%;
}
.art-mini-popup {
  position: fixed;
  z-index: 9999;
  width: 320px;
  height: 180px;
  background: #000;
  border-radius: var(--art-border-radius);
  cursor: move;
  user-select: none;
  overflow: hidden;
  transition: opacity 0.2s ease;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}
.art-mini-popup svg {
  fill: #fff;
}
.art-mini-popup .art-video {
  pointer-events: none;
}
.art-mini-popup .art-mini-close {
  position: absolute;
  z-index: 20;
  right: 10px;
  top: 10px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.art-mini-popup .art-mini-state {
  position: absolute;
  inset: 0;
  z-index: 30;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease;
  background-color: rgba(0, 0, 0, 0.25);
}
.art-mini-popup .art-mini-state .art-icon {
  opacity: 0.75;
  cursor: pointer;
  transform: scale(3);
  pointer-events: auto;
  transition: transform 0.2s ease;
}
.art-mini-popup .art-mini-state .art-icon:active {
  transform: scale(2.5);
}
.art-mini-popup.art-mini-dragging {
  opacity: 0.9;
}
.art-mini-popup:hover .art-mini-close,
.art-mini-popup:hover .art-mini-state {
  opacity: 1;
}
.art-video-player[data-flip='horizontal'] .art-video {
  transform: scaleX(-1);
}
.art-video-player[data-flip='vertical'] .art-video {
  transform: scaleY(-1);
}
.art-video-player .art-layer-lock {
  display: none;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 50%;
  border-radius: 50%;
  transform: translateY(-50%);
  height: var(--art-lock-size);
  width: var(--art-lock-size);
  left: var(--art-padding);
  background-color: var(--art-tip-background);
}
.art-video-player .art-layer-auto-playback {
  display: none;
  gap: 10px;
  align-items: center;
  position: absolute;
  border-radius: var(--art-border-radius);
  padding: 10px;
  line-height: 1;
  left: var(--art-padding);
  bottom: calc(var(--art-control-height) + var(--art-bottom-gap) + 10px);
  background-color: var(--art-widget-background);
}
.art-video-player .art-layer-auto-playback .art-auto-playback-close {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.art-video-player .art-layer-auto-playback .art-auto-playback-close svg {
  width: 15px;
  height: 15px;
  fill: var(--art-theme);
}
.art-video-player .art-layer-auto-playback .art-auto-playback-jump {
  color: var(--art-theme);
  cursor: pointer;
}
.art-video-player.art-lock .art-subtitle {
  bottom: var(--art-subtitle-bottom) !important;
}
.art-video-player.art-mini-progress-bar .art-bottom,
.art-video-player.art-lock .art-bottom {
  opacity: 1;
  padding: 0;
  background-image: none;
}
.art-video-player.art-mini-progress-bar .art-bottom .art-controls,
.art-video-player.art-lock .art-bottom .art-controls,
.art-video-player.art-mini-progress-bar .art-bottom .art-progress,
.art-video-player.art-lock .art-bottom .art-progress {
  transform: translateY(calc(var(--art-control-height) + var(--art-bottom-gap) + var(--art-progress-height) / 4));
}
.art-video-player.art-mini-progress-bar .art-bottom .art-progress-indicator,
.art-video-player.art-lock .art-bottom .art-progress-indicator {
  display: none !important;
}
.art-video-player.art-control-show .art-layer-lock {
  display: flex;
}
.art-control-selector {
  position: relative;
  display: flex;
  justify-content: center;
}
.art-control-selector .art-selector-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: absolute;
  border-radius: var(--art-border-radius);
  overflow-y: auto;
  overflow-x: hidden;
  opacity: 0;
  transform: translateY(10px);
  pointer-events: none;
  bottom: var(--art-control-height);
  max-height: var(--art-selector-max-height);
  background-color: var(--art-widget-background);
  transition: all var(--art-transition-duration) ease;
}
.art-control-selector .art-selector-list .art-selector-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 10px 15px;
  flex-shrink: 0;
  line-height: 1;
}
.art-control-selector .art-selector-list .art-selector-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.art-control-selector .art-selector-list .art-selector-item:hover,
.art-control-selector .art-selector-list .art-selector-item.art-current {
  color: var(--art-theme);
}
.art-control-selector:hover .art-selector-list {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
.art-video-player {
  /*! Hint.css - v2.7.0 - 2021-10-01
    * https://kushagra.dev/lab/hint/
    * Copyright (c) 2021 Kushagra Gour */
  /*-------------------------------------*\\
        HINT.css - A CSS tooltip library
    \\*-------------------------------------*/
  /**
    * HINT.css is a tooltip library made in pure CSS.
    *
    * Source: https://github.com/chinchang/hint.css
    * Demo: http://kushagragour.in/lab/hint/
    *
    */
  /**
    * source: hint-core.scss
    *
    * Defines the basic styling for the tooltip.
    * Each tooltip is made of 2 parts:
    * 	1) body (:after)
    * 	2) arrow (:before)
    *
    * Classes added:
    * 	1) hint
    */
  /**
    * source: hint-position.scss
    *
    * Defines the positoning logic for the tooltips.
    *
    * Classes added:
    * 	1) hint--top
    * 	2) hint--bottom
    * 	3) hint--left
    * 	4) hint--right
    */
  /**
    * set default color for tooltip arrows
    */
  /**
    * top tooltip
    */
  /**
    * bottom tooltip
    */
  /**
    * right tooltip
    */
  /**
    * left tooltip
    */
  /**
    * top-left tooltip
    */
  /**
    * top-right tooltip
    */
  /**
    * bottom-left tooltip
    */
  /**
    * bottom-right tooltip
    */
  /**
    * source: hint-sizes.scss
    *
    * Defines width restricted tooltips that can span
    * across multiple lines.
    *
    * Classes added:
    * 	1) hint--small
    * 	2) hint--medium
    * 	3) hint--large
    *
    */
  /**
    * source: hint-theme.scss
    *
    * Defines basic theme for tooltips.
    *
    */
  /**
    * source: hint-color-types.scss
    *
    * Contains tooltips of various types based on color differences.
    *
    * Classes added:
    * 	1) hint--error
    * 	2) hint--warning
    * 	3) hint--info
    * 	4) hint--success
    *
    */
  /**
    * Error
    */
  /**
    * Warning
    */
  /**
    * Info
    */
  /**
    * Success
    */
  /**
    * source: hint-always.scss
    *
    * Defines a persisted tooltip which shows always.
    *
    * Classes added:
    * 	1) hint--always
    *
    */
  /**
    * source: hint-rounded.scss
    *
    * Defines rounded corner tooltips.
    *
    * Classes added:
    * 	1) hint--rounded
    *
    */
  /**
    * source: hint-effects.scss
    *
    * Defines various transition effects for the tooltips.
    *
    * Classes added:
    * 	1) hint--no-animate
    * 	2) hint--bounce
    *
    */
}
.art-video-player [class*='hint--'] {
  position: relative;
  display: inline-block;
  font-style: normal;
  /**
        * tooltip arrow
        */
  /**
        * tooltip body
        */
}
.art-video-player [class*='hint--']:before,
.art-video-player [class*='hint--']:after {
  position: absolute;
  -webkit-transform: translate3d(0, 0, 0);
  -moz-transform: translate3d(0, 0, 0);
  transform: translate3d(0, 0, 0);
  visibility: hidden;
  opacity: 0;
  z-index: 1000000;
  pointer-events: none;
  -webkit-transition: 0.3s ease;
  -moz-transition: 0.3s ease;
  transition: 0.3s ease;
  -webkit-transition-delay: 0ms;
  -moz-transition-delay: 0ms;
  transition-delay: 0ms;
}
.art-video-player [class*='hint--']:hover:before,
.art-video-player [class*='hint--']:hover:after {
  visibility: visible;
  opacity: 1;
}
.art-video-player [class*='hint--']:hover:before,
.art-video-player [class*='hint--']:hover:after {
  -webkit-transition-delay: 100ms;
  -moz-transition-delay: 100ms;
  transition-delay: 100ms;
}
.art-video-player [class*='hint--']:before {
  content: '';
  position: absolute;
  background: transparent;
  border: 6px solid transparent;
  z-index: 1000001;
}
.art-video-player [class*='hint--']:after {
  background: #000000;
  color: white;
  padding: 8px 10px;
  font-size: 12px;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  line-height: 12px;
  white-space: nowrap;
}
.art-video-player [class*='hint--'][aria-label]:after {
  content: attr(aria-label);
}
.art-video-player [class*='hint--'][data-hint]:after {
  content: attr(data-hint);
}
.art-video-player [aria-label='']:before,
.art-video-player [aria-label='']:after,
.art-video-player [data-hint='']:before,
.art-video-player [data-hint='']:after {
  display: none !important;
}
.art-video-player .hint--top-left:before {
  border-top-color: #000000;
}
.art-video-player .hint--top-right:before {
  border-top-color: #000000;
}
.art-video-player .hint--top:before {
  border-top-color: #000000;
}
.art-video-player .hint--bottom-left:before {
  border-bottom-color: #000000;
}
.art-video-player .hint--bottom-right:before {
  border-bottom-color: #000000;
}
.art-video-player .hint--bottom:before {
  border-bottom-color: #000000;
}
.art-video-player .hint--left:before {
  border-left-color: #000000;
}
.art-video-player .hint--right:before {
  border-right-color: #000000;
}
.art-video-player .hint--top:before {
  margin-bottom: -11px;
}
.art-video-player .hint--top:before,
.art-video-player .hint--top:after {
  bottom: 100%;
  left: 50%;
}
.art-video-player .hint--top:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--top:after {
  -webkit-transform: translateX(-50%);
  -moz-transform: translateX(-50%);
  transform: translateX(-50%);
}
.art-video-player .hint--top:hover:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--top:hover:after {
  -webkit-transform: translateX(-50%) translateY(-8px);
  -moz-transform: translateX(-50%) translateY(-8px);
  transform: translateX(-50%) translateY(-8px);
}
.art-video-player .hint--bottom:before {
  margin-top: -11px;
}
.art-video-player .hint--bottom:before,
.art-video-player .hint--bottom:after {
  top: 100%;
  left: 50%;
}
.art-video-player .hint--bottom:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--bottom:after {
  -webkit-transform: translateX(-50%);
  -moz-transform: translateX(-50%);
  transform: translateX(-50%);
}
.art-video-player .hint--bottom:hover:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--bottom:hover:after {
  -webkit-transform: translateX(-50%) translateY(8px);
  -moz-transform: translateX(-50%) translateY(8px);
  transform: translateX(-50%) translateY(8px);
}
.art-video-player .hint--right:before {
  margin-left: -11px;
  margin-bottom: -6px;
}
.art-video-player .hint--right:after {
  margin-bottom: -14px;
}
.art-video-player .hint--right:before,
.art-video-player .hint--right:after {
  left: 100%;
  bottom: 50%;
}
.art-video-player .hint--right:hover:before {
  -webkit-transform: translateX(8px);
  -moz-transform: translateX(8px);
  transform: translateX(8px);
}
.art-video-player .hint--right:hover:after {
  -webkit-transform: translateX(8px);
  -moz-transform: translateX(8px);
  transform: translateX(8px);
}
.art-video-player .hint--left:before {
  margin-right: -11px;
  margin-bottom: -6px;
}
.art-video-player .hint--left:after {
  margin-bottom: -14px;
}
.art-video-player .hint--left:before,
.art-video-player .hint--left:after {
  right: 100%;
  bottom: 50%;
}
.art-video-player .hint--left:hover:before {
  -webkit-transform: translateX(-8px);
  -moz-transform: translateX(-8px);
  transform: translateX(-8px);
}
.art-video-player .hint--left:hover:after {
  -webkit-transform: translateX(-8px);
  -moz-transform: translateX(-8px);
  transform: translateX(-8px);
}
.art-video-player .hint--top-left:before {
  margin-bottom: -11px;
}
.art-video-player .hint--top-left:before,
.art-video-player .hint--top-left:after {
  bottom: 100%;
  left: 50%;
}
.art-video-player .hint--top-left:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--top-left:after {
  -webkit-transform: translateX(-100%);
  -moz-transform: translateX(-100%);
  transform: translateX(-100%);
}
.art-video-player .hint--top-left:after {
  margin-left: 12px;
}
.art-video-player .hint--top-left:hover:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--top-left:hover:after {
  -webkit-transform: translateX(-100%) translateY(-8px);
  -moz-transform: translateX(-100%) translateY(-8px);
  transform: translateX(-100%) translateY(-8px);
}
.art-video-player .hint--top-right:before {
  margin-bottom: -11px;
}
.art-video-player .hint--top-right:before,
.art-video-player .hint--top-right:after {
  bottom: 100%;
  left: 50%;
}
.art-video-player .hint--top-right:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--top-right:after {
  -webkit-transform: translateX(0);
  -moz-transform: translateX(0);
  transform: translateX(0);
}
.art-video-player .hint--top-right:after {
  margin-left: -12px;
}
.art-video-player .hint--top-right:hover:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--top-right:hover:after {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--bottom-left:before {
  margin-top: -11px;
}
.art-video-player .hint--bottom-left:before,
.art-video-player .hint--bottom-left:after {
  top: 100%;
  left: 50%;
}
.art-video-player .hint--bottom-left:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--bottom-left:after {
  -webkit-transform: translateX(-100%);
  -moz-transform: translateX(-100%);
  transform: translateX(-100%);
}
.art-video-player .hint--bottom-left:after {
  margin-left: 12px;
}
.art-video-player .hint--bottom-left:hover:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--bottom-left:hover:after {
  -webkit-transform: translateX(-100%) translateY(8px);
  -moz-transform: translateX(-100%) translateY(8px);
  transform: translateX(-100%) translateY(8px);
}
.art-video-player .hint--bottom-right:before {
  margin-top: -11px;
}
.art-video-player .hint--bottom-right:before,
.art-video-player .hint--bottom-right:after {
  top: 100%;
  left: 50%;
}
.art-video-player .hint--bottom-right:before {
  left: calc(50% - 6px);
}
.art-video-player .hint--bottom-right:after {
  -webkit-transform: translateX(0);
  -moz-transform: translateX(0);
  transform: translateX(0);
}
.art-video-player .hint--bottom-right:after {
  margin-left: -12px;
}
.art-video-player .hint--bottom-right:hover:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--bottom-right:hover:after {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--small:after,
.art-video-player .hint--medium:after,
.art-video-player .hint--large:after {
  white-space: normal;
  line-height: 1.4em;
  word-wrap: break-word;
}
.art-video-player .hint--small:after {
  width: 80px;
}
.art-video-player .hint--medium:after {
  width: 150px;
}
.art-video-player .hint--large:after {
  width: 300px;
}
.art-video-player [class*='hint--'] {
  /**
        * tooltip body
        */
}
.art-video-player [class*='hint--']:after {
  text-shadow: 0 -1px 0px black;
  box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3);
}
.art-video-player .hint--error:after {
  background-color: #b34e4d;
  text-shadow: 0 -1px 0px #592726;
}
.art-video-player .hint--error.hint--top-left:before {
  border-top-color: #b34e4d;
}
.art-video-player .hint--error.hint--top-right:before {
  border-top-color: #b34e4d;
}
.art-video-player .hint--error.hint--top:before {
  border-top-color: #b34e4d;
}
.art-video-player .hint--error.hint--bottom-left:before {
  border-bottom-color: #b34e4d;
}
.art-video-player .hint--error.hint--bottom-right:before {
  border-bottom-color: #b34e4d;
}
.art-video-player .hint--error.hint--bottom:before {
  border-bottom-color: #b34e4d;
}
.art-video-player .hint--error.hint--left:before {
  border-left-color: #b34e4d;
}
.art-video-player .hint--error.hint--right:before {
  border-right-color: #b34e4d;
}
.art-video-player .hint--warning:after {
  background-color: #c09854;
  text-shadow: 0 -1px 0px #6c5328;
}
.art-video-player .hint--warning.hint--top-left:before {
  border-top-color: #c09854;
}
.art-video-player .hint--warning.hint--top-right:before {
  border-top-color: #c09854;
}
.art-video-player .hint--warning.hint--top:before {
  border-top-color: #c09854;
}
.art-video-player .hint--warning.hint--bottom-left:before {
  border-bottom-color: #c09854;
}
.art-video-player .hint--warning.hint--bottom-right:before {
  border-bottom-color: #c09854;
}
.art-video-player .hint--warning.hint--bottom:before {
  border-bottom-color: #c09854;
}
.art-video-player .hint--warning.hint--left:before {
  border-left-color: #c09854;
}
.art-video-player .hint--warning.hint--right:before {
  border-right-color: #c09854;
}
.art-video-player .hint--info:after {
  background-color: #3986ac;
  text-shadow: 0 -1px 0px #1a3c4d;
}
.art-video-player .hint--info.hint--top-left:before {
  border-top-color: #3986ac;
}
.art-video-player .hint--info.hint--top-right:before {
  border-top-color: #3986ac;
}
.art-video-player .hint--info.hint--top:before {
  border-top-color: #3986ac;
}
.art-video-player .hint--info.hint--bottom-left:before {
  border-bottom-color: #3986ac;
}
.art-video-player .hint--info.hint--bottom-right:before {
  border-bottom-color: #3986ac;
}
.art-video-player .hint--info.hint--bottom:before {
  border-bottom-color: #3986ac;
}
.art-video-player .hint--info.hint--left:before {
  border-left-color: #3986ac;
}
.art-video-player .hint--info.hint--right:before {
  border-right-color: #3986ac;
}
.art-video-player .hint--success:after {
  background-color: #458746;
  text-shadow: 0 -1px 0px #1a321a;
}
.art-video-player .hint--success.hint--top-left:before {
  border-top-color: #458746;
}
.art-video-player .hint--success.hint--top-right:before {
  border-top-color: #458746;
}
.art-video-player .hint--success.hint--top:before {
  border-top-color: #458746;
}
.art-video-player .hint--success.hint--bottom-left:before {
  border-bottom-color: #458746;
}
.art-video-player .hint--success.hint--bottom-right:before {
  border-bottom-color: #458746;
}
.art-video-player .hint--success.hint--bottom:before {
  border-bottom-color: #458746;
}
.art-video-player .hint--success.hint--left:before {
  border-left-color: #458746;
}
.art-video-player .hint--success.hint--right:before {
  border-right-color: #458746;
}
.art-video-player .hint--always:after,
.art-video-player .hint--always:before {
  opacity: 1;
  visibility: visible;
}
.art-video-player .hint--always.hint--top:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--always.hint--top:after {
  -webkit-transform: translateX(-50%) translateY(-8px);
  -moz-transform: translateX(-50%) translateY(-8px);
  transform: translateX(-50%) translateY(-8px);
}
.art-video-player .hint--always.hint--top-left:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--always.hint--top-left:after {
  -webkit-transform: translateX(-100%) translateY(-8px);
  -moz-transform: translateX(-100%) translateY(-8px);
  transform: translateX(-100%) translateY(-8px);
}
.art-video-player .hint--always.hint--top-right:before {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--always.hint--top-right:after {
  -webkit-transform: translateY(-8px);
  -moz-transform: translateY(-8px);
  transform: translateY(-8px);
}
.art-video-player .hint--always.hint--bottom:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--always.hint--bottom:after {
  -webkit-transform: translateX(-50%) translateY(8px);
  -moz-transform: translateX(-50%) translateY(8px);
  transform: translateX(-50%) translateY(8px);
}
.art-video-player .hint--always.hint--bottom-left:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--always.hint--bottom-left:after {
  -webkit-transform: translateX(-100%) translateY(8px);
  -moz-transform: translateX(-100%) translateY(8px);
  transform: translateX(-100%) translateY(8px);
}
.art-video-player .hint--always.hint--bottom-right:before {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--always.hint--bottom-right:after {
  -webkit-transform: translateY(8px);
  -moz-transform: translateY(8px);
  transform: translateY(8px);
}
.art-video-player .hint--always.hint--left:before {
  -webkit-transform: translateX(-8px);
  -moz-transform: translateX(-8px);
  transform: translateX(-8px);
}
.art-video-player .hint--always.hint--left:after {
  -webkit-transform: translateX(-8px);
  -moz-transform: translateX(-8px);
  transform: translateX(-8px);
}
.art-video-player .hint--always.hint--right:before {
  -webkit-transform: translateX(8px);
  -moz-transform: translateX(8px);
  transform: translateX(8px);
}
.art-video-player .hint--always.hint--right:after {
  -webkit-transform: translateX(8px);
  -moz-transform: translateX(8px);
  transform: translateX(8px);
}
.art-video-player .hint--rounded:after {
  border-radius: 4px;
}
.art-video-player .hint--no-animate:before,
.art-video-player .hint--no-animate:after {
  -webkit-transition-duration: 0ms;
  -moz-transition-duration: 0ms;
  transition-duration: 0ms;
}
.art-video-player .hint--bounce:before,
.art-video-player .hint--bounce:after {
  -webkit-transition: opacity 0.3s ease, visibility 0.3s ease, -webkit-transform 0.3s cubic-bezier(0.71, 1.7, 0.77, 1.24);
  -moz-transition: opacity 0.3s ease, visibility 0.3s ease, -moz-transform 0.3s cubic-bezier(0.71, 1.7, 0.77, 1.24);
  transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s cubic-bezier(0.71, 1.7, 0.77, 1.24);
}
.art-video-player .hint--no-shadow:before,
.art-video-player .hint--no-shadow:after {
  text-shadow: initial;
  box-shadow: initial;
}
.art-video-player .hint--no-arrow:before {
  display: none;
}
.art-video-player.art-mobile {
  --art-bottom-gap: 10px;
  --art-control-height: 38px;
  --art-control-icon-scale: 1;
  --art-state-size: 60px;
  --art-settings-max-height: 180px;
  --art-selector-max-height: 180px;
  --art-indicator-scale: 1;
  --art-control-opacity: 1;
}
.art-video-player.art-mobile .art-controls-left {
  margin-left: calc(var(--art-padding) / -1);
}
.art-video-player.art-mobile .art-controls-right {
  margin-right: calc(var(--art-padding) / -1);
}
`;class cr extends it{constructor(t){super(t),this.name="subtitle",this.option=null,this.destroyEvent=()=>null,this.init(t.option.subtitle);let n=!1;t.on("video:timeupdate",()=>{if(!this.url)return;const o=this.art.template.$video.webkitDisplayingFullscreen;typeof o=="boolean"&&o!==n&&(n=o,this.createTrack(o?"subtitles":"metadata",this.url))})}get url(){return this.art.template.$track.src}set url(t){this.switch(t)}get textTrack(){return this.art.template.$video?.textTracks?.[0]}get activeCues(){return this.textTrack?Array.from(this.textTrack.activeCues):[]}get cues(){return this.textTrack?Array.from(this.textTrack.cues):[]}style(t,n){const{$subtitle:o}=this.art.template;return typeof t=="object"?Mt(o,t):p(o,t,n)}update(){const{option:{subtitle:t},template:{$subtitle:n}}=this.art;n.innerHTML="",this.activeCues.length&&(this.art.emit("subtitleBeforeUpdate",this.activeCues),n.innerHTML=this.activeCues.map((o,r)=>o.text.split(/\r?\n/).filter(i=>i.trim()).map(i=>`<div class="art-subtitle-line" data-group="${r}">
                                ${t.escape?de(i):i}
                            </div>`).join("")).join(""),this.art.emit("subtitleAfterUpdate",this.activeCues))}async switch(t,n={}){const{i18n:o,notice:r,option:i}=this.art,a={...i.subtitle,...n,url:t},s=await this.init(a);return n.name&&(r.show=`${o.get("Switch Subtitle")}: ${n.name}`),s}createTrack(t,n){const{template:o,proxy:r,option:i}=this.art,{$video:a,$track:s}=o,c=P("track");c.default=!0,c.kind=t,c.src=n,c.label=i.subtitle.name||"Artplayer",c.track.mode="hidden",c.onload=()=>{this.art.emit("subtitleLoad",this.cues,this.option)},this.art.events.remove(this.destroyEvent),s.onload=null,zt(s),g(a,c),o.$track=c,this.destroyEvent=r(this.textTrack,"cuechange",()=>this.update())}async init(t){const{notice:n,template:{$subtitle:o}}=this.art;if(!this.textTrack)return null;if(mt(t,Vt.subtitle),!!t.url)return this.option=t,this.style(t.style),fetch(t.url).then(r=>r.arrayBuffer()).then(r=>{const a=new TextDecoder(t.encoding).decode(r);switch(t.type||yt(t.url)){case"srt":{const s=ue(a),c=t.onVttLoad(s);return Ct(c)}case"ass":{const s=he(a),c=t.onVttLoad(s);return Ct(c)}case"vtt":{const s=t.onVttLoad(a);return Ct(s)}default:return t.url}}).then(r=>(o.innerHTML="",this.url===r||(URL.revokeObjectURL(this.url),this.createTrack("metadata",r)),r)).catch(r=>{throw o.innerHTML="",n.show=r,r})}}class Et{constructor(t){this.art=t;const{option:n,constructor:o}=t;n.container instanceof Element?this.$container=n.container:(this.$container=H(n.container),U(this.$container,`No container element found by ${n.container}`)),U(ae(),"The current browser does not support flex layout");const r=this.$container.tagName.toLowerCase();U(r==="div",`Unsupported container element type, only support 'div' but got '${r}'`),U(o.instances.every(i=>i.template.$container!==this.$container),"Cannot mount multiple instances on the same dom element"),this.query=this.query.bind(this),this.$container.dataset.artId=t.id,this.init()}static get html(){return`
          <div class="art-video-player art-subtitle-show art-layer-show art-control-show art-mask-show">
            <video class="art-video">
              <track default kind="metadata" src=""></track>
            </video>
            <div class="art-poster"></div>
            <div class="art-subtitle"></div>
            <div class="art-danmuku"></div>
            <div class="art-layers"></div>
            <div class="art-mask">
              <div class="art-state"></div>
            </div>
            <div class="art-bottom">
              <div class="art-progress"></div>
              <div class="art-controls">
                <div class="art-controls-left"></div>
                <div class="art-controls-center"></div>
                <div class="art-controls-right"></div>
              </div>
            </div>
            <div class="art-loading"></div>
            <div class="art-notice">
              <div class="art-notice-inner"></div>
            </div>
            <div class="art-settings"></div>
            <div class="art-info">
              <div class="art-info-panel">
                <div class="art-info-item">
                  <div class="art-info-title">Player version:</div>
                  <div class="art-info-content">${Ot}</div>
                </div>
                <div class="art-info-item">
                  <div class="art-info-title">Video url:</div>
                  <div class="art-info-content" data-video="currentSrc"></div>
                </div>
                <div class="art-info-item">
                  <div class="art-info-title">Video volume:</div>
                  <div class="art-info-content" data-video="volume"></div>
                </div>
                <div class="art-info-item">
                  <div class="art-info-title">Video time:</div>
                  <div class="art-info-content" data-video="currentTime"></div>
                </div>
                <div class="art-info-item">
                  <div class="art-info-title">Video duration:</div>
                  <div class="art-info-content" data-video="duration"></div>
                </div>
                <div class="art-info-item">
                  <div class="art-info-title">Video resolution:</div>
                  <div class="art-info-content">
                    <span data-video="videoWidth"></span> x <span data-video="videoHeight"></span>
                  </div>
                </div>
              </div>
              <div class="art-info-close">[x]</div>
            </div>
            <div class="art-contextmenus"></div>
          </div>
        `}query(t){return H(t,this.$container)}init(){const{option:t}=this.art;if(t.useSSR||(this.$container.innerHTML=Et.html),this.$player=this.query(".art-video-player"),this.$video=this.query(".art-video"),this.$track=this.query("track"),this.$poster=this.query(".art-poster"),this.$subtitle=this.query(".art-subtitle"),this.$danmuku=this.query(".art-danmuku"),this.$bottom=this.query(".art-bottom"),this.$progress=this.query(".art-progress"),this.$controls=this.query(".art-controls"),this.$controlsLeft=this.query(".art-controls-left"),this.$controlsCenter=this.query(".art-controls-center"),this.$controlsRight=this.query(".art-controls-right"),this.$layer=this.query(".art-layers"),this.$loading=this.query(".art-loading"),this.$notice=this.query(".art-notice"),this.$noticeInner=this.query(".art-notice-inner"),this.$mask=this.query(".art-mask"),this.$state=this.query(".art-state"),this.$setting=this.query(".art-settings"),this.$info=this.query(".art-info"),this.$infoPanel=this.query(".art-info-panel"),this.$infoClose=this.query(".art-info-close"),this.$contextmenu=this.query(".art-contextmenus"),t.proxy){const n=t.proxy.call(this.art,this.art);U(n instanceof HTMLVideoElement||n instanceof HTMLCanvasElement,"Function 'option.proxy' needs to return 'HTMLVideoElement' or 'HTMLCanvasElement'"),Nt(n,this.$video),n.className="art-video",this.$video=n}t.backdrop&&k(this.$player,"art-backdrop"),L&&k(this.$player,"art-mobile")}destroy(t){t?this.$container.innerHTML="":k(this.$player,"art-destroy")}}class Gt{on(t,n,o){const r=this.e||(this.e={});return(r[t]||(r[t]=[])).push({fn:n,ctx:o}),this}once(t,n,o){const r=this;function i(...a){r.off(t,i),n.apply(o,a)}return i._=n,this.on(t,i,o)}emit(t,...n){const o=((this.e||(this.e={}))[t]||[]).slice();for(let r=0;r<o.length;r+=1)o[r].fn.apply(o[r].ctx,n);return this}off(t,n){const o=this.e||(this.e={}),r=o[t],i=[];if(r&&n)for(let a=0,s=r.length;a<s;a+=1)r[a].fn!==n&&r[a].fn._!==n&&i.push(r[a]);return i.length?o[t]=i:delete o[t],this}}let dr=0;const $t=[];class T extends Gt{constructor(t,n){if(super(),!St)throw new Error("Artplayer can only be used in the browser environment");this.id=++dr;const o=Lt(T.option,t);if(o.container=t.container,this.option=mt(o,Vt),this.isLock=!1,this.isReady=!1,this.isFocus=!1,this.isInput=!1,this.isRotate=!1,this.isDestroy=!1,this.template=new Et(this),this.events=new _n(this),this.storage=new lr(this),this.icons=new ao(this),this.i18n=new In(this),this.notice=new uo(this),this.player=new Ko(this),this.layers=new lo(this),this.controls=new bn(this),this.contextmenu=new ln(this),this.subtitle=new cr(this),this.info=new so(this),this.loading=new co(this),this.hotkey=new Ln(this),this.mask=new po(this),this.setting=new sr(this),this.plugins=new nr(this),typeof n=="function"&&this.on("ready",()=>n.call(this,this)),T.DEBUG){const r=i=>console.log(`[ART.${this.id}] -> ${i}`);r(`Version@${T.version}`);for(let i=0;i<gt.events.length;i++)this.on(`video:${gt.events[i]}`,a=>r(`Event@${a.type}`))}$t.push(this)}static get instances(){return $t}static get version(){return Ot}static get config(){return gt}static get utils(){return tn}static get scheme(){return Vt}static get Emitter(){return Gt}static get validator(){return mt}static get kindOf(){return mt.kindOf}static get html(){return Et.html}static get option(){return{id:"",container:"#artplayer",url:"",poster:"",type:"",theme:"#f00",volume:.7,isLive:!1,muted:!1,autoplay:!1,autoSize:!1,autoMini:!1,loop:!1,flip:!1,playbackRate:!1,aspectRatio:!1,screenshot:!1,setting:!1,hotkey:!0,pip:!1,mutex:!0,backdrop:!0,fullscreen:!1,fullscreenWeb:!1,subtitleOffset:!1,miniProgressBar:!1,useSSR:!1,playsInline:!0,lock:!1,gesture:!0,fastForward:!1,autoPlayback:!1,autoOrientation:!1,airplay:!1,proxy:void 0,layers:[],contextmenu:[],controls:[],settings:[],quality:[],highlight:[],plugins:[],thumbnails:{url:"",number:60,column:10,width:0,height:0,scale:1},subtitle:{url:"",type:"",style:{},name:"",escape:!0,encoding:"utf-8",onVttLoad:t=>t},moreVideoAttr:{controls:!1,preload:te?"auto":"metadata"},i18n:{},icons:{},cssVar:{},customType:{},lang:navigator?.language.toLowerCase()}}get proxy(){return this.events.proxy}get query(){return this.template.query}get video(){return this.template.$video}reset(){this.video.removeAttribute("src"),this.video.load()}destroy(t=!0){T.REMOVE_SRC_WHEN_DESTROY&&this.reset(),this.events.destroy(),this.template.destroy(t),$t.splice($t.indexOf(this),1),this.isDestroy=!0,this.emit("destroy")}}T.STYLE=be;T.DEBUG=!1;T.CONTEXTMENU=!0;T.NOTICE_TIME=2e3;T.SETTING_WIDTH=250;T.SETTING_ITEM_WIDTH=200;T.SETTING_ITEM_HEIGHT=35;T.RESIZE_TIME=200;T.SCROLL_TIME=200;T.SCROLL_GAP=50;T.AUTO_PLAYBACK_MAX=10;T.AUTO_PLAYBACK_MIN=5;T.AUTO_PLAYBACK_TIMEOUT=3e3;T.RECONNECT_TIME_MAX=5;T.RECONNECT_SLEEP_TIME=1e3;T.CONTROL_HIDE_TIME=3e3;T.DBCLICK_TIME=300;T.DBCLICK_FULLSCREEN=!0;T.MOBILE_DBCLICK_PLAY=!0;T.MOBILE_CLICK_PLAY=!1;T.AUTO_ORIENTATION_TIME=200;T.INFO_LOOP_TIME=1e3;T.FAST_FORWARD_VALUE=3;T.FAST_FORWARD_TIME=1e3;T.TOUCH_MOVE_RATIO=.5;T.VOLUME_STEP=.1;T.SEEK_STEP=5;T.PLAYBACK_RATE=[.5,.75,1,1.25,1.5,2];T.ASPECT_RATIO=["default","4:3","16:9"];T.FLIP=["normal","horizontal","vertical"];T.FULLSCREEN_WEB_IN_BODY=!0;T.LOG_VERSION=!0;T.USE_RAF=!1;T.REMOVE_SRC_WHEN_DESTROY=!0;St&&(ie("artplayer-style",be),setTimeout(()=>{T.LOG_VERSION&&console.log(`%c ArtPlayer %c ${T.version} %c https://artplayer.org`,"color: #fff; background: #5f5f5f","color: #fff; background: #4bc729","")},100));const pr={__name:"VideoPlayer",props:{src:{type:String,required:!0},poster:{type:String,default:""},thumbnails:{type:String,default:""},thumbnailsCount:{type:Number,default:0}},emits:["ready","error"],setup(e,{emit:t}){const n=e,o=t,r=X(null);let i=null;const a=()=>"http://8.148.251.135/api".replace(/\/api\/?$/,""),s=()=>{if(i&&i.destroy(),!r.value||!n.src)return;const c={container:r.value,url:n.src,poster:n.poster,autoplay:!1,pip:!0,autoSize:!0,autoMini:!0,screenshot:!0,setting:!0,loop:!1,flip:!0,playbackRate:!0,aspectRatio:!0,fullscreen:!0,subtitleOffset:!0,miniProgressBar:!0,mutex:!0,backdrop:!0,playsInline:!0,autoPlayback:!0,airplay:!0,theme:"#409eff",lang:navigator.language.toLowerCase(),moreVideoAttr:{crossOrigin:"anonymous"}};if(n.thumbnails&&n.thumbnailsCount>0){let l=n.thumbnails;if(!l.startsWith("http")){const d=a();l.startsWith("/media/")?l=`${d}${l}`:l=`${d}/media/${l}`}console.log("[VideoPlayer] Thumbnails config:",{url:l,number:n.thumbnailsCount,original:n.thumbnails}),c.thumbnails={url:l,number:n.thumbnailsCount,width:160,height:90,column:10}}else console.log("[VideoPlayer] No thumbnails:",{thumbnails:n.thumbnails,count:n.thumbnailsCount});i=new T(c),i.on("ready",()=>{o("ready")}),i.on("error",l=>{o("error",l)})};return Ae(()=>n.src,()=>{n.src&&s()}),Kt(()=>{s()}),Zt(()=>{i&&(i.destroy(),i=null)}),(c,l)=>(D(),j("div",{ref_key:"artRef",ref:r,class:"artplayer-container"},null,512))}},ur=bt(pr,[["__scopeId","data-v-ee08c435"]]),hr=["disabled"],fr={__name:"PreviewButton",props:{disabled:{type:Boolean,default:!1}},emits:["click"],setup(e){return(t,n)=>(D(),j("button",{class:"preview-btn",onClick:n[0]||(n[0]=o=>t.$emit("click")),disabled:e.disabled},[...n[1]||(n[1]=[Ve('<svg class="preview-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" data-v-a6a59d27><rect x="3" y="3" width="18" height="18" rx="2" ry="2" data-v-a6a59d27></rect><circle cx="8.5" cy="8.5" r="1.5" data-v-a6a59d27></circle><polyline points="21 15 16 10 5 21" data-v-a6a59d27></polyline></svg><span class="preview-text" data-v-a6a59d27>预览</span>',2)])],8,hr))}},mr=bt(fr,[["__scopeId","data-v-a6a59d27"]]),gr={class:"upload-text"},vr={key:0,class:"upload-progress"},yr={__name:"UploadButton",props:{text:{type:String,default:"上传文件"},loadingText:{type:String,default:"上传中"},loading:{type:Boolean,default:!1},progress:{type:Number,default:0}},setup(e){return(t,n)=>(D(),j("div",{class:De(["upload-btn",{"is-loading":e.loading}])},[n[0]||(n[0]=N("svg",{class:"upload-icon",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":"2"},[N("path",{d:"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"}),N("polyline",{points:"17 8 12 3 7 8"}),N("line",{x1:"12",y1:"3",x2:"12",y2:"15"})],-1)),N("span",gr,Jt(e.loading?`${e.loadingText} ${e.progress}%`:e.text),1),e.loading?(D(),j("div",vr,[N("div",{class:"upload-progress-bar",style:Oe({width:e.progress+"%"})},null,4)])):Qt("",!0)],2))}},br=bt(yr,[["__scopeId","data-v-c0cc5c1a"]]),wr=["disabled"],xr={__name:"RetryButton",props:{disabled:{type:Boolean,default:!1}},emits:["click"],setup(e){return(t,n)=>(D(),j("button",{class:"retry-btn",onClick:n[0]||(n[0]=o=>t.$emit("click")),disabled:e.disabled},[...n[1]||(n[1]=[N("svg",{class:"retry-icon",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":"2"},[N("polyline",{points:"23 4 23 10 17 10"}),N("path",{d:"M20.49 15a9 9 0 1 1-2.12-9.36L23 10"})],-1),N("span",{class:"retry-text"},"重试",-1)])],8,wr))}},kr=bt(xr,[["__scopeId","data-v-6de68e75"]]),$r={class:"media-page"},Tr={class:"card-header"},Cr={key:0,class:"thumbnail-status"},Er={style:{display:"inline-flex","align-items":"center",gap:"4px"}},Sr={key:3,class:"failed-status"},zr={key:1},Mr={class:"action-buttons"},_r={class:"preview-container"},Lr=["src"],Ir=["src"],Pr={key:3,class:"preview-unsupported"},Rr={__name:"Media",setup(e){const t=Ne(),n=X(!1),o=X([]),r=X(1),i=X(20),a=X(0),s=X(!1),c=X(null),l=X(""),d=X(!1),u=X(0);let h=null;const m="http://8.148.251.135/api",f=dt(()=>`${m}/media/`),y=dt(()=>({Authorization:`Bearer ${t.token}`})),b=dt(()=>c.value?(c.value.file_type||"").startsWith("image/"):!1),C=dt(()=>c.value?(c.value.file_type||"").startsWith("video/"):!1),z=dt(()=>c.value?(c.value.file_type||"").startsWith("audio/"):!1),E=dt(()=>{if(!c.value)return"";if(C.value)return`${m}/media/${c.value.id}/`;const x=c.value.url||c.value.file;return Wt(x)}),$=()=>o.value.some(x=>x.thumbnail_status==="pending"||x.thumbnail_status==="processing"),S=()=>{h&&clearInterval(h),h=setInterval(()=>{$()?_():(clearInterval(h),h=null)},3e3)},_=async()=>{n.value=!0;try{const x=(r.value-1)*i.value,{data:w}=await At.get("/media/",{params:{limit:i.value,offset:x}});o.value=w.results||w,a.value=w.count||o.value.length,$()&&S()}catch{F.error("获取媒体列表失败")}finally{n.value=!1}},B=x=>x<1024?x+" B":x<1024*1024?(x/1024).toFixed(2)+" KB":(x/(1024*1024)).toFixed(2)+" MB",ot=x=>{d.value=!0,u.value=Math.round(x.percent)},It=x=>{if(!x.type.startsWith("video/")&&x.size>10485760)return F.error("文件大小不能超过 10MB（视频文件不限大小）"),!1;if(!["image/jpeg","image/png","image/gif","image/webp","image/svg+xml","video/mp4","video/webm","video/ogg","video/quicktime","application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(x.type))return F.error(`不支持的文件类型：${x.type}。支持的类型：图片（jpg, png, gif, webp, svg）、视频（mp4, webm, ogg）、文档（pdf, doc, docx）`),!1;const J=[".jpg",".jpeg",".png",".gif",".webp",".svg",".mp4",".webm",".ogg",".mov",".pdf",".doc",".docx"],at="."+x.name.split(".").pop().toLowerCase();return J.includes(at)?!0:(F.error(`不支持的文件扩展名：${at}。支持的扩展名：${J.join(", ")}`),!1)},we=()=>{d.value=!1,u.value=0,F.success("上传成功"),_()},xe=x=>{d.value=!1,u.value=0;const w=x?.response?.data?.file?.[0]||x?.response?.data?.error||"上传失败";F.error(w)},ke=x=>{c.value=x,s.value=!0},$e=x=>{const w=Wt(x.file);navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(w).then(()=>{F.success("链接已复制到剪贴板")}).catch(()=>{Yt(w)}):Yt(w)},Yt=x=>{const w=document.createElement("textarea");w.value=x,w.style.position="fixed",w.style.top="0",w.style.left="0",w.style.width="2em",w.style.height="2em",w.style.padding="0",w.style.border="none",w.style.outline="none",w.style.boxShadow="none",w.style.background="transparent",w.style.opacity="0",document.body.appendChild(w),w.focus(),w.select();try{document.execCommand("copy")?F.success("链接已复制到剪贴板"):F.error("复制失败，请手动复制")}catch{F.error("浏览器不支持复制，请手动复制")}finally{document.body.removeChild(w)}},Te=()=>{},Ce=x=>{F.error("视频加载失败，请检查视频格式或网络连接")},Ee=()=>{if(E.value){const x=document.createElement("a");x.href=E.value,x.download=c.value?.filename||"download",x.target="_blank",document.body.appendChild(x),x.click(),document.body.removeChild(x)}},Se=async x=>{await We.confirm("确定删除该文件？","提示",{type:"warning"});try{await At.delete(`/media/${x.id}/`),F.success("删除成功"),_()}catch{F.error("删除失败")}},ze=async x=>{try{await At.post(`/media/${x.id}/regenerate_thumbnails/`),F.success("缩略图生成任务已启动"),_()}catch{F.error("启动缩略图生成失败")}},Me=()=>{r.value=1,_()};return Kt(()=>{_()}),Zt(()=>{h&&(clearInterval(h),h=null)}),(x,w)=>{const kt=et("el-upload"),J=et("el-table-column"),at=et("el-tag"),Pt=et("el-icon"),Ft=et("el-button"),_e=et("el-table"),Le=et("el-pagination"),Ie=et("el-card"),Pe=et("el-dialog"),Re=Be("loading");return D(),j("div",$r,[I(Ie,null,{header:Y(()=>[N("div",Tr,[w[3]||(w[3]=N("span",null,"媒体管理",-1)),I(kt,{action:f.value,headers:y.value,"before-upload":It,"on-success":we,"on-error":xe,"on-progress":ot,"show-file-list":!1,multiple:""},{default:Y(()=>[I(br,{loading:d.value,progress:u.value},null,8,["loading","progress"])]),_:1},8,["action","headers"])])]),default:Y(()=>[Ye((D(),ut(_e,{data:o.value,stripe:""},{default:Y(()=>[I(J,{prop:"filename",label:"文件名","min-width":"200","show-overflow-tooltip":""}),I(J,{prop:"file_type",label:"类型",width:"150"}),I(J,{prop:"file_size",label:"大小",width:"100"},{default:Y(({row:V})=>[ct(Jt(B(V.file_size)),1)]),_:1}),I(J,{label:"缩略图",width:"150"},{default:Y(({row:V})=>[V.is_video?(D(),j("div",Cr,[V.thumbnail_status==="pending"?(D(),ut(at,{key:0,type:"info",size:"small"},{default:Y(()=>[...w[4]||(w[4]=[ct("等待中 ",-1)])]),_:1})):V.thumbnail_status==="processing"?(D(),ut(at,{key:1,type:"warning",size:"small"},{default:Y(()=>[N("span",Er,[I(Pt,{class:"is-loading"},{default:Y(()=>[I(Ht(Fe))]),_:1}),w[5]||(w[5]=N("span",null,"生成中",-1))])]),_:1})):V.thumbnail_status==="completed"?(D(),ut(at,{key:2,type:"success",size:"small"},{default:Y(()=>[...w[6]||(w[6]=[ct(" 已完成 ",-1)])]),_:1})):V.thumbnail_status==="failed"?(D(),j("div",Sr,[I(at,{type:"danger",size:"small"},{default:Y(()=>[...w[7]||(w[7]=[ct("失败",-1)])]),_:1}),I(kr,{onClick:Rt=>ze(V)},null,8,["onClick"])])):Qt("",!0)])):(D(),j("span",zr,"-"))]),_:1}),I(J,{prop:"uploader_name",label:"上传者",width:"120"}),I(J,{prop:"created_at",label:"上传时间",width:"180"}),I(J,{label:"操作",width:"200",fixed:"right"},{default:Y(({row:V})=>[N("div",Mr,[I(mr,{onClick:Rt=>ke(V)},null,8,["onClick"]),I(Ft,{type:"primary",size:"small",onClick:Rt=>$e(V)},{default:Y(()=>[...w[8]||(w[8]=[ct(" 复制链接 ",-1)])]),_:1},8,["onClick"]),I(Ue,{onClick:Rt=>Se(V)},null,8,["onClick"])])]),_:1})]),_:1},8,["data"])),[[Re,n.value]]),I(Le,{"current-page":r.value,"onUpdate:currentPage":w[0]||(w[0]=V=>r.value=V),"page-size":i.value,"onUpdate:pageSize":w[1]||(w[1]=V=>i.value=V),"page-sizes":[10,20,50,100],total:a.value,layout:"total, sizes, prev, pager, next, jumper",onCurrentChange:_,onSizeChange:Me},null,8,["current-page","page-size","total"])]),_:1}),I(Pe,{modelValue:s.value,"onUpdate:modelValue":w[2]||(w[2]=V=>s.value=V),title:c.value?.filename||"预览",width:"900px","destroy-on-close":""},{default:Y(()=>[N("div",_r,[b.value?(D(),j("img",{key:0,src:E.value,class:"preview-image",alt:"预览图片"},null,8,Lr)):C.value?(D(),ut(ur,{key:1,src:E.value,poster:l.value,thumbnails:c.value?.thumbnails_url,"thumbnails-count":c.value?.thumbnails_count||0,onReady:Te,onError:Ce},null,8,["src","poster","thumbnails","thumbnails-count"])):z.value?(D(),j("audio",{key:2,src:E.value,controls:"",class:"preview-audio"},null,8,Ir)):(D(),j("div",Pr,[I(Pt,{size:64},{default:Y(()=>[I(Ht(He))]),_:1}),w[10]||(w[10]=N("p",null,"该文件类型不支持预览",-1)),I(Ft,{type:"primary",onClick:Ee},{default:Y(()=>[...w[9]||(w[9]=[ct("下载文件",-1)])]),_:1})]))])]),_:1},8,["modelValue","title"])])}}},Dr=bt(Rr,[["__scopeId","data-v-a281fcb7"]]);export{Dr as default};
