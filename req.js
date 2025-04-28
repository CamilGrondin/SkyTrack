const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Navigate to the URL
    const url = 'https://seashells.io/p/ACf9Ekjj';
    await page.goto(url);

    // Extract the content of the page
    const content = await page.evaluate(() => document.body.innerText);
    // Write the content to data.json
    const formattedContent = JSON.stringify({ 
        data: content.split('\n')
                     .filter(line => line.trim() !== '')
                     .map(line => line.slice(1, -1)) 
    }, null, 2);
    
    fs.writeFileSync('data.json', formattedContent);

    await browser.close();
})();