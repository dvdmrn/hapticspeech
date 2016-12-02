// Constructor
function IoHandler(io) {
  // always initialize all instance properties
  this.io = io;
  // this.baz = 'baz'; // default value
}
// class methods
// IoHandler.prototype.test = function() {
// 	console.log("Tested IO as class")
// };

IoHandler.prototype.broadcastAmp = function (a) {
	this.io.emit("amp",a);
	return a;
}

IoHandler.prototype.broadcastPitch = function (f0) {
	this.io.emit("pitch", f0);
	return f0;
}

IoHandler.prototype.broadcastAmpGain = function (amp_gain) {
	this.io.emit("amp_gain", amp_gain);
	return amp_gain;
}

IoHandler.prototype.broadcastPitchGain = function (pitch_gain) {
	this.io.emit("pitch_gain", pitch_gain);
	return pitch_gain;
}

IoHandler.prototype.broadcastMix = function (mix) {
	this.io.emit("mixdown", mix);
	return mix;
}

IoHandler.prototype.broadcastScale = function (scale){
	this.io.emit("scale", scale);
	return scale;
}

IoHandler.prototype.broadcast = function (msg){
	this.io.emit("broadcast", msg);
	return msg;
}



// export the class
module.exports = IoHandler;

