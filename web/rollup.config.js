import babel from '@rollup/plugin-babel';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import {uglify} from 'rollup-plugin-uglify';

export default {
  input: 'main.js',
  output: {
    file: 'bundle.js',
    format: 'cjs',
  },
  plugins:
      [
        resolve({
          browser: true,
        }),
        commonjs(),
        babel({
          include: ['**.js', 'node_modules/**'],
          babelHelpers: 'bundled',
          presets: ['@babel/preset-env'],
        }),
        uglify(),
      ],
};
