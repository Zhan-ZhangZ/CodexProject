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
    deviceScaleFactor: 2, // 2x high resolution (1580px wide)
  });

  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(2000); // Wait for rendering to settle

  // Get element coordinates dynamically
  const layout = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll(".step-card"));
    const advantages = document.querySelector(".advantages-section");
    const warning = document.querySelector(".warning-box");

    const getBox = (el) => {
      const rect = el.getBoundingClientRect();
      return {
        top: window.scrollY + rect.top,
        bottom: window.scrollY + rect.bottom,
        height: rect.height
      };
    };

    return {
      card1Top: getBox(cards[0]).top,
      card2Bot: getBox(cards[1]).bottom,
      card3Top: getBox(cards[2]).top,
      card5Bot: getBox(cards[4]).bottom,
      card6Top: getBox(cards[5]).top,
      card8Bot: getBox(cards[7]).bottom,
      card9Top: getBox(cards[8]).top,
      advBot: getBox(advantages).bottom,
      warnTop: getBox(warning).top,
      totalHeight: document.documentElement.scrollHeight
    };
  });

  console.log("Layout coordinates:", layout);

  // Resize viewport to total height to ensure the clipped areas are inside the viewport
  await page.setViewportSize({ width: 790, height: layout.totalHeight });
  await page.waitForTimeout(500);

  // Slices definitions: we pad slightly to avoid edge clipping
  const slices = [
    { name: "part1_header", startY: 0, endY: Math.round(layout.card2Bot + 10) },
    { name: "part2_skills", startY: Math.round(layout.card3Top - 15), endY: Math.round(layout.card5Bot + 10) },
    { name: "part3_skills", startY: Math.round(layout.card6Top - 15), endY: Math.round(layout.card8Bot + 10) },
    { name: "part4_skills", startY: Math.round(layout.card9Top - 15), endY: Math.round(layout.advBot + 15) },
    { name: "part5_footer", startY: Math.round(layout.warnTop - 15), endY: Math.round(layout.totalHeight) }
  ];

  for (let i = 0; i < slices.length; i++) {
    const slice = slices[i];
    const clipHeight = slice.endY - slice.startY;
    console.log(`Capturing ${slice.name}: y=[${slice.startY} to ${slice.endY}], height=${clipHeight}`);
    
    await page.screenshot({
      path: path.join(outputDir, `taobao_skills_showcase_${slice.name}.png`),
      clip: {
        x: 0,
        y: slice.startY,
        width: 790,
        height: clipHeight
      }
    });
  }

  console.log("All 5 slices captured successfully at 2x resolution!");
  await browser.close();
})();
