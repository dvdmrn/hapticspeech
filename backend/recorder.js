// Constructor
function Recorder() {
  // always initialize all instance properties
  // this.io = io;
  // this.baz = 'baz'; // default value
}
// class methods
Recorder.prototype.test = function() {
	console.log("Tested IO as class")
};

// export the class
module.exports = Recorder;

