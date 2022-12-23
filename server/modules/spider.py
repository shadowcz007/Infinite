from playwright.sync_api import Playwright, sync_playwright, expect
browserLaunchOptionDict = {
    "headless": False,
    # "proxy": {
    #     "server": PROXY_HTTP,
    # }
}
import utils
import os
import requests

items=[
    {
        "title": "AI Code Reviewer",
        "url": "https://futuretools.link/code-reviewer",
        "description": "Automatic code review by AI",
        "tag": "Generative Code",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150550ebce31a75252ac_OGP-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150550ebce31a75252ac_OGP.png"
    },
    {
        "title": "AI Data Sidekick",
        "url": "https://futuretools.link/sidekick",
        "description": "Write SQL, documentation and more with powerful AI recipes",
        "tag": "Generative Code",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21505945e5ee2014837c2_639793ad11defcc773d9980a_screenshot-airops-sidekick-%25231-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21505945e5ee2014837c2_639793ad11defcc773d9980a_screenshot-airops-sidekick-%25231.png"
    },
    {
        "title": "AI Image Enlarger",
        "url": "https://futuretools.link/ai-image-enlarger",
        "description": "Use AI to upscale small or pixelated images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31be501f8106cc0daff_639a92681680c460c3f8a187_Screenshot%2520(22)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31be501f8106cc0daff_639a92681680c460c3f8a187_Screenshot%2520(22).png"
    },
    {
        "title": "AI Image Upscaler",
        "url": "https://futuretools.link/ai-image-upscaler",
        "description": "Use AI to upscale small or pixelated images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31b0a971f62c26f091e_639a9294ad32142bf1c9ebf9_Screenshot%2520(24)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31b0a971f62c26f091e_639a9294ad32142bf1c9ebf9_Screenshot%2520(24).png"
    },
    {
        "title": "AI Library",
        "url": "https://futuretools.link/ai-library",
        "description": "Catalog of 400+ neural networks and tools for art and CG",
        "tag": "Aggregators",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23df80d1f2c68c8e9ff37_d3cf5168-9057-4528-b9d9-4cc5cae66f96-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23df80d1f2c68c8e9ff37_d3cf5168-9057-4528-b9d9-4cc5cae66f96.jpeg"
    },
    {
        "title": "AI Time Machine",
        "url": "https://futuretools.link/ai-time-machine",
        "description": "Create historic looking AI avatars and profile pics",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece51585124b6b4ac8b_timemachine_6-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece51585124b6b4ac8b_timemachine_6.jpeg"
    },
    {
        "title": "AdCreative.ai",
        "url": "https://futuretools.link/adcreative",
        "description": "AI powered ad creative and banner generator",
        "tag": "Marketing,Copywriting,Social Media",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc03268ba6961_630601ea4dc69407d51c916f_MetaImg-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc03268ba6961_630601ea4dc69407d51c916f_MetaImg.jpeg"
    },
    {
        "title": "Adobe Speech Enhancer",
        "url": "https://futuretools.link/speech-enhancer",
        "description": "Use AI to remove background noise and clean up audio",
        "tag": "Voice Modulation",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c29fbc3164ef3bcef4_enhancespeech-thumbnail-small%401x.9787c296594f24c0afc0.png",
        "imgurl_large": ""
    },
    {
        "title": "Adstra",
        "url": "https://futuretools.link/limitless",
        "description": "Find and read only the articles that will solve your problems",
        "tag": "Productivity,Research",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b53176a0b0bdf787b4e_63a217f5d56afc559d0f3361_Screenshot%2520(46)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b53176a0b0bdf787b4e_63a217f5d56afc559d0f3361_Screenshot%2520(46).png"
    },
    {
        "title": "Apeture (by Lexica)",
        "url": "https://futuretools.link/apeture",
        "description": "Generate AI art that looks like real photos",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba095df237f3b621ce3_lexica-meta-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba095df237f3b621ce3_lexica-meta.png"
    },
    {
        "title": "Automatic 1111",
        "url": "https://futuretools.link/automatic-1111",
        "description": "Web-based Dreambooth Google Colab",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31ba9624303044a727c_63996e8028a4d13366cc0117_colab_favicon_256px.png",
        "imgurl_large": ""
    },
    {
        "title": "Avatar AI",
        "url": "https://futuretools.link/avatar-ai",
        "description": "Create AI avatars and profile pictures",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece7a191c1acec02506_social-media-pic-2022-12-13-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece7a191c1acec02506_social-media-pic-2022-12-13.jpeg"
    },
    {
        "title": "Awesome ChatGPT prompts",
        "url": "https://futuretools.link/awesome-chatgpt-prompts",
        "description": "This repo includes ChatGPT promt curation to use ChatGPT better",
        "tag": "Chat,Inspiration",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215068a9a094c4ce8779a_awesome-chatgpt-prompts-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215068a9a094c4ce8779a_awesome-chatgpt-prompts.png"
    },
    {
        "title": "BearlyAI",
        "url": "https://futuretools.link/bearly-ai",
        "description": "AI writing assistant that leverages GPT-3",
        "tag": "Research,Copywriting",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111921b0e90aba8c3d919_twitter-card-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111921b0e90aba8c3d919_twitter-card.png"
    },
    {
        "title": "Character.AI",
        "url": "https://futuretools.link/character-ai",
        "description": "Have chat conversations with AI characters",
        "tag": "Chat,For Fun",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec738e93f0f4cd39bc8_639bca34ba62963dd710cc16_Character%2520AI-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec738e93f0f4cd39bc8_639bca34ba62963dd710cc16_Character%2520AI.jpeg"
    },
    {
        "title": "ChatGPT (OpenAI)",
        "url": "https://futuretools.link/chatgpt",
        "description": "Ask any question or prompt to AI - The tool most other writing tools are based on",
        "tag": "Chat,Copywriting,Generative Code",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c3ba62961a34105d77_ChatGPT-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c3ba62961a34105d77_ChatGPT.jpeg"
    },
    {
        "title": "Clip Interrogator",
        "url": "https://futuretools.link/clip-interrogator",
        "description": "Plug-in an image and it will attempt to give you a prompt to replicate that image",
        "tag": "Generative Art,Image Scanning",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31ba9624303044a727c_63996e8028a4d13366cc0117_colab_favicon_256px.png",
        "imgurl_large": ""
    },
    {
        "title": "ClipDrop",
        "url": "https://futuretools.link/clipdrop",
        "description": "Upscale images, remove backgrounds, remove unwanted elements from images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31bab43ca50f32593f8_639a92ed3df148b5a6af0a2e_Screenshot%2520(27)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31bab43ca50f32593f8_639a92ed3df148b5a6af0a2e_Screenshot%2520(27).png"
    },
    {
        "title": "Cloudinary",
        "url": "https://futuretools.link/cloudinary",
        "description": "APIs to develop AI Art Software",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c6ca245d55dcf6bc9_Cld_SocShare_Card_FB_2020-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c6ca245d55dcf6bc9_Cld_SocShare_Card_FB_2020.jpeg"
    },
    {
        "title": "ContentEdge",
        "url": "https://futuretools.link/contentedge",
        "description": "AI tool for writing SEO optimized content",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bf23d8b245a996af5_ai-content-writer-seo-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bf23d8b245a996af5_ai-content-writer-seo.png"
    },
    {
        "title": "Cool Gift Ideas",
        "url": "https://futuretools.link/coolgiftideas",
        "description": "AI Generated Gift Ideas",
        "tag": "For Fun,Inspiration",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5541bfdb452136c04d_63a2162cc12e99d847dbe5e0_Screenshot%2520(50)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5541bfdb452136c04d_63a2162cc12e99d847dbe5e0_Screenshot%2520(50).png"
    },
    {
        "title": "Copy.AI",
        "url": "https://futuretools.link/copy-ai",
        "description": "AI tool for writing marketing sales copy and blog content",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b9011da4b298c8603_629a702fc90e970b2626cd52_fb-og-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b9011da4b298c8603_629a702fc90e970b2626cd52_fb-og.jpeg"
    },
    {
        "title": "Coqui",
        "url": "https://futuretools.link/coqui",
        "description": "Generative AI Voices",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a223cecca9b01c12c_og-image-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a223cecca9b01c12c_og-image.png"
    },
    {
        "title": "Craiyon",
        "url": "https://futuretools.link/craiyon",
        "description": "Simple free AI art generator",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc0f416ba698a_craiyon_preview-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc0f416ba698a_craiyon_preview.png"
    },
    {
        "title": "Cutout Pro",
        "url": "https://futuretools.link/cutout-pro",
        "description": "Use AI to remove the background from an image",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba11b1ad881f5682b41_home-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba11b1ad881f5682b41_home.jpeg"
    },
    {
        "title": "D-ID Creative Reality",
        "url": "https://futuretools.link/d-id",
        "description": "Create videos from plain text in minutes",
        "tag": "Generative Video,Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215050df9a5117e52a607_Screenshot-2022-09-18-112522-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215050df9a5117e52a607_Screenshot-2022-09-18-112522.png"
    },
    {
        "title": "DALL-E (OpenAI)",
        "url": "https://futuretools.link/dall-e-openai",
        "description": "The Original AI Image Generator",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba2e1266ceada1e2787_dall-e-2-og-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba2e1266ceada1e2787_dall-e-2-og.jpeg"
    },
    {
        "title": "DDMM",
        "url": "https://futuretools.link/ddmm-ai",
        "description": "Literally search any image on the internet",
        "tag": "Research,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150554d1eb6a5d2734fa_logo-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150554d1eb6a5d2734fa_logo.png"
    },
    {
        "title": "Deciphr AI",
        "url": "https://futuretools.link/deciphr",
        "description": "Deciphr timestamps and summarizes your entire podcast transcript for you",
        "tag": "Speech-To-Text,Podcasting",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3bb1104383d5ee49360a8_Screenshot%20(57)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3bb1104383d5ee49360a8_Screenshot%20(57).png"
    },
    {
        "title": "Descript",
        "url": "https://futuretools.link/descript",
        "description": "Train your own voice and use it for text-to-speech",
        "tag": "Text-To-Speech,Speech-To-Text",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639fa807de9394eb823c02db_63769fa40123c0578ff42ca2_DescriptHero%2520(1)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639fa807de9394eb823c02db_63769fa40123c0578ff42ca2_DescriptHero%2520(1).png"
    },
    {
        "title": "DiffusionBee",
        "url": "https://futuretools.link/diffusionbee",
        "description": "Stable Diffusion user-interface for Mac users",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba1e08e87e67e710536_diffusionbee_banner-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba1e08e87e67e710536_diffusionbee_banner.jpeg"
    },
    {
        "title": "Dream Studio",
        "url": "https://futuretools.link/dream-studio",
        "description": "Web-based Stable Diffusion Interface",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b5e15e75a9d4d55c8e393_639acb289130cb3a027eceb2_Screenshot%2520(31)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b5e15e75a9d4d55c8e393_639acb289130cb3a027eceb2_Screenshot%2520(31).png"
    },
    {
        "title": "DreamBooth",
        "url": "https://futuretools.link/dreambooth",
        "description": "Train your own face into Stable Diffusion",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31ba9624303044a727c_63996e8028a4d13366cc0117_colab_favicon_256px.png",
        "imgurl_large": ""
    },
    {
        "title": "EbSynth",
        "url": "https://futuretools.link/ebsynth",
        "description": "Combine a reference video and reference image to make unique animations",
        "tag": "Generative Video,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940dd9aa26f45b8d97f3_ebsynth-image-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940dd9aa26f45b8d97f3_ebsynth-image.jpeg"
    },
    {
        "title": "Elephas",
        "url": "https://futuretools.link/elephas",
        "description": "AI writing assistant for Apple products",
        "tag": "Copywriting",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11192a97b934a92c1f46a_brand-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11192a97b934a92c1f46a_brand.png"
    },
    {
        "title": "Excel Formula Bot",
        "url": "https://futuretools.link/excel-formula-bot",
        "description": "Use normal language to create complex Excel formulas",
        "tag": "Generative Code,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c5ba1add9ff8c1abc_https%253A%252F%252Fs3.amazonaws.com%252Fappforest_uf%252Ff1665622638602x985604001714210400%252FScreen%252520Shot%2525202022-10-12%252520at%2525208.57.04%252520PM-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c5ba1add9ff8c1abc_https%253A%252F%252Fs3.amazonaws.com%252Fappforest_uf%252Ff1665622638602x985604001714210400%252FScreen%252520Shot%2525202022-10-12%252520at%2525208.57.04%252520PM.jpeg"
    },
    {
        "title": "Explainpaper",
        "url": "https://futuretools.link/explainpaper",
        "description": "Upload a paper, highlight confusing text, get an explanation.",
        "tag": "Research,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2135453755657e945f8a3_63a114b3ae022514d5de69ef_Screenshot%2520(45)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2135453755657e945f8a3_63a114b3ae022514d5de69ef_Screenshot%2520(45).png"
    },
    {
        "title": "Futurepedia",
        "url": "https://futuretools.link/futurepedia",
        "description": "Futurepedia is the largest AI tools directory",
        "tag": "Aggregators",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5d212e7e8a0593ff3f_ZG1wAgN-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5d212e7e8a0593ff3f_ZG1wAgN.jpeg"
    },
    {
        "title": "GPT-3 Demo",
        "url": "https://futuretools.link/gpt3demo",
        "description": "Discover how companies are implementing the OpenAI GPT-3 API to power new use cases",
        "tag": "Aggregators",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5d458cd65216403e80_tydpjcahbncuqfqwepxe.png",
        "imgurl_large": ""
    },
    {
        "title": "Generated Photos",
        "url": "https://futuretools.link/generated-photos",
        "description": "Quickly create a randomly generated human face",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0a95e0e655ea2140a_generated-photo-og-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0a95e0e655ea2140a_generated-photo-og.png"
    },
    {
        "title": "Gift Genie AI",
        "url": "https://futuretools.link/giftgenie",
        "description": "Free Personalized Gift Ideas for Christmas, Birthdays, Holidays, etc",
        "tag": "For Fun,Inspiration",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215060df9a5499752a613_gift-genie-logo%403x-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215060df9a5499752a613_gift-genie-logo%403x.png"
    },
    {
        "title": "Gigapixel AI Upscaler",
        "url": "https://futuretools.link/gigapixel",
        "description": "Use AI to upscale small or pixelated images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b5e15c7e7cc161902215c_639acb3b16d4d922a00fe124_Screenshot%2520(30)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b5e15c7e7cc161902215c_639acb3b16d4d922a00fe124_Screenshot%2520(30).png"
    },
    {
        "title": "Github Copilot",
        "url": "https://futuretools.link/github-copilot",
        "description": "Generate code in real time using AI",
        "tag": "Generative Code",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c6ca2451fe0cf6bd4_copilot-ga-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c6ca2451fe0cf6bd4_copilot-ga.png"
    },
    {
        "title": "Glasp YouTube Summarizer",
        "url": "https://futuretools.link/youtube-summary",
        "description": "Chrome extension - Runs YouTube videos through GPT and summarizes them",
        "tag": "Speech-To-Text,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150554d1eb5a6c2734fd_youtube_summary_ogp-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150554d1eb5a6c2734fd_youtube_summary_ogp.jpeg"
    },
    {
        "title": "Hairstyle AI",
        "url": "https://futuretools.link/hairstyleai",
        "description": "Upload your photos and let the AI generate new hairstyles for you",
        "tag": "For Fun,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215058a30035b15b522df_HairstyleAIcover-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215058a30035b15b522df_HairstyleAIcover.jpeg"
    },
    {
        "title": "HeroPack",
        "url": "https://futuretools.link/heropack",
        "description": "Make gaming avatars with AI, inspired by video games",
        "tag": "Generative Art,Avatar,Gaming",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150627614de0fa642619_Social-Share-Image-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150627614de0fa642619_Social-Share-Image.jpeg"
    },
    {
        "title": "Hints",
        "url": "https://futuretools.link/hints-so",
        "description": "Create and update tickets and sales pipeline from messengers, email, or SMS",
        "tag": "Marketing,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150547b5263c73229029_Badge_Home_1200x630-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150547b5263c73229029_Badge_Home_1200x630.jpeg"
    },
    {
        "title": "Hotpot Art Generator",
        "url": "https://futuretools.link/hotpot-art-generator",
        "description": "Simple free AI art generator",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece7ec3cc76c51d3832_teaser-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece7ec3cc76c51d3832_teaser.jpeg"
    },
    {
        "title": "Hugging Face",
        "url": "https://futuretools.link/hugging-face",
        "description": "Required tool for Face Training in Stable Diffusion",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0ce8fc063819769ad_v2-2-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0ce8fc063819769ad_v2-2.png"
    },
    {
        "title": "HyperWrite",
        "url": "https://futuretools.link/hyperwrite",
        "description": "HyperWrite provides suggestions and sentence completions (Chrome Extension)",
        "tag": "Copywriting,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3baf552784427488977af_Screenshot%20(56)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3baf552784427488977af_Screenshot%20(56).png"
    },
    {
        "title": "InVideo",
        "url": "https://futuretools.link/invideo",
        "description": "Video maker with a large suite of AI tools",
        "tag": "Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c4ec069146384eea74_298025636_1113057562980637_7615670122075360388_n-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c4ec069146384eea74_298025636_1113057562980637_7615670122075360388_n.png"
    },
    {
        "title": "InboxPro",
        "url": "https://futuretools.link/inboxpro",
        "description": "AI-powered email assistant, calendar scheduling and auto-followups",
        "tag": "Productivity,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece88734f443e0e93b1_inboxpro-social-preview-image-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece88734f443e0e93b1_inboxpro-social-preview-image.png"
    },
    {
        "title": "Interior AI",
        "url": "https://futuretools.link/interior-ai",
        "description": "Take a picture of an empty room and let AI do your interior designing",
        "tag": "For Fun,Generative Art,Inspiration",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0aff1d85cf010ac90_tropical-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0aff1d85cf010ac90_tropical.png"
    },
    {
        "title": "Invoke AI",
        "url": "https://futuretools.link/invoke-ai-github",
        "description": "Stable Diffusion user-interface",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba074ff5773f86c8f2f_InvokeAI-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba074ff5773f86c8f2f_InvokeAI.png"
    },
    {
        "title": "Jasper",
        "url": "https://futuretools.link/jasper",
        "description": "AI tool for writing marketing sales copy and blog content",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b6ca2452b57cf6bbb_634e2322ba6592f9b19b11be_Homepage%2520Social%2520Share-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b6ca2452b57cf6bbb_634e2322ba6592f9b19b11be_Homepage%2520Social%2520Share.jpeg"
    },
    {
        "title": "Kive",
        "url": "https://futuretools.link/kive",
        "description": "Upload photos and videos and let AI organize and tag them",
        "tag": "Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639d60d48e74352ac972bfb2_iTOpMOjAVkwxySPZk2M5pQmpsA-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639d60d48e74352ac972bfb2_iTOpMOjAVkwxySPZk2M5pQmpsA.jpeg"
    },
    {
        "title": "Lama Cleaner",
        "url": "https://futuretools.link/lama-cleaner",
        "description": "Remove unwanted objects from pictures or replace anything in a picture",
        "tag": "Image Improvement,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639d60d55158510af3bebe21_lama-cleaner-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639d60d55158510af3bebe21_lama-cleaner.png"
    },
    {
        "title": "Lensa",
        "url": "https://futuretools.link/lensa",
        "description": "AI Image Editing App (Mobile)",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0916db461fd45a092_Lensa-og-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0916db461fd45a092_Lensa-og.jpeg"
    },
    {
        "title": "Let's Enhance",
        "url": "https://futuretools.link/lets-enhance",
        "description": "Use AI to upscale small or pixelated images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0e7010048f98b1235_fb1200-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba0e7010048f98b1235_fb1200.jpeg"
    },
    {
        "title": "Lex",
        "url": "https://futuretools.link/lex",
        "description": "AI writing assistant",
        "tag": "Copywriting,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec96affc04a73477e84_639bc5554da4a3db41f350da_Screenshot%2520(36)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec96affc04a73477e84_639bc5554da4a3db41f350da_Screenshot%2520(36).png"
    },
    {
        "title": "Lexica",
        "url": "https://futuretools.link/lexica",
        "description": "AI generated art gallery - See prompts others have used",
        "tag": "Generative Art,Inspiration",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba095df237f3b621ce3_lexica-meta-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acba095df237f3b621ce3_lexica-meta.png"
    },
    {
        "title": "Luma AI",
        "url": "https://futuretools.link/luma-ai",
        "description": "Scan real world items into 3D images (Using modern NeRF technology)",
        "tag": "Image Scanning",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c4da4a32dd3f184be_splash_4x3-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c4da4a32dd3f184be_splash_4x3.jpeg"
    },
    {
        "title": "Magic AI Avatars",
        "url": "https://futuretools.link/magicaiavatars",
        "description": "AI Avatar / Profile Pic Generator",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b59844de908ec87a82d_63a2175054d1eba2a8275435_Screenshot%2520(47)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b59844de908ec87a82d_63a2175054d1eba2a8275435_Screenshot%2520(47).png"
    },
    {
        "title": "Magic Eraser",
        "url": "https://futuretools.link/magic-eraser",
        "description": "Remove unwanted elements from images",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac6b3206ed63ba78d32da_magiceraser-og-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac6b3206ed63ba78d32da_magiceraser-og.png"
    },
    {
        "title": "MagicPic",
        "url": "https://futuretools.link/magicpic",
        "description": "AI Avatar / Profile Pic Generator",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215068a9a09fbf6e87797_6395aefd883c856265dc837e_New%2520Project%2520(23)%2520(1)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215068a9a09fbf6e87797_6395aefd883c856265dc837e_New%2520Project%2520(23)%2520(1).png"
    },
    {
        "title": "MakeLogoAI",
        "url": "https://futuretools.link/makelogo-ai",
        "description": "Generate unique logos for your startup, powered by AI",
        "tag": "Generative Art,Avatar",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150650ebcecd4b5252bc_social-share-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a2150650ebcecd4b5252bc_social-share.png"
    },
    {
        "title": "Melville App",
        "url": "https://futuretools.link/melville",
        "description": "A.I. Powered Podcast Copywriter",
        "tag": "Speech-To-Text,Podcasting",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3b9d816e18661fb083cdc_thumbnail.png",
        "imgurl_large": ""
    },
    {
        "title": "Metaphor",
        "url": "https://futuretools.link/metaphor",
        "description": "Use AI to predict links instead of text",
        "tag": "Research",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec98defc05fddba68b5_639bc57f2d3d573b9f013543_Screenshot%2520(37)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec98defc05fddba68b5_639bc57f2d3d573b9f013543_Screenshot%2520(37).png"
    },
    {
        "title": "Midjourney",
        "url": "https://futuretools.link/midjourney",
        "description": "Discord-based AI art tool",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acb660a971f18596fe9bd_639ac65c1b1ad88cd567d66f_Screenshot%2520(29)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acb660a971f18596fe9bd_639ac65c1b1ad88cd567d66f_Screenshot%2520(29).png"
    },
    {
        "title": "Monster Mash",
        "url": "https://futuretools.link/monster-mash",
        "description": "Convert drawn images into 3D images and then animate them",
        "tag": "Image Scanning,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940f2296e4d05081138b_thumbnail_wide-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940f2296e4d05081138b_thumbnail_wide.png"
    },
    {
        "title": "Movio",
        "url": "https://futuretools.link/movio",
        "description": "AI text-to-video - Add voice and speaking animation to avatars",
        "tag": "Text-To-Speech,Marketing,Generative Video",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c5ba62965200105d84_maxresdefault-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c5ba62965200105d84_maxresdefault.jpeg"
    },
    {
        "title": "Murf.ai",
        "url": "https://futuretools.link/murf-ai",
        "description": "AI realistic text-to-speech voice generator",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a5e72f493ea582a11_632477da0c3f22323d039ea3_home-small-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a5e72f493ea582a11_632477da0c3f22323d039ea3_home-small.png"
    },
    {
        "title": "Musenet (OpenAI)",
        "url": "https://futuretools.link/musenet",
        "description": "Create AI generated music",
        "tag": "Music",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdaf26aea7a5e3b1a8_Screen-Shot-2019-04-25-at-7.37.40-AM-1-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdaf26aea7a5e3b1a8_Screen-Shot-2019-04-25-at-7.37.40-AM-1.png"
    },
    {
        "title": "Namelix",
        "url": "https://futuretools.link/namelix",
        "description": "AI business name generator",
        "tag": "Inspiration,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c61a4b9d0e69ecb7e7_639bbbcd2d3d57db8f004540_Screenshot%2520(33)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c61a4b9d0e69ecb7e7_639bbbcd2d3d57db8f004540_Screenshot%2520(33).png"
    },
    {
        "title": "No-Code AI Model Builder",
        "url": "https://futuretools.link/no-code-ai-model-builder",
        "description": "Create fully customised OpenAI models with your own data",
        "tag": "Generative Code,Chat",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215050df9a552bc52a610_https%253A%252F%252Fs3.amazonaws.com%252Fappforest_uf%252Ff1671455959557x323055236625483970%252FDALL%2525C2%2525B7E%2525202022-12-19%25252013.01%2525201%252520%2525281%252529-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a215050df9a552bc52a610_https%253A%252F%252Fs3.amazonaws.com%252Fappforest_uf%252Ff1671455959557x323055236625483970%252FDALL%2525C2%2525B7E%2525202022-12-19%25252013.01%2525201%252520%2525281%252529.jpeg"
    },
    {
        "title": "Notion AI",
        "url": "https://futuretools.link/notion",
        "description": "Productivity and organization tool, now with AI prompting",
        "tag": "Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21506d56afc96880effa4_default-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21506d56afc96880effa4_default.png"
    },
    {
        "title": "Omniverse Audio2Face",
        "url": "https://futuretools.link/audio2face",
        "description": "AI avatar and facial animation",
        "tag": "Motion Capture,Generative Video",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e6533aea796152ce2_nvidia-omniverse-audio2face-app-og-image-1200x630-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e6533aea796152ce2_nvidia-omniverse-audio2face-app-og-image-1200x630.jpeg"
    },
    {
        "title": "OpenArt Photo Booth",
        "url": "https://futuretools.link/photo-booth",
        "description": "A tool that makes it simple to train your likeness into AI",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f974ff57e32c6c2605_photobooth_cover_11212022_191151-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f974ff57e32c6c2605_photobooth_cover_11212022_191151.jpeg"
    },
    {
        "title": "Otter.ai",
        "url": "https://futuretools.link/otter-ai",
        "description": "AI voice-to-text - Virtual note-taker",
        "tag": "Speech-To-Text,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b9fd05826990c5ab6_620d386acf1b61fec39b06c6_otter-og-image-02-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00b9fd05826990c5ab6_620d386acf1b61fec39b06c6_otter-og-image-02.png"
    },
    {
        "title": "Palette",
        "url": "https://futuretools.link/palette",
        "description": "Use AI to colorize black and white photos",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac6b3508aeffb3511628a_preview-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac6b3508aeffb3511628a_preview.png"
    },
    {
        "title": "Peppertype",
        "url": "https://futuretools.link/peppertype",
        "description": "AI tool for writing marketing sales copy and blog content",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cbcf2ad64ab42954d_pt_og_image_1e30ed1b3b-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cbcf2ad64ab42954d_pt_og_image_1e30ed1b3b.png"
    },
    {
        "title": "PhotoFix",
        "url": "https://futuretools.link/photofix",
        "description": "Remove people or things from photos",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b59176a0b6f3f787bc4_63a21776945e5e5236485f5c_Screenshot%2520(48)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b59176a0b6f3f787bc4_63a21776945e5e5236485f5c_Screenshot%2520(48).png"
    },
    {
        "title": "Photosonic",
        "url": "https://futuretools.link/photosonic",
        "description": "Online AI image generator",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31a4ae3265b63197c5a_63996caf1033710c246b0b6b_Photosonic-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31a4ae3265b63197c5a_63996caf1033710c246b0b6b_Photosonic.png"
    },
    {
        "title": "Pictory",
        "url": "https://futuretools.link/pictory",
        "description": "Convert text scripts and articles into videos with stock footage",
        "tag": "Video Editing,Text-To-Speech,Text-To-Video",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e082c9d4b088f38d8_thumb-home-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e082c9d4b088f38d8_thumb-home.jpeg"
    },
    {
        "title": "Play.ht",
        "url": "https://futuretools.link/play-ht",
        "description": "AI realistic text-to-speech voice generator",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00af23d8b818c996aea_playht-min.png",
        "imgurl_large": ""
    },
    {
        "title": "Playground (OpenAI)",
        "url": "https://futuretools.link/playground",
        "description": "Free AI writing tool - Let the AI generate any text you can imagine",
        "tag": "Copywriting,Research",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbb88e2900e61db9e_639bc5a25ba1ad78518d928c_Screenshot%2520(38)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbb88e2900e61db9e_639bc5a25ba1ad78518d928c_Screenshot%2520(38).png"
    },
    {
        "title": "Point-e",
        "url": "https://futuretools.link/point-e",
        "description": "AI Generative 3D Models",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3b9d8913e2702b205bc53_point-e.png",
        "imgurl_large": ""
    },
    {
        "title": "Poised",
        "url": "https://futuretools.link/poised",
        "description": "Real-time feedback on your speaking, using AI",
        "tag": "Chat,Self-Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a988cd82a50ccbcf7_626a64ba7b1b9932d0970ea0_Preview%2520image-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a988cd82a50ccbcf7_626a64ba7b1b9932d0970ea0_Preview%2520image.jpeg"
    },
    {
        "title": "Polycam",
        "url": "https://futuretools.link/polycam",
        "description": "Scan real world items into 3D images",
        "tag": "Image Scanning",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00d5e72f44ca9582a54_polycam-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00d5e72f44ca9582a54_polycam.png"
    },
    {
        "title": "Postwise",
        "url": "https://futuretools.link/postwise",
        "description": "Use AI to write tweets and Twitter threads",
        "tag": "Social Media,Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bf23d8b5590996afd_header-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bf23d8b5590996afd_header.png"
    },
    {
        "title": "Predia.ai",
        "url": "https://futuretools.link/predis-ai",
        "description": "AI Social Media Post Generator",
        "tag": "Copywriting,Marketing,Social Media",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111921b0e902dccc3d913_predis_logo.png",
        "imgurl_large": ""
    },
    {
        "title": "Prisma",
        "url": "https://futuretools.link/prisma",
        "description": "Upload photos and convert them into paintings",
        "tag": "Avatar,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f9e08e876a83709c72_Prisma-og-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f9e08e876a83709c72_Prisma-og.jpeg"
    },
    {
        "title": "Product Hunt AI Tools",
        "url": "https://futuretools.link/producthunt",
        "description": "Find the best Artificial Intelligence apps on Product Hunt",
        "tag": "Aggregators",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23df8c8814bfbad18dec6_0418cd04-f440-4021-8cf9-56be06164b0d-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23df8c8814bfbad18dec6_0418cd04-f440-4021-8cf9-56be06164b0d.png"
    },
    {
        "title": "QuillBot AI",
        "url": "https://futuretools.link/quillbot-ai",
        "description": "AI Writer, Content Generator & Writing Assistant",
        "tag": "Copywriting,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbb88e2900e61db9e_639bc5a25ba1ad78518d928c_Screenshot%2520(38)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbb88e2900e61db9e_639bc5a25ba1ad78518d928c_Screenshot%2520(38).png"
    },
    {
        "title": "Relayed",
        "url": "https://futuretools.link/relayed-ai",
        "description": "AI assistant for video calls",
        "tag": "Speech-To-Text,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11192096251057c7b14e4_relayed-meta-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11192096251057c7b14e4_relayed-meta.png"
    },
    {
        "title": "Replicate - Image-To-Prompt",
        "url": "https://futuretools.link/replicate",
        "description": "Plug-in an image and it will attempt to give you a prompt to replicate that image",
        "tag": "Generative Art,Image Scanning",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f9a95e0ecf29a1bf01_a_high_detail_shot_of_a_cat_wearing_a_suit_realism_8k_-n_9_-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f9a95e0ecf29a1bf01_a_high_detail_shot_of_a_cat_wearing_a_suit_realism_8k_-n_9_.png"
    },
    {
        "title": "Replika",
        "url": "https://futuretools.link/replika",
        "description": "Create your own AI character and have chat conversations with them",
        "tag": "For Fun,Chat",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c988cd80bd6ccbcff_replika_og_image-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c988cd80bd6ccbcff_replika_og_image.png"
    },
    {
        "title": "Resemble.ai",
        "url": "https://futuretools.link/resemble-ai",
        "description": "AI realistic text-to-speech voice generator - Can train your own voice",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a9fbc31e7eb3a37a1_Large-Logo-Text-small-size-1-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00a9fbc31e7eb3a37a1_Large-Logo-Text-small-size-1.png"
    },
    {
        "title": "Revspot AI",
        "url": "https://futuretools.link/revspot",
        "description": "AI copywriting for sales, marketing, and ads",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111915b0fe60c963c8ea9_nVWBAtDS43JGeXCuGGo06vmd56w-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111915b0fe60c963c8ea9_nVWBAtDS43JGeXCuGGo06vmd56w.jpeg"
    },
    {
        "title": "Rewind",
        "url": "https://futuretools.link/rewind-ai",
        "description": "Save anything, including conversations and make them searchable",
        "tag": "Productivity,Speech-To-Text",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111915382ea4e6a62591a_rewind-thumb-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a111915382ea4e6a62591a_rewind-thumb.jpeg"
    },
    {
        "title": "Riffusion",
        "url": "https://futuretools.link/riffusion",
        "description": "Uses Stable Diffusion models to generate music",
        "tag": "Music",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3b9d816e186f2f0083cd9_fywZpQ7.jpeg",
        "imgurl_large": ""
    },
    {
        "title": "Rokoko",
        "url": "https://futuretools.link/rokoko",
        "description": "Create motion capture animations using your webcam",
        "tag": "Motion Capture,Image Scanning",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e6533ae338c152ce5_63931d110aa6200b7694a3ec_rokoko.com%2520homepage-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e6533ae338c152ce5_63931d110aa6200b7694a3ec_rokoko.com%2520homepage.jpeg"
    },
    {
        "title": "Runway",
        "url": "https://futuretools.link/runway",
        "description": "Video editing tool with AI background remover and more",
        "tag": "Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e17a94bb31c120bbf_og_2022-V1-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e17a94bb31c120bbf_og_2022-V1.png"
    },
    {
        "title": "Rytr",
        "url": "https://futuretools.link/rytr",
        "description": "AI Writer, Content Generator & Writing Assistant",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbf9aaf0babda8644_639bc61c9fd058ba9e0df836_logo-spaced-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecbbf9aaf0babda8644_639bc61c9fd058ba9e0df836_logo-spaced.png"
    },
    {
        "title": "Scenario",
        "url": "https://futuretools.link/scenario",
        "description": "AI-generated gaming assets",
        "tag": "Gaming,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11191359ab0630a87fb81_639c67442f8b5f1dfa9d6e65_meta-img-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a11191359ab0630a87fb81_639c67442f8b5f1dfa9d6e65_meta-img.jpeg"
    },
    {
        "title": "ShowGPT",
        "url": "https://futuretools.link/showgpt",
        "description": "Ideas for prompts for Chat GPT",
        "tag": "Inspiration,Chat",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c4da4a3546cf184b7_Twitter-Post-1024x512-px-2-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c4da4a3546cf184b7_Twitter-Post-1024x512-px-2.jpeg"
    },
    {
        "title": "Soundraw",
        "url": "https://futuretools.link/soundraw",
        "description": "Generate royalty-free AI music in any theme",
        "tag": "Music",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bc658fc0724b93967_soundraw_ogp_EN-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00bc658fc0724b93967_soundraw_ogp_EN.png"
    },
    {
        "title": "Speech Studio",
        "url": "https://futuretools.link/speech-studio",
        "description": "AI realistic text-to-speech voice generator",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639cceccbcb1915c08c947fb_639bc77ffadc9eb259e5b61d_Screenshot%2520(39).png",
        "imgurl_large": ""
    },
    {
        "title": "Stocknews AI",
        "url": "https://futuretools.link/stocknews-ai",
        "description": "The latest stock news as found by AI",
        "tag": "Finance,Research",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5b81250d0474fbd77a_63a216d19bf8f16a3bd4afcc_Screenshot%2520(49)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5b81250d0474fbd77a_63a216d19bf8f16a3bd4afcc_Screenshot%2520(49).png"
    },
    {
        "title": "Supercreator.ai",
        "url": "https://futuretools.link/supercreator-ai",
        "description": "Create AI videos from scripts on your smart phone",
        "tag": "Marketing,Social Media,Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e082c9d53fa8f38d9_61d86070203e0e0b0b6c2cb3_app_icon_white_bg_1024-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940e082c9d53fa8f38d9_61d86070203e0e0b0b6c2cb3_app_icon_white_bg_1024.png"
    },
    {
        "title": "Synthesia",
        "url": "https://futuretools.link/synthesia",
        "description": "AI text-to-video - Add voice and speaking animation to avatars",
        "tag": "Text-To-Speech,Generative Video,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940eeaa548a2487fed8b_62556b0c0f63294bbf9b2353_OG%2520image%2520front%2520(4)%2520(1)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940eeaa548a2487fed8b_62556b0c0f63294bbf9b2353_OG%2520image%2520front%2520(4)%2520(1).png"
    },
    {
        "title": "Talk to Books (Google)",
        "url": "https://futuretools.link/talk-to-books",
        "description": "Ask a question and find answers from books in Google's database",
        "tag": "Productivity,Self-Improvement,Research",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c7ec0691ce9f4eea77_639bbba944c78556927e73f4_Screenshot%2520(34)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bc4c7ec0691ce9f4eea77_639bbba944c78556927e73f4_Screenshot%2520(34).png"
    },
    {
        "title": "Text-To-Pokemon",
        "url": "https://futuretools.link/text-to-pokemon",
        "description": "Create Pokemon character based on a prompt",
        "tag": "For Fun,Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f954dd54fdbd8c53f4_pokemontage-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac4f954dd54fdbd8c53f4_pokemontage.jpeg"
    },
    {
        "title": "Text-To-Song",
        "url": "https://futuretools.link/text-to-song",
        "description": "Uses AI to take your text and turn it into a song",
        "tag": "Text-To-Speech,Music,For Fun",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639e817588734fa5042a00a1_6389f66f8061c4393fc3bbe1_tt-song-og-img-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639e817588734fa5042a00a1_6389f66f8061c4393fc3bbe1_tt-song-og-img.png"
    },
    {
        "title": "Thing Translator",
        "url": "https://futuretools.link/thing-translator",
        "description": "Take a picture and Google's AI will tell you what it is",
        "tag": "Image Scanning,Translation",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c5ba1ad81148c1abf_khbjth0AxLYjz8E74iSUkuFssohsIG5qIQ-8x0PXOieEm0wm-g98OFFS0TURr6-381CsKGI7iSxahUKm6PcyoV4rxHClvZ67UA-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00c5ba1ad81148c1abf_khbjth0AxLYjz8E74iSUkuFssohsIG5qIQ-8x0PXOieEm0wm-g98OFFS0TURr6-381CsKGI7iSxahUKm6PcyoV4rxHClvZ67UA.png"
    },
    {
        "title": "This Person Does Not Exist",
        "url": "https://futuretools.link/this-person-does-not-exist",
        "description": "Quickly create a randomly generated human face",
        "tag": "Generative Art",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acb664ae326f53319ff94_639ac41d9130cba39b7e59e9_Screenshot%2520(28)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639acb664ae326f53319ff94_639ac41d9130cba39b7e59e9_Screenshot%2520(28).png"
    },
    {
        "title": "Timebolt",
        "url": "https://futuretools.link/timebolt",
        "description": "Remove silence, speed-up scenes, and cut commentary in video and podcasts",
        "tag": "Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fe293afdb26f46813_jJW1qt6VRRmmh34UXWXy_Screen_Shot_2020-11-21_at_2.18.55_PM-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fe293afdb26f46813_jJW1qt6VRRmmh34UXWXy_Screen_Shot_2020-11-21_at_2.18.55_PM.jpeg"
    },
    {
        "title": "Tome",
        "url": "https://futuretools.link/tome-app",
        "description": "Create amazing slide decks with AI",
        "tag": "Generative Art,Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a1119162ffe93fbe724e84_unfurl-3-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a1119162ffe93fbe724e84_unfurl-3.png"
    },
    {
        "title": "Translate.Video",
        "url": "https://futuretools.link/translate-video",
        "description": "Translate videos with just 1-Click",
        "tag": "Translation,Speech-To-Text",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21506854d8b75de81fccf_thumbnail-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a21506854d8b75de81fccf_thumbnail.png"
    },
    {
        "title": "Tribescaler",
        "url": "https://futuretools.link/tribescaler",
        "description": "Use AI to write tweets and Twitter threads",
        "tag": "Copywriting,Social Media,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cb0b773512e5b4a97_social_card-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cb0b773512e5b4a97_social_card.png"
    },
    {
        "title": "Uberduck",
        "url": "https://futuretools.link/uberduck",
        "description": "AI realistic text-to-speech voice generator - Can train your own voice",
        "tag": "Text-To-Speech",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecc5158515286b4ac48_639bc7931b57a035c5350f2f_Screenshot%2520(40)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecc5158515286b4ac48_639bc7931b57a035c5350f2f_Screenshot%2520(40).png"
    },
    {
        "title": "Unschooler",
        "url": "https://futuretools.link/unschooler",
        "description": "Personal AI mentor that adapts tutorials to your skills and career",
        "tag": "Chat,Research,Self-Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5c41bfdb8e5836c0e5_63a2156f2733122d68b1a3ae_Screenshot%2520(51)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a23b5c41bfdb8e5836c0e5_63a2156f2733122d68b1a3ae_Screenshot%2520(51).png"
    },
    {
        "title": "User Story Generator",
        "url": "https://futuretools.link/userstorygenerator",
        "description": "Use AI to generate user stories",
        "tag": "Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3b9d867095218713b7ce2_logo.png",
        "imgurl_large": ""
    },
    {
        "title": "Voice.ai",
        "url": "https://futuretools.link/voice-ai",
        "description": "Change your voice to famous celebrities in real time",
        "tag": "Voice Modulation",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec7e553bf1dad7d2cf5_639bc5151a4b9dd1c9ecbccb_Screenshot%2520(35)-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccec7e553bf1dad7d2cf5_639bc5151a4b9dd1c9ecbccb_Screenshot%2520(35).png"
    },
    {
        "title": "Voicemod",
        "url": "https://futuretools.link/voicemod",
        "description": "Voice transformer and modifier",
        "tag": "Voice Modulation",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639e81768defc00b11d66e38_Image-1-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639e81768defc00b11d66e38_Image-1.jpeg"
    },
    {
        "title": "Watermark Remover",
        "url": "https://futuretools.link/watermark-remover",
        "description": "Use AI to remove watermarks from an image",
        "tag": "Image Improvement",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31aab43ca97f72593f5_watermark_remover-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ac31aab43ca97f72593f5_watermark_remover.jpeg"
    },
    {
        "title": "Wave.Video",
        "url": "https://futuretools.link/wave-video",
        "description": "Create, edit, trim, cut and add subtitles to videos",
        "tag": "Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece88734f6efb0e93aa_meta-preview-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece88734f6efb0e93aa_meta-preview.jpeg"
    },
    {
        "title": "Whisper (OpenAI)",
        "url": "https://futuretools.link/whisper",
        "description": "Translate audio or video to text with language translation",
        "tag": "Speech-To-Text,Translation",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdf5414f1cb41870a4_social-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdf5414f1cb41870a4_social.png"
    },
    {
        "title": "Wisecut",
        "url": "https://futuretools.link/wisecut",
        "description": "Remove silence, speed-up scenes, and cut commentary in video and podcasts",
        "tag": "Video Editing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fd9aa2635ca8d97f6_b7657c_0037ee37bc8343208d74ca074baaf30c%257Emv2-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fd9aa2635ca8d97f6_b7657c_0037ee37bc8343208d74ca074baaf30c%257Emv2.png"
    },
    {
        "title": "Wordtune",
        "url": "https://futuretools.link/wordtune",
        "description": "AI writing assistant - Chrome Extension",
        "tag": "Copywriting,Productivity",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cd6a46deeb135e2db_6007dd9185f529bf1968574b_Social%2520Share%2520v2%2520-%2520Main-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639bb00cd6a46deeb135e2db_6007dd9185f529bf1968574b_Social%2520Share%2520v2%2520-%2520Main.png"
    },
    {
        "title": "Writer",
        "url": "https://futuretools.link/writer",
        "description": "AI writing platform that can be trained on your own content and brand guidelines",
        "tag": "Copywriting,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/63a3b9d8ed5955cc2e06378e_Share-image_-Home-Goodbye-content-bottlenecks-3.png",
        "imgurl_large": ""
    },
    {
        "title": "Writesonic",
        "url": "https://futuretools.link/writesonic",
        "description": "AI writing, copywriting & paraphrasing tool",
        "tag": "Copywriting,Productivity,Marketing",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdf5414ff77e1870a3_writesonic-og-p-500.jpeg",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccecdf5414ff77e1870a3_writesonic-og.jpeg"
    },
    {
        "title": "Xpression Camera",
        "url": "https://futuretools.link/xpression",
        "description": "Real-time AI-generated face filtering app",
        "tag": "Motion Capture,Generative Video",
        "imgurl": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fd9aa2644ab8d97f9_xpression_ogp-p-500.png",
        "imgurl_large": "https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639b940fd9aa2644ab8d97f9_xpression_ogp.png"
    }
]

items=  [{'title': 'Craiyon', 'url': 'https://futuretools.link/craiyon', 'description': 'Simple free AI art generator', 'tag': 'Generative Art', 'imgurl': 'https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc0f416ba698a_craiyon_preview-p-500.png', 'imgurl_large': 'https://uploads-ssl.webflow.com/63994dae1033718bee6949ce/639ccece8defc0f416ba698a_craiyon_preview.png'}]

dirp='./futureTools/'

def download_img(img_url):
    dirpath,filename=os.path.split(img_url)
    r = requests.get(img_url,stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(dirp+filename, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r
    return filename

def run(playwright):
    global items
    browser = playwright.chromium.launch(**browserLaunchOptionDict)
    context = browser.new_context()
    page = context.new_page()
    re_download=[]
    for item in items:
        print(item['url'])
        ss=dirp+item['title']+'_screenshot.png'
        ssm=dirp+item['title']+'_screenshot_poster.png'
        try:
            page.goto(item['url'],timeout=0 )
            page.wait_for_timeout(1500)
            item['url']=page.evaluate('''window.location.href''')
            item['url']=item['url'].split("?")[0]
            if os.path.exists(ss)==False:
                page.screenshot(full_page =True,path =ss)
            if os.path.exists(ssm)==False:
                page.screenshot(full_page =False,path =ssm)

            item={
                "title": item['title'],
                "url":item['url'],
                "description":item['description'],
                "tag":item['tag'],
                "imgurl":item['title']+'_screenshot_poster.png',
                "screenshot":item['title']+'_screenshot.png'
            } 
            
            utils.write_json(item,dirp+item['title']+'_item.json')
            
        except:
            print('---')
            re_download.append(item)
    print('re_download',re_download)
        
    # # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)