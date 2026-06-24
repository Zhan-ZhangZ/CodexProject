import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";

(async () => {
  const browser = await chromium.launch({
    args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
  });

  const taobaoDir = "./taobao_design";
  const outputDir = "./taobao_design/output";
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 1. Render the 5 main images (800x800, scale 2 for high-res 1600x1600)
  for (let i = 1; i <= 5; i++) {
    const htmlPath = path.resolve(taobaoDir, `image${i}.html`);
    const url = "file://" + htmlPath;
    console.log(`Rendering image${i}.html -> taobao_image${i}.png...`);

    const ctx = await browser.newContext({
      viewport: { width: 800, height: 800 },
      deviceScaleFactor: 2,
    });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(1000);

    const outputPath = path.resolve(outputDir, `taobao_image${i}.png`);
    await page.screenshot({ path: outputPath });
    console.log(`Saved: ${outputPath}`);
    await ctx.close();
  }

  // 2. Render instructions_long.html (790px, scale 2, fullPage)
  {
    const htmlPath = path.resolve(taobaoDir, "instructions_long.html");
    const url = "file://" + htmlPath;
    console.log("Rendering instructions_long.html -> taobao_instructions_long.png...");

    const ctx = await browser.newContext({
      viewport: { width: 790, height: 1000 },
      deviceScaleFactor: 2,
    });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(1000);

    const outputPath = path.resolve(outputDir, "taobao_instructions_long.png");
    await page.screenshot({ path: outputPath, fullPage: true });
    console.log(`Saved: ${outputPath}`);
    await ctx.close();
  }

  // 3. Render skills_showcase.html (790px, scale 1, fullPage)
  {
    const htmlPath = path.resolve(taobaoDir, "skills_showcase.html");
    const url = "file://" + htmlPath;
    console.log("Rendering skills_showcase.html -> taobao_skills_showcase.png...");

    const ctx = await browser.newContext({
      viewport: { width: 790, height: 1000 },
      deviceScaleFactor: 1,
    });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(1000);

    const outputPath = path.resolve(outputDir, "taobao_skills_showcase.png");
    await page.screenshot({ path: outputPath, fullPage: true });
    console.log(`Saved: ${outputPath}`);
    await ctx.close();
  }

  await browser.close();
  console.log("All primary assets rendered successfully!");
})();
