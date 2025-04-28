const { Client } = require("@googlemaps/google-maps-services-js");
const fs = require('fs');
const puppeteer = require('puppeteer');

const HEX_ARRAY = JSON.parse(fs.readFileSync('./data.json', 'utf8'));

if (HEX_ARRAY.length < 2) {
    console.error("Not enough messages to decode position.");
    process.exit(1);
}

const bin = hex => BigInt(`0x${hex}`).toString(2).padStart(112, '0');

const ME = bin(HEX_ARRAY[1]);
const ME2 = bin(HEX_ARRAY[0]);

const ME_EVEN = ME.slice(32, 88);
const ME_ODD = ME2.slice(32, 88);

console.log("Even Frame ME:", ME_EVEN);
console.log("Odd Frame ME:", ME_ODD);

const latCprEncEven = parseInt(ME_EVEN.slice(22, 39), 2);
const lonCprEncEven = parseInt(ME_EVEN.slice(39, 56), 2);

const latCprEncOdd = parseInt(ME_ODD.slice(22, 39), 2);
const lonCprEncOdd = parseInt(ME_ODD.slice(39, 56), 2);

console.log("Encoded Latitude (Even):", latCprEncEven);
console.log("Encoded Latitude (Odd):", latCprEncOdd);
console.log("Encoded Longitude (Even):", lonCprEncEven);
console.log("Encoded Longitude (Odd):", lonCprEncOdd);

const latCprEven = latCprEncEven / Math.pow(2, 17);
const lonCprEven = lonCprEncEven / Math.pow(2, 17);

const latCprOdd = latCprEncOdd / Math.pow(2, 17);
const lonCprOdd = lonCprEncOdd / Math.pow(2, 17);

const Nz = 15;
const dLatEven = 90 / (4 * Nz);
const dLatOdd = 90 / (4 * Nz - 1);

const j = Math.floor(59 * latCprEven - 60 * latCprOdd + 0.5);

let latEven = dLatEven * ((j % 60) + latCprEven);
let latOdd = dLatOdd * ((j % 59) + latCprOdd);

if (latEven >= 270) latEven -= 360;
if (latOdd >= 270) latOdd -= 360;

let lat = Math.abs(latOdd);
console.log("Decoded Latitude:", lat.toFixed(6), "N");

function NL(lat) {
    if (lat >= 87 || lat <= -87) return 1;
    return Math.floor(2 * Math.PI / Math.acos(1 - (1 - Math.cos(Math.PI / 30)) / Math.pow(Math.cos(lat * Math.PI / 180), 2)));
}

let m = Math.floor(lonCprEven * (NL(lat) - 1) - lonCprOdd * NL(lat) + 0.5);
let nEven = Math.max(NL(lat), 1);
let nOdd = Math.max(NL(lat) - 1, 1);

let dLonEven = 90 / nEven;
let dLonOdd = 90 / nOdd;

let lonEven = dLonEven * ((m % nEven) + lonCprEven);
let lonOdd = dLonOdd * ((m % nOdd) + lonCprOdd);

let lon = Math.abs(lonOdd);
if (lon >= 180) lon -= 360;
console.log("Decoded Longitude:", lon.toFixed(6), "E");

async function openMapInBrowser(lat, lon) {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    const mapUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`;
    await page.goto(mapUrl);
    console.log("Opened Google Maps at:", mapUrl);
}

openMapInBrowser(lat, lon);