import React from 'react';
var Voodle = require('./voodle.jsx');
require('../css/voodle.css');

function main() {
		React.render(<Voodle />,
		document.getElementById('app'));
}

main();
