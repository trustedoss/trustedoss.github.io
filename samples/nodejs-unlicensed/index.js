/**
 * Sample app that demonstrates the risk of a package with no declared license.
 *
 * A minimal hello world example using express (MIT), lodash (MIT), and
 * legacy-parser (no declared license).
 */

const express = require('express');
const _ = require('lodash');
const {parseGreeting} = require('legacy-parser');

const app = express();
const PORT = 3000;

// A small utility built on lodash (MIT)
const greetings = ['Hello', 'World', 'OpenChain', 'SBOM'];
const shuffled = _.shuffle(greetings);

app.get('/', (req, res) => {
  res.json({
    message: 'Hello, World!',
    greeting: parseGreeting(shuffled[0]),
    warning: 'This app includes a package with no declared license.',
    packages: {
      express: 'MIT, clear',
      lodash: 'MIT, clear',
      'legacy-parser': 'no declared license, no clear right to use it',
    },
  });
});

app.listen(PORT, () => {
  console.log(`Server started: http://localhost:${PORT}`);
  console.log('Warning: the legacy-parser package declares no license.');
  console.log(
    'No declared license means all rights reserved by default, so you may not use it.'
  );
});
