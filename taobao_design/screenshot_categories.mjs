import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";

(async () => {
  const htmlPath = path.resolve("./taobao_design/skills_categories_infographic.html");
  const url = "file://" + htmlPath;
  console.log("Loading URL:", url);

  const browser = await chromium.launch({
    args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
  });
  
  const ctx = await browser.newContext({
    viewport: { width: 790, height: 600 },
    deviceScaleFactor: 2, // Retinal crisp resolution
  });

  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(1000); // Wait for styles to settle

  const outputDir = "./taobao_design/output";
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputPath = path.join(outputDir, "taobao_skills_categories_overview.png");
  console.log("Taking element-bound screenshot of #capture-target...");
  
  const target = await page.$("#capture-target");
  if (target) {
    await target.screenshot({
      path: outputPath,
    });
    console.log("Screenshot successfully saved to", path.resolve(outputPath));
  } else {
    console.error("Could not find #capture-target element!");
  }

  await browser.close();
})();
