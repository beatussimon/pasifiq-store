const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    const url = 'http://127.0.0.1:8000/products/sample-vehicles-product/';

    // Wait a bit to ensure the server is ready
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
        console.log('Navigating to ' + url);
        await page.goto(url, { waitUntil: 'networkidle2' });
        
        // Take Desktop Screenshot
        console.log('Taking Desktop Screenshot...');
        await page.setViewport({ width: 1440, height: 900 });
        await page.screenshot({ path: 'desktop_screenshot.png', fullPage: true });

        // Take Mobile Screenshot
        console.log('Taking Mobile Screenshot...');
        await page.setViewport({ width: 375, height: 667, isMobile: true });
        await page.screenshot({ path: 'mobile_screenshot.png', fullPage: true });

        console.log('Screenshots saved successfully!');
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
})();