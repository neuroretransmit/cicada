/*
MP3 Player
Copyright (C) 2008, Florian Plag, www.video-flash.de

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
*/

package org.florianplag {
	
	import flash.display.MovieClip;
	import flash.display.DisplayObject;	
	
	/**
	* The Param class handles the input parameteres from the URL/HTML/SWFObject
	* It also checks the parameters and sets default values 
	*	
	*/
	
	public class Param {
		
		
		/**
		* URL of the audio file
		* 
		* @example /song.mp3
		* @example http://www.video-flash.de/myaudio.mp3
		*
		* @default 
		*/
		private var _audio:String;	
		
		
		/**
		* auto play
		* 
		*/
		private var _autoPlay:Boolean;		


		/**
		* 
		* Constants
		* 
		*
		*/
		private static var DEFAULT_AUTO_PLAY:Boolean = true;
	
					
			/**
			* Constructor; does do anything at the moment
			*
			*/
			public function Param() {
	

			}




			/**
			* This function gets the parameters from HTML/SWFObject/URL. They are saved into variables.
			*
			* @param base	A DisplayObject, where the parameters are; Normally "root"
			*/
			public function setByFlashVars(base:DisplayObject) {

				audio = base.loaderInfo.parameters.audio;					
				//audio = "test.mp3";
				autoPlay = changeParamToBoolean(base.loaderInfo.parameters.autoplay, DEFAULT_AUTO_PLAY);
	
			}




			/**
			* set the filename of the audio file
			* @param  arg      String
			*/
			public function set audio( arg:String ) : void { 
				
				if ((arg != null) && (arg != "")) {
					_audio = arg; 
				}
				else {
					_audio = null;
				}
			}
	
			public function get audio() : String { 
				return _audio; 
			}



			/**
			* set the autoplay parameter (true or false)
			* @param  arg      Boolean
			*/
	
			public function set autoPlay( arg:Boolean ) : void { 
				_autoPlay = arg; 

			}
			

			public function get autoPlay():Boolean { 
				return _autoPlay; 
			}


			
			/**
			* This function converts the incoming String to Boolean
			* @param  arg  String
			* @return true/false
			*/	
	
			private function changeParamToBoolean(arg:String, defaultValue:Boolean):Boolean {
				var myBool:Boolean;
				if ((arg == "true") ||(arg == "false")) {
					
					if (arg == "true") {
						myBool = true;
					}
					
					if (arg == "false") {
						myBool = false;
					}		
				}
				else {
					myBool = defaultValue;
				}		
				
				return myBool;

			}
			
			

	
	} // class



} // package
