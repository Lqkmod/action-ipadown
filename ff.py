# -*- coding: utf-8 -*-
import logging
import httpx
import json
import html
import os
import time
import random
import string
import re
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict

# Thêm import cho Inline Keyboard
from telegram import Update, Message, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    JobQueue,
    CallbackQueryHandler,
    ApplicationHandlerStop # Cần thiết để dừng handler
)
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, TelegramError

# --- Cấu hình ---
BOT_TOKEN = "7416039734:AAHi1YS3uxLGg_KAyqddbZL8OxXB1wamga8" # <--- TOKEN CỦA BẠN
API_KEY = "khangdino99" # <--- API KEY TIM (VẪN CẦN CHO LỆNH /tim)
ADMIN_USER_ID = 7193749511 # <<< --- ID TELEGRAM CỦA ADMIN (Người quản lý bot)

# --- ID của bot/user nhận bill ---
BILL_FORWARD_TARGET_ID = 7193749511 # <<< --- THAY THẾ BẰNG ID SỐ CỦA @khangtaixiu_bot HOẶC USER ADMIN
# ----------------------------------------------------------------

# ID Nhóm chính để THỐNG KÊ. Bill được gửi từ PM.
ALLOWED_GROUP_ID = -1002191171631 # <--- ID NHÓM CHÍNH CỦA BẠN CHO THỐNG KÊ HOẶC None

LINK_SHORTENER_API_KEY = "cb879a865cf502e831232d53bdf03813caf549906e1d7556580a79b6d422a9f7" # Token Yeumoney
BLOGSPOT_URL_TEMPLATE = "https://khangleefuun.blogspot.com/2025/04/key-ngay-body-font-family-arial-sans_11.html?m=1&ma={key}" # Link đích chứa key
LINK_SHORTENER_API_BASE_URL = "https://yeumoney.com/QL_api.php" # API Yeumoney

# --- Thời gian ---
TIM_FL_COOLDOWN_SECONDS = 15 * 60 # 15 phút
GETKEY_COOLDOWN_SECONDS = 2 * 60  # 2 phút
KEY_EXPIRY_SECONDS = 6 * 3600   # 6 giờ (Key chưa nhập)
ACTIVATION_DURATION_SECONDS = 6 * 3600 # 6 giờ (Sau khi nhập key)
CLEANUP_INTERVAL_SECONDS = 3600 # 1 giờ
TREO_INTERVAL_SECONDS = 15 * 60 # 15 phút (Khoảng cách giữa các lần gọi API /treo)
TREO_FAILURE_MSG_DELETE_DELAY = 5 # 5 giây (Thời gian xoá tin nhắn treo thất bại)
TREO_STATS_INTERVAL_SECONDS = 24 * 3600 # 24 giờ (Khoảng cách thống kê follow tăng)
PENDING_BILL_TIMEOUT_SECONDS = 15 * 60 # 15 phút chờ gửi bill

# --- API Endpoints ---
VIDEO_API_URL_TEMPLATE = "https://nvp310107.x10.mx/tim.php?video_url={video_url}&key={api_key}" # API TIM
FOLLOW_API_URL_BASE = "https://api.thanhtien.site/lynk/dino/telefl.php" # API FOLLOW MỚI

# --- Thông tin VIP ---
VIP_PRICES = {
    15: {"price": "15.000 VND", "limit": 2, "duration_days": 15},
    30: {"price": "30.000 VND", "limit": 5, "duration_days": 30},
}
BANK_ACCOUNT = "KHANGDINO" # <--- THAY STK CỦA BẠN
BANK_NAME = "VCB BANK" # <--- THAY TÊN NGÂN HÀNG
ACCOUNT_NAME = "LE QUOC KHANG" # <--- THAY TÊN CHỦ TK
PAYMENT_NOTE_PREFIX = "VIP DinoTool ID"

# --- Lưu trữ ---
DATA_FILE = "bot_persistent_data.json"

# --- Biến toàn cục ---
user_tim_cooldown = {}
user_fl_cooldown = defaultdict(dict)
user_getkey_cooldown = {}
valid_keys = {}
activated_users = {}
vip_users = {}
active_treo_tasks = defaultdict(dict)
persistent_treo_configs = defaultdict(dict)
treo_stats = defaultdict(lambda: defaultdict(int))
last_stats_report_time = 0
pending_bill_user_ids = set()

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
    handlers=[logging.FileHandler("bot.log", encoding='utf-8'), logging.StreamHandler()]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.JobQueue").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.Application").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# --- Kiểm tra cấu hình ---
if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN": logger.critical("!!! BOT_TOKEN is missing !!!"); exit(1)
if not BILL_FORWARD_TARGET_ID or not isinstance(BILL_FORWARD_TARGET_ID, int): logger.critical("!!! BILL_FORWARD_TARGET_ID missing or invalid !!!"); exit(1)
else: logger.info(f"Bill forwarding target set to: {BILL_FORWARD_TARGET_ID}")
if ALLOWED_GROUP_ID: logger.info(f"Stats reporting restricted to Group ID: {ALLOWED_GROUP_ID}")
else: logger.warning("!!! ALLOWED_GROUP_ID is not set. Stats reporting will be disabled. !!!")
if not LINK_SHORTENER_API_KEY: logger.critical("!!! LINK_SHORTENER_API_KEY is missing !!!"); exit(1)
if not API_KEY: logger.warning("!!! API_KEY (for /tim) missing. /tim might fail. !!!")
if not ADMIN_USER_ID: logger.critical("!!! ADMIN_USER_ID is missing !!!"); exit(1)

# --- Hàm lưu/tải dữ liệu ---
def save_data():
    global persistent_treo_configs, user_fl_cooldown
    data_to_save = {
        "valid_keys": valid_keys,
        "activated_users": {str(k): v for k, v in activated_users.items()},
        "vip_users": {str(k): v for k, v in vip_users.items()},
        "user_cooldowns": {
            "tim": {str(k): v for k, v in user_tim_cooldown.items()},
            "fl": {str(uid): dict(targets) for uid, targets in user_fl_cooldown.items() if targets},
            "getkey": {str(k): v for k, v in user_getkey_cooldown.items()}
        },
        "treo_stats": {str(uid): dict(targets) for uid, targets in treo_stats.items() if targets},
        "last_stats_report_time": last_stats_report_time,
        "persistent_treo_configs": {str(uid): dict(targets) for uid, targets in persistent_treo_configs.items() if targets}
    }
    try:
        temp_file = DATA_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, DATA_FILE)
        logger.debug(f"Data saved to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data: {e}", exc_info=True)
        if os.path.exists(temp_file):
            try: os.remove(temp_file)
            except: pass

def load_data():
    global valid_keys, activated_users, vip_users, user_tim_cooldown, user_fl_cooldown, user_getkey_cooldown, treo_stats, last_stats_report_time, persistent_treo_configs
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            valid_keys = data.get("valid_keys", {})
            activated_users = data.get("activated_users", {})
            vip_users = data.get("vip_users", {})
            all_cooldowns = data.get("user_cooldowns", {})
            user_tim_cooldown = all_cooldowns.get("tim", {})
            user_fl_cooldown = defaultdict(dict, {str(uid): d for uid, d in all_cooldowns.get("fl", {}).items()})
            user_getkey_cooldown = all_cooldowns.get("getkey", {})
            treo_stats = defaultdict(lambda: defaultdict(int), {str(uid): defaultdict(int, d) for uid, d in data.get("treo_stats", {}).items()})
            last_stats_report_time = data.get("last_stats_report_time", 0)
            persistent_treo_configs = defaultdict(dict)
            # Correctly load persistent configs ensuring keys are strings and value is int
            for uid_str, configs_dict in data.get("persistent_treo_configs", {}).items():
                valid_targets = {}
                if isinstance(configs_dict, dict):
                     for target, chatid in configs_dict.items():
                          try: valid_targets[str(target)] = int(chatid) # Validate and convert
                          except (ValueError, TypeError): logger.warning(f"Skipping invalid persistent treo entry: {uid_str} -> {target}:{chatid}")
                if valid_targets: persistent_treo_configs[str(uid_str)] = valid_targets
            logger.info(f"Data loaded from {DATA_FILE}")
        else:
             logger.info(f"{DATA_FILE} not found, initializing empty structures.")
             valid_keys, activated_users, vip_users, user_tim_cooldown, user_getkey_cooldown = {}, {}, {}, {}, {}
             user_fl_cooldown = defaultdict(dict)
             treo_stats = defaultdict(lambda: defaultdict(int))
             persistent_treo_configs = defaultdict(dict)
             last_stats_report_time = 0
    except Exception as e:
        logger.error(f"Failed load/parse {DATA_FILE}: {e}. Using empty structures.", exc_info=True)
        valid_keys, activated_users, vip_users, user_tim_cooldown, user_getkey_cooldown = {}, {}, {}, {}, {}
        user_fl_cooldown = defaultdict(dict)
        treo_stats = defaultdict(lambda: defaultdict(int))
        persistent_treo_configs = defaultdict(dict)
        last_stats_report_time = 0

# --- Hàm trợ giúp ---
async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int | None = None):
    msg_id = message_id or (update.message.message_id if update and update.message else None)
    chat_id = update.effective_chat.id if update and update.effective_chat else None
    if not msg_id or not chat_id: return
    try: await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except (Forbidden, BadRequest): pass # Ignore common errors
    except Exception as e: logger.warning(f"Del msg err {msg_id} in {chat_id}: {e}")

async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data.get('chat_id'); msg_id = context.job.data.get('message_id')
    if chat_id and msg_id:
        try: await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except (Forbidden, BadRequest): pass
        except Exception as e: logger.warning(f"Job del err {context.job.name} msg {msg_id}: {e}")

async def send_temporary_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, duration: int = 15, parse_mode: str = ParseMode.HTML, reply: bool = True):
    if not update or not update.effective_chat: return
    chat_id = update.effective_chat.id; sent_msg = None
    try:
        reply_to = update.message.message_id if reply and update.message else None
        try: # Try replying first
             sent_msg = await context.bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=True, reply_to_message_id=reply_to)
        except BadRequest as e_reply: # If reply failed, send normally
             if reply_to and "reply message not found" in str(e_reply).lower():
                  sent_msg = await context.bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=True)
             else: raise e_reply # Raise other BadRequests
        # Schedule deletion
        if sent_msg and context.job_queue:
            job_name = f"del_tmp_{chat_id}_{sent_msg.message_id}"
            context.job_queue.run_once(delete_message_job, duration, data={'chat_id': chat_id, 'message_id': sent_msg.message_id}, name=job_name)
    except Exception as e: logger.warning(f"Send temp msg err to {chat_id}: {e}")

def generate_random_key(length=8):
    return f"Dinotool-{''.join(random.choices(string.ascii_uppercase + string.digits, k=length))}"

# --- Hàm dừng Task ---
async def stop_treo_task(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE | None, reason: str = "Unknown") -> bool:
    """ Dừng task runtime và xóa config persistent. context=None khi gọi từ shutdown """
    global persistent_treo_configs, active_treo_tasks # Cần khai báo để sửa đổi
    stopped = False
    user_tasks = active_treo_tasks.get(user_id_str)
    if user_tasks and target_username in user_tasks:
        task = user_tasks.pop(target_username, None)
        if task and not task.done():
            task.cancel()
            try: await asyncio.wait_for(task, timeout=0.5) # Ngắn thôi
            except (asyncio.CancelledError, asyncio.TimeoutError): pass
            except Exception as e: logger.warning(f"Await cancel err {user_id_str}@{target_username}: {e}")
        if not user_tasks: # Nếu dict của user rỗng thì xóa key user
            active_treo_tasks.pop(user_id_str, None)
        logger.info(f"Stopped runtime task {user_id_str} -> @{target_username}. Reason: {reason}")
        stopped = True

    user_configs = persistent_treo_configs.get(user_id_str)
    if user_configs and target_username in user_configs:
        user_configs.pop(target_username, None)
        if not user_configs: # Nếu dict của user rỗng thì xóa key user
            persistent_treo_configs.pop(user_id_str, None)
        logger.info(f"Removed persistent config {user_id_str} -> @{target_username}.")
        save_data() # Lưu lại vì config persistent đã thay đổi
        stopped = True

    return stopped

async def stop_all_treo_tasks_for_user(user_id_str: str, context: ContextTypes.DEFAULT_TYPE | None, reason: str = "Unknown"):
    """Dừng tất cả task và xóa config cho user. context=None khi gọi từ shutdown"""
    targets_r = list(active_treo_tasks.get(user_id_str, {}).keys())
    targets_p = list(persistent_treo_configs.get(user_id_str, {}).keys())
    all_tgts = set(targets_r + targets_p)
    if not all_tgts: return 0
    logger.info(f"Stopping all {len(all_tgts)} tasks/configs for {user_id_str}. Reason: {reason}")
    count = 0
    for target in list(all_tgts): # Iterate copy
        if await stop_treo_task(user_id_str, target, context, reason): # context có thể là None
            count += 1
    logger.info(f"Finished stop for {user_id_str}. Stopped/removed {count} items.")
    return count


# --- Cleanup Job ---
async def cleanup_expired_data(context: ContextTypes.DEFAULT_TYPE):
    global valid_keys, activated_users, vip_users
    now = time.time(); removed_k=0; dead_act=0; dead_vip=0; stop_tasks=0; data_changed=False
    logger.debug("[Cleanup] Running cleanup...")
    k_remove = [k for k,d in valid_keys.items() if d.get('used_by') is None and now > d.get('expiry_time', 0)]
    if k_remove: removed_k=len(k_remove); [valid_keys.pop(k,None) for k in k_remove]; data_changed=True
    act_remove = [uid for uid,exp in activated_users.items() if now > exp]
    if act_remove: dead_act=len(act_remove); [activated_users.pop(uid,None) for uid in act_remove]; data_changed=True
    vip_remove = [uid for uid,data in vip_users.items() if now > data.get('expiry',0)]
    if vip_remove:
        dead_vip=len(vip_remove); app = context.application
        for uid_s in vip_remove:
            vip_users.pop(uid_s,None); data_changed=True
            logger.info(f"[Cleanup] Scheduling task stop for expired VIP {uid_s}")
            app.create_task(stop_all_treo_tasks_for_user(uid_s,context,"VIP Expired Cleanup"), name=f"cleanup_stop_{uid_s}") # Context ở đây luôn tồn tại
            stop_tasks+=1
    if data_changed: save_data()
    logger.info(f"[Cleanup] Done. Keys:{removed_k}, Act:{dead_act}, VIP:{dead_vip}, StopSched:{stop_tasks}")

# --- Kiểm tra VIP/Key ---
def is_user_vip(user_id: int) -> bool:
    data = vip_users.get(str(user_id))
    return bool(data and time.time() < data.get("expiry", 0))

def get_vip_limit(user_id: int) -> int:
    return vip_users.get(str(user_id), {}).get("limit", 0) if is_user_vip(user_id) else 0

def is_user_activated_by_key(user_id: int) -> bool:
    expiry = activated_users.get(str(user_id))
    return bool(expiry and time.time() < expiry)

def can_use_feature(user_id: int) -> bool:
    return is_user_vip(user_id) or is_user_activated_by_key(user_id)

# --- API Call Follow ---
async def call_follow_api(user_id_str: str, target_username: str, bot_token: str) -> dict:
    params = {"user": target_username, "userid": user_id_str, "tokenbot": bot_token}
    result = {"success": False, "message": "Lỗi gọi API", "data": None}
    ua = 'DinoToolBot/1.1'
    try:
        async with httpx.AsyncClient(verify=False, timeout=90.0, headers={'User-Agent': ua}) as client:
            resp = await client.get(FOLLOW_API_URL_BASE, params=params)
            content_type = resp.headers.get("content-type", "").lower(); resp_bytes = await resp.aread(); response_text = "N/A"
            try: response_text = resp_bytes.decode('utf-8', errors='replace')[:1000] # Decode đơn giản
            except Exception as e: logger.warning(f"Decode fail @{target_username}: {e}")

            if resp.status_code == 200:
                if "application/json" in content_type:
                    try: data = json.loads(resp_bytes); result["data"] = data; status = data.get("status"); msg = data.get("message")
                    except Exception as e_json: logger.error(f"JSON Parse Error @{target_username}: {e_json} | Text: {response_text}"); result["message"] = "Lỗi JSON API"; result["success"] = False; data=None # Set data=None on fail
                    if data: # Chỉ xử lý nếu parse thành công
                        result["success"] = str(status).lower() in ['true', 'success', 'ok'] if status is not None else False
                        result["message"] = str(msg) if msg else ("Thành công" if result["success"] else "Thất bại?")
                else: # Không phải JSON
                    result["success"] = "lỗi" not in response_text.lower() and "error" not in response_text.lower()
                    result["message"] = "OK (non-JSON)" if result["success"] else f"Lỗi API (text): {response_text[:60]}"
            else: result["message"] = f"Lỗi API ({resp.status_code})"; result["success"] = False
    except httpx.TimeoutException: result["message"]=f"Timeout API @{target_username}"; result["success"]=False
    except httpx.RequestError as e: result["message"]=f"Lỗi mạng @{target_username}"; result["success"]=False; logger.warning(f"Net err @{target_username}: {e}")
    except Exception as e: result["message"]="Lỗi hệ thống bot"; result["success"]=False; logger.error(f"API Call sys err @{target_username}: {e}", exc_info=True)
    # Ensure message is string
    result["message"] = str(result.get("message", "Lỗi không rõ"))
    logger.info(f"API @{target_username} -> S={result['success']}, M='{result['message'][:60]}...'")
    return result

# --- Handlers Commands ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user = update.effective_user; act_h = ACTIVATION_DURATION_SECONDS // 3600
    msg = (f"👋 Chào {user.mention_html()}!\n"
           f"🤖 DinoTool Bot.\n\n"
           f"✨ Free: <code>/getkey</code>➜Lấy Key➜<code>/nhapkey <key></code>➜Dùng <code>/tim</code>,<code>/fl</code>({act_h}h).\n"
           f"👑 VIP: <code>/muatt</code>. VIP có <code>/treo</code>,<code>/dungtreo</code>,<code>/listtreo</code>.\n\n"
           f"ℹ️ <code>/lenh</code> | Hỗ trợ: Admin <a href='tg://user?id={ADMIN_USER_ID}'>tại đây</a>.")
    await update.message.reply_html(msg, disable_web_page_preview=True)

async def lenh_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); is_vip=is_user_vip(uid); is_key=is_user_activated_by_key(uid); can_std=is_vip or is_key
    tf_cd=TIM_FL_COOLDOWN_SECONDS//60; gk_cd=GETKEY_COOLDOWN_SECONDS//60; act_h=ACTIVATION_DURATION_SECONDS//3600; key_h=KEY_EXPIRY_SECONDS//3600; treo_i=TREO_INTERVAL_SECONDS//60
    sts=[f"👤 {user.mention_html()} (<code>{uid}</code>)"]; exp="?"; lim="?"
    if is_vip: try: exp=datetime.fromtimestamp(vip_users[uid_s]['expiry']).strftime('%d/%m') except:pass; lim=get_vip_limit(uid); sts.append(f"👑 VIP: ✅ ({exp}, Lim:{lim})")
    elif is_key: try: exp=datetime.fromtimestamp(activated_users[uid_s]).strftime('%d/%m %H:%M') except:pass; sts.append(f"🔑 Key: ✅ ({exp})")
    else: sts.append("▫️ Status: Thường")
    sts.append(f"⚡️ /tim,/fl: {'✅' if can_std else '❌'}")
    sts.append(f"⚙️ /treo: {'✅ ('+str(len(persistent_treo_configs[uid_s]))+'/'+str(lim)+')' if is_vip else '❌'}")
    cmds=["\n📜=== LỆNH ===📜","🔑 Free:",f" <code>/getkey</code> ({gk_cd}p)",f" <code>/nhapkey</code> <key> ({act_h}h)",
          "❤️ Interact:",f" <code>/tim</code> <link> ({tf_cd}p)",f" <code>/fl</code> <user> ({tf_cd}p)",
          "👑 VIP:",f" <code>/muatt</code>",f" <code>/treo</code> <user> ({treo_i}p/lần)",f" <code>/dungtreo</code> <user>",f" <code>/listtreo</code>"]
    if uid==ADMIN_USER_ID: cmds.extend(["🛠️ Admin:",f" <code>/addtt</code> <id> <gói> ({','.join(map(str,VIP_PRICES.keys()))})"])
    cmds.extend(["ℹ️ Chung:", " <code>/start</code> | <code>/lenh</code>", "Bot by DinoTool"])
    try: await delete_user_message(update,context); await context.bot.send_message(uid, "\n".join(sts+cmds), ParseMode.HTML, True) # Send PM
    except Exception as e: logger.warning(f"Lenh err {uid}: {e}")


async def tim_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); orig_id=update.message.message_id; chat_id=update.effective_chat.id
    if not can_use_feature(uid): await send_temporary_message(update,context,"⚠️ Cần VIP/Key.",15); await delete_user_message(update,context,orig_id); return
    now=time.time(); cd=TIM_FL_COOLDOWN_SECONDS; last=user_tim_cooldown.get(uid_s)
    if last and now-last<cd: await send_temporary_message(update,context,f"⏳ Chờ {cd-(now-last):.0f}s.",10); await delete_user_message(update,context,orig_id); return
    args=context.args; url=None; err=None; if not args: err="⚠️ Thiếu link."
    elif "tiktok.com/" not in args[0]: err="⚠️ Link lỗi."
    else: m=re.search(r"(https?://\S*tiktok\.com/\S*\d+)", args[0]); url=m.group(1) if m else args[0]
    if err or not url: await send_temporary_message(update,context,err or "⚠️ Link lỗi.",15); await delete_user_message(update,context,orig_id); return
    if not API_KEY: await send_temporary_message(update,context,"❌ Lỗi API Key.",15); await delete_user_message(update,context,orig_id); return
    logger.info(f"/tim {uid}"); api_url=VIDEO_API_URL_TEMPLATE.format(video_url=url, api_key=API_KEY)
    pmsg=None; ftxt=""
    try:
        pmsg=await update.message.reply_html("⏳ Tim..."); await delete_user_message(update,context,orig_id)
        async with httpx.AsyncClient(verify=False,timeout=60.0) as c: r=await c.get(api_url); d=r.json()
        if r.status_code==200 and d.get("success"):
            user_tim_cooldown[uid_s]=time.time(); save_data(); dt=d.get("data",{}); a=html.escape(str(dt.get("author","?"))); v=html.escape(str(dt.get("video_url",url))); db=str(dt.get('digg_before','?')); di=str(dt.get('digg_increased','?')); da=str(dt.get('digg_after','?'))
            ftxt=f"❤️ Tim OK!\n👤{user.mention_html()}\n🎬<a href='{v}'>{a}</a>\n👍{db}➜+{di}➜✅{da}"
        else: ftxt=f"💔 Tim Fail!\nℹ️{html.escape(d.get('message','API Error'))}"
    except Exception as e: ftxt=f"❌ Lỗi:{e}"; logger.error(f"/tim err {uid}: {e}")
    finally:
        if pmsg: try: await pmsg.edit_text(ftxt,ParseMode.HTML,disable_web_page_preview=True) except: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, True)
        else: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, True)

async def process_fl_request_background(ctx, chat_id, uid_s, uname, msg_id, user_mention):
    logger.info(f"BG /fl: {uid_s} -> @{uname}")
    res=await call_follow_api(uid_s, uname, ctx.bot.token); succ=res["success"]; msg=res["message"]; data=res.get("data",{})
    uinfo=""; finfo=""; ftxt=""
    if data: n=html.escape(str(data.get("name","?"))); ttu=html.escape(str(data.get("username",uname))); fb=html.escape(str(data.get("followers_before","?"))); fa=html.escape(str(data.get("followers_add","?"))); faf=html.escape(str(data.get("followers_after","?"))); uinfo = f"👤<a href='https://tiktok.com/@{ttu}'>{n}</a>(@{ttu})\n"; if any(x!="?" for x in [fb,fa,faf]): finfo = f"📊FL:<code>{fb}</code>"+(f"➜<b>+{fa}</b>✨ " if fa!="?" and fa!="0" else "")+f"➜<code>{faf}</code>"
    if succ: user_fl_cooldown[uid_s][uname]=time.time(); save_data(); ftxt = f"✅ Follow OK!\n{uinfo or f'👤 @{html.escape(uname)}\n'}{finfo}"
    else: ftxt = f"❌ Follow Fail!\n🎯@{html.escape(uname)}\n💬{html.escape(msg or '?')}"
    try: await ctx.bot.edit_message_text(chat_id, msg_id, ftxt, ParseMode.HTML, True)
    except Exception as e: logger.warning(f"BG /fl Edit {msg_id} err: {e}")

async def fl_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); umention=user.mention_html(); orig_id=update.message.message_id
    if not can_use_feature(uid): await send_temporary_message(update,context,"⚠️ Cần VIP/Key.",15); await delete_user_message(update,context,orig_id); return
    now=time.time(); cool=TIM_FL_COOLDOWN_SECONDS; args=context.args; uname=None; err=None; rgx=r"^[a-zA-Z0-9_.]{2,24}$"
    if not args: err="⚠️ Thiếu user."; else: uarg=args[0].strip().lstrip('@');
    if not err and (not uarg or not re.match(rgx, uarg) or uarg.startswith(('_','.')) or uarg.endswith(('_','.'))): err=f"⚠️ User <code>{html.escape(args[0])}</code> lỗi."
    elif not err: uname=uarg
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_id); return
    last=user_fl_cooldown[uid_s].get(uname)
    if last and now-last<cool: await send_temporary_message(update,context,f"⏳ Chờ {cool-(now-last):.0f}s @{uname}",10); await delete_user_message(update,context,orig_id); return
    pmsg=None; chat_id=update.effective_chat.id
    try:
        pmsg = await update.message.reply_html(f"⏳ Follow @{html.escape(uname)}...")
        await delete_user_message(update,context,orig_id)
        context.application.create_task(process_fl_request_background(context,chat_id,uid_s,uname,pmsg.message_id,umention), name=f"fl_{uid_s}_{uname}")
    except Exception as e: logger.error(f"/fl err {uid}: {e}",exc_info=True); await delete_user_message(update,context,orig_id)
    if pmsg and e: try: await pmsg.edit_text("❌ Lỗi") except: pass


async def getkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); now=time.time(); orig_id=update.message.message_id; chat_id=update.effective_chat.id
    last=user_getkey_cooldown.get(uid_s); cool=GETKEY_COOLDOWN_SECONDS
    if last and now-last<cool: await send_temporary_message(update,context,f"⏳ Chờ {cool-(now-last):.0f}s",10); await delete_user_message(update,context,orig_id); return
    gkey=generate_random_key(); while gkey in valid_keys: gkey=generate_random_key()
    target=BLOGSPOT_URL_TEMPLATE.format(key=gkey)+f"&ts={int(now)}"; params={"token":LINK_SHORTENER_API_KEY,"format":"json","url":target}
    logger.info(f"GetKey {uid}->{gkey}"); pmsg=None; ftxt=""; stored=False; kh=KEY_EXPIRY_SECONDS//3600
    try:
        pmsg=await update.message.reply_html("⏳ Tạo link..."); await delete_user_message(update,context,orig_id)
        valid_keys[gkey]={"user_id_generator":uid,"expiry_time":now+KEY_EXPIRY_SECONDS,"used_by":None,"activation_time":None}; save_data(); stored=True
        async with httpx.AsyncClient(timeout=30.0) as c: r=await c.get(LINK_SHORTENER_API_BASE_URL,params=params); d=r.json()
        if r.status_code==200 and d.get("status")=="success" and d.get("shortenedUrl"): surl=d["shortenedUrl"]; user_getkey_cooldown[uid_s]=now; save_data(); ftxt=f"🚀 Link Key {user.mention_html()}:\n<a href='{html.escape(surl)}'>{html.escape(surl)}</a>\n➡️Click»Lấy Key»<code>/nhapkey <key></code>({kh}h)"
        else: ftxt=f"❌ Lỗi link:{html.escape(d.get('message','?'))}"
    except Exception as e: ftxt=f"❌ Lỗi:{e}"; logger.error(f"Getkey err {uid}: {e}", exc_info=True)
    if not ftxt.startswith("🚀") and stored and gkey in valid_keys and valid_keys[gkey].get('used_by') is None: try: del valid_keys[gkey];save_data();logger.warning("Removed key on fail") except: pass
    finally:
        if pmsg: try: await pmsg.edit_text(ftxt,ParseMode.HTML,True) except: await context.bot.send_message(chat_id,ftxt,ParseMode.HTML,True)
        else: await context.bot.send_message(chat_id,ftxt,ParseMode.HTML,True)


async def nhapkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); now=time.time(); orig_id=update.message.message_id; chat_id=update.effective_chat.id
    args=context.args; key=None; err=None; rgx=re.compile(r"^Dinotool-[A-Z0-9]+$")
    if not args: err="⚠️ Thiếu key."; elif len(args)>1: err="⚠️ Chỉ nhập key."; elif not rgx.match(args[0].strip()): err=f"⚠️ Key lỗi."
    else: key=args[0].strip()
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_id); return
    logger.info(f"NhapKey {uid}->{key}"); kdata=valid_keys.get(key); ftxt=""
    if not kdata: ftxt=f"❌ Key lỗi."; elif kdata.get("used_by"): ftxt=f"❌ Key đã dùng"+(" bởi bạn." if str(kdata.get('used_by'))==uid_s else ".")
    elif now > kdata.get("expiry_time",0): ftxt=f"❌ Key hết hạn."; if key in valid_keys: del valid_keys[key];save_data()
    else:
        try:
            kdata["used_by"]=uid; kdata["activation_time"]=now; exp_ts=now+ACTIVATION_DURATION_SECONDS; activated_users[uid_s]=exp_ts; save_data()
            exp_s=datetime.fromtimestamp(exp_ts).strftime('%H:%M %d/%m/%y'); act_h=ACTIVATION_DURATION_SECONDS//3600
            ftxt=f"✅ OK!\n👤{user.mention_html()}\n🔑<code>{key}</code>\n⏳Dùng đến {exp_s}({act_h}h)"
        except Exception as e: ftxt=f"❌ Lỗi kích hoạt:{e}"; logger.error(f"Activate err {uid} {key}: {e}")
    await delete_user_message(update,context,orig_id); await update.message.reply_html(ftxt,True)


async def addtt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user or update.effective_user.id!=ADMIN_USER_ID: return
    adm=update.effective_user; args=context.args; err=None; tid=None; dkey=None; lim=None; dur=None; vdays=list(VIP_PRICES.keys()); vdays_s=', '.join(map(str,vdays))
    if len(args)!=2: err=f"⚠️ /addtt <id> <gói> ({vdays_s})"; else: try: tid=int(args[0]) except: err="⚠️ ID lỗi."; if not err: try: dkey=int(args[1]); info=VIP_PRICES[dkey]; lim=info['limit']; dur=info['duration_days'] except: err=f"⚠️ Gói lỗi ({vdays_s})."
    if err: await update.message.reply_html(err); return
    tid_s=str(tid); now=time.time(); curr=vip_users.get(tid_s); start=now; op="Nâng cấp"
    if curr and curr.get('expiry',0)>now: start=curr['expiry']; op="Gia hạn"
    new_exp=start+dur*86400; new_exp_s=datetime.fromtimestamp(new_exp).strftime('%d/%m/%y %H:%M')
    vip_users[tid_s]={"expiry":new_exp,"limit":lim}; save_data(); logger.info(f"Admin {adm.id} {op} VIP {dur}d for {tid_s}->{new_exp_s} L:{lim}")
    await update.message.reply_html(f"✅ Đã {op} {dur}d VIP!\n👤ID:{tid}\n⏳Hạn:{new_exp_s}\n🚀Limit:{lim}")
    u_m=f"ID<code>{tid}</code>"; try: info=await context.bot.get_chat(tid); u_m=info.mention_html() or u_m except:pass
    n_msg=f"🎉 {u_m}! Bạn đc Admin {op} {dur}d VIP.\nHạn:{new_exp_s} Limit:{lim}. /lenh."; n_chat=ALLOWED_GROUP_ID or ADMIN_USER_ID
    try: await context.bot.send_message(n_chat,n_msg,ParseMode.HTML)
    except Exception as e: logger.error(f"VIP Notify Fail {tid}: {e}")


# --- Lệnh /muatt (ĐÃ SỬA: Chỉ gửi text) ---
async def muatt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    chat_id = update.effective_chat.id; user = update.effective_user; original_message_id = update.message.message_id; user_id = user.id
    payment_note = f"{PAYMENT_NOTE_PREFIX} {user_id}"
    text_lines = ["👑 <b>Thông Tin Nâng Cấp VIP - DinoTool</b> 👑",
                  "\nVIP: <code>/treo</code>, không cần key, nhiều ưu đãi!",
                  "\n💎 <b>Các Gói VIP:</b>"]
    for days_key, info in VIP_PRICES.items():
        text_lines.append(f"\n⭐️ <b>Gói {info['duration_days']} Ngày:</b> Giá <b>{info['price']}</b> - Limit <b>{info['limit']} user</b>")
    text_lines.extend(["\n🏦 <b>Thanh toán:</b>",
                       f"   - NH: <b>{BANK_NAME}</b>",
                       f"   - STK: <a href=\"https://t.me/share/url?url={BANK_ACCOUNT}\"><code>{BANK_ACCOUNT}</code></a> (👈 Copy)",
                       f"   - Tên TK: <b>{ACCOUNT_NAME}</b>",
                       "\n📝 <b>ND Chuyển Khoản (Quan trọng!):</b>",
                       f"   » <code>{payment_note}</code> <a href=\"https://t.me/share/url?url={payment_note}\">(👈 Copy)</a>",
                       f"   <i>(Sai nội dung xử lý chậm)</i>",
                       "\n📸 <b>Sau Khi Chuyển Khoản:</b>",
                       f"   1️⃣ Chụp ảnh bill.",
                       f"   2️⃣ Nhấn nút 'Gửi Bill' bên dưới.",
                       f"   3️⃣ Bot yêu cầu gửi ảnh <b>VÀO ĐÂY</b>.", # Nhấn mạnh
                       f"   4️⃣ Gửi ảnh vào chat này.",
                       f"   5️⃣ Bot tự chuyển ảnh đến Admin.",
                       f"   6️⃣ Admin kiểm tra và kích hoạt.",
                       "\n<i>Cảm ơn bạn!</i> ❤️"])
    text = "\n".join(text_lines)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📸 Gửi Bill Thanh Toán", callback_data=f"prompt_send_bill_{user_id}")]])
    await delete_user_message(update, context, original_message_id)
    try: # Chỉ gửi text
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True, reply_markup=keyboard)
        logger.info(f"Sent /muatt text to {user_id} in {chat_id}")
    except Exception as e_text: logger.error(f"Error sending /muatt text to {chat_id}: {e_text}")

# --- Callback và Xử lý Bill (Hoạt động qua PM, check pending) ---
async def prompt_send_bill_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; user = query.from_user; chat_id = query.message.chat.id
    if not query or not user: return
    expected_uid = None; try: expected_uid = int(query.data.split("_")[-1]) except: pass
    if user.id != expected_uid: await query.answer("Đây không phải nút của bạn.", show_alert=True); return
    pending_bill_user_ids.add(user.id)
    if context.job_queue: context.job_queue.run_once(remove_pending_bill_user_job, PENDING_BILL_TIMEOUT_SECONDS, data={'user_id': user.id}, name=f"rm_pending_{user.id}")
    await query.answer()
    logger.info(f"User {user.id} clicked bill btn in {chat_id}. Added pending.")
    prompt = f"📸 {user.mention_html()}, gửi ảnh bill của bạn <b><u>vào đây</u></b>." # Yêu cầu gửi vào đây
    try: await context.bot.send_message(chat_id, prompt, ParseMode.HTML)
    except Exception as e: logger.warning(f"Fail send bill prompt to {user.id}: {e}")

async def remove_pending_bill_user_job(context: ContextTypes.DEFAULT_TYPE):
    uid = context.job.data.get('user_id')
    if uid in pending_bill_user_ids: pending_bill_user_ids.discard(uid); logger.info(f"Removed {uid} from pending bill (timeout).")

async def handle_photo_bill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or (msg.text and msg.text.startswith('/')): return
    user = update.effective_user; chat = update.effective_chat
    if not user or not chat: return
    # ----> Chỉ xử lý nếu user đang trong danh sách chờ <----
    if user.id not in pending_bill_user_ids: return
    # ----> Chỉ xử lý nếu là ảnh <----
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith('image/'))): return

    logger.info(f"Bill from PENDING user {user.id} in {chat.type} ({chat.id}). Forwarding...")
    pending_bill_user_ids.discard(user.id) # Xóa khỏi chờ
    # Hủy job timeout
    if context.job_queue: [j.schedule_removal() for j in context.job_queue.get_jobs_by_name(f"rm_pending_{user.id}")]

    # Tạo caption và forward
    lines = [f"📄 <b>Bill Nhận Được</b>", f"👤 <b>Từ:</b> {user.mention_html()} (<code>{user.id}</code>)"]
    cinfo = f"Chat {chat.type} ({chat.id})"; if chat.title: cinfo = f"{html.escape(chat.title)}({chat.id})"; elif chat.type=='private': cinfo="PM"
    lines.append(f"💬 <b>Tại:</b> {cinfo}")
    try: link = msg.link; lines.append(f"🔗 <a href='{link}'>Tin gốc</a>") if link else None except: pass
    if msg.caption: lines.append(f"\n📝 <b>Caption:</b>\n{html.escape(msg.caption[:500])}")

    try: # Gửi đến TARGET_ID
        await context.bot.forward_message(BILL_FORWARD_TARGET_ID, chat.id, msg.message_id)
        await context.bot.send_message(BILL_FORWARD_TARGET_ID, "\n".join(lines), ParseMode.HTML, True)
        logger.info(f"Forwarded bill from {user.id} OK.")
        await msg.reply_html("✅ Đã nhận & chuyển bill.") # Phản hồi user
    except Exception as e: # Xử lý lỗi gửi
        logger.error(f"Fail forward bill {user.id}: {e}", exc_info=True)
        await msg.reply_html(f"❌ Lỗi gửi bill! Báo Admin <a href='tg://user?id={ADMIN_USER_ID}'>tại đây</a>.")
        if ADMIN_USER_ID != BILL_FORWARD_TARGET_ID: try: await context.bot.send_message(ADMIN_USER_ID, f"⚠️ Lỗi forward bill từ {user.id} ({chat.id}): {e}") except: pass

    raise ApplicationHandlerStop # Ngăn handler khác chạy

# --- Logic Treo (ĐÃ SỬA format message) ---
async def run_treo_loop(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE | None, chat_id: int):
    user_id_int = int(user_id_str); task_name = f"treo_{user_id_str}_{target_username}"
    logger.info(f"Task Start: {task_name} in chat {chat_id}")
    last_call=0; fails=0; MAX_FAILS=5
    msg_context = ContextTypes.DEFAULT_TYPE(application=context.application, chat_id=chat_id) if context and hasattr(context, 'application') else None # Context để gửi msg

    while True:
        try:
            now = time.time()
            # Check validity & VIP status
            current_task = active_treo_tasks.get(user_id_str, {}).get(target_username)
            if current_task is not asyncio.current_task(): logger.warning(f"Task Stop: {task_name} mismatch."); break
            if not is_user_vip(user_id_int):
                logger.warning(f"Task Stop: {task_name} user not VIP."); await stop_treo_task(user_id_str, target_username, context, "VIP Expired Check")
                if msg_context: try: await msg_context.bot.send_message(chat_id,f"ℹ️ Treo @{html.escape(target_username)} dừng(VIP hết hạn).", ParseMode.HTML,True) except:pass
                break
            # Wait
            if last_call>0: wait=TREO_INTERVAL_SECONDS-(now-last_call); await asyncio.sleep(wait) if wait>0 else None
            last_call = time.time()
            # Call API
            logger.info(f"Task Run: {task_name} API Call")
            res = await call_follow_api(user_id_str, target_username, context.bot.token if context else BOT_TOKEN) # Lấy token từ context hoặc global
            success=res["success"]; msg_api=res["message"]; data=res.get("data",{}); gain=0; fb="?"; fa="?"
            # Process result
            if success:
                fails=0
                if isinstance(data,dict):
                    fb = html.escape(str(data.get("followers_before", "?")))
                    fa = html.escape(str(data.get("followers_after", "?")))
                    try: g_str=str(data.get("followers_add","0")); m=re.search(r'\d+',g_str); gain=int(m.group(0)) if m else 0
                    except: gain=0
                    if gain>0: treo_stats[user_id_str][target_username]+=gain; logger.info(f"Stats +{gain}")
            else: # Handle fail
                fails+=1; logger.warning(f"Task Fail: {task_name} ({fails}/{MAX_FAILS}). Msg: {msg_api[:60]}")
                if fails>=MAX_FAILS: logger.error(f"Task Stop: {task_name} max fails."); await stop_treo_task(user_id_str,target_username,context,f"{fails} fails")
                if msg_context: try: await msg_context.bot.send_message(chat_id,f"⚠️ Treo @{html.escape(target_username)} dừng(lỗi).", ParseMode.HTML,True) except:pass; break
            # Send status msg (formatted)
            if msg_context:
                sts_lines=[]; sent_sts=None
                try:
                    if success: sts_lines=[f"✅ Đã Treo @{html.escape(target_username)} thành công!", f"➕ Thêm: <b>{gain}</b>"]; if fb!="?":sts_lines.append(f"📊 Trước: <code>{fb}</code>"); if fa!="?":sts_lines.append(f"📊 Hiện tại: <code>{fa}</code>")
                    else: sts_lines=[f"❌ Treo @{html.escape(target_username)} thất bại!", f"💬 Lý do: <i>{html.escape(msg_api)}</i>"]
                    sent_sts = await msg_context.bot.send_message(chat_id, "\n".join(sts_lines), ParseMode.HTML, True)
                    if not success and sent_sts and context and context.job_queue: context.job_queue.run_once(delete_message_job, TREO_FAILURE_MSG_DELETE_DELAY, data={'chat_id': chat_id, 'message_id': sent_sts.message_id}, name=f"del_f_{sent_sts.message_id}")
                except Forbidden: logger.warning(f"Task Stop:{task_name} forbidden {chat_id}."); await stop_treo_task(user_id_str,target_username,context,"Forbidden"); break
                except Exception as e_send: logger.warning(f"Send Status Err:{task_name}:{e_send}")
        except asyncio.CancelledError: logger.info(f"Task Cancelled: {task_name}"); break
        except Exception as loop_e: logger.error(f"Task Loop Err: {task_name}: {loop_e}", exc_info=True); await stop_treo_task(user_id_str,target_username,context,f"Loop Err:{loop_e}"); if msg_context: try: await msg_context.bot.send_message(chat_id,f"💥 Lỗi treo @{target_username}.", ParseMode.HTML, True) except:pass; break
    logger.info(f"Task End: {task_name} stopped.")


# --- Lệnh /treo ---
async def treo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; user_id=user.id; uid_s=str(user_id); chat_id=update.effective_chat.id; orig_id=update.message.message_id
    if not is_user_vip(user_id): await send_temporary_message(update,context,"⚠️ Chỉ VIP.",15); await delete_user_message(update,context,orig_id); return
    args=context.args; uname=None; err=None; rgx=r"^[a-zA-Z0-9_.]{2,24}$"
    if not args: err="⚠️ Thiếu user."; else: uarg=args[0].strip().lstrip('@');
    if not err and (not uarg or not re.match(rgx,uarg) or uarg.startswith(('.','_')) or uarg.endswith(('.','_'))): err=f"⚠️ User <code>{html.escape(args[0])}</code> lỗi."
    elif not err: uname=uarg
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_id); return
    if uname:
        limit=get_vip_limit(user_id); count=len(persistent_treo_configs[uid_s])
        if uname in persistent_treo_configs[uid_s]: await send_temporary_message(update,context,f"⚠️ Đã treo @{uname}.",15); await delete_user_message(update,context,orig_id); return
        if count>=limit: await send_temporary_message(update,context,f"⚠️ Hết slot {count}/{limit}.",15); await delete_user_message(update,context,orig_id); return
        task=None; interval_m=TREO_INTERVAL_SECONDS//60; try:
            app=context.application; task=app.create_task(run_treo_loop(uid_s,uname,context,chat_id), name=f"treo_{uid_s}_{uname}"); active_treo_tasks[uid_s][uname]=task; persistent_treo_configs[uid_s][uname]=chat_id; save_data()
            logger.info(f"Treo Start OK: {uid_s}->@{uname} in {chat_id}"); ncount=len(persistent_treo_configs[uid_s])
            await update.message.reply_html(f"✅ Treo OK!\n🎯 @{html.escape(uname)}\n⏳ {interval_m}p | Slot:{ncount}/{limit}"); await delete_user_message(update,context,orig_id)
        except Exception as e: logger.error(f"Treo Start Err {uid_s} @{uname}: {e}", exc_info=True); await send_temporary_message(update,context,"❌ Lỗi treo.",15); await delete_user_message(update,context,orig_id); # Rollback on fail
        if e: persistent_treo_configs[uid_s].pop(uname,None); save_data(); if task and not task.done():task.cancel(); active_treo_tasks[uid_s].pop(uname,None)


# --- Lệnh /dungtreo ---
async def dungtreo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); orig_id=update.message.message_id
    args=context.args; uname_stop=None; err=None; current_t=list(persistent_treo_configs[uid_s].keys())
    if not args: err="⚠️ Thiếu user dừng."+(f" Đang treo: {', '.join(['@'+t for t in current_t])}" if current_t else "")
    else: uarg=args[0].strip().lstrip('@'); uname_stop=uarg if uarg else None
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_id); return
    if uname_stop:
        logger.info(f"DungTreo {uid}->@{uname_stop}"); stopped=await stop_treo_task(uid_s,uname_stop,context,f"/dungtreo {uid}"); await delete_user_message(update,context,orig_id)
        if stopped: ncount=len(persistent_treo_configs[uid_s]); lim=get_vip_limit(uid); lim_s=lim if is_user_vip(uid) else "N/A"; await update.message.reply_html(f"✅ Đã dừng @{html.escape(uname_stop)}.\n(Slot:{ncount}/{lim_s})")
        else: await send_temporary_message(update,context,f"⚠️ Không tìm thấy @{html.escape(uname_stop)}.",15)
    else: await send_temporary_message(update,context,"⚠️ User trống?",15); await delete_user_message(update,context,orig_id)

# --- Lệnh /listtreo ---
async def listtreo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); orig_id=update.message.message_id; chat_id=update.effective_chat.id
    targets=list(persistent_treo_configs[uid_s].keys()); lines=[f"📊 List Treo {user.mention_html()}"]
    if not targets: lines.append("\nChưa treo tk nào.")
    else: lim=get_vip_limit(uid); lim_s=lim if is_user_vip(uid) else "N/A"; lines.append(f"\n🔍 Treo:<b>{len(targets)}/{lim_s}</b>"); [lines.append(f" -<code>@{html.escape(t)}</code>") for t in sorted(targets)]; lines.append("\nℹ️ /dungtreo <user>")
    try: await delete_user_message(update,context,orig_id); await context.bot.send_message(chat_id,"\n".join(lines),ParseMode.HTML,True)
    except Exception as e: logger.warning(f"ListTreo err {uid}: {e}")


# --- Job Thống kê ---
async def report_treo_stats(context: ContextTypes.DEFAULT_TYPE):
    global last_stats_report_time, treo_stats; now=time.time(); interval=TREO_STATS_INTERVAL_SECONDS
    if now < last_stats_report_time+interval*0.95 and last_stats_report_time!=0: return
    logger.info("[Stats Job] Running..."); chat_id=ALLOWED_GROUP_ID
    if not chat_id: logger.info("Stats skip (No Group)"); return
    snapshot={}; try: snapshot=json.loads(json.dumps(treo_stats)) except: logger.error("Stats snapshot err"); return
    treo_stats.clear(); last_stats_report_time=now; save_data(); logger.info("Stats cleared.")
    if not snapshot: logger.info("No stats data"); return
    top=[]; total=0
    for uid,tgts in snapshot.items():
        if isinstance(tgts,dict): [ (top.append((g,str(uid),str(t))), total:=total+g) for t,g in tgts.items() if isinstance(g,int) and g>0 ]
    if not top: logger.info("No gains"); return
    top.sort(key=lambda x:x[0],reverse=True); rep=[f"📊 Treo Stats (24h)",f"(Tổng:<b>{total:,}</b>)","\n🏆 Top:"]
    mentions={}; disp=0
    for g, uids, tu in top[:10]: m=mentions.get(uids); if not m: try: info=await context.bot.get_chat(int(uids)); m=info.mention_html() or f"ID:{uids}"; mentions[uids]=m except: m=f"ID:{uids}"; rep.append(f"🏅+{g:,}@{html.escape(tu)} (By:{m})"); disp+=1
    if not disp: rep.append("<i>Ko có data.</i>")
    rep.append("\n🕒 Auto 24h"); txt="\n".join(rep)
    try: await context.bot.send_message(chat_id, txt, ParseMode.HTML, True, True)
    except Exception as e: logger.error(f"Stats send err to {chat_id}: {e}")
    logger.info("Stats Job Done.")

# --- Shutdown helper ---
async def shutdown_async_tasks(tasks_to_cancel: list[asyncio.Task]):
    if not tasks_to_cancel: return logger.info("No tasks on shutdown.")
    logger.info(f"Cancelling {len(tasks_to_cancel)} tasks..."); [t.cancel() for t in tasks_to_cancel if t and not t.done()]
    await asyncio.gather(*[asyncio.wait_for(t, timeout=1.0) for t in tasks_to_cancel], return_exceptions=True)
    logger.info("Shutdown wait done.")

# --- Main Function ---
def main() -> None:
    start_time=time.time(); print(f"--- Bot Starting [{datetime.now().isoformat()}] ---")
    # Config summary printout
    print("Loading data...")
    load_data()
    print(f"Load OK. VIP:{len(vip_users)} Treo:{sum(len(v) for v in persistent_treo_configs.values())}/{len(persistent_treo_configs)} users.")

    # App Setup
    app=(Application.builder().token(BOT_TOKEN).job_queue(JobQueue()).pool_timeout(120).connect_timeout(60).read_timeout(90).build())

    # Jobs
    jq = app.job_queue
    if jq:
        jq.run_repeating(cleanup_expired_data, CLEANUP_INTERVAL_SECONDS, 60, name="cleanup")
        if ALLOWED_GROUP_ID: jq.run_repeating(report_treo_stats, TREO_STATS_INTERVAL_SECONDS, 120, name="stats")
        logger.info("Jobs scheduled.")
    else: logger.critical("JobQueue NA!")

    # Handlers
    app.add_handler(MessageHandler((filters.PHOTO|filters.Document.IMAGE)&(~filters.COMMAND)&filters.UpdateType.MESSAGE, handle_photo_bill), group=-1) # Bill handler first
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("lenh", lenh_command))
    app.add_handler(CommandHandler("getkey", getkey_command))
    app.add_handler(CommandHandler("nhapkey", nhapkey_command))
    app.add_handler(CommandHandler("tim", tim_command))
    app.add_handler(CommandHandler("fl", fl_command))
    app.add_handler(CommandHandler("muatt", muatt_command)) # Text only
    app.add_handler(CommandHandler("treo", treo_command)) # Formatted msg
    app.add_handler(CommandHandler("dungtreo", dungtreo_command))
    app.add_handler(CommandHandler("listtreo", listtreo_command))
    app.add_handler(CommandHandler("addtt", addtt_command))
    app.add_handler(CallbackQueryHandler(prompt_send_bill_callback, pattern=r"^prompt_send_bill_\d+$")) # Correct pattern
    logger.info("Handlers registered.")

    # Restore Tasks
    print("Restarting tasks...")
    restored=0; cleanup=[]; tasks=[]
    for uid_s, targets in list(persistent_treo_configs.items()): # Iterate copy
        try:
            uid_i=int(uid_s)
            if not is_user_vip(uid_i): cleanup.append(uid_s); continue # Cleanup non-VIP
            limit=get_vip_limit(uid_i); count=0
            for target, cid in list(targets.items()): # Iterate copy
                if count>=limit: persistent_treo_configs[uid_s].pop(target,None); continue # Remove excess config
                if target not in active_treo_tasks.get(uid_s,{}): tasks.append((uid_s,target,cid)); count+=1
                else: count+=1 # Count active ones too for limit check
        except Exception as e: logger.error(f"Restore Prep Err {uid_s}:{e}"); cleanup.append(uid_s)

    cleaned=0 # Cleanup configs
    if cleanup: [ (persistent_treo_configs.pop(cuid,None), cleaned:=cleaned+1) for cuid in cleanup if cuid in persistent_treo_configs ]; logger.info(f"Cleaned {cleaned} user configs.")
    if cleaned>0: save_data()

    logger.info(f"Creating {len(tasks)} restore tasks...") # Create tasks
    for uid_s, target, cid in tasks:
        try: task=app.create_task(run_treo_loop(uid_s,target,context,cid), name=f"treo_{uid_s}_{target}_restored"); active_treo_tasks[uid_s][target]=task; restored+=1
        except Exception as e: logger.error(f"Restore Create Task {uid_s}@{target} Err:{e}"); persistent_treo_configs[uid_s].pop(target,None); save_data(); # Remove config on fail

    print(f"Restored {restored} tasks."); print(f"Bot Init OK ({time.time()-start_time:.2f}s). Running...")
    logger.info("Bot running...")

    # Run Bot
    try: app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e: logger.critical(f"BOT CRASHED: {e}", exc_info=True)
    finally: # Shutdown
        logger.info("Shutdown..."); tasks=[t for users in active_treo_tasks.values() for t in users.values() if t and not t.done()]
        if tasks: logger.info("Cancelling tasks..."); try: asyncio.get_event_loop().run_until_complete(shutdown_async_tasks(tasks)) except: pass
        logger.info("Final save..."); save_data(); logger.info("Bot stopped.")

if __name__ == "__main__":
    main()
