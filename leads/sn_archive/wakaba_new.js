var postByNum=[];var ajaxPosts=[];var ajaxThrds={};var refMap=[];var Posts=[];var opPosts=[];var pView,dForm,pForm,pArea,qArea,admin;var board=window.location.toString().split('/')[3];var isMain=window.location.pathname.indexOf('/res/')<0;var isIE=/*@cc_on!@*/0;function get_cookie(name){with(document.cookie){var regexp=new RegExp('(^|;\\s+)'+ name+'=(.*?)(;|$)');var hit=regexp.exec(document.cookie);if(hit&&hit.length>2)return unescape(hit[2]);else return'';}}
function set_cookie(name,value,days){if(days){var date=new Date();date.setTime(date.getTime()+ days*24*60*60*1000);var expires='; expires='+ date.toGMTString();}else expires='';document.cookie=name+'='+ value+ expires+'; path=/';}
function $id(id){return document.getElementById(id);}
function $n(id){return document.getElementsByName(id)[0];}
function $t(id,root){return(root||document).getElementsByTagName(id);}
function $c(id,root){return(root||document).getElementsByClassName(id);}
function $each(arr,fn){for(var el,i=0;el=arr[i++];)
fn(el);}
function $html(el,htm){var cln=el.cloneNode(false);cln.innerHTML=htm;el.parentNode.replaceChild(cln,el);return cln;}
function $attr(el,attr){for(var key in attr){if(key=='text'){el.textContent=attr[key];continue;}
if(key=='value'){el.value=attr[key];continue;}
if(key=='html'){el.innerHTML=attr[key];continue;}
el.setAttribute(key,attr[key]);}
return el;}
function $event(el,events){for(var key in events)
el.addEventListener(key,events[key],false);}
function $before(el,nodes){for(var i=0,len=nodes.length;i<len;i++)
if(nodes[i])el.parentNode.insertBefore(nodes[i],el);}
function $after(el,nodes){var i=nodes.length;while(i--)if(nodes[i])el.parentNode.insertBefore(nodes[i],el.nextSibling);}
function $new(tag,attr,events){var el=document.createElement(tag);if(attr)$attr(el,attr);if(events)$event(el,events);return el;}
function $disp(el){el.style.display=el.style.display=='none'?'':'none';}
function $del(el){if(el)el.parentNode.removeChild(el);}
function $offset(el,xy){var c=0;while(el){c+=el[xy];el=el.offsetParent;}
return c;}
function $close(el){if(!el)return;var h=el.clientHeight- 18;el.style.height=h+'px';var i=8;var closing=setInterval(function(){if(!el||i--<0){clearInterval(closing);$del(el);return;}
var s=el.style;s.opacity=i/10;s.paddingTop=parseInt(s.paddingTop)- 1+'px';s.paddingBottom=parseInt(s.paddingBottom)- 1+'px';var hh=parseInt(s.height)- h/10;s.height=(hh<0?0:hh)+'px';},35);}
function $show(el){var i=0;var showing=setInterval(function(){if(!el||i++>8){clearInterval(showing);return;}
var s=el.style;s.opacity=i/10;s.paddingTop=parseInt(s.paddingTop)+ 1+'px';s.paddingBottom=parseInt(s.paddingBottom)+ 1+'px';},35);}
function insert(txt){var el=document.forms.postform.shampoo;if(el){if(el.createTextRange&&el.caretPos){var caretPos=el.caretPos;caretPos.txt=caretPos.txt.charAt(caretPos.txt.length-1)==' '?txt+' ':txt;}else if(el.setSelectionRange){var start=el.selectionStart;var end=el.selectionEnd;el.value=el.value.substr(0,start)+ txt+ el.value.substr(end);el.setSelectionRange(start+ txt.length,start+ txt.length);}else el.value+=txt+' ';el.focus();}}
function AJAX(b,id,fn){var xhr;if(window.XMLHttpRequest)xhr=new XMLHttpRequest()
else if(window.ActiveXObject){try{xhr=new ActiveXObject("Msxml2.XMLHTTP");}
catch(e){try{xhr=new ActiveXObject("Microsoft.XMLHTTP");}catch(e){}}}else return false;xhr.onreadystatechange=function(){if(xhr.readyState!=4)return;if(xhr.status==200){var x=xhr.responseText;x=x.split(/<form[^>]+del[^>]+>/)[1].split('</form>')[0];var thrds=x.substring(0,x.lastIndexOf(x.match(/<br[^>]+left/))).split(/<br[^>]+left[^>]*>\s*<hr[^>]*>/);for(var i=0,tLen=thrds.length;i<tLen;i++){var tNum=thrds[i].match(/<input[^>]+checkbox[^>]+>/i)[0].match(/(\d+)/)[0];var posts=thrds[i].split(/<table[^>]*>/);ajaxThrds[tNum]={keys:[],pcount:posts.length};for(var j=0,pLen=posts.length;j<pLen;j++){var x=posts[j];var pNum=x.match(/<input[^>]+checkbox[^>]+>/i)[0].match(/(\d+)/)[0];ajaxThrds[tNum].keys.push(pNum);ajaxPosts[pNum]=x.substring(!/<td/.test(x)&&/filesize[^>]*>/.test(x)?x.search(/filesize[^>]*>/)- 13:x.indexOf('<label'),/<td/.test(x)?x.lastIndexOf('</td'):(/omittedposts[^>]*>/.test(x)?x.lastIndexOf('</span')+ 7:x.lastIndexOf('</blockquote')+ 13));ajaxRefmap(ajaxPosts[pNum].substr(ajaxPosts[pNum].indexOf('<blockquote>')+ 12),pNum);}}
fn();}else fn('HTTP '+ xhr.status+' '+ xhr.statusText);};xhr.open('GET','/'+ b+'/res/'+ id+'.html',true);xhr.setRequestHeader('Accept-Encoding','deflate, gzip, x-gzip');xhr.send();}
function delPostPreview(e){pView=e.relatedTarget;while(1){if(/^preview/.test(pView.id))break;else{pView=pView.parentNode;if(!pView)break;}}
setTimeout(function(){if(!pView)$each($t('div'),function(el){if(/^preview/.test(el.id))$del(el);});else while(pView.nextSibling)$del(pView.nextSibling);},800);}
function funcPostPreview(htm){if(!pView)return;pView.innerHTML=htm;$each($t('script',pView),function(el){$del(el);});eventPostPreview(pView);var pNum=pView.id.match(/\d+/);if(!$c('ABU_refmap',pView)[0]&&!postByNum[pNum]&&refMap[pNum])
showRefMap(pView,pNum);}
function showPostPreview(e){var link=e.target;var tNum=link.pathname.substring(link.pathname.lastIndexOf('/')).match(/\d+/);var pNum=link.hash.match(/\d+/)||tNum;var scrW=document.body.clientWidth,scrH=window.innerHeight;x=$offset(link,'offsetLeft')+ link.offsetWidth/2;y=$offset(link,'offsetTop');if(e.clientY<scrH*0.75)y+=link.offsetHeight;pView=$new('div',{'id':'preview_'+ pNum,'class':'reply','html':'<span class="ABU_icn_wait">&nbsp;</span>&nbsp;Загрузка...','style':('position:absolute; z-index:300; border:1px solid grey; '
+(x<scrW/2?'left:'+ x:'right:'+ parseInt(scrW- x+ 2))+'px; '
+(e.clientY<scrH*0.75?'top:'+ y:'bottom:'+ parseInt(scrH- y- 4))+'px')},{'mouseout':delPostPreview,'mouseover':function(){if(!pView)pView=this;}});if(postByNum[pNum])funcPostPreview(postByNum[pNum].innerHTML);else if(ajaxPosts[pNum])funcPostPreview(ajaxPosts[pNum]);else AJAX(board,tNum,function(err){funcPostPreview(err||ajaxPosts[pNum]||'Пост не найден')});$del($id(pView.id));dForm.appendChild(pView);}
function eventPostPreview(node){$each($t('a',node),function(link){if(link.textContent.indexOf('>>')==0&&!link.getAttribute('onmouseover'))
$event(link,{'mouseover':showPostPreview,'mouseout':delPostPreview});});}
function getRefMap(pNum,rNum){if(!refMap[rNum])refMap[rNum]=[];if((','+ refMap[rNum].toString()+',').indexOf(','+ pNum+',')<0)
refMap[rNum].push(pNum);}
function ajaxRefmap(txt,pNum){var x=txt.match(/&gt;&gt;\d+/g);if(x)for(var i=0;rLen=x.length,i<rLen;i++)
getRefMap(pNum,x[i].match(/\d+/g));}
function showRefMap(post,pNum,isUpd){if(typeof refMap[pNum]!=='object'||!post)return;var txt='Ответы: '+ refMap[pNum].toString().replace(/(\d+)/g,'<a href="#$1" onmouseover="showPostPreview(event)" onmouseout="delPostPreview(event)">&gt;&gt;$1</a>');var el=isUpd?$id('ABU_refmap_'+ pNum):null;if(!el){el=$new('div',{'class':'ABU_refmap','id':'ABU_refmap_'+ pNum,'html':txt});$after($t('blockquote',post)[0],[el]);}else $html(el,txt);}
function addRefMap(post){$each($t('a',post),function(link){if(link.textContent.indexOf('>>')==0){var rNum=link.hash.match(/\d+/);if(postByNum[rNum]){while((link=link.parentNode).tagName!='BLOCKQUOTE');getRefMap(link.parentNode.id.match(/\d+/),rNum);}}});for(var rNum in refMap)
showRefMap(postByNum[rNum],rNum,Boolean(post));}
function buildTablePost(id){return $new('table',{'class':'post','id':'post_'+ id,'html':'<tbody><tr> '+ ajaxPosts[id]+' </tr></tbody>'});}
function updateThread(){var btn=$id('ABU_getnewposts');btn.innerHTML='[<span style="cursor:default">Обновить тред</span>]';$alert('Загрузка...','wait');var thrd=$c('thread')[0];var tNum=thrd.id.match(/\d+/)[0];var last=Posts.length+ 1;AJAX(board,tNum,function(err){$close($id('ABU_alert_wait'));if(err){alert(err);return;}
if(ajaxThrds[tNum].pcount- last==0)$alert('Нет новых постов');for(var i=last,len=ajaxThrds[tNum].pcount;i<len;i++){var pNum=ajaxThrds[tNum].keys[i];var post=buildTablePost(pNum);post.Num=pNum;thrd.appendChild(post);postByNum[pNum]=post;Posts.push(post);eventPostPreview(post);addRefMap(post);}
setTimeout(function(){btn.innerHTML='[<a href="#" onclick="javascript:updateThread(); return false;">Обновить тред</a>]';},2000);},true);}
function expandThread(tNum,last){$alert('Загрузка...','wait');var thrd=$id('thread_'+ tNum);AJAX(board,tNum,function(err){$close($id('ABU_alert_wait'));if(err){$alert(err);return;}
var oppost=postByNum[tNum];var opbloq=$t('blockquote',oppost)[0];while(opbloq.nextSibling)$del(opbloq.nextSibling);while(oppost.nextSibling)$del(oppost.nextSibling);var len=ajaxThrds[tNum].keys.length;last=last?len- last:1;if(last>1)oppost.appendChild($new('span',{'class':'omittedposts','text':' Пропущено '+ parseInt(last- 1)
+' ответов. Нажмите "ответ", чтобы увидеть тред целиком.'}));for(var i=last;i<len;i++){var pNum=ajaxThrds[tNum].keys[i];var post=buildTablePost(pNum);post.Num=pNum;thrd.appendChild(post);postByNum[pNum]=post;Posts.push(post);eventPostPreview(post);addRefMap(post);}});}
function expandPost(link){$alert('Загрузка...','wait');var tNum=link.pathname.match(/\/(\d+)\./)[1];var pNum=link.hash.match(/\d+/)||tNum;AJAX(board,tNum,function(err){$close($id('ABU_alert_wait'));if(err)return;link.parentNode.parentNode.innerHTML=ajaxPosts[pNum].substr(ajaxPosts[pNum].indexOf('<blockquote>')+ 12,ajaxPosts[pNum].indexOf('</blockquote>'));});}
function getTitle(post){var t=$c('filetitle',post)[0];if(t)t=t.textContent.trim();if(!t||t=='')t=$t('blockquote',post)[0].textContent;return t.replace(/\s+/g,' ');}
function storeHiddenThread(id){id='t'+ id;var data=get_cookie(thread_cookie);if(data.indexOf(id+',')!=-1)return;else set_cookie(thread_cookie,data+ id+',',365);}
function removeHiddenThread(id){id='t'+ id;var data=get_cookie(thread_cookie);var re=new RegExp(id+',','g');data=data.replace(re,'');set_cookie(thread_cookie,data,365);}
function toggleHidden(id){var tNum=id.match(/\d+/);var thrd=$id('thread_'+ tNum);hideThread(thrd,tNum);}
function toggleThread(pNum){hideThread(postByNum[pNum].parentNode,pNum);storeHiddenThread(pNum)}
function unhideThread(thrd,tNum){$disp(thrd);$del($id('ABU_hiddenthr_'+ tNum));removeHiddenThread(tNum);}
function hideThread(thrd,tNum){$disp(thrd);var info=$new('span',{'class':'reply','id':'ABU_hiddenthr_'+ tNum,'style':'padding:1px 5px; border:2px solid grey','html':'Скрытый тред <a style="cursor:pointer; font-weight:bold">№'
+ tNum+'</a><i> ('+ getTitle(thrd).substring(0,50)+')'});$event($t('a',info)[0],{'click':function(){unhideThread(thrd,tNum);}});$before(thrd,[info]);}
function areYouShure(el){if(confirm('Вы уверены в своих действиях?'))document.location=el.href;return false;}
function writeBan(el){var reason=prompt('Напишите причину бана, пожалуйста:');if(reason)document.location=el.href+'&comment='+ encodeURIComponent(reason);return false;}
function addDate(n){var d=new Date();d.setTime(d.getTime()+ n*24*60*60*1000);return(d.getMonth()+ 1).toString()+'%2F'
+ d.getDate().toString()+'%2F'
+ d.getFullYear().toString();}
function getMultiplePostsForBanset(){var ToAction="";var All=document.forms['delform'];for(var i=0;i<All.elements.length;++i){if(All.elements[i].checked){ToAction+=All.elements[i].value+",";}}
return ToAction.slice(0,-1);}
function removeAdminMenu(e){var el=e.relatedTarget;while(1){if(el.id=='ABU_select')break;else{el=el.parentNode;if(!el)break;}}
if(!el)$del($id('ABU_select'));}
function addAdminMenu(el){var pNum=el.parentNode.parentNode.id.match(/\d+/);var pMultipleNums=getMultiplePostsForBanset();if(pMultipleNums==""){pMultipleNums=pNum;}
document.body.appendChild($new('div',{'class':'reply','id':'ABU_select','style':'left:'+($offset(el,'offsetLeft').toString()- 18)+'px; top:'+
($offset(el,'offsetTop')+ el.offsetHeight- 1).toString()+'px','html':'<a href="/'+ board+'/wakaba.pl?task=delete&admin='+ admin+'&delete='+ pMultipleNums+'&mode=2" onclick="return areYouShure(this)\">Удалить</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&mode=3" onclick="return writeBan(this)">Забанить</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&date='+ addDate(2)+'" onclick="return writeBan(this)">Бан на 2 дня</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&date='+ addDate(7)+'" onclick="return writeBan(this)">Бан на неделю</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&date='+ addDate(31)+'" onclick="return writeBan(this)">Бан на месяц</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&mode=1" onclick="return writeBan(this)">Забанить и удалить</a>'+'<a href="/'+ board+'/wakaba.pl?task=banpost&admin='+ admin+'&post='+ pMultipleNums+'&mode=5" onclick="return areYouShure(this)">Удалить все</a>'+'<a href="/'+ board+'/wakaba.pl?task=banpost&admin='+ admin+'&post='+ pNum+'&mode=7" onclick="return areYouShure(this)">Удалить все в треде</a>'+'<a href="/'+ board+'/wakaba.pl?admin='+ admin+'&task=banpost&post='+ pMultipleNums+'&mode=6" onclick="return writeBan(this)">Забанить и удалить все</a>'+'<a href="/'+ board+'/wakaba.pl?task=delete&admin='+ admin+'&delete='+ pMultipleNums+'&fileonly=on&mode=2" onclick="return areYouShure(this)">Удалить файл</a>'+'<a href="/'+ board+'/wakaba.pl?task=banpost&admin='+ admin+'&post='+ pMultipleNums+'&mode=warning" onclick="return areYouShure(this)">Предупредить</a>'+'<a href="/'+ board+'/wakaba.pl?task=lock&admin='+ admin+'&num='+ pNum+'" onclick=\"return areYouShure(this)\">Закрыть тред</a>'+'<a href="/'+ board+'/wakaba.pl?task=unlock&admin='+ admin+'&num='+ pNum+'" onclick="return areYouShure(this)">Открыть тред</a>'+'<a href="/'+ board+'/wakaba.pl?task=stick&admin='+ admin+'&num='+ pNum+'" onclick="return areYouShure(this)">Прикрепить тред</a>'+'<a href="/'+ board+'/wakaba.pl?task=unstick&admin='+ admin+'&num='+ pNum+'" onclick="return areYouShure(this)">Отцепить тред</a>'+'<a href="/'+ board+'/wakaba.pl?task=delete&admin='+ admin+'&archive=Archive&mode=2&delete='+ pNum+'" onclick="return areYouShure(this)">Перенести в архив</a>'+'<a href="/'+ board+'/wakaba.pl?task=edit&admin='+ admin+'&num='+ pNum+'" onclick="return areYouShure(this)">Редактировать</a>'},{'mouseout':removeAdminMenu}));}
function $alert(txt,id){var el,nid='ABU_alert';if(id){nid+='_'+ id;el=$id(nid);}
if(!el){el=$new('div',{'class':'reply','id':nid,'style':'float:right; clear:both; opacity:0; width:auto; min-width:0; padding:0 10px 0 10px;'+' margin:1px; overflow:hidden; white-space:pre-wrap; outline:0; border:1px solid grey'});if(id=='wait')el.appendChild($new('span',{'class':'ABU_icn_wait'}));el.appendChild($new('div',{'style':'display:inline-block; margin-top:4px'}));$show($id('ABU_alertbox').appendChild(el));}
$t('div',el)[0].innerHTML=txt;if(id!='wait')setTimeout(function(){$close(el);},2000);}
function addQuickReply(pNum){var post=postByNum[pNum];var tNum=post.parentNode.id.match(/\d+/);if(!qArea.hasChildNodes()){qArea.appendChild(pForm);$disp($id('togglereply'));$disp(pArea);$disp(qArea);if(isMain)$before(pForm.firstChild,[$new('input',{'type':'hidden','name':'parent','value':tNum})]);}else if(post.nextSibling==qArea){$disp(qArea);return;}
$after(post,[qArea]);qArea.style.display='block';$n('parent').value=tNum;insert('>>'+ pNum);addDate(1);}
function addNormalReply(e){e.preventDefault();pArea.appendChild(pForm);$disp($id('togglereply'));$disp(pArea);$disp(qArea);if(isMain)$del($n('parent'));}
function doPost(){$alert('Проверка...','wait');}
function iframeLoad(e){try{frm=e.target.contentDocument;if(!frm||!frm.body||!frm.body.innerHTML)return;}
catch(e){$alert('Iframe error:\n'+ e);$close($id('DESU_alert_wait'));return;}
var err;if(!frm.getElementById('delform'))err=$t('font',$t('center',frm)[1])[0];if(err){$close($id('ABU_alert_wait'));$alert(err?err.innerHTML:'Ошибка:\n'+(frm.body||frm).innerHTML);}else{var text=$t('textarea',pForm)[0];var pFile=$n('file');var pVideo=$n('video');var pCapinp=$n('recaptcha_response_field');if(text)text.value='';if(pFile)$html(pFile.parentNode,pFile.parentNode.innerHTML);if(pVideo)pVideo.value='';if(pCapinp){pCapinp.value='';Recaptcha.reload();}
if(!isMain)updateThread();else if(pArea.hasChildNodes())window.location=frm.location;else expandThread($n('parent').value,5);}
frm.location.replace('about:blank');}
function addSubmitIframe(){var load=window.opera?'DOMFrameContentLoaded':'load';$t('body')[0].appendChild($new('iframe',{'name':'ABU_submitframe','id':'ABU_submitframe','src':'about:blank','style':'display:none; width:0px; height:0px; border:none'},{load:iframeLoad}));$attr(pForm,{'target':'ABU_submitframe'});}
function toggleMommy(){set_cookie('mommy',(get_cookie('mommy')||0)==0?1:0);scriptCSS();}
function hotkeyMommy(e){if(!e)e=window.event;if(e.altKey&&e.keyCode==78)toggleMommy();}
function scriptCSS(){var x=[];if(admin)x.push('.postbtn_adm {display:inline !important;}');if(get_cookie('mommy')==1)
x.push('img[src*="thumb"], object[width="320"] {opacity:0.04 !important} img[src*="thumb"]:hover, object[width="320"]:hover {opacity:1 !important}');if(!$id('ABU_css'))
$t('head')[0].appendChild($new('style',{'id':'ABU_css','type':'text/css','text':x.join(' ')}));else $id('ABU_css').textContent=x.join(' ');}
function fastload(){dForm=$id('delform');if(!dForm)return;admin=get_cookie('wakaadmin');pForm=$id('postform');pArea=$c('postarea')[0];qArea=$new('div',{'id':'quickarea','class':'reply','style':'display:none'});$each($c('oppost'),function(post){opPosts.push(post);var pNum=post.id.match(/\d+/);post.Num=pNum;postByNum[pNum]=post;});$each($c('post'),function(post){Posts.push(post);var pNum=post.id.match(/\d+/);post.Num=pNum;postByNum[pNum]=post;});eventPostPreview();addRefMap();dForm.appendChild($new('div',{'id':'ABU_alertbox'}));addSubmitIframe();scriptCSS();document.onkeydown=hotkeyMommy;}
function expand(num,src,thumb_src,n_w,n_h,o_w,o_h){if(n_w>screen.width){n_h=((screen.width-80)*n_h)/n_w;n_w=screen.width-80;}
$id('exlink_'+ num).innerHTML='<a href="'+ src+'" onClick="expand('+ num+",'"+ src+"','"+ thumb_src+"',"+
o_w+','+ o_h+','+ n_w+','+ n_h+'); return false;"><img src="'+
(n_w>o_w&&n_h>o_h?src:thumb_src)+'" width="'+ n_w+'" height="'+ n_h+'" class="img" /></a>';}
function get_password(name){var pass=get_cookie(name);var chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';if(pass)return pass;pass='';for(var i=0;i<8;i++){var rnd=Math.floor(Math.random()*chars.length);pass+=chars.substring(rnd,rnd+ 1);}
return pass;}
function update_captcha(e){e.src=e.src.replace(/dummy=[0-9]*/,'dummy='+ Math.floor(Math.random()*1000).toString());}
function update_captcha2(){var e=$id('imgcaptcha');if(e)update_captcha(e);}
function reverseCaptcha(e){var key;if(e.which<1040||e.which>1279)return;try{e.preventDefault();}catch(e){}
switch(e.which){case 1081:key='q';break;case 1094:key='w';break;case 1091:key='e';break;case 1082:key='r';break;case 1077:key='t';break;case 1085:key='y';break;case 1075:key='u';break;case 1096:key='i';break;case 1097:key='o';break;case 1079:key='p';break;case 1092:key='a';break;case 1099:key='s';break;case 1074:key='d';break;case 1072:key='f';break;case 1087:key='g';break;case 1088:key='h';break;case 1086:key='j';break;case 1083:key='k';break;case 1076:key='l';break;case 1103:key='z';break;case 1095:key='x';break;case 1089:key='c';break;case 1084:key='v';break;case 1080:key='b';break;case 1090:key='n';break;case 1100:key='m';break;default:return;}
e.target.value=e.target.value+ key;}
function load(id,url){var element=$id(id);if(!element)return;var xhr;if(window.XMLHttpRequest)xhr=new XMLHttpRequest()
else if(window.ActiveXObject){try{xhr=new ActiveXObject("Msxml2.XMLHTTP");}
catch(e){try{xhr=new ActiveXObject("Microsoft.XMLHTTP");}catch(e){}}}else return false;if(xhr){xhr.open('GET',url,false);xhr.send(null);element.innerHTML=xhr.responseText;}else element.innerHTML='NotLoaded';}
function highlight(post){var cells=document.getElementsByTagName('td');var reply=$id('reply'+ post);for(var i=0;i<cells.length;i++){if(cells[i].className=='highlight')cells[i].className='reply';}
if(reply){reply.className='highlight';return false;}
return true;}
function set_stylesheet_frame(styletitle,framename){var list=get_frame_by_name(framename);set_stylesheet(styletitle);if(list)set_stylesheet(styletitle,list);}
function set_stylesheet(styletitle,target){set_cookie('wakabastyle',styletitle,365);var links=target?target.document.getElementsByTagName('link'):document.getElementsByTagName('link');var rel,title,found=false;for(var i=0;i<links.length;i++){var rel=links[i].getAttribute('rel');var title=links[i].getAttribute('title');if(rel.indexOf('style')!=-1&&title){links[i].disabled=true;if(styletitle==title){links[i].disabled=false;found=true;}}}
if(!found)set_preferred_stylesheet(target?target:false)}
function set_preferred_stylesheet(target){var links=target?target.document.getElementsByTagName('link'):document.getElementsByTagName('link')
var rel,title;for(var i=0;i<links.length;i++){rel=links[i].getAttribute('rel'),title=links[i].getAttribute('title');if(rel.indexOf('style')!=-1&&title){links[i].disabled=(rel.indexOf('alt')!=-1);}}}
function get_active_stylesheet(){var links=document.getElementsByTagName('link');var rel,title;for(var i=0;i<links.length;i++){rel=links[i].getAttribute('rel'),title=links[i].getAttribute('title');if(rel.indexOf('style')!=-1&&title&&!links[i].disabled)return title;}
return null;}
function get_preferred_stylesheet(){var links=document.getElementsByTagName('link');var rel,title;for(var i=0;i<links.length;i++){rel=links[i].getAttribute('rel');title=links[i].getAttribute('title');if(rel.indexOf('style')!=-1&&rel.indexOf('alt')==-1&&title)return title;}
return null;}
function get_frame_by_name(name){var frames=window.parent.frames;for(i=0;i<frames.length;i++)
if(name==frames[i].name)return(frames[i]);}
function set_inputs(id){var form=$id(id);var gb2=form.gb2;var gb2val=get_cookie('gb2');if(gb2&&gb2val)
for(var i=0;i<gb2.length;i++)
gb2[i].checked=(gb2[i].value==gb2val);function setVal(input,cookie){var val=get_cookie(cookie);if(!form[input].value)form[input].value=val===undefined?'':val;}
setVal('akane','name');setVal('password','password');}
function buttonOK(){$id('dynamicNamed').name=$id('opt'+ select.selectedIndex).value;}
function set_delpass(id){try{$id(id).password.value=get_cookie('password');}catch(e){}}
set_stylesheet(get_cookie('wakabastyle'));var match;if(match=/#i([0-9]+)/.exec(document.location.toString())&&!document.forms.postform.shampoo.value)
insert('>>'+ match[1]);if(match=/#([0-9]+)/.exec(document.location.toString()))
highlight(match[1]);