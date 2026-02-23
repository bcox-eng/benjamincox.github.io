from playwright.sync_api import sync_playwright
import os
import sys

def verify_partcheck_images():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the local HTML file
        file_path = os.path.abspath("docs/partcheck.html")
        page.goto(f"file://{file_path}")

        # Check if the images are present
        images = page.locator(".detail-images img")
        count = images.count()
        print(f"Found {count} images in .detail-images sections")

        # Verify specific images are loaded
        expected_srcs = [
            "resources/PartCheckProject/24.5mmPart.png",
            "resources/PartCheckProject/25.5mmPart.png",
            "resources/PartCheckProject/25mmPart.png",
            "resources/PartCheckProject/Phone.jpg"
        ]

        found_srcs = []
        for i in range(count):
            src = images.nth(i).get_attribute("src")
            found_srcs.append(src)

        print("Found image sources:", found_srcs)

        # Verify at least the critical new ones are there
        missing = []
        for expected in expected_srcs:
            if expected not in found_srcs:
                missing.append(expected)

        if missing:
            print(f"Missing images: {missing}")
            # Take a full page screenshot for debugging
            page.screenshot(path="verification_partcheck_debug.png", full_page=True)
        else:
            print("All expected images found.")
            # Take a screenshot of the relevant section
            # We target the last detail-images section which contains the 4 images
            page.locator(".detail-images").last.screenshot(path="verification_partcheck_images_fix.png")

        browser.close()

if __name__ == "__main__":
    verify_partcheck_images()
