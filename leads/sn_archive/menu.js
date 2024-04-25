var VIS_VISIBLE = "";
var VIS_HIDDEN = "hidden";

function cookie_name(name) {
	return "2ch_" + name + "_menu";
}

function get_cookie(name) {
	name = cookie_name(name);
	with (document.cookie) {
		var regexp = new RegExp("(^|;\\s+)"+name+"=(.*?)(;|$)");
		var hit = regexp.exec(document.cookie);
		if(hit && hit.length > 2)
			return unescape(hit[2]);
		else return null;
	}
};

function set_cookie(name, value, days) {
	name = cookie_name(name);
	if (!days)
		days = 8192;
	
	var date = new Date();
	date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
	var expires = "; expires=" + date.toGMTString();
	document.cookie = name + "=" + value + expires + "; path=/";
}

function init_visibility() {
	var nodelist = document.getElementById("menu").childNodes;
	var idx;

	if (!nodelist) {
		return;
	}

	current_id = null;
	vis_class = VIS_VISIBLE;

	for (idx = 0; idx < nodelist.length; idx++) {
		var sub = nodelist[idx];

		if (sub.nodeName == "DT") {
			current_id = sub.id;
			var cookie = get_cookie(current_id);
			
			if (cookie == VIS_HIDDEN)
				vis_class = VIS_HIDDEN;
			else
				vis_class = VIS_VISIBLE;
			
			sub.dvach_visible = vis_class;

			if (cookie)
				set_cookie(current_id, vis_class);

		} else if (sub.nodeName == "DD")
			sub.className = vis_class;
	}
}

function toggle(obj) {
	/* I tried traversing nextSubling attributes,
	   but for some reason they are undefined at
	   time of execution of this function.
	*/
	var current_id = obj.id;
	var vis_class = obj.dvach_visible;
	
	if (vis_class == VIS_VISIBLE)
		vis_class = VIS_HIDDEN;
	else
		vis_class = VIS_VISIBLE;
	
	obj.dvach_visible = vis_class;
	
	var idx;
	var nodelist = obj.parentNode.childNodes;
	
	for (idx = 0; idx < nodelist.length; idx++)
		if (nodelist[idx] == obj) break;
		
	if (idx == nodelist.length) {
		alert("could not find " + obj.nodeName);
		return;
	}

	for (idx++; idx < nodelist.length; idx++) {
		var sub = nodelist[idx];
		
		if (sub.nodeName == "DT")
			break;

		if (sub.nodeName == "DD") 
			sub.className = vis_class;
	}

	set_cookie(current_id, vis_class);
}

window.onload = init_visibility;
