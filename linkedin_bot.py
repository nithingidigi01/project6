from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random


LINKEDIN_LOGIN = "https://www.linkedin.com/login"
LINKEDIN_FEED = "https://www.linkedin.com/feed/"


# ============================================================
# HUMAN-LIKE HELPERS
# ============================================================

def human_delay(a=0.3, b=1.2):
    time.sleep(random.uniform(a, b))


def human_type(page, text):
    for char in text:
        page.keyboard.type(char)
        time.sleep(random.uniform(0.02, 0.05))


# ============================================================
# LOGIN VALIDATION
# ============================================================

def validate_login(interactive=False, state_file=None):

    state_path = Path(state_file)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=not interactive,
            channel="chrome",
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        # =========================
        # INTERACTIVE LOGIN
        # =========================
        if interactive:

            context = browser.new_context(viewport=None)
            page = context.new_page()

            page.goto(LINKEDIN_LOGIN, wait_until="domcontentloaded", timeout=60000)

            print("Waiting for manual LinkedIn login...")

            try:
                # 🔥 EVENT-BASED WAIT (NO LOOP)
                page.wait_for_url("**/feed/**", timeout=300000)

                # small stabilization for cookies/localStorage
                time.sleep(2)

                context.storage_state(path=str(state_path))
                print("✅ Login state saved")

                browser.close()
                return True

            except Exception:
                print("❌ Login timeout")
                browser.close()
                return False

        # =========================
        # SESSION VALIDATION
        # =========================
        else:

            if not state_path.exists():
                browser.close()
                return False

            context = browser.new_context(
                storage_state=str(state_path),
                viewport=None
            )

            page = context.new_page()

            try:
                page.goto(LINKEDIN_FEED, wait_until="domcontentloaded", timeout=60000)

                # If redirected to login -> expired
                if any(x in page.url.lower() for x in ["login", "checkpoint"]):
                    browser.close()
                    return False

                # Light selector check only
                page.wait_for_selector(
                    'nav[aria-label="Primary Navigation"]',
                    timeout=8000
                )

                browser.close()
                return True

            except Exception:
                browser.close()
                return False


# ============================================================
# POSTING
# ============================================================

def post_to_linkedin(content, state_file):

    state_path = Path(state_file)

    if not state_path.exists():
        print("❌ storage_state missing")
        return False

    success = False

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            storage_state=str(state_path),
            viewport=None
        )

        page = context.new_page()

        try:

            print("Opening LinkedIn composer...")

            page.goto(
                "https://www.linkedin.com/feed/?shareActive=true",
                wait_until="domcontentloaded",
                timeout=60000
            )

            human_delay(2, 3)

            if any(x in page.url.lower() for x in ["login", "checkpoint"]):
                print("❌ Session expired")
                browser.close()
                return False

            page.wait_for_selector("div[role='textbox']", timeout=15000)

            editor = page.locator("div[role='textbox']").first

            if editor.count() == 0:
                print("❌ Editor not found")
                browser.close()
                return False

            editor.click()
            human_delay(1, 2)

            print("Typing content...")
            human_type(page, content)

            human_delay(2, 3)

            # Click Post
            page.evaluate("""
                () => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const postBtn = btns.find(b =>
                        b.innerText && b.innerText.trim() === 'Post'
                    );
                    if (postBtn) postBtn.click();
                }
            """)

            human_delay(2, 3)

            # Handle settings popup
            settings = page.locator("div[role='dialog']")
            if settings.count() > 0:

                page.evaluate("""
                    () => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const doneBtn = btns.find(b =>
                            b.innerText && b.innerText.trim() === 'Done'
                        );
                        if (doneBtn) doneBtn.click();
                    }
                """)

                human_delay(1, 2)

                page.evaluate("""
                    () => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const postBtn = btns.find(b =>
                            b.innerText && b.innerText.trim() === 'Post'
                        );
                        if (postBtn) postBtn.click();
                    }
                """)

            # Wait for confirmation
            start = time.time()

            while time.time() - start < 60:

                if page.locator("text=Your post is now live").count() > 0:
                    success = True
                    break

                if page.locator("div[role='textbox']").count() == 0:
                    success = True
                    break

                time.sleep(1)

            if success:
                print("✅ Post successful")
                context.storage_state(path=str(state_path))
            else:
                print("❌ Post confirmation not detected")

        except Exception as e:
            print("❌ Post error:", e)

        finally:
            browser.close()

    return success