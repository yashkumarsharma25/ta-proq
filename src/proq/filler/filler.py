import os
import json
from playwright.async_api import async_playwright

class Filler:
    async def init(self, headless=False, login_id=None, profile_directory=None, user_data_dir=None):
        self.playwright = await async_playwright().start()
        self.browser = self.playwright.chromium
    
        if not user_data_dir:
            if os.name == "posix":  # linux
                user_data_dir = f"/home/{os.getlogin()}/.config/google-chrome/"
                name_key = "gaia_given_name"
            elif os.name == "nt":  # windows
                user_data_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
                name_key = "shortcut_name"

        if not profile_directory:
            with open(os.path.join(user_data_dir, "Local State")) as f:
                content = json.load(f)
            profiles = [
                {
                    "profile": profile_name,
                    "name": (data[name_key]).split("(")[0].strip(),
                    "email": data["user_name"],
                }
                for profile_name, data in content["profile"]["info_cache"].items()
            ]

            if not login_id:
                for i, profile in enumerate(profiles):
                    print(f"{i+1}. {profile['name']}({profile['email']})")

                profile_directory = profiles[int(input("Select a Profile: ")) - 1][
                    "profile"
                ]
            else:
                for profile in profiles:
                    if profile["email"] == login_id:
                        profile_directory = profile["profile"]
                        print(f"The profile with the given email is {profile['profile']}")
                        break

        self.context = await self.browser.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=headless,
            args=[
                f"--profile-directory={profile_directory}",
                "--start-maximized",
                "--disable-web-security"
            ],
            no_viewport=True,
        )
        self.page = self.context.pages[0]

