var coreAudio = require("node-core-audio");
var pitchFinder = require('pitchfinder');
var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
var fs = require('fs');
var five = require('johnny-five');
var NodeSynth = require('nodesynth')

// Local requires
var IoHandler = require('./iohandler.js');
var iohandle = new IoHandler(io);

var Recorder = require('./recorder.js');
var recHandler = new Recorder();

// Globals

var parameters = {
	smoothValue: 0.8, 
	gain_for_amp: 0.4,
	gain_for_pitch: 0.6,
	scaleFactor: 3,
	servoMax: 75,
	servoMin: 10,
	motorMinSpeed:50,
	motorMaxSpeed:255,
	frameRate:34,
	framesPerBuffer:128,
	sampleRate:44100,
	reverse:false,
	on:true
}
var startRecTime = new Date();
var startRecTimeString = Date.now() // string like 123214312341234

// David

var led;
var ledCreated = false;
var servoMode = true;
var motorMode = false;
var ledMode = false;

var motor;
var motorCreated = false;

var servoCreated = false;
var servo;


//

var board;


var pitch;
var ampRaw;
var smoothOut = 1;

var detectPitchAMDF;

// var detectPitchDW = new pitchFinder.DynamicWavelet();
var last = new Date() //imposes a framerate with `var now`

var recording = false
var name;

var globalAmp = 400

var ns = new NodeSynth.Synth({bitDepth: 16, sampleRate: 44100});

 
ns.source = new NodeSynth.Oscillator('sin',400);



console.log("\n\n\nNS FREQ",ns.freq)

ns.play();


function getFreq(t){
	// console.log("glob amp at time t", globalAmp*10000, t)
	return globalAmp*10000
}
///////////////////////////////////////////////////////////////////
// Main
function main() {
	//set up server
	server.listen(2000);
	

	app.use(express.static(__dirname + '/js'));

	app.get('/', function (req, res) {
	  res.sendfile(__dirname + '/voodle-index.html');
	});
	console.log("dir name: ",__dirname)

	app.use(express.static(__dirname + '/css'));

	board = new five.Board();

	detectPitchAMDF = new pitchFinder.AMDF({
		sampleRate:40000,
		minFrequency:5,
		maxFrequency:1200
	});

	///////////////////////////////////////////////////////////////
	//start of audio analysis//////////////////////////////////////
	///////////////////////////////////////////////////////////////

	// Create a new audio engine
	var engine = coreAudio.createNewAudioEngine();

		engine.setOptions({
		outputChannels:1,
		inputChannels:1,
		framesPerBuffer:parameters.framesPerBuffer,
		sampleRate:parameters.sampleRate
	});

	engine.addAudioCallback( processAudio );

	//////////listens for updates from frontend/////////////////////////////

	io.on('connection', function (socket) {
		console.log("connected to client!");
	  	socket.on("updateParams", function (data) {

	  		console.log("UpdateParams", data) //remember that this is slightly asynch. with the render loop.
	  		if ('ap_weight' in data){
	  			parameters.gain_for_amp = data.ap_weight;
	  			parameters.gain_for_pitch = 1 - parameters.gain_for_amp;
	  		}
	  		if('scale' in data){
	  			parameters.scaleFactor = data.scale;
	  			console.log("\nnew scale factor: " + parameters.scaleFactor)
	  		}
	  		if('smoothing' in data){
	  			parameters.smoothValue = data.smoothing;
	  			console.log("\nnew smooth factor: "+ parameters.smoothValue)
	  		}
	  		if ('servoMax' in data){
	  			console.log("\nnew max servo range:" + parameters.servoMax)
	  			parameters.servoMax = data.servoMax;
	  		}
			if ('servoMin' in data){
				console.log("\nnew min servo range:" + parameters.servoMin)
				parameters.servoMin = data.servoMin;
			}
			if ('motorMax' in data){
				console.log("\nnew max motor speed: "+ parameters.motorMaxSpeed)
				parameters.motorMaxSpeed = data.motorMax;
			}
			if ('motorMin' in data){
				console.log("\nnew min motor speed: "+ parameters.motorMinSpeed)
				parameters.motorMinSpeed = data.motorMin;
			}
	 
	  });
	  	socket.on("startRec",function(){
	  		startRecording()
	  	})
	  	socket.on("stopRec", function(){
	  		stopRecording()
	  	})
	  	socket.on("reverse", function(){
	  		parameters.reverse = !parameters.reverse
	  	})
	  	socket.on("toggleOn", function(){
	  		parameters.on = !parameters.on
	  	})
	  	socket.on("exportParams", function(){
	  		var time = new Date().getTime();
	  		bigFatParametersList = "";
	  		
	  		for (key in parameters) {
	  			console.log(key);
	  			console.log(parameters[key])

	  			bigFatParametersList = bigFatParametersList+key+": "+parameters[key]+"  \n"
	  		};
            console.log('exporting parameters!');
            fs.writeFile('recordings/'+time+'_parameters_snapshot.txt', bigFatParametersList, function (err) {
                  if (err) return console.log(err);
              })
	  	})
	});

	board.on("ready", function() {

	if (servoMode){
			console.log('servo created!')
			servo = new five.Servo({
		    pin: 10,
		    startAt: 90
		  });

		  servoCreated=true;
		};
	if (motorMode){
		//this uses the adafruit shield (v2).
		var configs = five.Motor.SHIELD_CONFIGS.ADAFRUIT_V2;
	  		motor = new five.Motor(configs.M1);

	  // Inject the `motor` hardware into
	  // the Repl instance's context;
	  // allows direct command line access
		board.repl.inject({
	    motor: motor
	    });
	    motorCreated=true;	
	};
	if (ledMode){
		//constructs an RGB LED
	  led = new five.Led.RGB({
	    pins: {
	      red: 9,
	      green: 10,
	      blue: 11,
	    }
	  });

	  this.repl.inject({
	    led: led
	  });
	  ledCreated =true;
	}

});

}

function handleRecording(buffer){
	if (recording ==  true){
		writeToAudioBufferFile(name, buffer)

	}
}

function writeToAudioBufferFile(name, buffer) {
	var out = ''
	buffer.forEach(function(f){
		out = out +'0,' + f + '\n'
	})
	fs.appendFile("C:\\Users\\David\\Documents\\CuddleBitV2\\recordings\\"+name+"_recording.csv", out, function(err){
		if (err){
			return console.log(err);
		}
	})

}

function startRecording(){
	console.log("start rec. has been called!")
	recording = true;
	startRecTime = new Date()
	startRecTimeString = Date.now() // unix time like 37452342345243
	name = startRecTime.getTime();
}

function stopRecording(){
	recording = false;
	writeParams();
	
}

function writeParams(){
	fs.appendFile("C:\\Users\\David\\Documents\\CuddleBitV2\\recordings\\" + name + "_parameters.json", JSON.stringify(parameters), function(err){
	if (err){
		return console.log(err);
	}
	console.log("wrote params file!")
	})
}

///////////////////////////////////////////////////////////////
//start of audio analysis//////////////////////////////////////
///////////////////////////////////////////////////////////////

// Add an audio processing callback
// This function accepts an input buffer coming from the sound card,
// and returns an ourput buffer to be sent to your speakers.
//
// Note: This function must return an output buffer
//		if you don't want the function to playback to your speakers,
//		return an array of 0 (maybe).



function processAudio( inputBuffer ) {
	var now = new Date()
	handleRecording(inputBuffer[0])

	//vars `now` and `last` ensures it runs at 30fps
	if ((now-last)>parameters.frameRate){	

		ampRaw = Math.abs(Math.max.apply(Math, inputBuffer[0]));

		

		// console.log("raw amp: ",ampRaw)
		ns.source.frequency = 100;
		//start of pitch analysis///////////////////////////////////////////		
		pitch = detectPitchAMDF(inputBuffer[0]);
		if (pitch==null){
			pitch = 0
		}
		else{
			pitch = mapValue(pitch, 0,1000,0,1)
		}
	
		//end of pitch analysis///////////////////////////////////////////
		
		//mixes amplitude and frequency, while scaling it up by scaleFactor.
		var ampPitchMix = (parameters.gain_for_amp * ampRaw + parameters.gain_for_pitch * pitch) * parameters.scaleFactor;
		
		//smooths values
		//Note: smoothValue is a number between 0-1
		smoothOut = parameters.smoothValue * smoothOut + (1 - parameters.smoothValue) * ampPitchMix;
		
		boost = ampRaw*10000;
		ns.source = new NodeSynth.Oscillator('sin',boost);

		//writes values to arduino
		setArduino(smoothOut);

		//resets timer to impose a framerate
		last = now;
		
		//broadcasts values to frontend
		if(parameters.on){
				broadcastValues();
		}
		}

		


		return [[0]];

}



//////////////socket.io emit functions////////////////
function broadcastValues() {
		//applies gain to pitch
		var pitchGain = parameters.gain_for_pitch * pitch
		if (pitchGain > 1.5) {
			pitchGain = 1.5;
		};

		var ampGain = parameters.gain_for_amp * ampRaw
		if (ampGain > 1) {
			ampGain = 1;
		};

		iohandle.broadcast({
				amp:ampGain,
				pitch:pitchGain,
				mix:smoothOut,
				recording:recording,
				startRecTimeString:startRecTimeString, // in unix time like 123123413413
			}
		);
		// iohandle.broadcastPitch(pitchGain);
		// iohandle.broadcastMix(smoothOut);
		// iohandle.broadcastAmpGain(parameters.gain_for_amp)
		// iohandle.broadcastPitchGain(parameters.gain_for_pitch) 
		// iohandle.broadcastScale(parameters.scaleFactor);
		
}


//////////////////////////////////////////////////////////////
//Arduino communication code/////////////////////////////////
////////////////////////////////////////////////////////////

function setArduino(sm) {
	// if (servoCreated){
	// 	if (reverse){
	// 	//maps the audio input to the servo value range, and calculates the difference
	// 	//so that it moves upwards with increased amplitude.
	// 	servo.to(mapValue(sm, 0, 1, parameters.servoMin, parameters.servoMax));
	// 	}
	// 	else {

	// 			servo.to(parameters.servoMax - mapValue(sm, 0, 1, parameters.servoMin, parameters.servoMax));
	// 		}
	// };

	if (servoCreated){
		if (parameters.reverse){
		//maps the audio input to the servo value range, and calculates the difference
		//so that it moves upwards with increased amplitude.
			servo.to(parameters.servoMax - mapValue(sm, 0, 1, parameters.servoMin, parameters.servoMax));
		}
		else {
				servo.to(mapValue(sm, 0, 1, parameters.servoMin, parameters.servoMax));
			}
	};
	if(motorCreated){
		if (parameters.reverse){
			motor.reverse(mapValue(sm, 0, 1, parameters.motorMinSpeed, parameters.motorMaxSpeed));
		}
		else {
			motor.forward(mapValue(sm, 0, 1, parameters.motorMinSpeed, parameters.motorMaxSpeed));
			}
	};
	if(ledCreated){
		n = mapValue(sm, 0, 1, 0, 255)
	    led.color(n,0,n);
  	};
};

function mapValue(value, minIn, maxIn, minOut, maxOut){
	return (value / (maxIn - minIn) )*(maxOut - minOut);
}

///////////////////////////////////////////////////////////////////////////
// RUN MAIN
main()

