import React from 'react';
var Slider = require("./slider.jsx")
var reverse = false;
var on = true;
var Settings = React.createClass({
	onChildChange: function(keyname){
		this.props.emit("updateParams", keyname);
		this.setState(keyname)
	},
	getInitialState: function(){

		return { 
			smoothing:0.8,
			amp:0.0,
			pitch:0.0,
			scale:3.0,
			servoMax:85,
			servoMin:20,
			ap_weight:0.0,
			motorMax: 255,
			motorMin: 50,
			socket:this.props.socket,
			maxRecLength: 3000
		}

	},
	startRecording: function(){
		console.log("startRecording in jsx called!")
		if (this.props.recording == false){
			console.log("in if")
			this.props.emit("startRec")
		}
	},
		
	recordingStatus: function(){
		if(this.props.recording){
			return "recording!" + (new Date() - this.props.startRecTime)
		}
		else{
			return ""
		}
	},
	stopRecording: function(){
		console.log('stop rec called')
		if (this.props.recording){
			console.log('in first if!')

			
			this.props.emit("stopRec")
			console.log("stop rec emit called!")
		}
		else{	
				console.log('stop rec else clause')
				
				}
		
	},
	reverse: function(){
			this.props.emit("reverse")
			console.log("reverse called!")

	},

	toggleOn: function(){
		this.props.emit("toggleOn")
		console.log("turning Voodle on/off!")
	},

	onItemClick: function (event) {
		if (!reverse){
    		event.currentTarget.style.backgroundColor = '#AC0';
    		reverse = true
    		this.reverse()
		}
		else if (reverse){
			event.currentTarget.style.backgroundColor = '#aaa';
			reverse = false
			this.reverse()
		}

	},

	toggleOnOff: function (event) {
		if (!on){
    		event.currentTarget.style.backgroundColor = '#AC0';
    		on = true
    		this.toggleOn()
		}
		else if (on){
			event.currentTarget.style.backgroundColor = '#aaa';
			on = false
			this.toggleOn()
		}

	},

	exportParams: function(event){
		this.props.emit("exportParams")
	},

	render: function(){
		var timeBar;
		var countdown = "0";
		var timeBarFill = "#FF9090"
		if (this.props.recording){
			// console.log("rec state",this.state.recording)
			countdown = new Date()-this.props.startRecTime
			timeBarFill = "#FF3830";
			if (countdown > this.state.maxRecLength){

				countdown=0
				this.props.emit("stopRec")
				console.log('countdown val: ',countdown)
				console.log('is anyone out there?')
				// console.log("in countdown IF")
				// this.stopRecording();
			};
		}
		else if (!this.props.recording){
			timeBarFill="#FF9090"
		}	
		else if (this.props.reverse){
			buttonFill="#FF9090"
		}
		
		return (
			<div>
			<div id ="leftPanel">
				<div id = "edit">
				<span id="title">Settings</span>
				<p />
					<button type="button" id="powerButton" onClick={this.someFun} onClick={this.toggleOnOff}><b>on/off</b></button>

					<button type="button" id="button" onClick={this.reverse} onClick={this.onItemClick}><b>Reverse</b></button>
					
					
				< p />
					{stringifyFloat(this.state.ap_weight)} <b>pitch bias</b> 
					<Slider inputValue={0.5}
							minValue={0}
							maxValue={1}
							name="ap_weight"
							stepValue={0.05}
							callback={this.onChildChange}/>
					<b> amp bias </b>{stringifyFloat(1.0-this.state.ap_weight)}

					<p />
					<b>output gain: </b>{this.state.scale} 
					<Slider inputValue={this.state.scale}
							minValue={0}
							maxValue={6}
							name="scale"
							stepValue={1} 
							callback={this.onChildChange}/>
					<p />
					<b>Smoothing:</b>{stringifyFloat(this.state.smoothing)} 
					<Slider inputValue={this.state.smoothing}
							minValue={0}
							maxValue={1}
							name="smoothing"
							stepValue={0.05}
							callback={this.onChildChange} />
					<p />
					
				</div>
				<p />
				<div id="edit">
					<span id='title'>Save to MacaronBit</span><p />
					<button type="button" id="button" onClick={this.startRecording}><b>Record</b></button>  
					<button type="button" id="button" onClick={this.stopRecording}><b>Stop</b></button>
					<br />

					{this.recordingStatus()}<br />
					
					<svg id = "recordingBar" height="20" >
						<rect id = "recordingbg" width="3000" height="20" />
						<rect width={(3000-countdown)/10} height="20" fill={timeBarFill} />
					</svg>
					<p />
					<button type ="button" id="button" onClick={this.exportParams}><b>export parameters</b></button>
				</div>
			</div>
			<div id="rightPanel">
				<p />
				<div id="edit">
					<span id='title'>Servo settings</span><p />
					<b>Max servo range: {this.state.servoMax}°</b>
					<Slider inputValue={this.state.servoMax}
							minValue={0}
							maxValue={360}
							name="servoMax"
							stepValue={1} 
							callback={this.onChildChange} />
					<p />
					<b>Min. servo range: {this.state.servoMin}°</b>
					<Slider inputValue={this.state.servoMin}
							minValue={0}
							maxValue={360}
							name="servoMin"
							stepValue={1}
							callback={this.onChildChange} />
				</div>
				<p />
				<div id="edit">
					<span id='title'>Motor settings</span><p />
					<b>Min. motor speed: {this.state.motorMin}</b> 
					<Slider inputValue={this.state.motorMin}
							minValue={0}
							maxValue={255}
							name="motorMin"
							stepValue={1}
							callback={this.onChildChange} />
					<p />
					<b>Max motor speed: {this.state.motorMax}</b> 
					<Slider inputValue={this.state.motorMax}
							minValue={0}
							maxValue={255}
							name="motorMax"
							stepValue={1}
							callback={this.onChildChange} />
				</div>
			</div>
			</div>
			)
	}
})


function stringifyFloat(n){
	if (n==0){
		return "0.00"
	}
	else if (n==1){
		return"1.00"
	}
	else if (n.toString().length < 4){
			return n.toString()+"0"
		}
	else {
		return n.toString().substring(0,4)
	}
}

module.exports = Settings;