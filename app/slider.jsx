import React from 'react';

var Slider = React.createClass({
	getInitialState: function() {
	  return {value: this.props.inputValue};
	},
	handleChange: function(event) {
	  this.setState({value: event.target.value});
	  var keyname = {}
	  keyname[this.props.name] = event.target.value
	  this.props.callback(keyname);
	},
	render: function() {
	  return (

	    <input 
	      className="slider"
	      type="range" 
	      min={this.props.minValue} 
	      max={this.props.maxValue} 
	      value={this.state.value} 
	      onChange={this.handleChange}
	      step={this.props.stepValue}/>

	  );}
})

module.exports = Slider;
