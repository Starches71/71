const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // HTML content with a gradient and text overlay
  const htmlContent = `
    <html>
      <head>
        <style>
          body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(to bottom right, #FF6347, #4682B4);
            font-family: Arial, sans-serif;
            color: white;
          }
          .text-overlay {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            padding: 20px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
          }
        </style>
      </head>
      <body>
        <div class="text-overlay">
          Samsung phones can now flip into two because they are the best
        </div>
      </body>
    </html>
  `;

  // Set content to the page
  await page.setContent(htmlContent);

  // Take a screenshot of the rendered content
  await page.screenshot({ path: 'output_image.png' });

  await browser.close();
})();
