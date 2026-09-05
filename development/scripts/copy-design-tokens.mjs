import { copyFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire( import.meta.url );
const scriptDirectory = dirname( fileURLToPath( import.meta.url ) );
const projectRoot = resolve( scriptDirectory, '..' );
const source = require.resolve( '@wordpress/theme/design-tokens.css' );
const destination = resolve( projectRoot, 'fixture/plugin/build/design-tokens.css' );

mkdirSync( dirname( destination ), { recursive: true } );
copyFileSync( source, destination );
console.log( `Copied public WPDS token stylesheet to ${ destination }` );
