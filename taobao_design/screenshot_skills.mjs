import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";

(async () => {
  const outputDir = "./taobao_design/output";
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  const htmlPath = path.resolve("./taobao_design/skills_showcase.html");
  const url = "file://" + htmlPath;
  console.log("Loading URL:", url);

  const browser = await chromium.launch({
    args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
  });
  
  const ctx = await browser.newContext({
    viewport: { width: 790, height: 1000 },
    deviceScaleFactor: 1, // Standard resolution to fit canvas bounds
  });

  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(2000); // Wait for fonts and layouts to settle

  console.log("Taking full page screenshot...");
  const outputPath = path.join(outputDir, "taobao_skills_showcase.png");
  await page.screenshot({
    path: outputPath,
    fullPage: true,
  });

  console.log(`Screenshot successfully saved to ${path.resolve(outputPath)}`);
  await browser.close();
})();
