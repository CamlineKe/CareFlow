#!/usr/bin/env node
import { chromium } from 'playwright';
import path from 'path';
import { pathToFileURL } from 'url';

const args = process.argv.slice(2);
const positional = [];
let landscape = false;

for (const arg of args) {
  if (arg === '--landscape') {
    landscape = true;
  } else {
    positional.push(arg);
  }
}

const [inputArg, outputArg] = positional;

if (!inputArg || !outputArg) {
  console.error('Usage: render-svg.mjs INPUT.svg OUTPUT.pdf [--landscape]');
  process.exit(1);
}

const svgPath = path.resolve(inputArg);
const outPath = path.resolve(outputArg);
const margin = landscape ? '10mm' : '15mm';

const browser = await chromium.launch();
try {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(pathToFileURL(svgPath).href, { waitUntil: 'load' });
  await page.pdf({
    path: outPath,
    format: 'A4',
    landscape,
    printBackground: true,
    margin: { top: margin, bottom: margin, left: margin, right: margin },
  });
} finally {
  await browser.close();
}

console.log('Wrote', outPath);
