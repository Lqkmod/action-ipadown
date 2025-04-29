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
    ApplicationHandlerStop
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

# ID Nhóm chính để thống kê. Bill được gửi từ PM.
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
user_fl_cooldown = defaultdict(dict) # Sử dụng defaultdict cho dễ quản lý cooldown /fl
user_getkey_cooldown = {}
valid_keys = {}
activated_users = {}
vip_users = {}
active_treo_tasks = defaultdict(dict) # Sử dụng defaultdict
persistent_treo_configs = defaultdict(dict) # Sử dụng defaultdict
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
# ... (Giữ nguyên các kiểm tra cấu hình ban đầu) ...
if not BOT_TOKEN or BOT_TOKEN == "7416039734:AAHi1YS3uxLGg_KAyqddbZL8OxXB1wamga8": logger.critical("!!! BOT_TOKEN missing or placeholder !!!"); exit(1)
if not BILL_FORWARD_TARGET_ID or not isinstance(BILL_FORWARD_TARGET_ID, int): logger.critical("!!! BILL_FORWARD_TARGET_ID missing or invalid !!!"); exit(1)
# ...

# --- Hàm lưu/tải dữ liệu ---
def save_data():
    global persistent_treo_configs, user_fl_cooldown, active_treo_tasks # Khai báo global các biến có thể thay đổi struct
    # Chuyển đổi các dict về dạng lưu trữ an toàn (string keys)
    data_to_save = {
        "valid_keys": valid_keys,
        "activated_users": {str(k): v for k, v in activated_users.items()},
        "vip_users": {str(k): v for k, v in vip_users.items()},
        "user_cooldowns": {
            "tim": {str(k): v for k, v in user_tim_cooldown.items()},
            "fl": {str(uid): dict(targets) for uid, targets in user_fl_cooldown.items()}, # Convert defaultdict back
            "getkey": {str(k): v for k, v in user_getkey_cooldown.items()}
        },
        "treo_stats": {str(uid): dict(targets) for uid, targets in treo_stats.items()}, # Convert defaultdict
        "last_stats_report_time": last_stats_report_time,
        "persistent_treo_configs": {str(uid): dict(targets) for uid, targets in persistent_treo_configs.items()} # Convert defaultdict
    }
    try:
        temp_file = DATA_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, DATA_FILE) # Atomic replace
        logger.debug(f"Data saved successfully to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data to {DATA_FILE}: {e}", exc_info=True)
        if os.path.exists(temp_file):
            try: os.remove(temp_file)
            except Exception as e_rem: logger.error(f"Failed to remove temporary save file {temp_file}: {e_rem}")

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
                # Load user_fl_cooldown vào defaultdict
                user_fl_cooldown = defaultdict(dict)
                loaded_fl = all_cooldowns.get("fl", {})
                for uid, targets in loaded_fl.items():
                    if isinstance(targets, dict): user_fl_cooldown[str(uid)] = targets # Key phải là string
                user_getkey_cooldown = all_cooldowns.get("getkey", {})

                # Load treo_stats vào defaultdict
                treo_stats = defaultdict(lambda: defaultdict(int))
                loaded_stats = data.get("treo_stats", {})
                for uid_str, targets in loaded_stats.items():
                    if isinstance(targets, dict):
                        for target, gain in targets.items():
                             try: treo_stats[str(uid_str)][str(target)] = int(gain)
                             except (ValueError, TypeError): pass # Bỏ qua entry lỗi

                last_stats_report_time = data.get("last_stats_report_time", 0)

                # Load persistent_treo_configs vào defaultdict
                persistent_treo_configs = defaultdict(dict)
                loaded_persistent_treo = data.get("persistent_treo_configs", {})
                for uid_str, configs in loaded_persistent_treo.items():
                    if isinstance(configs, dict):
                        valid_configs = {}
                        for target, chatid in configs.items():
                             try: valid_configs[str(target)] = int(chatid)
                             except (ValueError, TypeError): pass # Bỏ qua entry lỗi
                        if valid_configs: persistent_treo_configs[str(uid_str)] = valid_configs # Key phải là string

                logger.info(f"Data loaded successfully from {DATA_FILE}")
        else: # File không tồn tại, khởi tạo các biến global là defaultdict/set/dict rỗng
             logger.info(f"{DATA_FILE} not found, initializing empty structures.")
             valid_keys, activated_users, vip_users = {}, {}, {}
             user_tim_cooldown, user_getkey_cooldown = {}, {}
             user_fl_cooldown = defaultdict(dict)
             treo_stats = defaultdict(lambda: defaultdict(int))
             persistent_treo_configs = defaultdict(dict)
             last_stats_report_time = 0
    except (json.JSONDecodeError, TypeError, Exception) as e: # Nếu file lỗi, cũng khởi tạo rỗng
        logger.error(f"Failed to load/parse {DATA_FILE}: {e}. Using empty structures.", exc_info=True)
        valid_keys, activated_users, vip_users = {}, {}, {}
        user_tim_cooldown, user_getkey_cooldown = {}, {}
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
    except (Forbidden, BadRequest): pass # Ignore common deletion errors silently
    except Exception as e: logger.warning(f"Error deleting msg {msg_id} in {chat_id}: {e}")

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
        sent_msg = await context.bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=True, reply_to_message_id=reply_to)
        if sent_msg and context.job_queue:
            job_name = f"del_tmp_{chat_id}_{sent_msg.message_id}"
            context.job_queue.run_once(delete_message_job, duration, data={'chat_id': chat_id, 'message_id': sent_msg.message_id}, name=job_name)
    except BadRequest as e: # Handle reply not found specifically
        if "reply message not found" in str(e).lower() and reply_to:
            try: # Send without replying
                sent_msg = await context.bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=True)
                if sent_msg and context.job_queue:
                    job_name = f"del_tmp_{chat_id}_{sent_msg.message_id}_noreply"
                    context.job_queue.run_once(delete_message_job, duration, data={'chat_id': chat_id, 'message_id': sent_msg.message_id}, name=job_name)
            except Exception as e_send: logger.warning(f"Error sending temp msg (noreply) to {chat_id}: {e_send}")
        else: logger.warning(f"BadRequest sending temp msg to {chat_id}: {e}")
    except Exception as e: logger.warning(f"Error sending temp msg to {chat_id}: {e}")

def generate_random_key(length=8):
    return f"Dinotool-{''.join(random.choices(string.ascii_uppercase + string.digits, k=length))}"

# --- Hàm dừng Task ---
async def stop_treo_task(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE, reason: str = "Unknown") -> bool:
    global persistent_treo_configs, active_treo_tasks
    stopped = False
    # Dừng task runtime nếu có
    if target_username in active_treo_tasks.get(user_id_str, {}):
        task = active_treo_tasks[user_id_str][target_username]
        if task and not task.done():
            task.cancel()
            try: await asyncio.wait_for(task, timeout=0.5) # Chờ hủy ngắn
            except (asyncio.CancelledError, asyncio.TimeoutError): pass
            except Exception as e: logger.warning(f"Error awaiting task cancel {user_id_str}@{target_username}: {e}")
        del active_treo_tasks[user_id_str][target_username]
        if not active_treo_tasks[user_id_str]: del active_treo_tasks[user_id_str] # Xóa user nếu rỗng
        logger.info(f"Stopped runtime task for {user_id_str} -> @{target_username}. Reason: {reason}")
        stopped = True
    # Xóa config persistent nếu có
    if target_username in persistent_treo_configs.get(user_id_str, {}):
        del persistent_treo_configs[user_id_str][target_username]
        if not persistent_treo_configs[user_id_str]: del persistent_treo_configs[user_id_str] # Xóa user nếu rỗng
        logger.info(f"Removed persistent config for {user_id_str} -> @{target_username}.")
        save_data() # Lưu ngay sau khi xóa config
        stopped = True
    return stopped

async def stop_all_treo_tasks_for_user(user_id_str: str, context: ContextTypes.DEFAULT_TYPE, reason: str = "Unknown"):
    targets_runtime = list(active_treo_tasks.get(user_id_str, {}).keys())
    targets_persistent = list(persistent_treo_configs.get(user_id_str, {}).keys())
    all_targets = set(targets_runtime + targets_persistent)
    if not all_targets: return 0
    logger.info(f"Stopping all {len(all_targets)} tasks/configs for user {user_id_str}. Reason: {reason}")
    stopped_count = 0
    # Quan trọng: Lặp qua list cố định, không lặp qua set/dict đang thay đổi
    for target in list(all_targets):
        if await stop_treo_task(user_id_str, target, context, reason):
            stopped_count += 1
    # save_data() được gọi trong stop_treo_task nếu persistent thay đổi
    logger.info(f"Finished stopping for {user_id_str}. Stopped/removed {stopped_count} items.")
    return stopped_count

# --- Cleanup Job ---
async def cleanup_expired_data(context: ContextTypes.DEFAULT_TYPE):
    global valid_keys, activated_users, vip_users
    current_time = time.time()
    keys_removed = 0; users_deactivated_key = 0; users_deactivated_vip = 0; vip_tasks_stopped = 0
    basic_data_changed = False

    # --- Dọn dẹp Keys ---
    keys_to_remove = [k for k, d in valid_keys.items() if d.get("used_by") is None and current_time > d.get("expiry_time", 0)]
    if keys_to_remove:
        keys_removed = len(keys_to_remove)
        for k in keys_to_remove: del valid_keys[k]
        basic_data_changed = True
        logger.info(f"[Cleanup] Removed {keys_removed} expired unused keys.")

    # --- Dọn dẹp Activations ---
    users_to_remove_act = [uid for uid, exp in activated_users.items() if current_time > exp]
    if users_to_remove_act:
        users_deactivated_key = len(users_to_remove_act)
        for uid in users_to_remove_act: del activated_users[uid]
        basic_data_changed = True
        logger.info(f"[Cleanup] Deactivated {users_deactivated_key} users (key expired).")

    # --- Dọn dẹp VIPs ---
    users_to_remove_vip = [uid for uid, data in vip_users.items() if current_time > data.get("expiry", 0)]
    if users_to_remove_vip:
        users_deactivated_vip = len(users_to_remove_vip)
        app = context.application # Lấy application để tạo task
        for uid_str in users_to_remove_vip:
            if uid_str in vip_users: del vip_users[uid_str]; basic_data_changed = True
            # Dừng task của user VIP hết hạn (chạy ngầm)
            logger.info(f"[Cleanup] Scheduling task stop for expired VIP: {uid_str}")
            app.create_task(stop_all_treo_tasks_for_user(uid_str, context, "VIP Expired Cleanup"), name=f"cleanup_stop_{uid_str}")
            vip_tasks_stopped += 1 # Chỉ đếm số user được lên lịch dừng, không phải số task
        logger.info(f"[Cleanup] Deactivated {users_deactivated_vip} VIP users and scheduled task stops.")

    if basic_data_changed: save_data()

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
    ua = f'DinoToolBot/1.0 (+https://t.me/your_bot_username)' # Thay username bot của bạn
    try:
        async with httpx.AsyncClient(verify=False, timeout=90.0, headers={'User-Agent': ua}) as client:
            resp = await client.get(FOLLOW_API_URL_BASE, params=params)
            # (Code xử lý response, parse JSON/text, check status như cũ)
            # ... (phần này giữ nguyên logic parse và xử lý lỗi response)
            content_type = resp.headers.get("content-type", "").lower()
            resp_bytes = await resp.aread(); response_text = "N/A"; decoded = False
            try: # Decode robustly
                encs = ['utf-8', 'latin-1']; txt=""
                for enc in encs:
                    try: txt = resp_bytes.decode(enc, errors='strict'); decoded=True; break
                    except: continue
                if not decoded: txt = resp_bytes.decode('utf-8', errors='replace')
                response_text = txt[:1000] # Limit log length
            except Exception as e: logger.warning(f"Decode fail @{target_username}: {e}")

            if resp.status_code == 200:
                if "application/json" in content_type:
                    try:
                        data = json.loads(resp_bytes); logger.debug(f"API @{target_username} JSON: {data}")
                        result["data"] = data; status = data.get("status"); msg = data.get("message")
                        result["success"] = str(status).lower() in ['true', 'success', 'ok'] if status is not None else False
                        result["message"] = str(msg) if msg else ("Thành công" if result["success"] else "Thất bại không rõ")
                    except Exception as e: result["message"] = "Lỗi parse JSON"; result["success"] = False; logger.error(f"JSON parse err @{target_username}: {e} - text: {response_text}")
                else: # Not JSON but 200 OK
                     result["success"] = "lỗi" not in response_text.lower() and "error" not in response_text.lower() # Heuristic
                     result["message"] = "Thành công (phản hồi text)" if result["success"] else f"Lỗi API (phản hồi text): {response_text[:100]}"
            else: result["message"] = f"Lỗi API ({resp.status_code})"; result["success"] = False
    except httpx.TimeoutException: result["message"] = f"Timeout API @{target_username}"; result["success"]=False
    except httpx.RequestError as e: result["message"]=f"Lỗi mạng API @{target_username}"; result["success"]=False; logger.warning(f"Net err @{target_username}:{e}")
    except Exception as e: result["message"]="Lỗi hệ thống"; result["success"]=False; logger.error(f"API Call err @{target_username}:{e}", exc_info=True)

    logger.info(f"API @{target_username} Res: S={result['success']}, M='{result['message'][:60]}...'")
    return result

# --- Handlers Commands ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user = update.effective_user; act_h = ACTIVATION_DURATION_SECONDS // 3600
    msg = (f"👋 Chào {user.mention_html()}!\n"
           f"🤖 DinoTool Bot đây.\n\n"
           f"✨ Free: <code>/getkey</code>➜Lấy Key➜<code>/nhapkey <key></code>➜Dùng <code>/tim</code>, <code>/fl</code> ({act_h}h).\n"
           f"👑 VIP: <code>/muatt</code>. VIP có <code>/treo</code>, <code>/dungtreo</code>, <code>/listtreo</code>.\n\n"
           f"ℹ️ Lệnh: <code>/lenh</code>\n"
           f"💬 Hỗ trợ: Admin <a href='tg://user?id={ADMIN_USER_ID}'>tại đây</a>.")
    try: await update.message.reply_html(msg, disable_web_page_preview=True)
    except Exception as e: logger.warning(f"Start cmd err {user.id}: {e}")

async def lenh_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; user_id=user.id; user_id_str=str(user_id)
    tf_cd_m=TIM_FL_COOLDOWN_SECONDS//60; gk_cd_m=GETKEY_COOLDOWN_SECONDS//60; act_h=ACTIVATION_DURATION_SECONDS//3600; key_exp_h=KEY_EXPIRY_SECONDS//3600; treo_int_m=TREO_INTERVAL_SECONDS//60
    is_vip=is_user_vip(user_id); is_key=is_user_activated_by_key(user_id); can_std=is_vip or is_key
    status=[f"👤 {user.mention_html()} (<code>{user_id}</code>)"]
    exp_str="?"
    if is_vip:
        try: exp_str=datetime.fromtimestamp(vip_users[user_id_str]['expiry']).strftime('%d/%m')
        except: pass
        status.append(f"👑 VIP: ✅ (Hết hạn: {exp_str}, Limit: {get_vip_limit(user_id)})")
    elif is_key:
        try: exp_str=datetime.fromtimestamp(activated_users[user_id_str]).strftime('%d/%m %H:%M')
        except: pass
        status.append(f"🔑 Key: ✅ (Hết hạn: {exp_str})")
    else: status.append("▫️ Status: Thường")
    status.append(f"⚡️ /tim, /fl: {'✅' if can_std else '❌ (Cần VIP/Key)'}")
    status.append(f"⚙️ /treo: {'✅ ('+str(len(persistent_treo_configs[user_id_str]))+'/'+str(get_vip_limit(user_id))+')' if is_vip else '❌ (Chỉ VIP)'}")

    cmds=["\n📜=== LỆNH ===📜", "🔑 <b>Key Free:</b>",
          f"  <code>/getkey</code> (Lấy link, ⏳{gk_cd_m}p, Key {key_exp_h}h)",
          f"  <code>/nhapkey <key></code> (Kích hoạt {act_h}h)",
          "❤️ <b>Tương Tác (Cần VIP/Key):</b>",
          f"  <code>/tim <link_video></code> (Tăng tim, ⏳ {tf_cd_m}p)",
          f"  <code>/fl <username></code> (Tăng follow, ⏳ {tf_cd_m}p/user)",
          "👑 <b>VIP:</b>",
          f"  <code>/muatt</code> (Mua VIP)",
          f"  <code>/treo <user></code> (Treo follow {treo_int_m}p/lần)",
          f"  <code>/dungtreo <user></code> (Dừng treo)",
          f"  <code>/listtreo</code> (Xem list treo)"]
    if user_id==ADMIN_USER_ID:
        cmds.extend(["🛠️ <b>Admin:</b>",f"  <code>/addtt <id> <gói></code> (Thêm VIP, Gói: {', '.join(map(str, VIP_PRICES.keys()))})"])
    cmds.extend(["ℹ️ <b>Chung:</b>", f"  <code>/start</code> | <code>/lenh</code>", f"Bot by DinoTool"])
    txt="\n".join(status + cmds)
    try: await delete_user_message(update, context); await context.bot.send_message(user.id, txt, ParseMode.HTML, disable_web_page_preview=True) # Gửi vào PM
    except Exception as e: logger.warning(f"Lenh cmd err {user.id}: {e}")

async def tim_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /tim) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; user_id=user.id; user_id_str=str(user_id); orig_msg_id=update.message.message_id
    if not can_use_feature(user_id): await send_temporary_message(update,context,f"⚠️ {user.mention_html()}, cần VIP/Key",15); await delete_user_message(update,context,orig_msg_id); return
    now=time.time(); last=user_tim_cooldown.get(user_id_str); cooldown=TIM_FL_COOLDOWN_SECONDS
    if last and now - last < cooldown: await send_temporary_message(update,context,f"⏳ Chờ {cooldown-(now-last):.0f}s",10); await delete_user_message(update,context,orig_msg_id); return
    args=context.args; url=None; err=None
    if not args: err="⚠️ Thiếu link."
    elif "tiktok.com/" not in args[0]: err="⚠️ Link không hợp lệ."
    else: m=re.search(r"(https?://\S*tiktok\.com/\S*\d+)", args[0]); url=m.group(1) if m else args[0]
    if err or not url: await send_temporary_message(update,context, err or "⚠️ Lỗi link.",15); await delete_user_message(update,context,orig_msg_id); return
    if not API_KEY: await send_temporary_message(update,context,"❌ Lỗi API Key. Báo Admin.",15); await delete_user_message(update,context,orig_msg_id); return
    logger.info(f"/tim req from {user_id}"); api_url = VIDEO_API_URL_TEMPLATE.format(video_url=url, api_key=API_KEY)
    pmsg=None; ftxt=""; chat_id=update.effective_chat.id
    try:
        pmsg = await update.message.reply_html("⏳ Tim..."); await delete_user_message(update,context,orig_msg_id)
        async with httpx.AsyncClient(verify=False,timeout=60.0) as c: r=await c.get(api_url); d=r.json()
        if r.status_code==200 and d.get("success"):
            user_tim_cooldown[user_id_str]=time.time(); save_data(); dt=d.get("data",{});
            a=html.escape(str(dt.get("author","?"))); v=html.escape(str(dt.get("video_url",url))); db=str(dt.get('digg_before','?')); di=str(dt.get('digg_increased','?')); da=str(dt.get('digg_after','?'))
            ftxt=f"❤️ Tim OK!\n👤{user.mention_html()}\n🎬<a href='{v}'>Video</a> {a}\n👍 {db}➜+{di}➜✅{da}"
        else: ftxt = f"💔 Tim Fail!\nℹ️ {html.escape(d.get('message', 'Lỗi API'))}"
    except Exception as e: ftxt=f"❌ Lỗi: {e}"; logger.error(f"/tim err {user_id}: {e}", exc_info=True)
    finally:
        if pmsg: try: await context.bot.edit_message_text(chat_id, pmsg.message_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)
        except: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, disable_web_page_preview=True) # Send new on edit fail
        else: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)

async def process_fl_request_background(ctx, chat_id, uid_s, uname, msg_id, user_mention):
    # ... (Giữ nguyên logic task nền /fl) ...
    logger.info(f"BG /fl Start: {uid_s} -> @{uname}")
    api_res = await call_follow_api(uid_s, uname, ctx.bot.token); succ=api_res["success"]; msg=api_res["message"]; data=api_res.get("data",{})
    uinfo=""; finfo=""; ftxt=""
    if data: # Parse data if available
        n=html.escape(str(data.get("name","?"))); ttu=html.escape(str(data.get("username",uname)))
        fb=html.escape(str(data.get("followers_before","?"))); fa=html.escape(str(data.get("followers_add","?"))); faf=html.escape(str(data.get("followers_after","?")))
        uinfo = f"👤 <a href='https://tiktok.com/@{ttu}'>{n}</a> (<code>@{ttu}</code>)\n"
        if any(x!="?" for x in [fb,fa,faf]): finfo = f"📊 FL: <code>{fb}</code> "+(f"➜ <b>+{fa}</b>✨ " if fa!="?" and fa!="0" else "")+f"➜ <code>{faf}</code>"
    if succ:
        user_fl_cooldown[uid_s][uname]=time.time(); save_data() # Update cooldown on success
        ftxt = f"✅ Follow OK!\n{uinfo or f'👤 @{html.escape(uname)}\n'}{finfo}"
    else: ftxt = f"❌ Follow Fail!\n🎯 @{html.escape(uname)}\n💬 {html.escape(msg or 'Không rõ')}"
    try: await ctx.bot.edit_message_text(chat_id, msg_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e: logger.warning(f"BG /fl Edit fail {msg_id}: {e}")

async def fl_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /fl) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; user_id=user.id; uid_s=str(user_id); umention=user.mention_html(); orig_msg_id=update.message.message_id
    if not can_use_feature(user_id): await send_temporary_message(update,context,f"⚠️ {umention}, cần VIP/Key",15); await delete_user_message(update,context,orig_msg_id); return
    now=time.time(); cooldown=TIM_FL_COOLDOWN_SECONDS; args=context.args; uname=None; err=None; rgx=r"^[a-zA-Z0-9_.]{2,24}$"
    if not args: err = "⚠️ Thiếu username."
    else: uarg=args[0].strip().lstrip('@');
    if not err and (not uarg or not re.match(rgx, uarg) or uarg.startswith('.') or uarg.endswith('.') or uarg.startswith('_') or uarg.endswith('_')): err=f"⚠️ User <code>{html.escape(args[0])}</code> lỗi."
    elif not err: uname=uarg
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_msg_id); return
    last=user_fl_cooldown[uid_s].get(uname)
    if last and now - last < cooldown: await send_temporary_message(update,context,f"⏳ Chờ {cooldown-(now-last):.0f}s @{uname}",10); await delete_user_message(update,context,orig_msg_id); return
    pmsg=None; chat_id=update.effective_chat.id
    try:
        pmsg = await update.message.reply_html(f"⏳ Follow @{html.escape(uname)}...")
        await delete_user_message(update,context,orig_msg_id)
        context.application.create_task(process_fl_request_background(context,chat_id,uid_s,uname,pmsg.message_id,umention), name=f"fl_{uid_s}_{uname}")
    except Exception as e: logger.error(f"/fl err {user_id}: {e}"); await delete_user_message(update,context,orig_msg_id); # Del original msg if fail
    if pmsg and e: try: await context.bot.edit_message_text(chat_id,pmsg.message_id,"❌ Lỗi") except: pass

async def getkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /getkey) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); now=time.time(); orig_msg_id=update.message.message_id; chat_id=update.effective_chat.id
    last=user_getkey_cooldown.get(uid_s); cooldown=GETKEY_COOLDOWN_SECONDS
    if last and now - last < cooldown: await send_temporary_message(update,context,f"⏳ Chờ {cooldown-(now-last):.0f}s",10); await delete_user_message(update,context,orig_msg_id); return
    gkey = generate_random_key(); while gkey in valid_keys: gkey = generate_random_key()
    target = BLOGSPOT_URL_TEMPLATE.format(key=gkey) + f"&ts={int(now)}"; params={"token":LINK_SHORTENER_API_KEY, "format":"json", "url":target}
    logger.info(f"GetKey req {uid} -> {gkey}")
    pmsg=None; ftxt=""; stored=False; kh=KEY_EXPIRY_SECONDS//3600
    try:
        pmsg = await update.message.reply_html("⏳ Tạo link key..."); await delete_user_message(update,context,orig_msg_id)
        valid_keys[gkey]={"user_id_generator":uid,"expiry_time":now+KEY_EXPIRY_SECONDS,"used_by":None,"activation_time":None}; save_data(); stored=True
        async with httpx.AsyncClient(timeout=30.0) as c: r=await c.get(LINK_SHORTENER_API_BASE_URL, params=params); d=r.json()
        if r.status_code==200 and d.get("status")=="success" and d.get("shortenedUrl"):
            surl=d["shortenedUrl"]; user_getkey_cooldown[uid_s]=now; save_data();
            ftxt=f"🚀 Link Key {user.mention_html()}:\n<a href='{html.escape(surl)}'>{html.escape(surl)}</a>\n➡️Click link»Lấy Key»<code>/nhapkey <key></code> (Key {kh}h)"
        else: ftxt=f"❌ Lỗi tạo link: {html.escape(d.get('message', 'API Error'))}"
    except Exception as e: ftxt=f"❌ Lỗi: {e}"; logger.error(f"/getkey err {uid}: {e}", exc_info=True)
    if not ftxt.startswith("🚀") and stored and gkey in valid_keys and valid_keys[gkey]['used_by'] is None:
        try: del valid_keys[gkey]; save_data(); logger.warning(f"Removed key {gkey} on link fail")
        except: pass
    finally:
        if pmsg: try: await context.bot.edit_message_text(chat_id, pmsg.message_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)
        except: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)
        else: await context.bot.send_message(chat_id, ftxt, ParseMode.HTML, disable_web_page_preview=True)

async def nhapkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /nhapkey) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); now=time.time(); orig_msg_id=update.message.message_id; chat_id=update.effective_chat.id
    args=context.args; key=None; err=None; rgx=re.compile(r"^Dinotool-[A-Z0-9]+$")
    if not args: err="⚠️ Thiếu key."
    elif len(args)>1: err="⚠️ Chỉ nhập key."
    elif not rgx.match(args[0].strip()): err=f"⚠️ Key <code>{html.escape(args[0])}</code> sai."
    else: key=args[0].strip()
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_msg_id); return
    logger.info(f"NhapKey req {uid} -> {key}")
    kdata=valid_keys.get(key); ftxt=""
    if not kdata: ftxt=f"❌ Key <code>{key}</code> không hợp lệ."
    elif kdata.get("used_by"): ftxt=f"❌ Key <code>{key}</code> đã dùng."+(" bởi bạn." if str(kdata['used_by'])==uid_s else "")
    elif now > kdata.get("expiry_time",0): ftxt=f"❌ Key <code>{key}</code> hết hạn."; del valid_keys[key]; save_data()
    else:
        try:
            kdata["used_by"]=uid; kdata["activation_time"]=now; exp_ts=now+ACTIVATION_DURATION_SECONDS; activated_users[uid_s]=exp_ts; save_data()
            exp_dt=datetime.fromtimestamp(exp_ts); exp_str=exp_dt.strftime('%H:%M %d/%m/%Y'); act_h=ACTIVATION_DURATION_SECONDS//3600
            ftxt=f"✅ Kích hoạt OK!\n👤 {user.mention_html()}\n🔑 Key: <code>{key}</code>\n⏳ Dùng đến: {exp_str} ({act_h}h)"
        except Exception as e: ftxt=f"❌ Lỗi kích hoạt: {e}"; logger.error(f"Activate err {uid} {key}: {e}", exc_info=True); # Rollback logic needed?
    await delete_user_message(update,context,orig_msg_id); await update.message.reply_html(ftxt, disable_web_page_preview=True)

async def addtt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /addtt) ...
    if not update or not update.message or not update.effective_user or update.effective_user.id != ADMIN_USER_ID: return
    adm=update.effective_user; args=context.args; err=None; tid=None; dkey=None; lim=None; dur=None; vdays=list(VIP_PRICES.keys()); vdays_s=', '.join(map(str,vdays))
    if len(args)!=2: err=f"⚠️ Cú pháp: /addtt <id> <gói> (Gói:{vdays_s})"
    else:
        try: tid=int(args[0])
        except: err="⚠️ ID lỗi."
        if not err: try: dkey=int(args[1])
        except: err="⚠️ Gói lỗi."
        if not err and dkey not in VIP_PRICES: err=f"⚠️ Gói chỉ: {vdays_s}."
        elif not err: info=VIP_PRICES[dkey]; lim=info["limit"]; dur=info["duration_days"]
    if err: await update.message.reply_html(err); return
    tid_s=str(tid); now=time.time(); current=vip_users.get(tid_s); start=now; op="Nâng cấp"
    if current and current.get('expiry',0)>now: start=current['expiry']; op="Gia hạn"
    new_exp=start+dur*86400; new_exp_s=datetime.fromtimestamp(new_exp).strftime('%H:%M %d/%m/%Y')
    vip_users[tid_s]={"expiry":new_exp, "limit":lim}; save_data(); logger.info(f"Admin {adm.id} {op} {dur}d VIP for {tid_s} -> {new_exp_s} Lim:{lim}")
    adm_msg=f"✅ Đã {op} {dur}d VIP!\n👤 ID:{tid}\n⏳ Hạn:{new_exp_s}\n🚀Limit:{lim}"
    await update.message.reply_html(adm_msg)
    u_m=f"ID<code>{tid}</code>"; try: info=await context.bot.get_chat(tid); u_m=info.mention_html() or u_m except:pass
    u_notify=f"🎉 Chúc mừng {u_m}! Bạn được Admin {op} {dur}d VIP.\nHạn:{new_exp_s}. Limit:{lim}.\n(Lệnh /lenh)"; notify_chat=ALLOWED_GROUP_ID or ADMIN_USER_ID
    try: await context.bot.send_message(notify_chat,u_notify,ParseMode.HTML)
    except Exception as e: logger.error(f"Fail VIP notify {tid} to {notify_chat}: {e}")

# --- Lệnh /muatt (Đã sửa theo yêu cầu: bỏ QR) ---
async def muatt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message or not update.effective_user: return
    chat_id = update.effective_chat.id; user = update.effective_user; original_message_id = update.message.message_id; user_id = user.id
    payment_note = f"{PAYMENT_NOTE_PREFIX} {user_id}"
    text_lines = ["👑 <b>Thông Tin Nâng Cấp VIP - DinoTool</b> 👑",
                  "\nTrở thành VIP để mở khóa <code>/treo</code>, không cần lấy key và nhiều ưu đãi!",
                  "\n💎 <b>Các Gói VIP Hiện Có:</b>"]
    for days_key, info in VIP_PRICES.items():
        text_lines.extend([f"\n⭐️ <b>Gói {info['duration_days']} Ngày:</b>",
                           f"   - 💰 Giá: <b>{info['price']}</b>",
                           f"   - ⏳ Thời hạn: {info['duration_days']} ngày",
                           f"   - 🚀 Treo tối đa: <b>{info['limit']} tài khoản</b> TikTok"])
    text_lines.extend(["\n🏦 <b>Thông tin thanh toán:</b>",
                       f"   - Ngân hàng: <b>{BANK_NAME}</b>",
                       f"   - STK: <a href=\"https://t.me/share/url?url={BANK_ACCOUNT}\"><code>{BANK_ACCOUNT}</code></a> (👈 Click copy)",
                       f"   - Tên chủ TK: <b>{ACCOUNT_NAME}</b>",
                       "\n📝 <b>Nội dung CK (Quan trọng!):</b>",
                       f"   » <code>{payment_note}</code> <a href=\"https://t.me/share/url?url={payment_note}\">(👈 Click copy)</a>",
                       f"   <i>(Sai nội dung xử lý chậm)</i>",
                       "\n📸 <b>Sau Khi Chuyển Khoản Thành Công:</b>",
                       f"   1️⃣ Chụp ảnh màn hình bill.",
                       f"   2️⃣ Nhấn nút 'Gửi Bill Thanh Toán' bên dưới.",
                       f"   3️⃣ Bot sẽ yêu cầu gửi ảnh bill <b>VÀO ĐÂY</b>.", # Nhấn mạnh
                       f"   4️⃣ Gửi ảnh bill vào chat này.",
                       f"   5️⃣ Bot sẽ tự chuyển ảnh đến Admin.",
                       f"   6️⃣ Admin sẽ kiểm tra và kích hoạt.",
                       "\n<i>Cảm ơn bạn đã ủng hộ!</i> ❤️"])
    text = "\n".join(text_lines)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📸 Gửi Bill Thanh Toán", callback_data=f"prompt_send_bill_{user_id}")]] )
    await delete_user_message(update, context, original_message_id)
    # Chỉ gửi tin nhắn text, không gửi ảnh QR nữa
    try:
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True, reply_markup=keyboard)
        logger.info(f"Sent /muatt text info with prompt button to user {user_id} in chat {chat_id}")
    except Exception as e_text:
         logger.error(f"Error sending /muatt text to chat {chat_id}: {e_text}")

# --- Callback và Xử lý Bill ---
async def prompt_send_bill_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query; user = query.from_user; chat_id = query.message.chat.id
    if not query or not user: return
    expected_uid = None; try: expected_uid = int(query.data.split("_")[-1]) except: pass
    if user.id != expected_uid: await query.answer("Nút này không phải của bạn.", show_alert=True); return
    pending_bill_user_ids.add(user.id)
    if context.job_queue: context.job_queue.run_once(remove_pending_bill_user_job, PENDING_BILL_TIMEOUT_SECONDS, data={'user_id': user.id}, name=f"rm_pending_{user.id}")
    await query.answer()
    logger.info(f"User {user.id} click bill btn in {chat_id}. Added to pending.")
    prompt = f"📸 {user.mention_html()}, gửi ảnh bill của bạn <b><u>vào đây</u></b> nhé."
    try: await context.bot.send_message(chat_id, prompt, ParseMode.HTML)
    except Exception as e: logger.warning(f"Fail send bill prompt to {user.id}: {e}")

async def remove_pending_bill_user_job(context: ContextTypes.DEFAULT_TYPE):
    uid = context.job.data.get('user_id')
    if uid in pending_bill_user_ids: pending_bill_user_ids.remove(uid); logger.info(f"Removed {uid} from pending bill (timeout)")

async def handle_photo_bill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or (msg.text and msg.text.startswith('/')): return # Ignore commands/non-messages
    user = update.effective_user; chat = update.effective_chat
    if not user or user.id not in pending_bill_user_ids: return # Ignore if not pending user
    if not (msg.photo or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith('image/'))): return # Ignore non-image

    logger.info(f"Bill from PENDING user {user.id} in {chat.type} ({chat.id}). Forwarding...")
    pending_bill_user_ids.discard(user.id) # Remove from pending
    # Cancel timeout job
    if context.job_queue:
        jobs = context.job_queue.get_jobs_by_name(f"rm_pending_{user.id}")
        for j in jobs: j.schedule_removal()

    # Build caption
    lines = [f"📄 <b>Bill Nhận Được</b>", f"👤 <b>Từ:</b> {user.mention_html()} (<code>{user.id}</code>)"]
    chat_type_str = f"Chat {chat.type} ({chat.id})"
    if chat.title: chat_type_str = f"{html.escape(chat.title)} ({chat.id})"
    lines.append(f"💬 <b>Tại:</b> {chat_type_str}")
    try: link = msg.link; lines.append(f"🔗 <a href='{link}'>Tin nhắn gốc</a>") if link else None
    except: pass
    if msg.caption: lines.append(f"\n📝 <b>Caption:</b>\n{html.escape(msg.caption[:500])}")

    try:
        await context.bot.forward_message(BILL_FORWARD_TARGET_ID, chat.id, msg.message_id)
        await context.bot.send_message(BILL_FORWARD_TARGET_ID, "\n".join(lines), ParseMode.HTML, disable_web_page_preview=True)
        await msg.reply_html("✅ Đã nhận & chuyển bill đến Admin.")
        logger.info(f"Forwarded bill from {user.id} success.")
    except Exception as e:
        logger.error(f"Fail forward bill {user.id} -> {BILL_FORWARD_TARGET_ID}: {e}", exc_info=True)
        await msg.reply_html(f"❌ Lỗi gửi bill! Báo Admin <a href='tg://user?id={ADMIN_USER_ID}'>tại đây</a>.")
        if ADMIN_USER_ID != BILL_FORWARD_TARGET_ID:
            try: await context.bot.send_message(ADMIN_USER_ID, f"⚠️ Lỗi forward bill từ {user.id} ({chat.id}): {e}")
            except: pass
    raise ApplicationHandlerStop # Stop other handlers

# --- Logic Treo (Đã sửa format msg ở trên) ---
async def run_treo_loop(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    user_id_int = int(user_id_str); task_name = f"treo_{user_id_str}_{target_username}"
    logger.info(f"Task Start: {task_name} in chat {chat_id}")
    last_call=0; fails=0; MAX_FAILS=5
    while True:
        try:
            now = time.time()
            # Check task validity
            if active_treo_tasks.get(user_id_str, {}).get(target_username) is not asyncio.current_task():
                logger.warning(f"Task Stop: {task_name} mismatch/removed."); break
            # Check VIP status
            if not is_user_vip(user_id_int):
                logger.warning(f"Task Stop: {task_name} - User {user_id_str} no longer VIP.")
                await stop_treo_task(user_id_str, target_username, context, "VIP Expired Loop Check")
                try: await context.bot.send_message(chat_id,f"ℹ️ Treo @{html.escape(target_username)} dừng do VIP hết hạn.",ParseMode.HTML,disable_notification=True)
                except: pass; break
            # Wait interval
            if last_call > 0:
                wait = TREO_INTERVAL_SECONDS - (now-last_call)
                if wait > 0: await asyncio.sleep(wait)
            last_call=time.time() # Update before call
            # Call API
            logger.info(f"Task Run: {task_name} API Call @{target_username}")
            res = await call_follow_api(user_id_str, target_username, context.bot.token)
            success=res["success"]; msg_api=res["message"] or "N/A"; data=res.get("data",{})
            gain=0; fb="?"; fa="?"
            # Process Result
            if success:
                fails=0 # Reset fails on success
                if isinstance(data,dict):
                    fb = html.escape(str(data.get("followers_before", "?")))
                    fa = html.escape(str(data.get("followers_after", "?")))
                    try: gain_str=str(data.get("followers_add","0")); m=re.search(r'\d+',gain_str); gain=int(m.group(0)) if m else 0
                    except: gain=0
                    if gain>0: treo_stats[user_id_str][target_username] += gain; logger.info(f"Task Stats: {task_name} +{gain}. Total: {treo_stats[user_id_str][target_username]}")
            else: # Handle Failure
                fails+=1; logger.warning(f"Task Fail: {task_name} ({fails}/{MAX_FAILS}). Msg: {msg_api[:70]}")
                if fails >= MAX_FAILS:
                    logger.error(f"Task Stop: {task_name} max failures reached.")
                    await stop_treo_task(user_id_str, target_username, context, f"{MAX_FAILS} Consecutive Fails")
                    try: await context.bot.send_message(chat_id, f"⚠️ Treo @{html.escape(target_username)} dừng do lỗi liên tục.",ParseMode.HTML, disable_notification=True)
                    except: pass; break # Stop loop
            # Send Status Message
            status_lines=[]
            if success:
                status_lines.append(f"✅ Đã Treo @{html.escape(target_username)} thành công!")
                status_lines.append(f"➕ Thêm: <b>{gain}</b>")
                if fb!="?": status_lines.append(f"📊 Trước: <code>{fb}</code>")
                if fa!="?": status_lines.append(f"📊 Hiện tại: <code>{fa}</code>")
            else: # Failure message (not stopping yet)
                 status_lines.append(f"❌ Treo @{html.escape(target_username)} thất bại!")
                 status_lines.append(f"💬 Lý do: <i>{html.escape(msg_api)}</i>")
            sent_status=None
            try: sent_status = await context.bot.send_message(chat_id, "\n".join(status_lines), ParseMode.HTML, disable_notification=True)
            except Forbidden: logger.warning(f"Task Stop: {task_name} forbidden in {chat_id}"); await stop_treo_task(user_id_str, target_username, context, "Forbidden in Chat"); break
            except Exception as e_send: logger.warning(f"Task Send Status Err: {task_name}: {e_send}")
            # Schedule deletion for failure messages
            if not success and sent_status and context.job_queue:
                context.job_queue.run_once(delete_message_job, TREO_FAILURE_MSG_DELETE_DELAY, data={'chat_id': chat_id, 'message_id': sent_status.message_id}, name=f"del_fail_{sent_status.message_id}")
        except asyncio.CancelledError: logger.info(f"Task Cancelled: {task_name}"); break # Break cleanly on cancellation
        except Exception as loop_e: # Catch unexpected errors in loop
            logger.error(f"Task Error: {task_name} loop error: {loop_e}", exc_info=True)
            try: await context.bot.send_message(chat_id,f"💥 Lỗi Treo @{html.escape(target_username)}: {loop_e}. Đã dừng.",ParseMode.HTML,disable_notification=True)
            except: pass
            await stop_treo_task(user_id_str, target_username, context, f"Loop Error: {loop_e}")
            break # Stop loop on error
    logger.info(f"Task End: {task_name} stopped.")
    # Final runtime cleanup check
    if target_username in active_treo_tasks.get(user_id_str,{}):
        task_check = active_treo_tasks[user_id_str][target_username]
        if task_check and task_check.done(): # Remove if actually done
             del active_treo_tasks[user_id_str][target_username]
             if not active_treo_tasks[user_id_str]: del active_treo_tasks[user_id_str]
             logger.debug(f"Task Final Cleanup: {task_name} removed from runtime dict.")

# --- Lệnh /treo ---
async def treo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /treo) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; user_id=user.id; uid_s=str(user_id); chat_id=update.effective_chat.id; orig_msg_id=update.message.message_id
    if not is_user_vip(user_id): await send_temporary_message(update,context,"⚠️ /treo chỉ dành cho VIP.",15); await delete_user_message(update,context,orig_msg_id); return
    args=context.args; uname=None; err=None; rgx=r"^[a-zA-Z0-9_.]{2,24}$"
    if not args: err = "⚠️ Thiếu username."
    else: uarg=args[0].strip().lstrip('@')
    if not err and (not uarg or not re.match(rgx, uarg) or uarg.startswith('.') or uarg.endswith('.') or uarg.startswith('_') or uarg.endswith('_')): err=f"⚠️ User <code>{html.escape(args[0])}</code> lỗi."
    elif not err: uname=uarg
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_msg_id); return
    if uname:
        limit=get_vip_limit(user_id); current_count=len(persistent_treo_configs[uid_s])
        if uname in persistent_treo_configs[uid_s]: await send_temporary_message(update,context,f"⚠️ Đã treo <code>@{uname}</code>. /dungtreo để dừng.",15); await delete_user_message(update,context,orig_msg_id); return
        if current_count>=limit: await send_temporary_message(update,context,f"⚠️ Hết slot ({current_count}/{limit}). /dungtreo giải phóng.",15); await delete_user_message(update,context,orig_msg_id); return
        task=None; try:
            app = context.application
            task = app.create_task(run_treo_loop(uid_s, uname, context, chat_id), name=f"treo_{uid_s}_{uname}")
            active_treo_tasks[uid_s][uname]=task; persistent_treo_configs[uid_s][uname]=chat_id; save_data()
            logger.info(f"Task Start&Save OK: {uid_s} -> @{uname} in {chat_id}")
            new_count=len(persistent_treo_configs[uid_s]); interval_m=TREO_INTERVAL_SECONDS//60
            msg=f"✅ Treo OK!\n🎯 @{html.escape(uname)}\n⏳{interval_m}p/lần | Slot: {new_count}/{limit}"
            await update.message.reply_html(msg); await delete_user_message(update,context,orig_msg_id)
        except Exception as e:
             logger.error(f"Treo Start Err {uid_s} @{uname}: {e}", exc_info=True)
             await send_temporary_message(update,context,f"❌ Lỗi bắt đầu treo @{uname}. Báo Admin.",15); await delete_user_message(update,context,orig_msg_id)
             if uid_s in persistent_treo_configs and uname in persistent_treo_configs[uid_s]: del persistent_treo_configs[uid_s][uname]; save_data() # Rollback save
             if task and not task.done(): task.cancel()
             if uname in active_treo_tasks.get(uid_s,{}): del active_treo_tasks[uid_s][uname] # Rollback runtime
    else: logger.error(f"Treo cmd user {user_id}: uname is None!"); await send_temporary_message(update,context,"❌ Lỗi xử lý username",15); await delete_user_message(update,context,orig_msg_id)


# --- Lệnh /dungtreo ---
async def dungtreo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /dungtreo) ...
    if not update or not update.message or not update.effective_user: return
    user = update.effective_user; uid=user.id; uid_s=str(uid); orig_msg_id=update.message.message_id
    args=context.args; uname_stop=None; err=None; current_t=list(persistent_treo_configs[uid_s].keys())
    if not args: err = "⚠️ Thiếu username dừng."+ (f" Đang treo: {', '.join(['@'+t for t in current_t])}" if current_t else " Chưa treo.")
    else: uarg=args[0].strip().lstrip('@'); uname_stop=uarg if uarg else None
    if err: await send_temporary_message(update,context,err,15); await delete_user_message(update,context,orig_msg_id); return
    if uname_stop:
        logger.info(f"DungTreo req {uid} -> @{uname_stop}")
        stopped = await stop_treo_task(uid_s, uname_stop, context, f"/dungtreo by {uid}")
        await delete_user_message(update,context,orig_msg_id)
        if stopped:
            ncount=len(persistent_treo_configs[uid_s]); lim=get_vip_limit(uid); lim_s=lim if is_user_vip(uid) else "N/A"
            await update.message.reply_html(f"✅ Đã dừng treo <code>@{html.escape(uname_stop)}</code>.\n(Slot: {ncount}/{lim_s})")
        else: await send_temporary_message(update,context,f"⚠️ Không tìm thấy <code>@{html.escape(uname_stop)}</code> để dừng.",15)
    else: await send_temporary_message(update,context,f"⚠️ Username trống?",15); await delete_user_message(update,context,orig_msg_id)


# --- Lệnh /listtreo ---
async def listtreo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (Giữ nguyên logic /listtreo) ...
    if not update or not update.message or not update.effective_user: return
    user=update.effective_user; uid=user.id; uid_s=str(uid); orig_msg_id=update.message.message_id; chat_id=update.effective_chat.id
    logger.info(f"ListTreo req {uid} in {chat_id}")
    targets = list(persistent_treo_configs[uid_s].keys())
    lines = [f"📊 List Treo Của {user.mention_html()}"]
    if not targets: lines.append("\nKhông treo tài khoản nào.")
    else:
        lim=get_vip_limit(uid); lim_s=lim if is_user_vip(uid) else "N/A"
        lines.append(f"\n🔍 Treo: <b>{len(targets)} / {lim_s}</b> slot")
        for t in sorted(targets): lines.append(f"  - <code>@{html.escape(t)}</code>")
        lines.append("\nℹ️ Dùng <code>/dungtreo <user></code>")
    txt="\n".join(lines)
    try: await delete_user_message(update,context,orig_msg_id); await context.bot.send_message(chat_id,txt,ParseMode.HTML,disable_web_page_preview=True)
    except Exception as e: logger.warning(f"ListTreo send err {uid}: {e}")

# --- Job Thống kê ---
async def report_treo_stats(context: ContextTypes.DEFAULT_TYPE):
    # ... (Giữ nguyên logic job thống kê) ...
    global last_stats_report_time, treo_stats
    now=time.time(); interval=TREO_STATS_INTERVAL_SECONDS
    if now < last_stats_report_time + interval*0.95 and last_stats_report_time!=0: return # Check time
    logger.info("[Stats Job] Running...")
    chat_id=ALLOWED_GROUP_ID
    if not chat_id: logger.info("[Stats Job] Skipped (No Group ID)"); return
    snapshot={}; try: snapshot=json.loads(json.dumps(treo_stats)) # Deep copy
    except Exception as e: logger.error(f"Stats Snapshot Err: {e}"); return
    treo_stats.clear(); last_stats_report_time = now; save_data(); logger.info("Stats cleared, time updated.")
    if not snapshot: logger.info("No stats data."); return
    top=[]; total=0
    for uid, tgts in snapshot.items():
        if isinstance(tgts,dict):
            for t, g in tgts.items():
                if isinstance(g,int) and g>0: top.append((g,str(uid),str(t))); total+=g
    if not top: logger.info("No positive gains."); return
    top.sort(key=lambda x:x[0], reverse=True); report=[f"📊 Thống Kê Treo Follow (24h)",f"<i>(Tổng: <b>{total:,}</b>)</i>","\n🏆 Top Hiệu Quả:"]
    mentions={}; displayed=0
    for g, uids, tu in top[:10]:
        m=mentions.get(uids)
        if not m: try: info=await context.bot.get_chat(int(uids)); m=info.mention_html() or f"ID:{uids}"; mentions[uids]=m except: m=f"ID:{uids}"
        report.append(f"  🏅 +{g:,} @{html.escape(tu)} (By: {m})"); displayed+=1
    if not displayed: report.append("  <i>Không có dữ liệu.</i>")
    report.append("\n🕒 Auto update 24h")
    try: await context.bot.send_message(chat_id, "\n".join(report), ParseMode.HTML, True, True)
    except Exception as e: logger.error(f"Stats Send Err to {chat_id}: {e}")
    logger.info("Stats Job Finished.")

# --- Shutdown helper ---
async def shutdown_async_tasks(tasks_to_cancel: list[asyncio.Task]):
    # ... (Giữ nguyên logic shutdown helper) ...
    if not tasks_to_cancel: return logger.info("No tasks to cancel.")
    logger.info(f"Cancelling {len(tasks_to_cancel)} tasks...")
    for t in tasks_to_cancel:
        if t and not t.done(): t.cancel()
    await asyncio.gather(*[asyncio.wait_for(t, timeout=1.0) for t in tasks_to_cancel], return_exceptions=True)
    logger.info("Shutdown task wait complete.")

# --- Main ---
def main() -> None:
    start_time=time.time()
    print(f"--- Bot Starting [{datetime.now().isoformat()}] ---")
    # ... Config summary ...
    print("Loading data...")
    load_data() # Load data with proper initialization
    print(f"Load OK. Keys:{len(valid_keys)} Act:{len(activated_users)} VIP:{len(vip_users)} TreoCfg:{sum(len(v) for v in persistent_treo_configs.values())} ")

    # --- Application Setup ---
    app = (Application.builder().token(BOT_TOKEN).job_queue(JobQueue())
             .pool_timeout(120).connect_timeout(60).read_timeout(90).write_timeout(90)
             .build())

    # --- Job Queue Setup ---
    jq = app.job_queue
    if jq:
        jq.run_repeating(cleanup_expired_data, interval=CLEANUP_INTERVAL_SECONDS, first=60, name="cleanup")
        logger.info("Cleanup job scheduled.")
        if ALLOWED_GROUP_ID:
            jq.run_repeating(report_treo_stats, interval=TREO_STATS_INTERVAL_SECONDS, first=120, name="stats_report") # Start sooner
            logger.info("Stats report job scheduled.")
        else: logger.warning("Stats reporting disabled (ALLOWED_GROUP_ID not set).")
    else: logger.critical("JobQueue is not available!")

    # --- Handlers Setup ---
    # Priority -1: Bill handler to catch images early
    app.add_handler(MessageHandler((filters.PHOTO | filters.Document.IMAGE) & (~filters.COMMAND) & filters.UpdateType.MESSAGE, handle_photo_bill), group=-1)

    # Priority 0 (default): Commands and Callbacks
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("lenh", lenh_command))
    app.add_handler(CommandHandler("getkey", getkey_command))
    app.add_handler(CommandHandler("nhapkey", nhapkey_command))
    app.add_handler(CommandHandler("tim", tim_command))
    app.add_handler(CommandHandler("fl", fl_command))
    app.add_handler(CommandHandler("muatt", muatt_command))
    app.add_handler(CommandHandler("treo", treo_command))
    app.add_handler(CommandHandler("dungtreo", dungtreo_command))
    app.add_handler(CommandHandler("listtreo", listtreo_command))
    app.add_handler(CommandHandler("addtt", addtt_command))
    app.add_handler(CallbackQueryHandler(prompt_send_bill_callback, pattern="^prompt_send_bill_\d+$"))

    logger.info("Handlers registered.")

    # --- Restore Treo Tasks ---
    print("Restarting persistent treo tasks...")
    restored_count = 0; cleanup_ids = []; task_tuples = []
    for uid_s, targets in list(persistent_treo_configs.items()): # Iterate copy
        try:
            uid_i = int(uid_s)
            if not is_user_vip(uid_i): cleanup_ids.append(uid_s); continue # Cleanup non-VIP
            limit=get_vip_limit(uid_i); count=0
            for target, cid in list(targets.items()): # Iterate copy
                if count>=limit: logger.warning(f"Restore limit {limit} reached for {uid_s}, removing @{target}"); del persistent_treo_configs[uid_s][target]; continue
                if target not in active_treo_tasks.get(uid_s,{}): # Only if not already active
                    task_tuples.append((uid_s,target,cid)); count+=1
                else: logger.info(f"Restore skip: {uid_s} -> {target} already active."); count+=1
        except Exception as e: logger.error(f"Restore Prep Err user {uid_s}: {e}"); cleanup_ids.append(uid_s) # Cleanup error users

    cleaned=0;
    if cleanup_ids:
        logger.info(f"Cleaning configs for {len(cleanup_ids)} non-VIP/error users...")
        for cuid in cleanup_ids:
             if cuid in persistent_treo_configs: del persistent_treo_configs[cuid]; cleaned+=1
        if cleaned>0: save_data(); logger.info(f"Removed {cleaned} user configs.")

    logger.info(f"Creating {len(task_tuples)} tasks...")
    for uid_s, target, cid in task_tuples:
        try:
             # Pass None context, loop creates its own if needed for send_message
             task = app.create_task(run_treo_loop(uid_s, target, context=None, chat_id=cid), name=f"treo_{uid_s}_{target}_restored")
             active_treo_tasks[uid_s][target] = task; restored_count += 1
        except Exception as e:
            logger.error(f"Restore Task Create Err {uid_s}->{target}: {e}", exc_info=True)
            # Remove persistent config if task creation fails
            if uid_s in persistent_treo_configs and target in persistent_treo_configs[uid_s]:
                del persistent_treo_configs[uid_s][target]; save_data(); logger.warning("Removed persistent config on restore fail.")

    print(f"Restored {restored_count} treo tasks."); print("-" * 30)
    print("Bot Init Complete. Starting polling...")
    logger.info(f"Bot running... (Init took {time.time()-start_time:.2f}s)")

    # --- Run Bot ---
    try: app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e: logger.critical(f"BOT CRASHED: {e}", exc_info=True)
    finally: # Graceful Shutdown
        logger.info("Shutdown initiated...")
        tasks = []
        for targets in active_treo_tasks.values(): tasks.extend([t for t in targets.values() if t and not t.done()])
        if tasks:
             logger.info("Cancelling active tasks...")
             try: asyncio.get_event_loop().run_until_complete(shutdown_async_tasks(tasks))
             except Exception as e_shut: logger.error(f"Shutdown task cancel err: {e_shut}")
        logger.info("Saving final data...")
        save_data()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    main()
