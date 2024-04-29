// Countdown script  v1.1
// documentation: http://www.dithered.com/javascript/countdown/index.html
// license: http://creativecommons.org/licenses/by/1.0/
// code by Chris Nott (chris[at]dithered[dot]com)


function Countdown(name, updateFrequency) {
   this.name = name;
   this.updateFrequency = updateFrequency;
   this.images = null;
   this.endDate = new Date();
   this.format = (document.getElementById && document.getElementById(this.name)) ? document.getElementById(this.name).innerHTML : '';
}

Countdown.prototype.setImages = function(num0, num1, num2, num3, num4, num5, num6, num7, num8, num9) {
   this.images = new Array(num0, num1, num2, num3, num4, num5, num6, num7, num8, num9);
   preloadImages(num0, num1, num2, num3, num4, num5, num6, num7, num8, num9);
};

Countdown.prototype.setEndDate = function(year, month, day, hour, minute, second, milliseconds) {
	this.endDate = new Date(Date.UTC(year, month - 1, day, ( (hour) ? hour : 0), ( (minute) ? minute : 0), ( (second) ? second : 0), ( (milliseconds) ? milliseconds : 0)));
};

Countdown.prototype.start = function() {
   this.update();
   setInterval(this.name + '.update()', (this.updateFrequency ? this.updateFrequency : 1000) );
};

Countdown.prototype.update = function() {
   
   // calculate the time until countdown end date
   var now = new Date();
   var difference = this.endDate - now;
   
   // decompose difference into days, hours, minutes and seconds parts
   var days    = parseInt(difference / 86400000) + '';
   var hours   = parseInt((difference % 86400000) / 3600000) + '';
   var minutes = parseInt((difference % 3600000) / 60000) + '';
   var seconds = parseInt((difference % 60000) / 1000) + '';
   var milliseconds = parseInt(difference % 1000) + '';
   
   // negative values should be set to 0
   if (isNaN(days) || days.charAt(0) == '-') days = '0';
   if (isNaN(hours) || hours.charAt(0) == '-') hours = '0';
   if (isNaN(minutes) || minutes.charAt(0) == '-') minutes = '0';
   if (isNaN(seconds) || seconds.charAt(0) == '-') seconds = '0';
   if (isNaN(milliseconds) || milliseconds.charAt(0) == '-') milliseconds = '0';
   
   // display changes differently for images and text countdowns
   if (this.images != null) {
      
      // single digit values should have a '0' prepended to them
      if (days.length == 1) days = '000' + days;
      else if (days.length == 2) days = '00' + days;
      else if (days.length == 3) days = '0' + days;
      if (hours.length == 1) hours = '0' + hours;
      if (minutes.length == 1) minutes = '0' + minutes;
      if (seconds.length == 1) seconds = '0' + seconds;
      if (milliseconds.length == 1) milliseconds = '00' + milliseconds;
      else if (milliseconds.length == 2) milliseconds = '0' + milliseconds;
      
      // update images
      if (document.images[this.name + '_d1000']) document.images[this.name + '_d1000'].src = this.images[parseInt(days.charAt(0))];
      if (document.images[this.name + '_d100']) document.images[this.name + '_d100'].src = this.images[parseInt(days.charAt(1))];
      if (document.images[this.name + '_d10']) document.images[this.name + '_d10'].src = this.images[parseInt(days.charAt(2))];
      if (document.images[this.name + '_d1']) document.images[this.name + '_d1'].src = this.images[parseInt(days.charAt(3))];
      if (document.images[this.name + '_h10']) document.images[this.name + '_h10'].src = this.images[parseInt(hours.charAt(0))];
      if (document.images[this.name + '_h1']) document.images[this.name + '_h1'].src = this.images[parseInt(hours.charAt(1))];
      if (document.images[this.name + '_m10']) document.images[this.name + '_m10'].src = this.images[parseInt(minutes.charAt(0))];
      if (document.images[this.name + '_m1']) document.images[this.name + '_m1'].src = this.images[parseInt(minutes.charAt(1))];
      if (document.images[this.name + '_s10']) document.images[this.name + '_s10'].src = this.images[parseInt(seconds.charAt(0))];
      if (document.images[this.name + '_s1']) document.images[this.name + '_s1'].src = this.images[parseInt(seconds.charAt(1))];
      if (document.images[this.name + '_ms100']) document.images[this.name + '_ms100'].src = this.images[parseInt(milliseconds.charAt(0))];
      if (document.images[this.name + '_ms10']) document.images[this.name + '_ms10'].src = this.images[parseInt(milliseconds.charAt(1))];
      if (document.images[this.name + '_ms1']) document.images[this.name + '_ms1'].src = this.images[parseInt(milliseconds.charAt(2))];
   }
   else if (this.format != '') {
      if (document.getElementById && document.getElementById(this.name)) {
         var html = this.format;
         html = html.replace(/~d~/, days);
         html = html.replace(/~h~/, hours);
         html = html.replace(/~m~/, minutes);
         html = html.replace(/~s~/, seconds);
         html = html.replace(/~ms~/, milliseconds);
         
         document.getElementById(this.name).innerHTML = html;
      }
   }
};


// Image preloader
function preloadImages() {
	if (document.images) {
		for (var i = 0; i < preloadImages.arguments.length; i++) {
			(new Image()).src = preloadImages.arguments[i];
		}
	}
}

