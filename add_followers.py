import nodriver as uc
import csv
import os
import time
import random
import json
import logging
import asyncio
import bs4  # BeautifulSoup import
import pyautogui  # ADDED: Import pyautogui for keyboard simulation
from datetime import datetime
from typing import List, Dict, Set, Optional

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler("linkedin_bot.log"),
		logging.StreamHandler()
	]
)
logger = logging.getLogger(__name__)

# # Constants
# TARGET_KEYWORDS = [
# 	"reporter", "freelance", "writer", "writing", "journalist", 
# 	"anchor", "marketing", "marketer", "market analyst", 
# 	"media relations", "public relations", "outreach", 
# 	"editor", "community", "partnerships", "quant",
# 	"trader", "저널리스트"
# ]

TARGET_KEYWORDS = [
	# --- English Keywords (Expanded) ---
	"reporter", "journalist", "correspondent", "staff writer", "news writer",
	"editor", "managing editor", "editor-in-chief", "news editor", "features editor",
	"content writer", "copywriter", "freelance writer", "contributor", "columnist",
	"technical writer", "blogger", "author", "publisher",
	"anchor", "producer", "content creator", "content manager", "content strategist",
	"media producer", "multimedia journalist",
	"marketing manager", "marketing specialist", "digital marketer", "growth marketer", "growth hacker",
	"social media manager", "social media specialist", "community manager", "community lead",
	"public relations specialist", "pr manager", "media relations specialist", "communications manager",
	"communications specialist", "outreach coordinator", "brand ambassador", "evangelist",
	"analyst", "market analyst", "research analyst", "crypto analyst", "financial analyst",
	"data analyst", "quant", "quantitative analyst", "chartist", "technical analyst",
	"strategist", "researcher",
	"trader", "crypto trader", "investment analyst",
	"partnerships manager", "business development manager", "strategic partnerships",
	"product reviewer", "tech reviewer", "app reviewer", "curator",
	"influencer", # Added from the translation table context

	# --- Spanish (es) Translations ---
	"reportero", "reportera", # (gendered for reporter)
	"periodista",
	"escritor", "escritora", # (gendered for writer)
	"redactor", "redactora", # (gendered for writer/editor)
	"editor", "editora", # (gendered for editor)
	"curador", "curadora", # (gendered for curator/editor)
	"creador de contenido", "creadora de contenido", # (gendered for content creator)
	"marketing", "mercadotecnia",
	"gestor de redes sociales", "gestora de redes sociales", # (gendered for social media manager)
	"gestor de comunidad", "gestora de comunidad", # (gendered for community manager)
	"relaciones públicas",
	"analista", # (unisex for analyst)
	"analista de mercado",
	"comerciante", # (trader)
	"investigador", "investigadora", # (gendered for researcher)
	"bloguero", "bloguera", # (gendered for blogger)
	"influyente", # (influencer)

	# --- French (fr) Translations ---
	"reporter", # (can be m/f depending on context, or use reporteure for f)
	"journaliste", # (m/f)
	"écrivain", "écrivaine",
	"rédacteur", "rédactrice",
	"rédacteur en chef", "rédactrice en chef",
	"éditeur", "éditrice",
	"créateur de contenu", "créatrice de contenu",
	"marketing", # (word often used directly)
	"gestionnaire de médias sociaux", # (m/f with article)
	"gestionnaire de communauté", # (m/f with article)
	"relations publiques",
	"analyste", # (m/f)
	"analyste de marché",
	"négociant", "négociante", # (trader)
	"trader", # (word often used directly)
	"chercheur", "chercheuse",
	"blogueur", "blogueuse",
	"influenceur", "influenceuse",

	# --- German (de) Translations ---
	"Reporter", "Reporterin",
	"Journalist", "Journalistin",
	"Autor", "Autorin",
	"Texter", "Texterin",
	"Redakteur", "Redakteurin",
	"Lektor", "Lektorin",
	"Content Creator", "Inhaltsersteller", "Inhaltserstellerin",
	"Marketing", # (word often used directly)
	"Social Media Manager", "Social Media Managerin",
	"Community Manager", "Community Managerin",
	"Öffentlichkeitsarbeit", "Public Relations", # (PR is common)
	"Analyst", "Analystin",
	"Marktanalyst", "Marktanalystin",
	"Händler", "Händlerin", # (Trader)
	"Trader", # (word often used directly)
	"Forscher", "Forscherin",
	"Blogger", "Bloggerin",
	"Influencer", "Influencerin",

	# --- Italian (it) Translations ---
	"reporter", # (m/f)
	"giornalista", # (m/f)
	"scrittore", "scrittrice",
	"redattore", "redattrice",
	"curatore", "curatrice",
	"creatore di contenuti", "creatrice di contenuti",
	"marketing", # (word often used directly)
	"social media manager", # (m/f)
	"community manager", # (m/f)
	"relazioni pubbliche",
	"analista", # (m/f)
	"analista di mercato",
	"commerciante", # (trader)
	"trader", # (word often used directly)
	"ricercatore", "ricercatrice",
	"blogger", # (m/f)
	"influencer", # (m/f)

	# --- Portuguese (pt) Translations ---
	"repórter", # (m/f)
	"jornalista", # (m/f)
	"escritor", "escritora",
	"redator", "redatora",
	"editor", "editora",
	"criador de conteúdo", "criadora de conteúdo",
	"marketing", # (word often used directly, or 'mercadologia')
	"gerente de mídias sociais", # (m/f with article)
	"gerente de comunidade", # (m/f with article)
	"relações públicas",
	"analista", # (m/f)
	"analista de mercado",
	"negociador", "negociadora", # (trader)
	"trader", # (word often used directly)
	"pesquisador", "pesquisadora",
	"blogueiro", "blogueira",
	"influenciador", "influenciadora",

	# --- Russian (ru) Translations ---
	"репортер", # reporter
	"журналист", # zhurnalist
	"писатель", "автор", # pisatel', avtor (writer)
	"редактор", # redaktor
	"создатель контента", # sozdatel' kontenta (content creator)
	"маркетинг", # marketing
	"менеджер социальных сетей", # menedzher sotsial'nykh setey (social media manager)
	"комьюнити-менеджер", # kom'yuniti-menedzher (community manager)
	"связи с общественностью", # svyazi s obshchestvennost'yu (public relations)
	"аналитик", # analitik
	"рыночный аналитик", # rynochnyy analitik (market analyst)
	"трейдер", # treyder
	"исследователь", # issledovatel' (researcher)
	"блогер", # bloger
	"инфлюенсер", # inflyuenser

	# --- Chinese (Simplified, zh-CN) Translations ---
	"记者", # jìzhě (reporter/journalist)
	"新闻工作者", # xīnwén gōngzuòzhě (journalist)
	"作者", "写手", # zuòzhě, xiěshǒu (writer)
	"编辑", # biānjí (editor)
	"内容创作者", # nèiróng chuàngzuòzhě (content creator)
	"营销", "市场", # yíngxiāo, shìchǎng (marketing)
	"社交媒体经理", # shèjiāo méitǐ jīnglǐ (social media manager)
	"社区经理", # shèqū jīnglǐ (community manager)
	"公共关系", "公关", # gōnggòng guānxì, gōngguān (public relations)
	"分析师", # fēnxīshī (analyst)
	"市场分析师", # shìchǎng fēnxīshī (market analyst)
	"交易员", # jiāoyìyuán (trader)
	"研究员", # yánjiūyuán (researcher)
	"博主", # bózhǔ (blogger)
	"网红", "影响者", # wǎnghóng, yǐngxiǎngzhě (influencer)

	# --- Japanese (ja) Translations ---
	"レポーター", # repōtā
	"ジャーナリスト", # jānarīsuto
	"ライター", "作家", # raitā, sakka (writer)
	"編集者", # henshūsha (editor)
	"コンテンツクリエーター", # kontentsu kurieitā
	"マーケティング", # māketingu
	"ソーシャルメディアマネージャー", # sōsharu media manējā
	"コミュニティマネージャー", # komyuniti manējā
	"広報", "PR", # kōhō, pīāru (public relations)
	"アナリスト", # anarisuto
	"市場アナリスト", # shijō anarisuto
	"トレーダー", # torēdā
	"研究者", # kenkyūsha (researcher)
	"ブロガー", # burogā
	"インフルエンサー", # infuruensā

	# --- Korean (ko) Translations ---
	"리포터", # ripoteo (reporter)
	"기자", # gija (reporter/journalist) - common native word
	"저널리스트", # jeoneolliseuteu (journalist) - already in your list
	"작가", "필자", # jakga, pilja (writer)
	"편집자", # pyeonjipja (editor)
	"콘텐츠 크리에이터", # kontencheu keurieiteo
	"마케팅", # maketing
	"소셜 미디어 관리자", # sosyeol midieo gwallija (social media manager)
	"커뮤니티 매니저", # keomyuniti maenijeo
	"홍보", "PR", # hongbo, piareul (public relations)
	"분석가", # bunseokga (analyst)
	"시장 분석가", # sijang bunseokga (market analyst)
	"트레이더", # teureideo
	"연구원", # yeonguwon (researcher)
	"블로거", # beullogeo
	"인플루언서", # inpeullueonseo

	# --- Arabic (ar) Translations ---
	"مراسل", # murāsil (reporter)
	"صحفي", # ṣaḥafī (journalist)
	"كاتب", # kātib (writer)
	"محرر", # muḥarrir (editor)
	"منشئ المحتوى", # munshiʾ al-muḥtawá (content creator)
	"تسويق", # taswīq (marketing)
	"مدير وسائل التواصل الاجتماعي", # mudīr wasāʾil al-tawāṣul al-ʾijtimāʿī (social media manager)
	"مدير المجتمع", # mudīr al-mujtamaʿ (community manager)
	"علاقات عامة", # ʿalāqāt ʿāmma (public relations)
	"محلل", # muḥallil (analyst)
	"محلل سوق", # muḥallil sūq (market analyst)
	"متداول", # mutadāwil (trader)
	"باحث", # bāḥith (researcher)
	"مدون", # mudawwin (blogger)
	"مؤثر", # muʾaththir (influencer)

	# --- Hindi (hi) Translations ---
	"रिपोर्टर", # riporṭar
	"पत्रकार", # patrakār (journalist)
	"लेखक", # lekhak (writer)
	"संपादक", # sampādak (editor)
	"कंटेंट क्रिएटर", # kaṇṭeṇṭ krieṭar
	"मार्केटिंग", # mārkeṭiṅg
	"सोशल मीडिया मैनेजर", # sośal mīḍiyā mainaijar
	"कम्युनिटी मैनेजर", # kamyuniṭī mainaijar
	"जनसंपर्क", # janasampark (public relations)
	"विश्लेषक", # viśleṣak (analyst)
	"बाजार विश्लेषक", # bājār viśleṣak (market analyst)
	"ट्रेडर", # ṭreḍar
	"शोधकर्ता", # śodhakartā (researcher)
	"ब्लॉगर", # blŏgar
	"इन्फ्लुएंसर", # inphluensar

	# --- Turkish (tr) Translations ---
	"muhabir", # (reporter)
	"gazeteci", # (journalist)
	"yazar", # (writer)
	"editör", # (editor)
	"içerik üreticisi", # (content creator)
	"pazarlama", # (marketing)
	"sosyal medya yöneticisi", # (social media manager)
	"topluluk yöneticisi", # (community manager)
	"halkla ilişkiler", # (public relations)
	"analist", # (analyst)
	"piyasa analisti", # (market analyst)
	"tüccar", "trader", # (trader)
	"araştırmacı", # (researcher)
	"blogger", # (blogger - often used directly)
	"etkileyici", "influencer" # (influencer - English word also common)
]

# Optional: Remove duplicates if any (though less likely with multiple languages)
# TARGET_KEYWORDS_ALL_LANGUAGES = list(set(TARGET_KEYWORDS_ALL_LANGUAGES))

# You can then print or use this list:
# print(TARGET_KEYWORDS_ALL_LANGUAGES)
# print(f"Total keywords: {len(TARGET_KEYWORDS_ALL_LANGUAGES)}")
CSV_FILENAME = "linkedin_profiles.csv"
CSV_FILENAME_SECOND_PART = "writers_only_updated.csv"
CSV_HEADERS = ["profile_url", "name", "position", "company", "sent_connection", "connected"]

# Timing constants
MAX_RETRIES = 3
# RETRY_DELAY = 5  # seconds
RETRY_DELAY = 2  # seconds
MIN_DELAY = 1    # minimum seconds between profile processing
MAX_DELAY = 2    # maximum seconds between profile processing

# Get existing profiles from CSV
async def get_existing_profiles() -> Set[str]:
	"""Get set of already logged profile URLs from CSV file."""
	existing_profiles = set()
	if os.path.exists(CSV_FILENAME):
		try:
			with open(CSV_FILENAME, 'r', newline='', encoding='utf-8') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					if row.get('profile_url'):
						url = row[0].split('?')[0] if '?' in row[0] else row[0]
						existing_profiles.add(url)
			print(f"Loaded {len(existing_profiles)} existing profiles from CSV")
		except Exception as e:
			print(f"Error reading existing profiles: {e}")
	return existing_profiles


# Save new profile to CSV
async def save_profile_to_csv(profile_info: Dict[str, str], existing_profiles: Set[str]):
	"""Save profile info to CSV file if not already saved."""
	# Clean the URL to keep only the part before "?"
	profile_url = profile_info[0].split('?')[0] if '?' in profile_info[0] else profile_info[0]
	profile_info[0] = profile_url
	
	# Skip if already logged
	if profile_url in existing_profiles:
		print(f"Profile {profile_url} already exists in CSV, skipping")
		return
	
	file_exists = os.path.exists(CSV_FILENAME)
	
	try:
		with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
			
			if not file_exists:
				writer.writeheader()
			
			writer.writerow(profile_info)
		
		# Add to existing profiles set
		existing_profiles.add(profile_url)
		print(f"Saved new profile: {profile_info.get('name', 'N/A')} ({profile_url})")
	except Exception as e:
		print(f"Error saving profile to CSV: {e}")

# Login to LinkedIn
async def login_to_linkedin(driver, username: str, password: str) -> bool:
	"""Log in to LinkedIn. Returns True if successful."""
	tab = await driver.get("https://linkedin.com/login")
	await tab.sleep(3)
	
	# MODIFIED: Removed the check for already logged in based on URL
	
	for attempt in range(MAX_RETRIES):
		try:
			# Fill username and password
			email_input = await tab.select('input[name="session_key"]')
			await email_input.send_keys(username)
			
			password_input = await tab.select('input[name="session_password"]')
			await password_input.send_keys(password)
			
			# Click sign in button
			sign_in_button = await tab.select('button[type="submit"]')
			await sign_in_button.click()
			await tab.sleep(24)  # Wait for login to complete
			
			# MODIFIED: Removed URL check and just returning success
			return True, tab
		except Exception as e:
			print(f"Login attempt {attempt+1} error: {e}")
		
		if attempt < MAX_RETRIES - 1:
			await tab.sleep(RETRY_DELAY)
	
	print("All login attempts failed")
	return False, tab


async def debug_html(tab):
	current_html_list = await tab.get_content()
	
	# print("current_html_list: current_html_list: ", str(current_html_list))
	print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
	print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
	print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
	current_html = current_html_list[0]
	# print("current_html_list: current_html_list[0]: ", str(current_html_list[0]))
	print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
	print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
	print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
	# print("current_html_list: current_html: ", str(current_html))
	print("current_html_list: len(current_html): ", str(len(current_html)))
	print("current_html_list: len(current_html): ", str(len(current_html)))
	print("current_html_list: len(current_html): ", str(len(current_html)))

# MODIFIED: Scroll to bottom function using pyautogui instead of tab.press
async def scroll_to_bottom(tab: uc.Tab):
	"""Scroll to the bottom of the page and click 'Show more results' if available."""
	total_scrolls = 0
	max_scrolls = 30
	print("Starting to scroll and load all profiles")
	last_html_len = 0

	while total_scrolls < max_scrolls:
		await tab.scroll_down(2500)
		# await asyncio.sleep(random.uniform(1.5, 2.5))
		await asyncio.sleep(1)

		show_more_buttons = await tab.select_all('button.artdeco-button')
		found_and_clicked_show_more = False
		for button_element in show_more_buttons:
			try:
				# MODIFIED: button_element.text is a property, not a coroutine
				button_text_content = button_element.text
				if "show more results" in button_text_content.lower():
					print("Found 'Show more results' button, clicking")
					# debug_html(tab)
					await button_element.click()
					# await asyncio.sleep(random.uniform(2, 3))
					await asyncio.sleep(1)
					found_and_clicked_show_more = True
					last_html_len = -1 # Reset html length check to ensure next check sees change
					break
			except Exception as e:
				print(f"Error interacting with a potential 'Show more results' button: {e}")
		
		if found_and_clicked_show_more:
			total_scrolls += 1
			continue

		current_html_list = await tab.get_content()
		if not current_html_list:
			print("Failed to get HTML content during scroll check (current_html_list is None or empty).")
			await asyncio.sleep(RETRY_DELAY)
			total_scrolls += 1
			continue
		# print("current_html_list: current_html_list: ", str(current_html_list))
		print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
		print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
		print("current_html_list: len(current_html_list): ", str(len(current_html_list)))
		current_html = current_html_list
		# print("current_html_list: current_html_list[0]: ", str(current_html_list[0]))
		# print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
		# print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
		# print("current_html_list: len(current_html_list[0]): ", len(str(current_html_list[0])))
		# print("current_html_list: current_html: ", str(current_html))
		# print("current_html_list: len(current_html): ", str(len(current_html)))
		# print("current_html_list: len(current_html): ", str(len(current_html)))
		# print("current_html_list: len(current_html): ", str(len(current_html)))
		current_html_len = len(current_html)
		
		if current_html_len < 200: # Log if HTML is suspiciously short during scroll
			print(f"Scroll check: HTML content is very short (length: {current_html_len}). URL: {tab.url}. HTML snippet: {current_html[:200]}")

		# If HTML content didn't change significantly (and wasn't reset by "show more"), likely at bottom
		if last_html_len != -1 and abs(current_html_len - last_html_len) < 1000:
			print(f"Reached the bottom of the page (content length stabilized: {current_html_len} vs {last_html_len}), no 'Show more' button visible or no new content.")
			break
		
		last_html_len = current_html_len
		total_scrolls += 1
	
	if total_scrolls >= max_scrolls:
		print(f"Reached maximum scroll limit ({max_scrolls}) for URL: {tab.url}")




# Extract profile information
def extract_profile_info(profile_card_html: str, company_name: str) -> Optional[Dict[str, str]]: # Now synchronous
	"""Extract profile information from a profile card HTML using BeautifulSoup."""
	# try:
	# 	if not isinstance(profile_card_html, str):
	# 		print(f"extract_profile_info received non-string input for profile_card_html (type: {type(profile_card_html)})")
	# 		return None

	soup = bs4.BeautifulSoup(profile_card_html, 'html.parser')
	profile_info = {
		'profile_url': '',
		'name': '',
		'position': '',
		'company': company_name,
		'sent_connection': 'False',
		'connected': 'False'
	}

	# Extract profile URL
	# Priority to links clearly identifying a profile, e.g., within common card structures
	# profile_link_tag = soup.select_one('a.app-aware-link[href*="/in/"], .org-people-profile-card__profile-link[href*="/in/"]')
	profile_link_tag = soup.select_one('a')
	if not profile_link_tag: # Broader search if specific selectors fail
		profile_link_tag = soup.find('a', href=lambda href: href and "/in/" in href and "miniProfile" not in href and "spotlight/" not in href)

	if profile_link_tag and profile_link_tag.has_attr('href'):
		full_url = profile_link_tag['href']
		if full_url.startswith('/'): # Ensure URL is absolute
			full_url = "https://www.linkedin.com" + full_url
		profile_info[0] = full_url.split('?')[0] if '?' in full_url else full_url
	else:
		print("Could not find profile URL link in card HTML snippet.")
		# Profile URL is critical, so we might return None if not found.
		# For now, allow trying to extract other info but log this card later if name also fails.

	# Extract name
	# Common selectors for name:
	# 1. Specific span within a title structure
	# 2. The title class itself
	# 3. Text within a profile title specific to people cards
	name_tag = soup.select_one('.artdeco-entity-lockup__title span[aria-hidden="true"]')
	if not name_tag:
		name_tag = soup.select_one('.artdeco-entity-lockup__title')
	if not name_tag: # For org-people-profile-card structure
		name_tag = soup.select_one('.org-people-profile-card__profile-title span[aria-hidden="true"]')
	
	if name_tag:
		profile_info['name'] = name_tag.get_text(strip=True)
	
	# Extract position
	position_tag = soup.select_one('.artdeco-entity-lockup__subtitle')
	if position_tag:
		profile_info['position'] = position_tag.get_text(strip=True)

	# If critical info like URL or name is missing, consider the extraction failed.
	if not profile_info[0] or not profile_info['name']:
		print(
			f"Failed to extract critical info from card. "
			f"URL: '{profile_info[0]}', Name: '{profile_info['name']}'. "
			f"Card HTML (first 300 chars): {profile_card_html[:300]}"
		)
		return None # Essential data missing
		
	return profile_info
	# except Exception as e:
	# 	print(f"Error in extract_profile_info (BS4): {e}. HTML snippet: {profile_card_html[:300]}")
	# 	return None



# Scan company pages for relevant profiles
async def scan_company_page(driver: uc.Browser, initial_tab: uc.Tab, company_url: str, existing_profiles: Set[str]):
	print(f"Attempting to scan company page: {company_url}")
	tab = initial_tab # Use the passed tab
	try:
		# Ensure the tab is on the correct URL
		if tab.url != company_url:
			print(f"Tab URL '{tab.url}' differs from target '{company_url}'. Navigating.")
			tab = await driver.get(company_url)
		await asyncio.sleep(random.uniform(4,7)) # Increased initial wait
	except Exception as nav_err:
		print(f"Failed to navigate/ensure tab on {company_url}: {nav_err}", exc_info=True)
		if tab: await tab.save_screenshot(f"scan_page_nav_error_{int(time.time())}.png")
		return False

	for attempt in range(MAX_RETRIES):
		# try:
		# if tab.crashed:
		# 	print(f"Tab crashed before scroll for {company_url}. Attempting re-navigate.")
		# 	tab = await driver.get(company_url) # Try to get a fresh tab
		# 	await asyncio.sleep(random.uniform(5,8))
		# 	if tab.crashed:
		# 		print(f"Tab still crashed after re-navigate for {company_url}. Aborting scan for this company.")
		# 		return False
		
		# print(f"Scan attempt {attempt+1} for {company_url}. Starting scroll.")
		print(f"Scan attempt {attempt+1} for {company_url}. Starting scroll.")
		scroll_successful = await scroll_to_bottom(tab)
		# if not scroll_successful:
		# 	print(f"Scroll was not successful for {company_url} on attempt {attempt+1}. Retrying if possible.")
		# 	if attempt < MAX_RETRIES - 1: 
		# 		# Try a more forceful refresh if scrolling fails badly
		# 		print(f"Attempting to re-navigate to {company_url} due to scroll failure.")
		# 		tab = await driver.get(company_url)
		# 		await asyncio.sleep(random.uniform(5,8))
		# 		continue
		# 	else:
		# 		print(f"All scroll attempts failed for {company_url}.")
		# 		return False

		page_html_list = None
		# try:
		page_html_list = await tab.get_content() # Increased timeout
		# except asyncio.TimeoutError:
		# 	print(f"Timeout getting final page content from {tab.url} on attempt {attempt+1}.")
		# 	await tab.save_screenshot(f"scan_page_get_content_timeout_{attempt+1}_{int(time.time())}.png")
		# 	# Continue to next attempt if not max retries
		# 	if attempt < MAX_RETRIES - 1: continue
		# 	return False
		# except Exception as get_content_final_err:
		# 	print(f"Error getting final page content from {tab.url} on attempt {attempt+1}: {get_content_final_err}")
		# 	if tab.crashed: print("Tab confirmed crashed after final get_content error.")
		# 	await tab.save_screenshot(f"scan_page_get_content_exception_{attempt+1}_{int(time.time())}.png")
		# 	if attempt < MAX_RETRIES - 1: continue
		# 	return False


		# if not page_html_list or not page_html_list[0] or len(page_html_list[0]) < 500: # Stricter check here
		# 	timestamp = int(time.time())
		# 	page_len = len(page_html_list[0]) if page_html_list and page_html_list[0] else 0
		# 	print(f"Attempt {attempt+1}: Final page content for {company_url} is invalid or too short (length: {page_len}). URL: {tab.url}")
		# 	await tab.save_screenshot(f"scan_page_final_short_html_{timestamp}.png")
		# 	if attempt < MAX_RETRIES - 1:
		# 		print(f"Re-navigating to {company_url} due to final bad content.")
		# 		tab = await driver.get(company_url) # Try to get a fresh page
		# 		await asyncio.sleep(random.uniform(5,8))
		# 		continue 
		# 	return False # All retries failed to get good content

		# page_html = page_html_list[0]
		page_html = page_html_list
		print(f"Final page HTML (length: {len(page_html)}) fetched for BS4 processing. URL: {tab.url}")
		
		company_name = company_url.split('/company/')[1].split('/')[0] if '/company/' in company_url else "UnknownCompany"
		soup = bs4.BeautifulSoup(page_html, 'html.parser')
		profile_card_tags = soup.select('li.org-people-profile-card__profile-card-spacing, div.org-people-profile-card')
		
		# print(f"Found {len(profile_card_tags)} profile card tags with BS4 from {company_name} at {company_url}")
		# print("profile_card_tags: ")
		# print("profile_card_tags: ")
		# print("profile_card_tags: ")
		# print("profile_card_tags: ")
		# print(profile_card_tags)
		# if not profile_card_tags and len(page_html) > 10000 : # Has substantial HTML but no cards
		# 	 print(f"No profile cards found on {company_url} despite substantial HTML. Page might have different structure or no people listed in expected format.")

		profiles_matched = 0
		for profile_card_tag in profile_card_tags:
			# print("profile_card_tag: ")
			# print(profile_card_tag)
			card_html_str = str(profile_card_tag)
			action_buttons = profile_card_tag.select('button.artdeco-button, a[role="button"]')
			if not action_buttons: continue
			
			card_text_content = profile_card_tag.get_text(separator=" ", strip=True).lower() # Better text aggregation
			matched_keyword = next((kw for kw in TARGET_KEYWORDS if kw.lower() in card_text_content), None)
			
			if matched_keyword:
				profile_info = extract_profile_info(card_html_str, company_name)
				print("*"*50)
				print("*"*50)
				print("profile_info: ")
				print("profile_info: ")
				print("profile_info: ")
				print("profile_info: ")
				print("profile_info: ")
				print(profile_info)
				print("card_html_str: ")
				print(card_html_str)
				print(card_html_str)
				print(card_html_str)
				if profile_info:
					await save_profile_to_csv(profile_info, existing_profiles)
					profiles_matched += 1
		
		# print(f"Matched and saved {profiles_matched} profiles from {company_name} (BS4) at {company_url}")
		return True

		# except Exception as e:
		# 	print(f"Attempt {attempt+1} to scan company page {company_url} (BS4) encountered an error: {e}", exc_info=True)
		# 	if tab and not tab.crashed: 
		# 		try: await tab.save_screenshot(f"error_scan_company_{company_name if 'company_name' in locals() else 'unknown_co'}_attempt{attempt+1}_{int(time.time())}.png")
		# 		except Exception as ss_err: print(f"Failed to take screenshot: {ss_err}")

		# 	if attempt < MAX_RETRIES - 1:
		# 		print(f"Retrying scan for {company_url} in {RETRY_DELAY}s. Re-navigating.")
		# 		await asyncio.sleep(RETRY_DELAY)
		# 		try:
		# 			tab = await driver.get(company_url) # Fresh tab/page for retry
		# 			await asyncio.sleep(random.uniform(5,8))
		# 		except Exception as renav_err_loop:
		# 			print(f"Failed to re-navigate to {company_url} for retry in loop: {renav_err_loop}")
		# 			return False # If re-navigation itself fails, better to stop for this company.
		# 	else:
		# 		print(f"All BS4 attempts to scan company {company_url} failed.")
		# 		return False
	
	print(f"All attempts to scan company {company_url} exhausted without success.")
	return False



# Update CSV row
async def update_csv_row(profile_url: str, sent_connection: bool = None, connected: bool = None):
	"""Update a row in the CSV file based on profile URL."""
	if not os.path.exists(CSV_FILENAME):
		print(f"update_csv_row: CSV file {CSV_FILENAME} does not exist.")
		print(f"update_csv_row: CSV file {CSV_FILENAME} does not exist.")
		return False
	
	try:
		# Clean the URL to keep only the part before "?"
		profile_url_cleaned = profile_url.split('?')[0] if '?' in profile_url else profile_url
		
		rows = []
		updated = False
		header = CSV_HEADERS # Use predefined headers
		
		with open(CSV_FILENAME, 'r', newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			if reader.fieldnames: # Ensure header is read if file not empty
				header = reader.fieldnames
			for row in reader:
				print("update_csv_row: row: ", str(row))
				row_url_cleaned = row.get('profile_url','').split('?')[0] if '?' in row.get('profile_url','') else row.get('profile_url','')
				print("update_csv_row: profile_url_cleaned: ", str(profile_url_cleaned))
				print("update_csv_row: row_url_cleaned: ", str(row_url_cleaned))
				if row_url_cleaned == profile_url_cleaned:
					if sent_connection is not None:
						row['sent_connection'] = str(sent_connection)
					if connected is not None:
						row['connected'] = str(connected)
					updated = True
					print(f"update_csv_row: Updating CSV row for {profile_url_cleaned}: sent_connection={row['sent_connection']}, connected={row['connected']}")
				rows.append(row)
		
		if updated:
			with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=header)
				writer.writeheader()
				writer.writerows(rows)
			return True
		else:
			print(f"update_csv_row: Profile URL {profile_url_cleaned} not found in CSV for update.")
			return False
	except Exception as e:
		print(f"update_csv_row: Error updating CSV row for {profile_url}: {e}")
		return False


async def update_csv_row_part_2(profile_url: str, sent_connection: bool = None, connected: bool = None):
	"""Update a row in the CSV file based on profile URL."""
	if not os.path.exists(CSV_FILENAME_SECOND_PART):
		print(f"CSV file {CSV_FILENAME_SECOND_PART} does not exist.")
		print(f"CSV file {CSV_FILENAME_SECOND_PART} does not exist.")
		return False
	
	try:
		# Clean the URL to keep only the part before "?"
		profile_url_cleaned = profile_url.split('?')[0] if '?' in profile_url else profile_url
		
		rows = []
		updated = False
		header = CSV_HEADERS # Use predefined headers
		
		with open(CSV_FILENAME_SECOND_PART, 'r', newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			if reader.fieldnames: # Ensure header is read if file not empty
				header = reader.fieldnames
			for row in reader:
				row_url_cleaned = row.get('profile_url','').split('?')[0] if '?' in row.get('profile_url','') else row.get('profile_url','')
				if row_url_cleaned == profile_url_cleaned:
					if sent_connection is not None:
						row['sent_connection'] = str(sent_connection)
					if connected is not None:
						row['connected'] = str(connected)
					updated = True
					print(f"Updating CSV row for {profile_url_cleaned}: sent_connection={row['sent_connection']}, connected={row['connected']}")
				rows.append(row)
		
		if updated:
			with open(CSV_FILENAME_SECOND_PART, 'w', newline='', encoding='utf-8') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=header)
				writer.writeheader()
				writer.writerows(rows)
			return True
		else:
			print(f"Profile URL {profile_url_cleaned} not found in CSV for update.")
			return False
	except Exception as e:
		print(f"Error updating CSV row for {profile_url}: {e}")
		print(f"Error updating CSV row for {profile_url}: {e}")
		return False




# MODIFIED: Send connection request with driver.get()
async def send_connection_request(driver, profile_url: str) -> bool:
	"""Visit a profile and send a connection request if possible. Returns True if successful or already sent/connected."""
	print("*"*50)
	print("*"*50)
	print()
	print(f"send_connection_request: Processing profile for connection: {profile_url}")
	
	tab = None # Initialize tab to None
	soup = None

	for attempt in range(MAX_RETRIES):
		# try:
		if tab is None or attempt > 0: # Get new tab or refresh on retries
			tab = await driver.get(profile_url)
			# await tab.sleep(random.uniform(MIN_DELAY, MAX_DELAY))  # Wait for page to load
			await tab.sleep(5)  # Wait for page to load
			# page_content = await tab.get_content()
			# soup = bs4.BeautifulSoup(page_content, 'html.parser')
			# print(soup)
		# Check for "Pending" button - case insensitive search
		# This still requires nodriver to get button states and click
		# all_buttons = soup.select('button')
		all_buttons = await tab.select_all('.ph5.pb5 *:last-child button')
		for btn_element in all_buttons:
			try:
				# btn_text = btn_element.get_text().lower()
				btn_text = btn_element.text
				if "pending" in btn_text.lower():
					print(f"send_connection_request: Connection already pending for {profile_url}")
					await update_csv_row_part_2(profile_url, sent_connection=True)
					return True
			except Exception as e_btn:
				print(f"Could not read text from a button on {profile_url}: {e_btn}")


		# Check for "Connect" button
		connect_button_found = None
		for btn_element in all_buttons: # Re-iterate or re-fetch if necessary
			try:
				# btn_text = btn_element.get_text().lower()
				btn_text = btn_element.text
				print("send_connection_request: btn_text: ", str(btn_text))
				# Be specific: "Connect" and not part of "Remove connection" etc.
				if btn_text.strip().lower() == "connect":
					connect_button_found = btn_element
					print("send_connection_request: connect_button_found: ", str(connect_button_found))
					break
				else:
					print("send_connection_request: CONNECT BUTTON NOT FOUND")
			except Exception as e_btn:
				print(f"send_connection_request: Could not read text from a button (connect search) on {profile_url}: {e_btn}")
		print("send_connection_request: connect_button_found: 2nd: ", str(connect_button_found))
		if connect_button_found:
			print(f"send_connection_request: Clicking Connect button for {profile_url}")
			await connect_button_found.click()
			await tab.sleep(random.uniform(1.5, 2.5))
			
			# Handle the modal dialog: "Send without a note" or similar
			# modal_buttons = soup.select('button.artdeco-button--primary') # Often primary button
			# modal_buttons = await tab.select_all('button.artdeco-button--primary') # Often primary button
			modal_buttons = await tab.select_all('div[aria-labelledby="send-invite-modal"] button[aria-label="Send without a note"]') # Often primary button
			send_action_done = False
			for modal_btn in modal_buttons:
				try:
					# modal_btn_text = modal_btn.get_text().lower()
					modal_btn_text = modal_btn.text
					print("send_connection_request: modal_btn_text: ", str(modal_btn_text))
					# Common texts: "Send", "Send now", "Send invitation"
					if any(s in modal_btn_text.lower() for s in ["send", "send now", "send invitation"]):
						print(f"send_connection_request: Clicking '{modal_btn_text}' in connect modal for {profile_url}")
						await modal_btn.click()
						send_action_done = True
						await tab.sleep(random.uniform(1.5, 2.5))
						break
				except Exception as e_modal_btn:
					print(f"send_connection_request: Error with modal button on {profile_url}: {e_modal_btn}")

			if send_action_done:
					# Verify connection was sent by checking for "Pending"
				await tab.sleep(random.uniform(1,2)) # give page time to update
				# final_buttons = soup.select('button')
				final_buttons = await tab.select_all('.ph5.pb5 *:last-child button')
				for final_btn in final_buttons:
					try:
						# if "pending" in (final_btn.get_text().lower()).lower():
						if "pending" in (final_btn.text).lower():
							await update_csv_row_part_2(profile_url, sent_connection=True)
							print(f"send_connection_request: Connection request sent and verified (pending) to {profile_url}")
							return True
					except: pass # ignore errors reading final buttons if main action succeeded
				print(f"send_connection_request: Sent connection but couldn't verify 'Pending' status immediately for {profile_url}. Assuming sent.")
				await update_csv_row_part_2(profile_url, sent_connection=True) # Assume sent
				return True
			else:
				print(f"send_connection_request: Clicked 'Connect', but couldn't find 'Send' button in modal for {profile_url}")
				# May need to close modal: pyautogui.press('escape') or click a close button
				# For now, we'll consider this path as non-conclusive for this attempt.

		# Check for "More" button to find Connect, and also for "Remove connection" (already connected)
		more_button_found = None
		already_connected = False
		
		# Re-fetch buttons if page state might have changed
		# current_buttons = soup.select('button')
		current_buttons = await tab.select_all('.ph5.pb5 *:last-child button.artdeco-dropdown__trigger')
		print("send_connection_request: MORE DROPDOWN: current_buttons: ", str(current_buttons))
		for btn_element in current_buttons:
			try:
				# btn_text = btn_element.get_text().lower()
				btn_text = btn_element.text
				print("send_connection_request: btn_text: ", str(btn_text))
				if "more" in btn_text.lower() and not "show more results" in btn_text.lower() : # Ensure it's the profile actions 'More'
					more_button_found = btn_element
					print("send_connection_request: more_button_found: ", str(more_button_found))
				# Check for degree pill/text indicating 1st degree connection
				if "1st" in btn_text.lower() and "degree" in btn_text.lower(): # Heuristic for connected
					already_connected = True
					print("send_connection_request: already_connected: ", str(already_connected))
					break
			except Exception:
				pass
		
		if already_connected:
			print(f"send_connection_request: Already connected (1st degree) to {profile_url}")
			await update_csv_row_part_2(profile_url, connected=True, sent_connection=True) # If connected, implies sent
			return True

		if more_button_found:
			print(f"send_connection_request: Clicking 'More' button for {profile_url}")
			await more_button_found.click()
			await tab.sleep(random.uniform(1, 2))
			
			# dropdown_items = soup.select('div[role="button"], div.artdeco-dropdown__item') # Common dropdown item selectors
			dropdown_items = await tab.select_all('.ph5.pb5 *:last-child .artdeco-dropdown__content-inner div[role="button"], .ph5.pb5 *:last-child .artdeco-dropdown__content-inner div.artdeco-dropdown__item') # Common dropdown item selectors
			print("send_connection_request: dropdown_items: ", str(dropdown_items))
			connect_option_in_more = None
			remove_option_in_more = None

			for item in dropdown_items:
				try:
					# item_text_content = await item.text_all # text_all for elements with nested text
					# item_text_content = item.get_text().lower() # text_all for elements with nested text
					item_text_content = item.text # text_all for elements with nested text
					item_text = item_text_content.strip().lower()
					
					print("send_connection_request: item_text_content: ", str(item_text_content))

					if "remove connection" in item_text:
						remove_option_in_more = item # Found "Remove connection"
						print("send_connection_request: remove_option_in_more: ", str(remove_option_in_more))
						break 
					# Looking for "Connect" that is not part of "Remove Connection"
					if "connect" == item_text or ( "connect" in item_text and len(item_text) < 15 ): # Simple "Connect" or "Connect "
						connect_option_in_more = item # Found "Connect"
						print("send_connection_request: connect_option_in_more: ", str(connect_option_in_more))
						# Don't break yet, prioritize "Remove Connection" check
				except Exception as e_drop_item:
					print(f"send_connection_request: Error reading dropdown item on {profile_url}: {e_drop_item}")
			
			if remove_option_in_more:
				print(f"send_connection_request: Already connected to {profile_url} (found 'Remove connection' in More dropdown).")
				await update_csv_row_part_2(profile_url, connected=True, sent_connection=True)
				# Click outside to close dropdown, e.g. by focusing body or clicking a known static element
				try: await (tab.select('body')).focus()
				# try: await (soup.select('body')).focus()
				# except: pyautogui.press('escape') # Fallback
				except: pass
				await tab.sleep(0.5)
				return True

			if connect_option_in_more:
				print(f"send_connection_request: Clicking Connect in 'More' dropdown for {profile_url}")
				await connect_option_in_more.click()
				await tab.sleep(random.uniform(1.5, 2.5))
				
				# Handle the modal dialog again ("Send without a note")
				# modal_buttons_more = soup.select('button.artdeco-button--primary')

				modal_buttons_more = await tab.select_all('div[aria-labelledby="send-invite-modal"] button[aria-label="Send without a note"]') # Often primary button
				send_action_done_more = False
				for modal_btn_more in modal_buttons_more:
					try:
						# modal_btn_text_more = modal_btn_more.get_text().lower()
						modal_btn_text_more = modal_btn_more.text
						print("send_connection_request: modal_btn_text_more: ", str(modal_btn_text_more))
						if any(s in modal_btn_text_more.lower() for s in ["send", "send now", "send invitation"]):
							print(f"send_connection_request: Clicking '{modal_btn_text_more}' in connect modal (from More) for {profile_url}")
							await modal_btn_more.click()
							await tab.sleep(random.uniform(1.5, 2.5))
							send_action_done_more = True
							break
					except Exception as e_modal_btn_more:
						print(f"send_connection_request: Error with modal button (from More) on {profile_url}: {e_modal_btn_more}")
				
				if send_action_done_more:
					await update_csv_row_part_2(profile_url, sent_connection=True)
					print(f"send_connection_request: Connection request sent (from More dropdown) to {profile_url}")
					return True
				else:
					print(f"send_connection_request: Clicked 'Connect' (from More), but couldn't find 'Send' button in modal for {profile_url}")
			
			# Close dropdown if still open
			try: await (tab.select('body')).focus()
			# try: await (soup.select('body')).focus()
			# except: pyautogui.press('escape') # Fallback
			except: pass
			await tab.sleep(0.5)

		print(f"send_connection_request: No direct 'Connect' or 'Pending' button, nor 'Connect' in 'More' found for {profile_url} on attempt {attempt+1}. Might be a Follow-only profile or other restriction.")
		return False # No connect action taken successfully this attempt if it reaches here

		# except Exception as e:
		# 	print(f"send_connection_request: Attempt {attempt+1} to send connection request to {profile_url} failed: {e}", exc_info=True)
		# 	# if tab: await tab.screenshot(f"error_profile_{profile_url.split('/')[-1]}_attempt{attempt+1}.png") # Screenshot on error
		# 	if attempt < MAX_RETRIES - 1:
		# 		print(f"send_connection_request: Retrying connection attempt for {profile_url} in {RETRY_DELAY}s")
		# 		await asyncio.sleep(RETRY_DELAY) # Use asyncio.sleep for async functions
		# 		tab = None # Force reload by resetting tab
		# 	else:
		# 		print(f"send_connection_request: All attempts to process {profile_url} failed.")
		# 		return False # All retries failed
	
	print(f"send_connection_request: All attempts to process {profile_url} for connection failed (loop exhausted).")
	return False


# Run Part I - scan company pages
async def part1_scan_companies(linkedin_username: str, linkedin_password: str, company_urls: List[str]):
	"""Run Part I of the script - scan company pages for relevant profiles."""
	print("Starting Part I: Scanning company pages for relevant profiles")
	
	existing_profiles = await get_existing_profiles()
	
	driver = await uc.start()
	tab = None # Initialize tab
	try:
		success, tab = await login_to_linkedin(driver, linkedin_username, linkedin_password)
		if not success or not tab:
			print("Failed to log in to LinkedIn, aborting Part I")
			return # driver will be closed in finally
	
		for company_url in company_urls:
			try:
				# Pass the currently active tab to scan_company_page, it will re-navigate
				success_scan = await scan_company_page(driver, tab, company_url, existing_profiles)
				print(f"part1_scan_companies: scan_company_page success for {company_url}: {success_scan}")
				
				if success_scan:
					# Add random delay between company pages
					delay = random.uniform(MIN_DELAY, MAX_DELAY) # Use defined constants
					print(f"Waiting {delay:.2f} seconds before next company")
					await asyncio.sleep(delay) # Use asyncio.sleep
				else:
					print(f"part1_scan_companies: Failed to scan {company_url}. Skipping to next company.")
					print(f"Skipping to next company after failure with {company_url}")
					await asyncio.sleep(random.uniform(1,3)) # Shorter delay on failure before next

			except Exception as e_company_scan:
				print(f"Unhandled error scanning company {company_url}: {e_company_scan}", exc_info=True)
				await asyncio.sleep(RETRY_DELAY) # Wait before trying next company on major error
	
		print("Part I completed")
		print("Part I: Scanning company pages completed.")

	except Exception as e_main_part1:
		print(f"Critical Error in part1_scan_companies: {e_main_part1}", exc_info=True)
		pass
	# finally:
	# 	if driver:
	# 		print("Closing browser driver for Part I.")
	# 		await driver.close()



def read_csv(filepath):
	a = open(filepath, "r", encoding="utf8", errors="ignore", newline="")
	b = csv.reader(a)
	return [c for c in b]


def write_csv(filepath):
	a = open(filepath, "w", encoding="utf8", errors="ignore", newline="")
	b = csv.writer(a)
	return b




# Run Part II - send connection requests
async def part2_send_connection_requests(linkedin_username: str, linkedin_password: str):
	"""Run Part II of the script - send connection requests."""
	print("Starting Part II: Sending connection requests")
	
	if not os.path.exists(CSV_FILENAME_SECOND_PART):
		print(f"CSV file {CSV_FILENAME_SECOND_PART} does not exist.")
		return
	
	driver = await uc.start()
	await driver.main_tab.maximize()
	success, tab = await login_to_linkedin(driver, linkedin_username, linkedin_password)

	profiles_to_process = read_csv(CSV_FILENAME_SECOND_PART)
	
	print(f"Found {len(profiles_to_process)} profiles to process")
	
	counter = 0

	for profile_url in profiles_to_process:
		print("part2_send_connection_requests: profile_url: ", str(profile_url))
		print("part2_send_connection_requests: profile_url[0]: ", str(profile_url[0]))
		if counter <= 5:
			break
		if profile_url[4] == False or profile_url[4] == "False" or profile_url[4] == "false":
			await send_connection_request(driver, profile_url[0])
			delay = random.uniform(MIN_DELAY, MAX_DELAY)
			print(f"Waiting {delay:.2f} seconds before next profile")
			await tab.sleep(delay)
			counter += 1
		else:
			print(f"part2_send_connection_requests: ALREADY ADDED {profile_url[1].upper()}")
		
	
	print("Part II completed")


async def part3_get_sales_search(linkedin_username: str, linkedin_password: str):
	"""Run Part III of the script - Log all profiles from Sales Navigator search results to csv."""
	print("Starting Part III: Logging sales search results")
	
	CSV_FILENAME_SALES = "linkedin_sales_profiles.csv"
	CSV_HEADERS_SALES = ["profile_url", "name", "position", "company", "location", "about", "sent_connection", "connected"]
	
	# Ensure the CSV file exists with headers
	if not os.path.exists(CSV_FILENAME_SALES):
		with open(CSV_FILENAME_SALES, 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS_SALES)
			writer.writeheader()
	
	# Initialize driver and login
	driver = await uc.start()
	await driver.main_tab.maximize()
	success, tab = await login_to_linkedin(driver, linkedin_username, linkedin_password)
	
	if not success:
		print("Failed to log in to LinkedIn, aborting Part III")
		await driver.close()
		return
	
	# List of Sales Navigator search URLs to process
	searches_to_go_through = [
		"https://www.linkedin.com/sales/search/people?page=1&savedSearchId=1912972594&sessionId=7G2368oYRTKAtFLzAUk9%2FA%3D%3D",
		"https://www.linkedin.com/sales/search/people?page=1&savedSearchId=1912972586&sessionId=7G2368oYRTKAtFLzAUk9%2FA%3D%3D"
	]
	
	existing_profiles = set()
	# Load existing profiles to avoid duplicates
	try:
		with open(CSV_FILENAME_SALES, 'r', newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row.get('profile_url'):
					url = row['profile_url'].split('?')[0] if '?' in row['profile_url'] else row['profile_url']
					existing_profiles.add(url)
		print(f"Loaded {len(existing_profiles)} existing profiles from Sales CSV")
	except Exception as e:
		print(f"Error reading existing Sales profiles: {e}")
	
	# Process each search URL
	for search_url in searches_to_go_through:
		print(f"Processing search URL: {search_url}")
		base_url = search_url.split('page=')[0]
		param_part = search_url.split('page=1')[1]
		
		# Navigate to the search page
		tab = await driver.get(search_url)
		await tab.sleep(5)  # Allow page to load
		
		# Get total number of results
		try:
			# Try to find the total results count
			results_elements = await tab.select_all('.artdeco-pagination__page-info')
			total_results = 0
			
			for element in results_elements:
				text_content = await element.text_all
				print(f"Pagination info: {text_content}")
				
				# Format could be "Showing 1-25 of 1,234 results" or similar
				if "of" in text_content and "results" in text_content:
					# Extract the number after "of" and before "results"
					total_part = text_content.split("of ")[1].split(" results")[0]
					
					# Handle abbreviations like "1.2M" or "300K"
					total_part = total_part.replace(",", "")  # Remove commas
					if "M" in total_part:
						total_results = int(float(total_part.replace("M", "")) * 1000000)
					elif "K" in total_part:
						total_results = int(float(total_part.replace("K", "")) * 1000)
					else:
						total_results = int(total_part)
					
					break
			
			if total_results == 0:
				# Fallback method - try to find the total results count in other elements
				results_indicators = await tab.select_all('.search-results__total')
				for indicator in results_indicators:
					text_content = await indicator.text_all
					if "results" in text_content:
						# Extract numbers from the text
						numbers = ''.join(c for c in text_content if c.isdigit() or c in ',.KM')
						if "M" in numbers:
							total_results = int(float(numbers.replace("M", "")) * 1000000)
						elif "K" in numbers:
							total_results = int(float(numbers.replace("K", "")) * 1000)
						else:
							total_results = int(numbers.replace(",", ""))
						break
			
			print(f"Found approximately {total_results} total results")
			
			# Calculate number of pages (Sales Navigator shows 25 results per page)
			results_per_page = 25
			total_pages = (total_results + results_per_page - 1) // results_per_page  # Ceiling division
			
			# Limit to a reasonable number of pages to avoid excessive scraping
			max_pages = 20  # Adjust as needed
			total_pages = min(total_pages, max_pages)
			
			print(f"Will process {total_pages} pages for this search")
			
			# Process each page
			current_page = 1
			while current_page <= total_pages:
				print(f"Processing page {current_page} of {total_pages}")
				
				# If not on the first page, navigate to the next page
				if current_page > 1:
					next_page_url = f"{base_url}page={current_page}{param_part}"
					tab = await driver.get(next_page_url)
					await tab.sleep(5)  # Allow page to load
				
				# Get the list of profile cards
				page_html = await tab.get_content()
				soup = bs4.BeautifulSoup(page_html, 'html.parser')
				profile_cards = soup.select('li.artdeco-list__item')
				
				print(f"Found {len(profile_cards)} profile cards on page {current_page}")
				
				# Process each profile card
				for card in profile_cards:
					try:
						# Extract profile data
						profile_info = {
							'profile_url': '',
							'name': '',
							'position': '',
							'company': '',
							'location': '',
							'about': '',
							'sent_connection': 'False',
							'connected': 'False'
						}
						
						# Extract profile URL
						profile_link = card.select_one('a[href*="/sales/lead/"]')
						if profile_link and profile_link.has_attr('href'):
							full_url = profile_link['href']
							if full_url.startswith('/'):
								full_url = f"https://www.linkedin.com{full_url}"
							profile_info['profile_url'] = full_url.split('?')[0] if '?' in full_url else full_url
						
						# Skip if we already have this profile
						if profile_info['profile_url'] in existing_profiles:
							print(f"Skipping already saved profile: {profile_info['profile_url']}")
							continue
							
						# Extract name
						name_element = card.select_one('[data-anonymize="person-name"]')
						if name_element:
							profile_info['name'] = name_element.text.strip()
						
						# Extract position
						position_element = card.select_one('[data-anonymize="title"]')
						if position_element:
							profile_info['position'] = position_element.text.strip()
						
						# Extract company
						company_element = card.select_one('[data-anonymize="company-name"]')
						if company_element:
							profile_info['company'] = company_element.text.strip()
						
						# Extract location
						location_element = card.select_one('[data-anonymize="location"]')
						if location_element:
							profile_info['location'] = location_element.text.strip()
						
						# Extract about/description
						about_element = card.select_one('dt:contains("About:") + dd')
						if about_element:
							profile_info['about'] = about_element.text.strip()
						
						# Check if we have enough information to save this profile
						if profile_info['profile_url'] and profile_info['name']:
							# Save to CSV
							with open(CSV_FILENAME_SALES, 'a', newline='', encoding='utf-8') as csvfile:
								writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS_SALES)
								writer.writerow(profile_info)
							
							# Add to existing profiles set to avoid duplicates
							existing_profiles.add(profile_info['profile_url'])
							
							print(f"Saved profile: {profile_info['name']} ({profile_info['profile_url']})")
					except Exception as e:
						print(f"Error processing a profile card: {e}")
				
				# Move to the next page
				current_page += 1
				
				# Random delay between page loads
				await tab.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
				
		except Exception as e:
			print(f"Error processing search URL {search_url}: {e}")
	
	print(f"Part III completed. Saved profiles to {CSV_FILENAME_SALES}")
	await driver.close()




# Main function
async def main():
	print("LinkedIn Profile Scanner and Connection Sender")
	print("---------------------------------------------")
	
	# linkedin_username = "<redacted>"
	# linkedin_password = "<redacted>"
	linkedin_username = os.getenv("LINKEDIN_USERNAME", "")
	linkedin_password = os.getenv("LINKEDIN_PASSWORD", "")
	
	company_urls = [
		# "https://linkedin.com/company/coindesk/people/",
		# "https://www.linkedin.com/company/coindeskdata/people/",
		# "https://www.linkedin.com/company/messari/people/",
		# "https://www.linkedin.com/company/reuters2/people/",
		# "https://www.linkedin.com/company/techcrunch/people/",
		# "https://www.linkedin.com/company/reuters-news-agency/people/",
		# "https://www.linkedin.com/company/bloomberg-news/people/",
		# "https://www.linkedin.com/company/coindeskjapan/people/",
		# "https://www.linkedin.com/company/thomson-reuters/people/",
		# "https://www.linkedin.com/company/marketwatch/people/",
		# "https://www.linkedin.com/company/forbes-magazine/people/",
		# "https://www.linkedin.com/company/financial-times/people/",
		# "https://www.linkedin.com/company/businessinsider/people/",
		# "https://www.linkedin.com/company/the-wall-street-journal/people/",
		# "https://www.linkedin.com/company/yahoo-finance/people/",
		# "https://www.linkedin.com/company/cnbc-international/people/",
		# "https://www.linkedin.com/company/coindeskturkiye/people/",
		# "https://www.linkedin.com/company/cointelegraph/people/",
		# "https://www.linkedin.com/company/bitget-global/people/",
		# "https://www.linkedin.com/company/ctjapan/people/",
		# "https://www.linkedin.com/company/cryptoknowmics/people/",
		# "https://www.linkedin.com/company/ambcrypto/people/",
		# "https://www.linkedin.com/company/banklesshq/people/",
		# "https://www.linkedin.com/company/blockonomi/people/",
		# "https://www.linkedin.com/company/nulltx/people/",
		# "https://www.linkedin.com/company/ccndotcom/people/",
		# "https://www.linkedin.com/company/voice-of-crypto/people/",
		# "https://www.linkedin.com/company/cryptobriefing/people/",
		# "https://www.linkedin.com/company/blockchaincompany/people/",
		# "https://www.linkedin.com/company/defiantmedia/people/",
		# "https://www.linkedin.com/company/cryptoslate/people/",
		# "https://www.linkedin.com/company/ambcrypto/people/",
		# "https://www.linkedin.com/company/newsbtc/people/",
		# "https://www.linkedin.com/company/entrepreneur-media/people/",
		# "https://www.linkedin.com/company/cryptopotato/people/",
		# "https://www.linkedin.com/company/bitcoin.com/people/",
		# "https://www.linkedin.com/company/coin-bureau/people/",
		# "https://www.linkedin.com/company/bitcoinist-net/people/",
		# "https://www.linkedin.com/company/btctimes/people/",
		# "https://www.linkedin.com/company/ocean-mining/people/",
		# "https://www.linkedin.com/company/bitcoin-collective/people/",
		# "https://www.linkedin.com/company/bitfinex/people/",
		# "https://www.linkedin.com/company/dwf-labs/people/",
		# "https://www.linkedin.com/company/kucoin/people/",
		# "https://www.linkedin.com/company/sui-foundation/people/",
		# "https://www.linkedin.com/company/theblockcrypto/people/",
		# "https://www.linkedin.com/company/decrypt-media/people/",
		# "https://www.linkedin.com/company/metamask/people/",
		# "https://www.linkedin.com/company/kastofficial/people/",
		# "https://www.linkedin.com/company/krakenfx/people/",
		# "https://www.linkedin.com/company/stand-with-crypto-canada/people/",
		# "https://www.linkedin.com/company/arbitrum/people/",
		# "https://www.linkedin.com/company/zksync-network/people/",
		# "https://www.linkedin.com/company/polygonlabs/people/",
		# "https://www.linkedin.com/company/polkadot-blockchain-academy/people/",
		# "https://www.linkedin.com/company/aptos-foundation/people/",
		# "https://www.linkedin.com/company/beincrypto/people/",
		# "https://www.linkedin.com/company/phantomwallet/people/",
		# "https://www.linkedin.com/company/pudgy-penguins/people/",
		# "https://www.linkedin.com/company/bitmart/people/",
		# "https://www.linkedin.com/company/coinwofficial/people/",
		# "https://www.linkedin.com/company/cryptobreaking/people/",
		# "https://www.linkedin.com/company/altcoinbreaking/people/",
		# "https://www.linkedin.com/company/binance-vip-institutional/people/",
		# "https://www.linkedin.com/company/bitmex/people/",
		# "https://www.linkedin.com/company/bitcoinnews-com/people/",
		# "https://www.linkedin.com/company/the-blockworks-group/people/",
		# "https://www.linkedin.com/company/solana-foundation/people/",
		# "https://www.linkedin.com/company/coinmarketcap/people/",
		# "https://www.linkedin.com/company/coinedition/people/",
		# "https://www.linkedin.com/company/coingabbar/people/",
		# "https://www.linkedin.com/company/cryptodotnews/people/",
		# "https://www.linkedin.com/company/crypto-times-io/people/",
		# "https://www.linkedin.com/company/fxstreet/people/",
		# "https://www.linkedin.com/company/hindustantimes/people/",
		# "https://www.linkedin.com/company/thenewscrypto/people/",
		# "https://www.linkedin.com/company/cryptonewsz/people/",
		# "https://www.linkedin.com/company/mexcofficial/people/",
		# "https://www.linkedin.com/company/cryptojobslist/people/",
		# "https://www.linkedin.com/company/ripple-xrpl/people/",
		# "https://www.linkedin.com/company/stellar-development-foundation/people/",
		# "https://www.linkedin.com/company/coinbase/people/",
		# "https://www.linkedin.com/company/quantnetwork/people/",
		# "https://www.linkedin.com/company/vechain-foundation/people/",
		# "https://www.linkedin.com/company/avalancheavax/people/",
		# "https://www.linkedin.com/company/polkadot-network/people/",
		# "https://www.linkedin.com/company/hellohashgraph/people/",
		# "https://www.linkedin.com/company/coinbase-asset-management/people/",
		# "https://www.linkedin.com/company/tokinvest/people/",
		# "https://www.linkedin.com/company/xdc-foundation/people/",
		# "https://www.linkedin.com/company/hederafndn/people/",
		# "https://www.linkedin.com/company/rippleofficial/people/",
		# "https://www.linkedin.com/company/hedera-network/people/",
		# "https://www.linkedin.com/company/binance/people/",
		# "https://www.linkedin.com/company/chainlink-labs/people/",
		# "https://www.linkedin.com/company/uniswaporg/people/",
		# "https://www.linkedin.com/company/benzinga/people/",
		# "https://www.linkedin.com/company/coingecko/people/",
		# "https://www.linkedin.com/company/coingeek/people/",
		# "https://www.linkedin.com/company/crypto-banter/people/",
		# "https://www.linkedin.com/company/coinpedia/people/",
		# "https://www.linkedin.com/company/defi-planet/people/",
		# "https://www.linkedin.com/company/cryptocom/people/",
		# "https://www.linkedin.com/company/bitcoin-conference/people/",
		# "https://www.linkedin.com/company/btctimes/people/",
		# "https://www.linkedin.com/company/maraholdings/people/",
		# "https://www.linkedin.com/company/cryptonewscom/people/",
		# "https://www.linkedin.com/company/cryptopolitan/people/",
		# "https://www.linkedin.com/company/coingape/people/",
		# "https://www.linkedin.com/company/bitcoin-magazine/people/",
		# "https://www.linkedin.com/company/bitcoin-magazine-pro/people/",
		# "https://www.linkedin.com/company/tokenized-podcast/people/",
		# "https://www.linkedin.com/company/cointelegraph-france/people/",
		# "https://www.linkedin.com/company/cointelegraph-es/people/",
		# "https://www.linkedin.com/company/cointelegraph-ar/people/",
		# "https://www.linkedin.com/company/cointelegraph-brasil/people/",
		# "https://www.linkedin.com/company/cointelegraph-italy/people/",
		"https://www.linkedin.com/company/dow-jones/people/",
		"https://www.linkedin.com/company/the-new-york-times/people/",
		"https://www.linkedin.com/company/quartzmedia/people/",

		# Add more company URLs here
	]
	
	while True:
		print("\nSelect an option:")
		print("1. Run Part I: Scan company pages for relevant profiles")
		print("2. Run Part II: Send connection requests")
		print("3. Run both Part I and Part II")
		print("4. Exit")
		
		choice = input("Enter your choice (1-4): ")
		
		if choice == "1":
			await part1_scan_companies(linkedin_username, linkedin_password, company_urls)
		elif choice == "2":
			await part2_send_connection_requests(linkedin_username, linkedin_password)
		elif choice == "3":
			await part1_scan_companies(linkedin_username, linkedin_password, company_urls)
			await part2_send_connection_requests(linkedin_username, linkedin_password)
		elif choice == "4":
			await part3_get_sales_search(linkedin_username, linkedin_password)
			# break
		elif choice == "5":
			break
		else:
			print("Invalid choice. Please enter a number between 1 and 4.")
	
	print("Script execution complete.")

# Main entry point
if __name__ == "__main__":
	asyncio.run(main())