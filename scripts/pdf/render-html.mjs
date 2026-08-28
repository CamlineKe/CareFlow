#!/usr/bin/env node
import { chromium } from 'playwright';
import path from 'path';
import { pathToFileURL } from 'url';

const [inputArg, outputArg] = process.argv.slice(2);

if (!inputArg || !outputArg) {
  console.error('Usage: render-html.mjs INPUT.html OUTPUT.pdf');
  process.exit(1);
}

const htmlPath = path.resolve(inputArg);
const outPath = path.resolve(outputArg);

const browser = await chromium.launch();
try {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' },
  });
} finally {
  await browser.close();
}

console.log('Wrote', outPath);
