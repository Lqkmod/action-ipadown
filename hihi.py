
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
    CallbackQueryHandler
)
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, TelegramError

# --- Cấu hình ---
BOT_TOKEN = "7416039734:AAHi1YS3uxLGg_KAyqddbZL8OxXB1wamga8" # <--- TOKEN CỦA BẠN
API_KEY = "khangdino99" # <--- API KEY TIM (VẪN CẦN CHO LỆNH /tim)
ADMIN_USER_ID = 7193749511 # <<< --- ID TELEGRAM CỦA ADMIN (Người quản lý bot)

# --- YÊU CẦU 2: ID của bot @khangtaixiu_bot để nhận bill ---
# !!! QUAN TRỌNG: Bạn cần tìm ID SỐ của bot @khangtaixiu_bot và thay thế giá trị dưới đây !!!
# Cách tìm: Chat với @userinfobot, gửi username @khangtaixiu_bot vào đó.
BILL_FORWARD_TARGET_ID = 7193749511 # <<< --- THAY THẾ BẰNG ID SỐ CỦA @khangtaixiu_bot
# ----------------------------------------------------------------

# ID Nhóm chính để nhận bill và thống kê. Các lệnh khác hoạt động mọi nơi.
# Nếu không muốn giới hạn, đặt thành None, nhưng bill và thống kê sẽ không hoạt động hoặc cần sửa logic.
ALLOWED_GROUP_ID = -1002191171631 # <--- ID NHÓM CHÍNH CỦA BẠN HOẶC None

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

# --- API Endpoints ---
VIDEO_API_URL_TEMPLATE = "https://nvp310107.x10.mx/tim.php?video_url={video_url}&key={api_key}" # API TIM
FOLLOW_API_URL_BASE = "https://api.thanhtien.site/lynk/dino/telefl.php" # API FOLLOW MỚI

# --- Thông tin VIP ---
VIP_PRICES = {
    15: {"price": "15.000 VND", "limit": 2, "duration_days": 15},
    30: {"price": "30.000 VND", "limit": 5, "duration_days": 30},
}
QR_CODE_URL = "https://i.imgur.com/49iY7Ft.jpeg" # Link ảnh QR Code
BANK_ACCOUNT = "KHANGDINO" # <--- THAY STK CỦA BẠN
BANK_NAME = "VCB BANK" # <--- THAY TÊN NGÂN HÀNG
ACCOUNT_NAME = "LE QUOC KHANG" # <--- THAY TÊN CHỦ TK
PAYMENT_NOTE_PREFIX = "VIP DinoTool ID" # Nội dung chuyển khoản sẽ là: "VIP DinoTool ID <user_id>"

# --- Lưu trữ ---
DATA_FILE = "bot_persistent_data.json"

# --- Biến toàn cục ---
user_tim_cooldown = {}
user_fl_cooldown = {} # {user_id_str: {target_username: timestamp}}
user_getkey_cooldown = {}
valid_keys = {} # {key: {"user_id_generator": ..., "expiry_time": ..., "used_by": ..., "activation_time": ...}}
activated_users = {} # {user_id_str: expiry_timestamp} - Người dùng kích hoạt bằng key
vip_users = {} # {user_id_str: {"expiry": expiry_timestamp, "limit": user_limit}} - Người dùng VIP
active_treo_tasks = {} # {user_id_str: {target_username: asyncio.Task}} - Lưu các task /treo đang chạy (runtime)
# --- YÊU CẦU 1: Thêm cấu trúc lưu trữ config treo ---
persistent_treo_configs = {} # {user_id_str: {target_username: chat_id}} - Lưu để khôi phục sau restart

treo_stats = defaultdict(lambda: defaultdict(int)) # {user_id_str: {target_username: gain_since_last_report}}
last_stats_report_time = 0 # Thời điểm báo cáo thống kê gần nhất

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
    handlers=[logging.FileHandler("bot.log", encoding='utf-8'), logging.StreamHandler()] # Log ra file và console
)
# Giảm log nhiễu từ thư viện http và telegram.ext scheduling
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.JobQueue").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.Application").setLevel(logging.INFO) # Giữ INFO cho Application để xem khởi động
logger = logging.getLogger(__name__)

# --- Kiểm tra cấu hình ---
if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN": logger.critical("!!! BOT_TOKEN is missing !!!"); exit(1)
if not BILL_FORWARD_TARGET_ID or not isinstance(BILL_FORWARD_TARGET_ID, int) or BILL_FORWARD_TARGET_ID == 123456789: # Thêm kiểm tra placeholder
    logger.critical("!!! BILL_FORWARD_TARGET_ID is missing, invalid, or still the placeholder! Find the NUMERIC ID of @khangtaixiu_bot using @userinfobot !!!"); exit(1)
else: logger.info(f"Bill forwarding target set to: {BILL_FORWARD_TARGET_ID}")

if ALLOWED_GROUP_ID:
     logger.info(f"Bill forwarding source and Stats reporting restricted to Group ID: {ALLOWED_GROUP_ID}")
else:
     logger.warning("!!! ALLOWED_GROUP_ID is not set. Bill forwarding and Stats reporting will be disabled. !!!")

if not LINK_SHORTENER_API_KEY: logger.critical("!!! LINK_SHORTENER_API_KEY is missing !!!"); exit(1)
if not API_KEY: logger.warning("!!! API_KEY (for /tim) is missing. /tim command might fail. !!!")
if not ADMIN_USER_ID: logger.critical("!!! ADMIN_USER_ID is missing !!!"); exit(1)

# --- Hàm lưu/tải dữ liệu ---
def save_data():
    global persistent_treo_configs # Đảm bảo truy cập biến global
    # Chuyển key là số thành string để đảm bảo tương thích JSON
    string_key_activated_users = {str(k): v for k, v in activated_users.items()}
    string_key_tim_cooldown = {str(k): v for k, v in user_tim_cooldown.items()}
    string_key_fl_cooldown = {str(uid): {uname: ts for uname, ts in udict.items()} for uid, udict in user_fl_cooldown.items()}
    string_key_getkey_cooldown = {str(k): v for k, v in user_getkey_cooldown.items()}
    string_key_vip_users = {str(k): v for k, v in vip_users.items()}
    string_key_treo_stats = {str(uid): dict(targets) for uid, targets in treo_stats.items()}

    # --- YÊU CẦU 1: Lưu persistent_treo_configs ---
    # Đảm bảo key user_id là string, target_username là string, chat_id là int
    string_key_persistent_treo = {
        str(uid): {str(target): int(chatid) for target, chatid in configs.items()}
        for uid, configs in persistent_treo_configs.items() if configs # Chỉ lưu user có config
    }

    data_to_save = {
        "valid_keys": valid_keys,
        "activated_users": string_key_activated_users,
        "vip_users": string_key_vip_users,
        "user_cooldowns": {
            "tim": string_key_tim_cooldown,
            "fl": string_key_fl_cooldown,
            "getkey": string_key_getkey_cooldown
        },
        "treo_stats": string_key_treo_stats,
        "last_stats_report_time": last_stats_report_time,
        # --- YÊU CẦU 1: Thêm vào file lưu trữ ---
        "persistent_treo_configs": string_key_persistent_treo
    }
    try:
        # Sử dụng ghi an toàn hơn (ghi vào file tạm rồi đổi tên)
        temp_file = DATA_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, DATA_FILE)
        logger.debug(f"Data saved successfully to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data to {DATA_FILE}: {e}", exc_info=True)
        # Cố gắng xóa file tạm nếu có lỗi
        if os.path.exists(temp_file):
            try: os.remove(temp_file)
            except Exception as e_rem: logger.error(f"Failed to remove temporary save file {temp_file}: {e_rem}")

def load_data():
    global valid_keys, activated_users, vip_users, user_tim_cooldown, user_fl_cooldown, user_getkey_cooldown, treo_stats, last_stats_report_time, persistent_treo_configs # Thêm persistent_treo_configs
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                valid_keys = data.get("valid_keys", {})
                # Đảm bảo key là string khi tải
                activated_users = {str(k): v for k, v in data.get("activated_users", {}).items()}
                vip_users = {str(k): v for k, v in data.get("vip_users", {}).items()}

                all_cooldowns = data.get("user_cooldowns", {})
                user_tim_cooldown = {str(k): v for k, v in all_cooldowns.get("tim", {}).items()}
                loaded_fl = all_cooldowns.get("fl", {})
                user_fl_cooldown = {str(uid): {uname: ts for uname, ts in udict.items()} for uid, udict in loaded_fl.items()}
                user_getkey_cooldown = {str(k): v for k, v in all_cooldowns.get("getkey", {}).items()}

                # Tải dữ liệu thống kê và chuyển thành defaultdict
                loaded_stats = data.get("treo_stats", {})
                treo_stats = defaultdict(lambda: defaultdict(int))
                for uid_str, targets in loaded_stats.items():
                    for target, gain in targets.items():
                         treo_stats[str(uid_str)][target] = gain # Đảm bảo key user là string

                last_stats_report_time = data.get("last_stats_report_time", 0)

                # --- YÊU CẦU 1: Tải persistent_treo_configs ---
                loaded_persistent_treo = data.get("persistent_treo_configs", {})
                # Chuyển đổi lại cấu trúc khi tải, đảm bảo đúng kiểu dữ liệu
                persistent_treo_configs = {} # Khởi tạo lại trước khi điền
                for uid, configs in loaded_persistent_treo.items():
                    user_id_str = str(uid)
                    persistent_treo_configs[user_id_str] = {}
                    for target, chatid in configs.items():
                         try:
                             persistent_treo_configs[user_id_str][str(target)] = int(chatid)
                         except (ValueError, TypeError):
                             logger.warning(f"Skipping invalid persistent treo config entry: user {user_id_str}, target {target}, chatid {chatid}")


                logger.info(f"Data loaded successfully from {DATA_FILE}")
        else:
            logger.info(f"{DATA_FILE} not found, initializing empty data structures.")
            valid_keys, activated_users, vip_users = {}, {}, {}
            user_tim_cooldown, user_fl_cooldown, user_getkey_cooldown = {}, {}, {}
            treo_stats = defaultdict(lambda: defaultdict(int))
            last_stats_report_time = 0
            persistent_treo_configs = {} # Khởi tạo rỗng
    except (json.JSONDecodeError, TypeError, Exception) as e:
        logger.error(f"Failed to load or parse {DATA_FILE}: {e}. Using empty data structures.", exc_info=True)
        valid_keys, activated_users, vip_users = {}, {}, {}
        user_tim_cooldown, user_fl_cooldown, user_getkey_cooldown = {}, {}, {}
        treo_stats = defaultdict(lambda: defaultdict(int))
        last_stats_report_time = 0
        persistent_treo_configs = {} # Khởi tạo rỗng

# --- Hàm trợ giúp ---
async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int | None = None):
    """Xóa tin nhắn người dùng một cách an toàn."""
    msg_id_to_delete = message_id or (update.message.message_id if update and update.message else None)
    original_chat_id = update.effective_chat.id if update and update.effective_chat else None
    if not msg_id_to_delete or not original_chat_id: return

    try:
        await context.bot.delete_message(chat_id=original_chat_id, message_id=msg_id_to_delete)
        logger.debug(f"Deleted message {msg_id_to_delete} in chat {original_chat_id}")
    except Forbidden:
         logger.debug(f"Cannot delete message {msg_id_to_delete} in chat {original_chat_id}. Bot might not be admin or message too old.")
    except BadRequest as e:
        if "Message to delete not found" in str(e).lower() or "message can't be deleted" in str(e).lower() or "MESSAGE_ID_INVALID" in str(e).lower():
            logger.debug(f"Could not delete message {msg_id_to_delete} (already deleted?): {e}")
        else:
            logger.warning(f"BadRequest error deleting message {msg_id_to_delete} in chat {original_chat_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error deleting message {msg_id_to_delete} in chat {original_chat_id}: {e}", exc_info=True)

async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    """Job được lên lịch để xóa tin nhắn."""
    job_data = context.job.data
    chat_id = job_data.get('chat_id')
    message_id = job_data.get('message_id')
    job_name = context.job.name
    if chat_id and message_id:
        logger.debug(f"Job '{job_name}' running to delete message {message_id} in chat {chat_id}")
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Job '{job_name}' successfully deleted message {message_id}")
        except Forbidden:
             logger.info(f"Job '{job_name}' cannot delete message {message_id}. Bot might not be admin or message too old.")
        except BadRequest as e:
            if "Message to delete not found" in str(e).lower() or "message can't be deleted" in str(e).lower():
                logger.info(f"Job '{job_name}' could not delete message {message_id} (already deleted?): {e}")
            else:
                 logger.warning(f"Job '{job_name}' BadRequest deleting message {message_id}: {e}")
        except TelegramError as e:
             logger.warning(f"Job '{job_name}' Telegram error deleting message {message_id}: {e}")
        except Exception as e:
            logger.error(f"Job '{job_name}' unexpected error deleting message {message_id}: {e}", exc_info=True)
    else:
        logger.warning(f"Job '{job_name}' called missing chat_id or message_id.")

async def send_temporary_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, duration: int = 15, parse_mode: str = ParseMode.HTML, reply: bool = True):
    """Gửi tin nhắn và tự động xóa sau một khoảng thời gian."""
    if not update or not update.effective_chat: return

    chat_id = update.effective_chat.id
    sent_message = None
    try:
        reply_to_msg_id = update.message.message_id if update.message else None
        if reply and reply_to_msg_id:
            try:
                sent_message = await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, disable_web_page_preview=True, reply_to_message_id=reply_to_msg_id)
            except BadRequest as e:
                if "reply message not found" in str(e).lower():
                     logger.debug(f"Reply message {reply_to_msg_id} not found for temporary message. Sending without reply.")
                     sent_message = await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, disable_web_page_preview=True)
                else: raise
        else:
            sent_message = await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, disable_web_page_preview=True)

        if sent_message and context.job_queue:
            job_name = f"del_temp_{chat_id}_{sent_message.message_id}"
            context.job_queue.run_once(
                delete_message_job,
                duration,
                data={'chat_id': chat_id, 'message_id': sent_message.message_id},
                name=job_name
            )
            logger.debug(f"Scheduled job '{job_name}' to delete message {sent_message.message_id} in {duration}s")
    except (BadRequest, Forbidden, TelegramError) as e:
        logger.error(f"Error sending temporary message to {chat_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in send_temporary_message to {chat_id}: {e}", exc_info=True)

def generate_random_key(length=8):
    """Tạo key ngẫu nhiên dạng Dinotool-xxxx."""
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"Dinotool-{random_part}"

# --- YÊU CẦU 1: Sửa stop_treo_task để xóa khỏi persistent config ---
async def stop_treo_task(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE, reason: str = "Unknown") -> bool:
    """Dừng một task treo cụ thể VÀ xóa khỏi persistent config. Trả về True nếu dừng/xóa thành công, False nếu không tìm thấy."""
    global persistent_treo_configs, active_treo_tasks # Cần truy cập để sửa đổi
    task = None
    was_active_runtime = False # Cờ để biết task có thực sự đang chạy trong runtime không
    data_saved = False # Cờ để biết đã lưu data chưa

    # 1. Dừng task đang chạy (nếu có)
    if user_id_str in active_treo_tasks and target_username in active_treo_tasks[user_id_str]:
        task = active_treo_tasks[user_id_str][target_username]
        if task and not task.done():
            was_active_runtime = True
            task.cancel()
            logger.info(f"[Treo Task Stop] Attempting to cancel RUNTIME task for user {user_id_str} -> @{target_username}. Reason: {reason}")
            try:
                await asyncio.wait_for(task, timeout=1.0)
            except asyncio.CancelledError:
                logger.info(f"[Treo Task Stop] Runtime Task {user_id_str} -> @{target_username} confirmed cancelled.")
            except asyncio.TimeoutError:
                 logger.warning(f"[Treo Task Stop] Timeout waiting for cancelled runtime task {user_id_str}->{target_username}.")
            except Exception as e:
                 logger.error(f"[Treo Task Stop] Error awaiting cancelled runtime task for {user_id_str}->{target_username}: {e}")
        # Xóa khỏi runtime dict sau khi xử lý
        del active_treo_tasks[user_id_str][target_username]
        if not active_treo_tasks[user_id_str]:
            del active_treo_tasks[user_id_str]
        logger.info(f"[Treo Task Stop] Removed task entry for {user_id_str} -> @{target_username} from active (runtime) tasks.")
    else:
        logger.debug(f"[Treo Task Stop] No active runtime task found for {user_id_str} -> @{target_username}. Checking persistent config.")

    # 2. Xóa khỏi persistent config (nếu có)
    removed_persistent = False
    if user_id_str in persistent_treo_configs and target_username in persistent_treo_configs[user_id_str]:
        del persistent_treo_configs[user_id_str][target_username]
        if not persistent_treo_configs[user_id_str]:
            del persistent_treo_configs[user_id_str]
        logger.info(f"[Treo Task Stop] Removed entry for {user_id_str} -> @{target_username} from persistent_treo_configs.")
        save_data() # Lưu ngay sau khi xóa persistent config
        data_saved = True
        removed_persistent = True
    else:
         logger.debug(f"[Treo Task Stop] Entry for {user_id_str} -> @{target_username} not found in persistent_treo_configs.")

    # Trả về True nếu task đang chạy bị dừng HOẶC nếu config persistent bị xóa
    return was_active_runtime or removed_persistent


async def stop_all_treo_tasks_for_user(user_id_str: str, context: ContextTypes.DEFAULT_TYPE, reason: str = "Unknown"):
    """Dừng tất cả các task treo của một user và xóa khỏi persistent config."""
    stopped_count = 0
    # Lấy danh sách target từ persistent config VÀ runtime active tasks để đảm bảo xóa hết
    targets_in_persistent = list(persistent_treo_configs.get(user_id_str, {}).keys())
    targets_in_runtime = list(active_treo_tasks.get(user_id_str, {}).keys())
    all_targets_to_check = set(targets_in_persistent + targets_in_runtime)

    if not all_targets_to_check:
        logger.info(f"No active or persistent treo tasks found for user {user_id_str} to stop.")
        return

    logger.info(f"Stopping all {len(all_targets_to_check)} potential treo tasks for user {user_id_str}. Reason: {reason}")
    for target_username in all_targets_to_check:
        # stop_treo_task sẽ xử lý cả runtime và persistent và tự lưu nếu cần
        if await stop_treo_task(user_id_str, target_username, context, reason):
            stopped_count += 1

    # Không cần cleanup thêm ở đây vì stop_treo_task đã làm
    logger.info(f"Finished stopping tasks for user {user_id_str}. Stopped/Removed: {stopped_count}/{len(all_targets_to_check)}")


async def cleanup_expired_data(context: ContextTypes.DEFAULT_TYPE):
    """Job dọn dẹp dữ liệu hết hạn (keys, activations, VIPs)."""
    global valid_keys, activated_users, vip_users, persistent_treo_configs # Thêm persistent
    current_time = time.time()
    keys_to_remove = []
    users_to_deactivate_key = []
    users_to_deactivate_vip = []
    vip_users_to_stop_tasks = [] # User ID cần dừng task treo
    basic_data_changed = False # Cờ cho thay đổi không liên quan đến treo

    logger.info("[Cleanup] Starting cleanup job...")

    # Check expired keys
    for key, data in list(valid_keys.items()):
        try:
            expiry = float(data.get("expiry_time", 0))
            if data.get("used_by") is None and current_time > expiry:
                keys_to_remove.append(key)
        except (ValueError, TypeError):
            keys_to_remove.append(key)

    # Check expired key activations
    for user_id_str, expiry_timestamp in list(activated_users.items()):
        try:
            if current_time > float(expiry_timestamp):
                users_to_deactivate_key.append(user_id_str)
        except (ValueError, TypeError):
            users_to_deactivate_key.append(user_id_str)

    # Check expired VIP activations
    for user_id_str, vip_data in list(vip_users.items()):
        try:
            expiry = float(vip_data.get("expiry", 0))
            if current_time > expiry:
                users_to_deactivate_vip.append(user_id_str)
                vip_users_to_stop_tasks.append(user_id_str) # Add user to stop list
        except (ValueError, TypeError):
            users_to_deactivate_vip.append(user_id_str)
            vip_users_to_stop_tasks.append(user_id_str) # Add user to stop list

    # Perform deletions for non-treo data
    if keys_to_remove:
        logger.info(f"[Cleanup] Removing {len(keys_to_remove)} expired unused keys.")
        for key in keys_to_remove:
            if key in valid_keys: del valid_keys[key]; basic_data_changed = True
    if users_to_deactivate_key:
         logger.info(f"[Cleanup] Deactivating {len(users_to_deactivate_key)} users (key system).")
         for user_id_str in users_to_deactivate_key:
             if user_id_str in activated_users: del activated_users[user_id_str]; basic_data_changed = True
    if users_to_deactivate_vip:
         logger.info(f"[Cleanup] Deactivating {len(users_to_deactivate_vip)} VIP users from list.")
         for user_id_str in users_to_deactivate_vip:
             if user_id_str in vip_users: del vip_users[user_id_str]; basic_data_changed = True

    # Stop tasks for expired VIPs (this will handle persistent config removal and saving)
    if vip_users_to_stop_tasks:
         logger.info(f"[Cleanup] Scheduling stop for tasks of {len(vip_users_to_stop_tasks)} expired/invalid VIP users.")
         app = context.application
         for user_id_str in vip_users_to_stop_tasks:
             app.create_task(
                 stop_all_treo_tasks_for_user(user_id_str, context, reason="VIP Expired/Removed during Cleanup"),
                 name=f"cleanup_stop_tasks_{user_id_str}"
             )

    # Save data only if basic data changed (treo task stopping saves itself)
    if basic_data_changed:
        logger.info("[Cleanup] Basic data changed, saving...")
        save_data()
    else:
        logger.info("[Cleanup] No basic data changes found. Treo task stopping handles its own saving.")
    logger.info("[Cleanup] Cleanup job finished.")


def is_user_vip(user_id: int) -> bool:
    """Kiểm tra trạng thái VIP."""
    user_id_str = str(user_id)
    vip_data = vip_users.get(user_id_str)
    if vip_data:
        try:
            return time.time() < float(vip_data.get("expiry", 0))
        except (ValueError, TypeError): return False
    return False

def get_vip_limit(user_id: int) -> int:
    """Lấy giới hạn treo user của VIP."""
    user_id_str = str(user_id)
    if is_user_vip(user_id):
        return vip_users.get(user_id_str, {}).get("limit", 0)
    return 0

def is_user_activated_by_key(user_id: int) -> bool:
    """Kiểm tra trạng thái kích hoạt bằng key."""
    user_id_str = str(user_id)
    expiry_time_str = activated_users.get(user_id_str)
    if expiry_time_str:
        try: return time.time() < float(expiry_time_str)
        except (ValueError, TypeError): return False
    return False

def can_use_feature(user_id: int) -> bool:
    """Kiểm tra xem user có thể dùng tính năng (/tim, /fl) không."""
    return is_user_vip(user_id) or is_user_activated_by_key(user_id)

# --- Logic API Follow ---
async def call_follow_api(user_id_str: str, target_username: str, bot_token: str) -> dict:
    """Gọi API follow và trả về kết quả."""
    api_params = {"user": target_username, "userid": user_id_str, "tokenbot": bot_token}
    log_api_params = api_params.copy()
    log_api_params["tokenbot"] = f"...{bot_token[-6:]}" if len(bot_token) > 6 else "***"
    logger.info(f"[API Call] User {user_id_str} calling Follow API for @{target_username} with params: {log_api_params}")
    result = {"success": False, "message": "Lỗi không xác định khi gọi API.", "data": None}
    try:
        # Tăng timeout và tắt verify SSL nếu cần
        async with httpx.AsyncClient(verify=False, timeout=90.0) as client:
            resp = await client.get(FOLLOW_API_URL_BASE, params=api_params, headers={'User-Agent': 'TG Bot FL Caller'})
            content_type = resp.headers.get("content-type", "").lower()
            response_text_for_debug = ""
            try:
                # Thử decode với nhiều encoding phổ biến nếu utf-8 lỗi
                encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1']
                for enc in encodings_to_try:
                    try:
                        response_text_for_debug = (await resp.aread()).decode(enc, errors='strict')[:1000]
                        logger.debug(f"[API Call @{target_username}] Decoded response with {enc}")
                        break # Dừng khi decode thành công
                    except UnicodeDecodeError:
                        logger.debug(f"[API Call @{target_username}] Failed to decode with {enc}")
                        continue # Thử encoding tiếp theo
                    except Exception as e_read: # Bắt các lỗi đọc khác
                        logger.warning(f"[API Call @{target_username}] Error reading response body: {e_read}")
                        break
                else: # Nếu vòng lặp hoàn thành mà không break (không decode được)
                    response_text_for_debug = (await resp.aread()).decode('utf-8', errors='replace')[:1000] # Fallback
                    logger.warning(f"[API Call @{target_username}] Could not decode response with common encodings, using replace.")

            except Exception as e_read_outer:
                 logger.error(f"[API Call @{target_username}] Outer error reading response body: {e_read_outer}")

            logger.debug(f"[API Call @{target_username}] Status: {resp.status_code}, Content-Type: {content_type}")

            if resp.status_code == 200:
                # Cho phép cả text/html nếu JSON lỗi, cố gắng tìm message trong đó
                if "application/json" in content_type:
                    try:
                        data = resp.json()
                        logger.debug(f"[API Call @{target_username}] JSON Data: {data}")
                        result["data"] = data
                        api_status = data.get("status")
                        api_message = data.get("message", None) # Để None nếu không có

                        # Ưu tiên status boolean, sau đó mới check string 'true'/'false'
                        if isinstance(api_status, bool):
                            result["success"] = api_status
                        elif isinstance(api_status, str):
                            result["success"] = api_status.lower() == 'true'
                        else: # Nếu status không rõ ràng, coi là false
                            result["success"] = False

                        # Chuẩn hóa message
                        if result["success"] and not api_message:
                            api_message = "Follow thành công."
                        elif not result["success"] and not api_message:
                             api_message = f"Follow thất bại (API status={api_status})."
                        elif api_message is None: # Trường hợp message không tồn tại trong JSON
                             api_message = "Không có thông báo từ API."

                        result["message"] = api_message

                    except json.JSONDecodeError:
                        logger.error(f"[API Call @{target_username}] Response 200 OK (JSON type) but not valid JSON. Text: {response_text_for_debug}...")
                        # Cố gắng tìm lỗi trong text trả về nếu là HTML/text
                        error_match = re.search(r'<pre>(.*?)</pre>', response_text_for_debug, re.DOTALL | re.IGNORECASE)
                        if error_match:
                             result["message"] = f"Lỗi API (HTML): {html.escape(error_match.group(1).strip())}"
                        else:
                             result["message"] = "Lỗi: API trả về dữ liệu JSON không hợp lệ."
                        result["success"] = False # Chắc chắn là lỗi
                    except Exception as e_proc:
                        logger.error(f"[API Call @{target_username}] Error processing API JSON data: {e_proc}", exc_info=True)
                        result["message"] = "Lỗi xử lý dữ liệu JSON từ API."
                        result["success"] = False
                else: # Content-type không phải JSON nhưng status 200
                     logger.warning(f"[API Call @{target_username}] Response 200 OK but wrong Content-Type: {content_type}. Text: {response_text_for_debug}...")
                     # Giả định có thể là thành công nếu không thấy lỗi rõ ràng
                     if "lỗi" not in response_text_for_debug.lower() and "error" not in response_text_for_debug.lower() and len(response_text_for_debug) < 200 :
                         result["success"] = True
                         result["message"] = "Follow thành công (phản hồi không chuẩn JSON)."
                     else:
                         result["success"] = False
                         result["message"] = f"Lỗi định dạng phản hồi API (Type: {content_type})."

            else: # Các mã lỗi HTTP khác
                 logger.error(f"[API Call @{target_username}] HTTP Error Status: {resp.status_code}. Text: {response_text_for_debug}...")
                 result["message"] = f"Lỗi từ API follow (Code: {resp.status_code})."
                 result["success"] = False

    except httpx.TimeoutException:
        logger.warning(f"[API Call @{target_username}] API timeout.")
        result["message"] = f"Lỗi: API timeout khi follow @{html.escape(target_username)}."
        result["success"] = False
    except httpx.ConnectError as e_connect:
        logger.error(f"[API Call @{target_username}] Connection error: {e_connect}", exc_info=False)
        result["message"] = f"Lỗi kết nối đến API follow @{html.escape(target_username)}."
        result["success"] = False
    except httpx.RequestError as e_req:
        logger.error(f"[API Call @{target_username}] Network error: {e_req}", exc_info=False)
        result["message"] = f"Lỗi mạng khi kết nối API follow @{html.escape(target_username)}."
        result["success"] = False
    except Exception as e_unexp:
        logger.error(f"[API Call @{target_username}] Unexpected error during API call: {e_unexp}", exc_info=True)
        result["message"] = f"Lỗi hệ thống Bot khi xử lý follow @{html.escape(target_username)}."
        result["success"] = False

    # Đảm bảo message luôn là string
    if not isinstance(result["message"], str):
        result["message"] = str(result["message"]) if result["message"] is not None else "Lỗi không xác định."

    logger.info(f"[API Call @{target_username}] Final result: Success={result['success']}, Message='{result['message'][:200]}...'") # Log ngắn gọn message
    return result

# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lệnh /start."""
    if not update or not update.message: return
    user = update.effective_user
    chat_id = update.effective_chat.id
    if not user: return

    act_h = ACTIVATION_DURATION_SECONDS // 3600
    gk_cd_m = GETKEY_COOLDOWN_SECONDS // 60
    bot_username = context.bot.username

    msg = (f"👋 <b>Xin chào {user.mention_html()}!</b>\n\n"
           f"🤖 Chào mừng bạn đến với <b>DinoTool</b> - Bot hỗ trợ TikTok.\n\n"
           f"✨ <b>Cách sử dụng cơ bản (Miễn phí):</b>\n"
           f"   1️⃣ Dùng <code>/getkey</code> để nhận link.\n"
           f"   2️⃣ Truy cập link, làm theo các bước để lấy Key.\n"
           f"       (Ví dụ: <code>Dinotool-ABC123XYZ</code>).\n"
           f"   3️⃣ Quay lại chat này hoặc nhóm, dùng <code>/nhapkey &lt;key_cua_ban&gt;</code>.\n"
           f"   4️⃣ Sau khi kích hoạt, bạn có thể dùng <code>/tim</code> và <code>/fl</code> trong <b>{act_h} giờ</b>.\n\n"
           f"👑 <b>Nâng cấp VIP:</b>\n"
           f"   » Xem chi tiết và hướng dẫn với lệnh <code>/muatt</code>.\n"
           f"   » Thành viên VIP có thể dùng <code>/treo</code>, <code>/dungtreo</code>, không cần lấy key và nhiều ưu đãi khác.\n\n"
           f"ℹ️ <b>Danh sách lệnh:</b>\n"
           f"   » Gõ <code>/lenh</code> để xem tất cả các lệnh và trạng thái của bạn.\n\n"
           # Thay đổi cách liên hệ admin
           f"💬 Cần hỗ trợ? Liên hệ Admin <a href='tg://user?id={ADMIN_USER_ID}'>tại đây</a>.")
           # f"<i>Bot được phát triển bởi <a href='https://t.me/dinotool'>DinoTool</a></i>") # Thay link nếu cần

    try:
        await update.message.reply_html(msg, disable_web_page_preview=True)
    except (BadRequest, Forbidden, TelegramError) as e:
        logger.warning(f"Failed to send /start message to {user.id} in chat {chat_id}: {e}")

async def lenh_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lệnh /lenh - Hiển thị danh sách lệnh và trạng thái user."""
    if not update or not update.message: return
    user = update.effective_user
    chat_id = update.effective_chat.id
    if not user: return

    user_id = user.id
    user_id_str = str(user_id)
    tf_cd_m = TIM_FL_COOLDOWN_SECONDS // 60
    gk_cd_m = GETKEY_COOLDOWN_SECONDS // 60
    act_h = ACTIVATION_DURATION_SECONDS // 3600
    key_exp_h = KEY_EXPIRY_SECONDS // 3600
    treo_interval_m = TREO_INTERVAL_SECONDS // 60

    is_vip = is_user_vip(user_id)
    is_key_active = is_user_activated_by_key(user_id)
    can_use_std_features = is_vip or is_key_active

    # --- Thông tin User ---
    status_lines = []
    status_lines.append(f"👤 <b>Người dùng:</b> {user.mention_html()} (<code>{user_id}</code>)")

    if is_vip:
        vip_data = vip_users.get(user_id_str, {})
        expiry_ts = vip_data.get("expiry")
        limit = vip_data.get("limit", "?")
        expiry_str = "Không rõ"
        if expiry_ts:
            try: expiry_str = datetime.fromtimestamp(float(expiry_ts)).strftime('%d/%m/%Y %H:%M')
            except (ValueError, TypeError, OSError): pass
        status_lines.append(f"👑 <b>Trạng thái:</b> VIP ✨ (Hết hạn: {expiry_str}, Giới hạn treo: {limit} users)")
    elif is_key_active:
        expiry_ts = activated_users.get(user_id_str)
        expiry_str = "Không rõ"
        if expiry_ts:
            try: expiry_str = datetime.fromtimestamp(float(expiry_ts)).strftime('%d/%m/%Y %H:%M')
            except (ValueError, TypeError, OSError): pass
        status_lines.append(f"🔑 <b>Trạng thái:</b> Đã kích hoạt (Key) (Hết hạn: {expiry_str})")
    else:
        status_lines.append("▫️ <b>Trạng thái:</b> Thành viên thường")

    status_lines.append(f"⚡️ <b>Quyền dùng /tim, /fl:</b> {'✅ Có thể' if can_use_std_features else '❌ Chưa thể (Cần VIP/Key)'}")

    # --- YÊU CẦU 1 (Lenh Command): Lấy số lượng treo từ persistent config ---
    if is_vip:
        current_treo_count = len(persistent_treo_configs.get(user_id_str, {})) # Đếm từ persistent
        vip_limit = get_vip_limit(user_id)
        status_lines.append(f"⚙️ <b>Quyền dùng /treo:</b> ✅ Có thể (Đang treo: {current_treo_count}/{vip_limit} users)")
    else:
         status_lines.append(f"⚙️ <b>Quyền dùng /treo:</b> ❌ Chỉ dành cho VIP")

    # --- Danh sách lệnh ---
    cmd_lines = ["\n\n📜=== <b>DANH SÁCH LỆNH</b> ===📜"]
    cmd_lines.append("\n<b><u>🔑 Lệnh Miễn Phí (Kích hoạt Key):</u></b>")
    cmd_lines.append(f"  <code>/getkey</code> - Lấy link nhận key (⏳ {gk_cd_m}p/lần, Key hiệu lực {key_exp_h}h)")
    cmd_lines.append(f"  <code>/nhapkey &lt;key&gt;</code> - Kích hoạt tài khoản (Sử dụng {act_h}h)")
    cmd_lines.append("\n<b><u>❤️ Lệnh Tăng Tương Tác (Cần VIP/Key):</u></b>")
    cmd_lines.append(f"  <code>/tim &lt;link_video&gt;</code> - Tăng tim cho video TikTok (⏳ {tf_cd_m}p/lần)")
    cmd_lines.append(f"  <code>/fl &lt;username&gt;</code> - Tăng follow cho tài khoản TikTok (⏳ {tf_cd_m}p/user)")
    cmd_lines.append("\n<b><u>👑 Lệnh VIP:</u></b>")
    cmd_lines.append(f"  <code>/muatt</code> - Thông tin và hướng dẫn mua VIP")
    cmd_lines.append(f"  <code>/treo &lt;username&gt;</code> - Tự động chạy <code>/fl</code> mỗi {treo_interval_m} phút (Dùng slot)")
    cmd_lines.append(f"  <code>/dungtreo &lt;username&gt;</code> - Dừng treo cho một tài khoản")
    if user_id == ADMIN_USER_ID:
        cmd_lines.append("\n<b><u>🛠️ Lệnh Admin:</u></b>")
        valid_vip_packages = ', '.join(map(str, VIP_PRICES.keys()))
        cmd_lines.append(f"  <code>/addtt &lt;user_id&gt; &lt;gói_ngày&gt;</code> - Thêm/gia hạn VIP (Gói: {valid_vip_packages})")
        # cmd_lines.append(f"  <code>/removett &lt;user_id&gt;</code> - Xóa VIP (chưa implement)")
        # cmd_lines.append(f"  <code>/stats</code> - Xem thống kê bot (chưa implement)")
    cmd_lines.append("\n<b><u>ℹ️ Lệnh Chung:</u></b>")
    cmd_lines.append(f"  <code>/start</code> - Tin nhắn chào mừng")
    cmd_lines.append(f"  <code>/lenh</code> - Xem lại bảng lệnh và trạng thái này")
    cmd_lines.append("\n<i>Lưu ý: Các lệnh yêu cầu VIP/Key chỉ hoạt động khi bạn có trạng thái tương ứng.</i>")

    help_text = "\n".join(status_lines + cmd_lines)

    try:
        await delete_user_message(update, context)
        await context.bot.send_message(chat_id=chat_id, text=help_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except (BadRequest, Forbidden, TelegramError) as e:
        logger.warning(f"Failed to send /lenh message to {user.id} in chat {chat_id}: {e}")

async def tim_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lệnh /tim."""
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    user_id = user.id
    current_time = time.time()
    original_message_id = update.message.message_id
    user_id_str = str(user_id)

    if not can_use_feature(user_id):
        err_msg = (f"⚠️ {user.mention_html()}, bạn cần là <b>VIP</b> hoặc <b>kích hoạt key</b> để dùng lệnh này!\n\n"
                   f"➡️ Dùng: <code>/getkey</code> » <code>/nhapkey &lt;key&gt;</code>\n"
                   f"👑 Hoặc: <code>/muatt</code> để nâng cấp VIP.")
        await send_temporary_message(update, context, err_msg, duration=30)
        await delete_user_message(update, context, original_message_id)
        return

    # Check Cooldown
    last_usage = user_tim_cooldown.get(user_id_str)
    if last_usage:
        try:
            elapsed = current_time - float(last_usage)
            if elapsed < TIM_FL_COOLDOWN_SECONDS:
                rem_time = TIM_FL_COOLDOWN_SECONDS - elapsed
                cd_msg = f"⏳ {user.mention_html()}, đợi <b>{rem_time:.0f} giây</b> nữa để dùng <code>/tim</code>."
                await send_temporary_message(update, context, cd_msg, duration=15)
                await delete_user_message(update, context, original_message_id)
                return
        except (ValueError, TypeError):
             logger.warning(f"Invalid cooldown timestamp for /tim user {user_id_str}. Resetting.")
             if user_id_str in user_tim_cooldown: del user_tim_cooldown[user_id_str]; save_data()


    # Parse Arguments
    args = context.args
    video_url = None
    err_txt = None
    if not args:
        err_txt = ("⚠️ Chưa nhập link video.\n<b>Cú pháp:</b> <code>/tim https://tiktok.com/...</code>")
    elif "tiktok.com/" not in args[0] or not args[0].startswith(("http://", "https://")):
        err_txt = f"⚠️ Link <code>{html.escape(args[0])}</code> không hợp lệ. Phải là link video TikTok."
    else:
        # Cố gắng trích xuất URL chuẩn hơn
        match = re.search(r"(https?://(?:www\.|vm\.|vt\.)?tiktok\.com/(?:@[\w.-]+/video/|v/|t/)?\d+)", args[0])
        if match: video_url = match.group(1)
        else:
            logger.warning(f"Could not extract standard TikTok video URL from: {args[0]}. Using as is.")
            video_url = args[0] # Fallback

    if err_txt:
        await send_temporary_message(update, context, err_txt, duration=20)
        await delete_user_message(update, context, original_message_id)
        return
    if not video_url: # Kiểm tra lại sau khi xử lý
        await send_temporary_message(update, context, "⚠️ Không thể xử lý link video.", duration=20)
        await delete_user_message(update, context, original_message_id)
        return
    if not API_KEY:
        logger.error(f"Missing API_KEY for /tim command triggered by user {user_id}")
        await delete_user_message(update, context, original_message_id)
        await send_temporary_message(update, context, "❌ Lỗi cấu hình: Bot thiếu API Key. Báo Admin.", duration=20)
        return

    # Call API
    api_url = VIDEO_API_URL_TEMPLATE.format(video_url=video_url, api_key=API_KEY)
    log_api_url = VIDEO_API_URL_TEMPLATE.format(video_url=video_url, api_key="***")
    logger.info(f"User {user_id} calling /tim API: {log_api_url}")

    processing_msg = None
    final_response_text = ""

    try:
        processing_msg = await update.message.reply_html("<b><i>⏳ Đang xử lý yêu cầu tăng tim...</i></b> ❤️")
        await delete_user_message(update, context, original_message_id)

        async with httpx.AsyncClient(verify=False, timeout=60.0) as client: # verify=False nếu API dùng cert tự ký
            resp = await client.get(api_url, headers={'User-Agent': 'TG Bot Tim Caller'})
            content_type = resp.headers.get("content-type","").lower()
            response_text_for_debug = ""
            try: response_text_for_debug = (await resp.aread()).decode('utf-8', errors='replace')[:500]
            except Exception: pass

            logger.debug(f"/tim API response status: {resp.status_code}, content-type: {content_type}")

            if resp.status_code == 200 and "application/json" in content_type:
                try:
                    data = resp.json()
                    logger.debug(f"/tim API response data: {data}")
                    # API này có vẻ dùng success boolean
                    if data.get("success"):
                        user_tim_cooldown[user_id_str] = time.time()
                        save_data()
                        d = data.get("data", {})
                        a = html.escape(str(d.get("author", "?")))
                        v = html.escape(str(d.get("video_url", video_url)))
                        db = html.escape(str(d.get('digg_before', '?')))
                        di = html.escape(str(d.get('digg_increased', '?')))
                        da = html.escape(str(d.get('digg_after', '?')))

                        final_response_text = (
                            f"🎉 <b>Tăng Tim Thành Công!</b> ❤️\n"
                            f"👤 Cho: {user.mention_html()}\n\n"
                            f"📊 <b>Thông tin Video:</b>\n"
                            f"🎬 <a href='{v}'>Link Video</a>\n"
                            f"✍️ Tác giả: <code>{a}</code>\n"
                            f"👍 Trước: <code>{db}</code> ➜ 💖 Tăng: <code>+{di}</code> ➜ ✅ Sau: <code>{da}</code>"
                        )
                    else:
                        api_msg = data.get('message', 'Không rõ lý do từ API')
                        logger.warning(f"/tim API call failed for user {user_id}. API message: {api_msg}")
                        final_response_text = f"💔 <b>Tăng Tim Thất Bại!</b>\n👤 Cho: {user.mention_html()}\nℹ️ Lý do: <code>{html.escape(api_msg)}</code>"
                except json.JSONDecodeError as e_json:
                    logger.error(f"/tim API response 200 OK but not valid JSON. Error: {e_json}. Text: {response_text_for_debug}...")
                    final_response_text = f"❌ <b>Lỗi Phản Hồi API</b>\n👤 Cho: {user.mention_html()}\nℹ️ API không trả về JSON hợp lệ."
            else:
                logger.error(f"/tim API call HTTP error or wrong content type. Status: {resp.status_code}, Type: {content_type}. Text: {response_text_for_debug}...")
                final_response_text = f"❌ <b>Lỗi Kết Nối API Tăng Tim</b>\n👤 Cho: {user.mention_html()}\nℹ️ Mã lỗi: {resp.status_code}. Vui lòng thử lại sau."

    except httpx.TimeoutException:
        logger.warning(f"/tim API call timeout for user {user_id}")
        final_response_text = f"❌ <b>Lỗi Timeout</b>\n👤 Cho: {user.mention_html()}\nℹ️ API tăng tim không phản hồi kịp thời."
    except httpx.RequestError as e_req:
        logger.error(f"/tim API call network error for user {user_id}: {e_req}", exc_info=False)
        final_response_text = f"❌ <b>Lỗi Mạng</b>\n👤 Cho: {user.mention_html()}\nℹ️ Không thể kết nối đến API tăng tim."
    except Exception as e_unexp:
        logger.error(f"Unexpected error during /tim command for user {user_id}: {e_unexp}", exc_info=True)
        final_response_text = f"❌ <b>Lỗi Hệ Thống Bot</b>\n👤 Cho: {user.mention_html()}\nℹ️ Đã xảy ra lỗi. Báo Admin."
    finally:
        if processing_msg:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id, message_id=processing_msg.message_id, text=final_response_text,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True
                )
            except Exception as e_edit: logger.warning(f"Failed to edit /tim msg {processing_msg.message_id}: {e_edit}")
        else:
            logger.warning(f"Processing message for /tim user {user_id} was None. Sending new message.")
            try: await context.bot.send_message(chat_id=chat_id, text=final_response_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            except Exception as e_send: logger.error(f"Failed to send final /tim message for user {user_id}: {e_send}")


# --- /fl Command ---
async def process_fl_request_background(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_id_str: str,
    target_username: str,
    processing_msg_id: int,
    invoking_user_mention: str
):
    """Hàm chạy nền xử lý API follow và cập nhật kết quả."""
    logger.info(f"[BG Task /fl] Starting for user {user_id_str} -> @{target_username}")
    api_result = await call_follow_api(user_id_str, target_username, context.bot.token)
    success = api_result["success"]
    api_message = api_result["message"]
    api_data = api_result["data"]
    final_response_text = ""

    user_info_block = ""
    follower_info_block = ""
    if api_data:
        try: # Bọc trong try-except để tránh lỗi nếu data API không chuẩn
            name = html.escape(str(api_data.get("name", "?")))
            # Lấy username từ API nếu có, nếu không dùng username đã nhập
            tt_username_from_api = api_data.get("username")
            tt_username = html.escape(str(tt_username_from_api if tt_username_from_api else target_username))
            tt_user_id = html.escape(str(api_data.get("user_id", "?")))
            khu_vuc = html.escape(str(api_data.get("khu_vuc", "Không rõ")))
            avatar = api_data.get("avatar", "")
            create_time = html.escape(str(api_data.get("create_time", "?")))

            user_info_lines = [f"👤 <b>Tài khoản:</b> <a href='https://tiktok.com/@{tt_username}'>{name}</a> (<code>@{tt_username}</code>)"]
            if tt_user_id != "?": user_info_lines.append(f"🆔 <b>ID TikTok:</b> <code>{tt_user_id}</code>")
            if khu_vuc != "Không rõ": user_info_lines.append(f"🌍 <b>Khu vực:</b> {khu_vuc}")
            if create_time != "?": user_info_lines.append(f"📅 <b>Ngày tạo TK:</b> {create_time}")
            if avatar and isinstance(avatar, str) and avatar.startswith("http"):
                user_info_lines.append(f"🖼️ <a href='{html.escape(avatar)}'>Xem Avatar</a>")
            user_info_block = "\n".join(user_info_lines) + "\n"

            f_before = html.escape(str(api_data.get("followers_before", "?")))
            f_add = html.escape(str(api_data.get("followers_add", "?")))
            f_after = html.escape(str(api_data.get("followers_after", "?")))
            # Chỉ hiển thị block follower nếu có ít nhất 1 thông tin
            if any(x != "?" for x in [f_before, f_add, f_after]):
                follower_lines = ["📈 <b>Số lượng Follower:</b>"]
                if f_before != "?": follower_lines.append(f"   Trước: <code>{f_before}</code>")
                if f_add != "?" and f_add != "0": follower_lines.append(f"   Tăng:   <b><code>+{f_add}</code></b> ✨")
                elif f_add == "0": follower_lines.append(f"   Tăng:   <code>+{f_add}</code>")
                if f_after != "?": follower_lines.append(f"   Sau:    <code>{f_after}</code>")
                # Chỉ thêm nếu có ít nhất 1 dòng thông tin follower
                if len(follower_lines) > 1:
                    follower_info_block = "\n".join(follower_lines)
        except Exception as e_parse:
            logger.error(f"[BG Task /fl] Error parsing API data for @{target_username}: {e_parse}. Data: {api_data}")
            # Hiển thị lỗi rõ ràng hơn nếu không parse được data
            user_info_block = f"👤 <b>Tài khoản:</b> <code>@{html.escape(target_username)}</code>\n(Lỗi xử lý thông tin chi tiết từ API)"
            follower_info_block = ""

    if success:
        current_time_ts = time.time()
        # Đảm bảo user_id_str là str khi truy cập dict
        user_fl_cooldown.setdefault(str(user_id_str), {})[target_username] = current_time_ts
        save_data()
        logger.info(f"[BG Task /fl] Success for user {user_id_str} -> @{target_username}. Cooldown updated.")
        final_response_text = (
            f"✅ <b>Tăng Follow Thành Công!</b>\n"
            f"✨ Cho: {invoking_user_mention}\n\n"
            f"{user_info_block if user_info_block else f'👤 <b>Tài khoản:</b> <code>@{html.escape(target_username)}</code>\n'}" # Fallback nếu user_info_block rỗng
            f"{follower_info_block if follower_info_block else ''}" # Chỉ thêm nếu có
        )
    else:
        logger.warning(f"[BG Task /fl] Failed for user {user_id_str} -> @{target_username}. API Message: {api_message}")
        final_response_text = (
            f"❌ <b>Tăng Follow Thất Bại!</b>\n"
            f"👤 Cho: {invoking_user_mention}\n"
            f"🎯 Target: <code>@{html.escape(target_username)}</code>\n\n"
            # Đảm bảo api_message không phải None
            f"💬 Lý do API: <i>{html.escape(api_message or 'Không rõ')}</i>\n\n"
            f"{user_info_block if user_info_block else ''}" # Chỉ thêm nếu có thông tin
        )
        # Kiểm tra message chặt chẽ hơn
        if isinstance(api_message, str) and "đợi" in api_message.lower() and ("phút" in api_message.lower() or "giây" in api_message.lower()):
            final_response_text += f"\n\n<i>ℹ️ API yêu cầu chờ đợi. Vui lòng thử lại sau.</i>"

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id, message_id=processing_msg_id, text=final_response_text,
            parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        logger.info(f"[BG Task /fl] Edited message {processing_msg_id} for user {user_id_str} -> @{target_username}")
    except BadRequest as e:
         # Bỏ qua lỗi "Message is not modified"
         if "Message is not modified" in str(e):
             logger.debug(f"[BG Task /fl] Message {processing_msg_id} was not modified.")
         # Ghi log các lỗi BadRequest khác
         elif "message to edit not found" in str(e).lower():
             logger.warning(f"[BG Task /fl] Message {processing_msg_id} not found for editing.")
         else:
              logger.error(f"[BG Task /fl] BadRequest editing msg {processing_msg_id}: {e}")
    except Exception as e: # Bắt các lỗi khác
        logger.error(f"[BG Task /fl] Failed to edit msg {processing_msg_id}: {e}", exc_info=True)


async def fl_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lệnh /fl - Check quyền, cooldown, gửi tin chờ và chạy task nền."""
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    user_id = user.id
    user_id_str = str(user_id)
    invoking_user_mention = user.mention_html()
    current_time = time.time()
    original_message_id = update.message.message_id

    if not can_use_feature(user_id):
        err_msg = (f"⚠️ {invoking_user_mention}, bạn cần là <b>VIP</b> hoặc <b>kích hoạt key</b> để dùng lệnh này!\n\n"
                   f"➡️ Dùng: <code>/getkey</code> » <code>/nhapkey &lt;key&gt;</code>\n"
                   f"👑 Hoặc: <code>/muatt</code> để nâng cấp VIP.")
        await send_temporary_message(update, context, err_msg, duration=30)
        await delete_user_message(update, context, original_message_id)
        return

    # Parse Arguments
    args = context.args
    target_username = None
    err_txt = None
    username_regex = r"^[a-zA-Z0-9_.]{2,24}$" # Regex username TikTok

    if not args:
        err_txt = ("⚠️ Chưa nhập username TikTok.\n<b>Cú pháp:</b> <code>/fl username</code>")
    else:
        uname_raw = args[0].strip()
        uname = uname_raw.lstrip("@") # Bỏ @ nếu có
        if not uname: err_txt = "⚠️ Username không được trống."
        elif not re.match(username_regex, uname):
            err_txt = (f"⚠️ Username <code>{html.escape(uname_raw)}</code> không hợp lệ.\n"
                       f"(Chỉ chứa chữ, số, '.', '_', dài 2-24 ký tự)")
        # Thêm kiểm tra không bắt đầu/kết thúc bằng dấu '.' hoặc '_' (TikTok không cho phép)
        elif uname.startswith('.') or uname.endswith('.') or uname.startswith('_') or uname.endswith('_'):
             err_txt = f"⚠️ Username <code>{html.escape(uname_raw)}</code> không hợp lệ (không được bắt đầu/kết thúc bằng '.' hoặc '_')."
        else: target_username = uname

    if err_txt:
        await send_temporary_message(update, context, err_txt, duration=20)
        await delete_user_message(update, context, original_message_id)
        return

    # Check Cooldown
    if target_username: # Chỉ kiểm tra nếu username hợp lệ
        user_cds = user_fl_cooldown.get(user_id_str, {})
        last_usage = user_cds.get(target_username)
        if last_usage:
            try:
                elapsed = current_time - float(last_usage)
                if elapsed < TIM_FL_COOLDOWN_SECONDS:
                     rem_time = TIM_FL_COOLDOWN_SECONDS - elapsed
                     cd_msg = f"⏳ {invoking_user_mention}, đợi <b>{rem_time:.0f} giây</b> nữa để dùng <code>/fl</code> cho <code>@{html.escape(target_username)}</code>."
                     await send_temporary_message(update, context, cd_msg, duration=15)
                     await delete_user_message(update, context, original_message_id)
                     return
            except (ValueError, TypeError):
                 logger.warning(f"Invalid cooldown timestamp for /fl user {user_id_str} target {target_username}. Resetting.")
                 if user_id_str in user_fl_cooldown and target_username in user_fl_cooldown[user_id_str]:
                     del user_fl_cooldown[user_id_str][target_username]; save_data()


    # Gửi tin nhắn chờ và chạy nền
    processing_msg = None
    try:
        if not target_username: # Double check
             raise ValueError("Target username became None unexpectedly before processing")

        processing_msg = await update.message.reply_html(
            f"⏳ {invoking_user_mention}, đã nhận yêu cầu tăng follow cho <code>@{html.escape(target_username)}</code>. Đang xử lý..."
        )
        await delete_user_message(update, context, original_message_id) # Xóa lệnh gốc

        logger.info(f"Scheduling background task for /fl user {user_id} target @{target_username}")
        context.application.create_task(
            process_fl_request_background(
                context=context, chat_id=chat_id, user_id_str=user_id_str,
                target_username=target_username, processing_msg_id=processing_msg.message_id,
                invoking_user_mention=invoking_user_mention
            ),
            name=f"fl_bg_{user_id_str}_{target_username}" # Đặt tên cho task để debug
        )

    except (BadRequest, Forbidden, TelegramError, ValueError) as e:
        logger.error(f"Failed to send processing message or schedule task for /fl @{target_username or '???'}: {e}")
        # Cố gắng xóa lệnh gốc nếu chưa kịp xóa
        await delete_user_message(update, context, original_message_id)
        # Sửa tin nhắn chờ thành lỗi nếu đã gửi được
        if processing_msg:
            try: await context.bot.edit_message_text(chat_id, processing_msg.message_id, f"❌ Lỗi khi bắt đầu xử lý yêu cầu /fl cho @{html.escape(target_username or '???')}. Vui lòng thử lại.")
            except Exception: pass
    except Exception as e:
         logger.error(f"Unexpected error in fl_command for user {user_id} target @{target_username or '???'}: {e}", exc_info=True)
         await delete_user_message(update, context, original_message_id)


# --- Lệnh /getkey ---
async def getkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    user_id = user.id
    current_time = time.time()
    original_message_id = update.message.message_id
    user_id_str = str(user_id)

    # Check Cooldown
    last_usage = user_getkey_cooldown.get(user_id_str)
    if last_usage:
        try:
            elapsed = current_time - float(last_usage)
            if elapsed < GETKEY_COOLDOWN_SECONDS:
                remaining = GETKEY_COOLDOWN_SECONDS - elapsed
                cd_msg = f"⏳ {user.mention_html()}, đợi <b>{remaining:.0f} giây</b> nữa để dùng <code>/getkey</code>."
                await send_temporary_message(update, context, cd_msg, duration=15)
                await delete_user_message(update, context, original_message_id)
                return
        except (ValueError, TypeError):
             logger.warning(f"Invalid cooldown timestamp for /getkey user {user_id_str}. Resetting.")
             if user_id_str in user_getkey_cooldown: del user_getkey_cooldown[user_id_str]; save_data()

    # Tạo Key và Link
    generated_key = generate_random_key()
    while generated_key in valid_keys:
        logger.warning(f"Key collision detected for {generated_key}. Regenerating.")
        generated_key = generate_random_key()

    target_url_with_key = BLOGSPOT_URL_TEMPLATE.format(key=generated_key)
    # Thêm cache buster để link luôn mới
    cache_buster = f"&ts={int(time.time())}{random.randint(100,999)}"
    final_target_url = target_url_with_key + cache_buster

    shortener_params = { "token": LINK_SHORTENER_API_KEY, "format": "json", "url": final_target_url }
    log_shortener_params = { "token": f"...{LINK_SHORTENER_API_KEY[-6:]}" if len(LINK_SHORTENER_API_KEY) > 6 else "***",
                           "format": "json", "url": final_target_url } # Log URL đầy đủ để debug
    logger.info(f"User {user_id} requesting key. Generated: {generated_key}. Target URL for shortener: {final_target_url}")

    processing_msg = None
    final_response_text = ""
    key_saved_to_dict = False # Cờ để biết key đã được lưu tạm vào dict chưa

    try:
        processing_msg = await update.message.reply_html("<b><i>⏳ Đang tạo link lấy key, vui lòng chờ...</i></b> 🔑")
        await delete_user_message(update, context, original_message_id) # Xóa lệnh gốc

        # --- Lưu Key tạm thời VÀO DICT trước khi gọi API rút gọn ---
        # Để nếu API lỗi, key không bị mất oan
        generation_time = time.time()
        expiry_time = generation_time + KEY_EXPIRY_SECONDS
        valid_keys[generated_key] = {
            "user_id_generator": user_id,
            "generation_time": generation_time,
            "expiry_time": expiry_time,
            "used_by": None,
            "activation_time": None
        }
        key_saved_to_dict = True
        logger.info(f"Key {generated_key} temporarily stored for user {user_id}. Expires at {datetime.fromtimestamp(expiry_time).isoformat()}.")
        # Lưu data ngay sau khi tạo key (an toàn hơn)
        save_data()

        # --- Gọi API Rút Gọn Link ---
        logger.debug(f"Calling shortener API: {LINK_SHORTENER_API_BASE_URL} with params: {log_shortener_params}")
        async with httpx.AsyncClient(timeout=30.0, verify=True) as client:
            headers = {'User-Agent': 'Telegram Bot Key Generator'}
            response = await client.get(LINK_SHORTENER_API_BASE_URL, params=shortener_params, headers=headers)
            response_content_type = response.headers.get("content-type", "").lower()
            response_text_for_debug = ""
            try:
                 response_text_for_debug = (await response.aread()).decode('utf-8', errors='replace')[:500]
            except Exception: pass

            logger.debug(f"Shortener API response status: {response.status_code}, content-type: {response_content_type}")

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.debug(f"Parsed shortener API response: {response_data}")
                    status = response_data.get("status")
                    generated_short_url = response_data.get("shortenedUrl")

                    if status == "success" and generated_short_url:
                        # Thành công -> Cập nhật cooldown và lưu lại
                        user_getkey_cooldown[user_id_str] = time.time()
                        save_data() # Lưu cooldown mới
                        logger.info(f"Successfully generated short link for user {user_id}: {generated_short_url}. Key {generated_key} confirmed.")
                        final_response_text = (
                            f"🚀 <b>Link Lấy Key Của Bạn ({user.mention_html()}):</b>\n\n"
                            # Sử dụng MarkdownV2 để tạo link copy-paste dễ hơn
                            # f"🔗 `{generated_short_url}`\n\n" # Dùng backticks để dễ copy
                            f"🔗 <a href='{html.escape(generated_short_url)}'>{html.escape(generated_short_url)}</a>\n\n" # Vẫn dùng link HTML
                            f"📝 <b>Hướng dẫn:</b>\n"
                            f"   1️⃣ Click vào link trên.\n"
                            f"   2️⃣ Làm theo các bước trên trang web để nhận Key (VD: <code>Dinotool-ABC123XYZ</code>).\n"
                            f"   3️⃣ Copy Key đó và quay lại đây.\n"
                            f"   4️⃣ Gửi lệnh: <code>/nhapkey &lt;key_ban_vua_copy&gt;</code>\n\n"
                            f"⏳ <i>Key chỉ có hiệu lực để nhập trong <b>{KEY_EXPIRY_SECONDS // 3600} giờ</b>. Hãy nhập sớm!</i>"
                        )
                    else:
                        # Lỗi từ API rút gọn -> Key đã được lưu, không cần xóa
                        api_message = response_data.get("message", "Lỗi không xác định từ API rút gọn link.")
                        logger.error(f"Shortener API returned error for user {user_id}. Status: {status}, Message: {api_message}. Data: {response_data}")
                        final_response_text = f"❌ <b>Lỗi Khi Tạo Link:</b>\n<code>{html.escape(str(api_message))}</code>\nVui lòng thử lại sau hoặc báo Admin. Key của bạn vẫn được giữ lại."
                        # Không xóa key khỏi valid_keys ở đây nữa

                except json.JSONDecodeError:
                    logger.error(f"Shortener API Status 200 but JSON decode failed. Type: '{response_content_type}'. Text: {response_text_for_debug}...")
                    final_response_text = f"❌ <b>Lỗi Phản Hồi API:</b> Máy chủ rút gọn link trả về dữ liệu không hợp lệ. Vui lòng thử lại sau. Key của bạn vẫn được giữ lại."
                    # Không xóa key
            else:
                 logger.error(f"Shortener API HTTP error. Status: {response.status_code}. Type: '{response_content_type}'. Text: {response_text_for_debug}...")
                 final_response_text = f"❌ <b>Lỗi Kết Nối API Tạo Link</b> (Mã: {response.status_code}). Vui lòng thử lại sau hoặc báo Admin. Key của bạn vẫn được giữ lại."
                 # Không xóa key

    except httpx.TimeoutException:
        logger.warning(f"Shortener API timeout during /getkey for user {user_id}")
        final_response_text = "❌ <b>Lỗi Timeout:</b> Máy chủ tạo link không phản hồi kịp thời. Vui lòng thử lại sau. Key của bạn vẫn được giữ lại."
        # Không xóa key
    except httpx.ConnectError as e_connect:
        logger.error(f"Shortener API connection error during /getkey for user {user_id}: {e_connect}", exc_info=False)
        final_response_text = "❌ <b>Lỗi Kết Nối:</b> Không thể kết nối đến máy chủ tạo link. Vui lòng kiểm tra mạng hoặc thử lại sau. Key của bạn vẫn được giữ lại."
        # Không xóa key
    except httpx.RequestError as e_req:
        logger.error(f"Shortener API network error during /getkey for user {user_id}: {e_req}", exc_info=False)
        final_response_text = "❌ <b>Lỗi Mạng</b> khi gọi API tạo link. Vui lòng thử lại sau. Key của bạn vẫn được giữ lại."
        # Không xóa key
    except Exception as e_unexp:
        logger.error(f"Unexpected error during /getkey command for user {user_id}: {e_unexp}", exc_info=True)
        final_response_text = "❌ <b>Lỗi Hệ Thống Bot</b> khi tạo key. Vui lòng báo Admin. Key của bạn vẫn được giữ lại."
        # Không xóa key
    finally:
        if processing_msg:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id, message_id=processing_msg.message_id, text=final_response_text,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True # Tắt preview link rút gọn
                )
            except Exception as e_edit: logger.warning(f"Failed to edit /getkey msg {processing_msg.message_id}: {e_edit}")
        else:
             logger.warning(f"Processing message for /getkey user {user_id} was None. Sending new message.")
             try: await context.bot.send_message(chat_id=chat_id, text=final_response_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
             except Exception as e_send: logger.error(f"Failed to send final /getkey message for user {user_id}: {e_send}")

# --- Lệnh /nhapkey ---
async def nhapkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    user_id = user.id
    current_time = time.time()
    original_message_id = update.message.message_id
    user_id_str = str(user_id)

    # Parse Input
    args = context.args
    submitted_key = None
    err_txt = ""
    key_prefix = "Dinotool-"
    key_format_regex = re.compile(r"^" + re.escape(key_prefix) + r"[A-Z0-9]+$")

    if not args:
        err_txt = ("⚠️ Bạn chưa nhập key.\n"
                   "<b>Cú pháp đúng:</b> <code>/nhapkey Dinotool-KEYCỦABẠN</code>")
    elif len(args) > 1:
        err_txt = f"⚠️ Bạn đã nhập quá nhiều từ. Chỉ nhập key thôi.\nVí dụ: <code>/nhapkey {generate_random_key()}</code>"
    else:
        key_input = args[0].strip()
        if not key_format_regex.match(key_input):
             err_txt = (f"⚠️ Key <code>{html.escape(key_input)}</code> sai định dạng.\n"
                        f"Phải bắt đầu bằng <code>{key_prefix}</code> và theo sau là chữ IN HOA/số.")
        else:
            submitted_key = key_input

    if err_txt:
        await send_temporary_message(update, context, err_txt, duration=20)
        await delete_user_message(update, context, original_message_id)
        return

    # Validate Key Logic
    logger.info(f"User {user_id} attempting key activation with: '{submitted_key}'")
    key_data = valid_keys.get(submitted_key)
    final_response_text = ""

    if not key_data:
        logger.warning(f"Key validation failed for user {user_id}: Key '{submitted_key}' not found.")
        final_response_text = f"❌ Key <code>{html.escape(submitted_key)}</code> không hợp lệ hoặc không tồn tại. Dùng <code>/getkey</code> để lấy key mới."
    elif key_data.get("used_by") is not None:
        used_by_id = key_data["used_by"]
        activation_time_ts = key_data.get("activation_time")
        used_time_str = ""
        if activation_time_ts:
            try: used_time_str = f" lúc {datetime.fromtimestamp(float(activation_time_ts)).strftime('%H:%M:%S %d/%m/%Y')}"
            except: pass
        if str(used_by_id) == user_id_str:
             logger.info(f"Key validation: User {user_id} already used key '{submitted_key}'{used_time_str}.")
             final_response_text = f"⚠️ Bạn đã kích hoạt key <code>{html.escape(submitted_key)}</code> này rồi{used_time_str}."
        else:
             logger.warning(f"Key validation failed for user {user_id}: Key '{submitted_key}' already used by user {used_by_id}{used_time_str}.")
             final_response_text = f"❌ Key <code>{html.escape(submitted_key)}</code> đã được người khác sử dụng{used_time_str}."
    elif current_time > float(key_data.get("expiry_time", 0)):
        expiry_time_ts = key_data.get("expiry_time")
        expiry_time_str = ""
        if expiry_time_ts:
             try: expiry_time_str = f" vào lúc {datetime.fromtimestamp(float(expiry_time_ts)).strftime('%H:%M:%S %d/%m/%Y')}"
             except: pass
        logger.warning(f"Key validation failed for user {user_id}: Key '{submitted_key}' expired{expiry_time_str}.")
        final_response_text = f"❌ Key <code>{html.escape(submitted_key)}</code> đã hết hạn sử dụng{expiry_time_str}. Dùng <code>/getkey</code> để lấy key mới."
        # Xóa key hết hạn khỏi dict khi có người cố nhập
        if submitted_key in valid_keys:
             del valid_keys[submitted_key]; save_data(); logger.info(f"Removed expired key {submitted_key} upon activation attempt.")
    else:
        # Kích hoạt thành công!
        try:
            key_data["used_by"] = user_id
            key_data["activation_time"] = current_time
            activation_expiry_ts = current_time + ACTIVATION_DURATION_SECONDS
            activated_users[user_id_str] = activation_expiry_ts
            save_data() # Lưu trạng thái key đã dùng và user đã kích hoạt

            expiry_dt = datetime.fromtimestamp(activation_expiry_ts)
            expiry_str = expiry_dt.strftime('%H:%M:%S ngày %d/%m/%Y')
            logger.info(f"Key '{submitted_key}' successfully activated by user {user_id}. Activation expires at {expiry_str}.")
            final_response_text = (f"✅ <b>Kích Hoạt Key Thành Công!</b>\n\n"
                                   f"👤 Người dùng: {user.mention_html()}\n"
                                   f"🔑 Key: <code>{html.escape(submitted_key)}</code>\n\n"
                                   f"✨ Bạn có thể sử dụng <code>/tim</code> và <code>/fl</code>.\n"
                                   f"⏳ Hết hạn vào: <b>{expiry_str}</b> (sau {ACTIVATION_DURATION_SECONDS // 3600} giờ)."
                                 )
        except Exception as e_activate:
             logger.error(f"Unexpected error during key activation process for user {user_id} key {submitted_key}: {e_activate}", exc_info=True)
             final_response_text = f"❌ Lỗi hệ thống khi kích hoạt key <code>{html.escape(submitted_key)}</code>. Báo Admin."
             # Rollback nếu có lỗi
             if submitted_key in valid_keys and valid_keys[submitted_key].get("used_by") == user_id:
                 valid_keys[submitted_key]["used_by"] = None
                 valid_keys[submitted_key]["activation_time"] = None
             if user_id_str in activated_users: del activated_users[user_id_str]
             save_data() # Lưu lại trạng thái rollback

    # Gửi phản hồi cuối cùng
    await delete_user_message(update, context, original_message_id)
    try:
        await update.message.reply_html(final_response_text, disable_web_page_preview=True)
    except Exception as e:
         logger.error(f"Failed to send /nhapkey final response to user {user_id}: {e}")


# --- Lệnh /muatt ---
async def muatt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hiển thị thông tin mua VIP và nút gửi bill."""
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    original_message_id = update.message.message_id
    user_id = user.id

    payment_note = f"{PAYMENT_NOTE_PREFIX} {user_id}"

    # Xây dựng nội dung tin nhắn
    text_lines = []
    text_lines.append("👑 <b>Thông Tin Nâng Cấp VIP - DinoTool</b> 👑")
    text_lines.append("\nTrở thành VIP để mở khóa <code>/treo</code>, không cần lấy key và nhiều ưu đãi!")

    text_lines.append("\n💎 <b>Các Gói VIP Hiện Có:</b>")
    for days_key, info in VIP_PRICES.items(): # Đổi tên biến days thành days_key
        text_lines.append(f"\n⭐️ <b>Gói {info['duration_days']} Ngày:</b>")
        text_lines.append(f"   - 💰 Giá: <b>{info['price']}</b>")
        text_lines.append(f"   - ⏳ Thời hạn: {info['duration_days']} ngày")
        text_lines.append(f"   - 🚀 Treo tối đa: <b>{info['limit']} tài khoản</b> TikTok")

    text_lines.append("\n🏦 <b>Thông tin thanh toán:</b>")
    text_lines.append(f"   - Ngân hàng: <b>{BANK_NAME}</b>")
    text_lines.append(f"   - STK: <code>{BANK_ACCOUNT}</code> (👈 Click để copy)")
    text_lines.append(f"   - Tên chủ TK: <b>{ACCOUNT_NAME}</b>")

    text_lines.append("\n📝 <b>Nội dung chuyển khoản (Quan trọng!):</b>")
    text_lines.append(f"   » Chuyển khoản với nội dung <b>CHÍNH XÁC</b> là:")
    text_lines.append(f"   » <code>{payment_note}</code> (👈 Click để copy)")
    text_lines.append(f"   <i>(Sai nội dung có thể khiến giao dịch xử lý chậm)</i>")

    text_lines.append("\n📸 <b>Sau Khi Chuyển Khoản Thành Công:</b>")
    text_lines.append(f"   1️⃣ Chụp ảnh màn hình biên lai (bill) giao dịch.")
    # --- YÊU CẦU 2: Cập nhật hướng dẫn gửi bill ---
    text_lines.append(f"   2️⃣ Nhấn nút 'Gửi Bill Thanh Toán' bên dưới.")
    text_lines.append(f"   3️⃣ Bot sẽ yêu cầu bạn gửi ảnh bill VÀO ĐÂY.") # Nhấn mạnh gửi vào chat hiện tại
    text_lines.append(f"   4️⃣ Gửi ảnh bill của bạn.")
    text_lines.append(f"   5️⃣ Bot sẽ tự động chuyển tiếp ảnh đến Admin.")
    text_lines.append(f"   6️⃣ Admin sẽ kiểm tra và kích hoạt VIP sớm nhất.")

    text_lines.append("\n<i>Cảm ơn bạn đã quan tâm và ủng hộ DinoTool!</i> ❤️")

    text = "\n".join(text_lines)

    # Tạo Inline Keyboard
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Gửi Bill Thanh Toán", callback_data="prompt_send_bill")]
    ])

    # Gửi tin nhắn kèm ảnh QR và nút
    await delete_user_message(update, context, original_message_id) # Xóa lệnh /muatt

    try:
        # Gửi ảnh và caption cùng nhau
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=QR_CODE_URL,
            caption=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard # Thêm bàn phím vào tin nhắn
        )
    except (BadRequest, Forbidden, TelegramError) as e:
        logger.error(f"Error sending /muatt photo+caption to chat {chat_id}: {e}. Falling back to text.")
        # Fallback: Gửi chỉ text nếu gửi ảnh lỗi (vẫn kèm nút)
        try:
            await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=keyboard)
        except Exception as e_text:
             logger.error(f"Error sending fallback text for /muatt to chat {chat_id}: {e_text}")
    except Exception as e_unexp:
        logger.error(f"Unexpected error sending /muatt command to chat {chat_id}: {e_unexp}", exc_info=True)

# --- Callback Handler cho nút "Gửi Bill Thanh Toán" ---
async def prompt_send_bill_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xử lý khi người dùng nhấn nút Gửi Bill."""
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat_id
    if not query or not user: return

    # Trả lời callback để nút hết trạng thái loading
    await query.answer()

    logger.info(f"User {user.id} clicked 'prompt_send_bill' button in chat {chat_id}.")

    # Gửi tin nhắn yêu cầu user gửi ảnh vào CHAT HIỆN TẠI
    # Tin nhắn này sẽ được gửi như một tin nhắn mới, không reply vào tin nhắn cũ
    prompt_text = f"📸 {user.mention_html()}, vui lòng gửi ảnh chụp màn hình biên lai thanh toán của bạn vào cuộc trò chuyện này."

    try:
        await context.bot.send_message(chat_id=chat_id, text=prompt_text, parse_mode=ParseMode.HTML)
        # Không lưu trạng thái, hàm handle_photo_bill sẽ tự xử lý ảnh gửi vào group ALLOWED_GROUP_ID
        # Quan trọng: User phải gửi ảnh vào group ALLOWED_GROUP_ID thì handle_photo_bill mới bắt được
        if chat_id != ALLOWED_GROUP_ID and ALLOWED_GROUP_ID:
             await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Lưu ý: Hãy gửi ảnh bill vào nhóm chính (nơi bot thông báo bill và thống kê) để Admin có thể xử lý.", parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Error sending bill prompt message to {user.id} in chat {chat_id}: {e}", exc_info=True)


# --- YÊU CẦU 2: Sửa xử lý nhận ảnh bill ---
async def handle_photo_bill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Xử lý ảnh/document ảnh được gửi trong nhóm ALLOWED_GROUP_ID
    và chuyển tiếp đến BILL_FORWARD_TARGET_ID.
    Không gửi thông báo lại vào nhóm gốc.
    """
    # Chỉ xử lý nếu ALLOWED_GROUP_ID được cấu hình và tin nhắn đến từ group đó
    if not update or not update.message or not ALLOWED_GROUP_ID or update.effective_chat.id != ALLOWED_GROUP_ID:
        return

    # Bỏ qua nếu là caption của lệnh khác hoặc không phải ảnh/document ảnh
    if (update.message.text and update.message.text.startswith('/')):
        return
    is_photo = bool(update.message.photo)
    is_image_document = bool(update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('image/'))
    if not is_photo and not is_image_document:
        return

    user = update.effective_user
    chat = update.effective_chat
    message = update.message
    if not user or not chat or not message: return

    logger.info(f"Bill photo/document received in ALLOWED_GROUP {chat.id} from user {user.id}. Forwarding to {BILL_FORWARD_TARGET_ID}.")

    # Tạo caption mới cho tin nhắn chuyển tiếp đến admin/bot nhận bill
    forward_caption_lines = []
    forward_caption_lines.append(f"📄 <b>Bill Nhận Được Tự Động</b>")
    forward_caption_lines.append(f"👤 <b>Từ User:</b> {user.mention_html()} (<code>{user.id}</code>)")
    forward_caption_lines.append(f"👥 <b>Trong Group:</b> {html.escape(chat.title or str(chat.id))} (<code>{chat.id}</code>)")
    try:
        # Lấy link tới tin nhắn gốc trong group
        message_link = message.link
        if message_link: forward_caption_lines.append(f"🔗 <a href='{message_link}'>Link Tin Nhắn Gốc</a>")
    except AttributeError:
        logger.debug(f"Could not get message link for message {message.message_id} in chat {chat.id}")

    original_caption = message.caption # Lấy caption gốc nếu có
    if original_caption:
         forward_caption_lines.append(f"\n💬 <b>Caption gốc:</b>\n{html.escape(original_caption[:500])}{'...' if len(original_caption) > 500 else ''}")

    forward_caption_text = "\n".join(forward_caption_lines)

    # Chuyển tiếp tin nhắn gốc (chứa ảnh) VÀ gửi caption thông tin
    try:
        # 1. Chuyển tiếp tin nhắn gốc
        await context.bot.forward_message(
            chat_id=BILL_FORWARD_TARGET_ID,
            from_chat_id=chat.id,
            message_id=message.message_id
        )
        # 2. Gửi tin nhắn thông tin bổ sung
        await context.bot.send_message(
            chat_id=BILL_FORWARD_TARGET_ID,
            text=forward_caption_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        logger.info(f"Successfully forwarded bill message {message.message_id} and sent info to {BILL_FORWARD_TARGET_ID}.")

        # --- YÊU CẦU 2: KHÔNG gửi thông báo lại vào nhóm gốc ---
        # Dòng sau bị xóa/comment:
        # reply_text = f"✅ Đã nhận và gửi ảnh của {user.mention_html()} cho Admin xem xét."
        # await send_temporary_message(update, context, reply_text, duration=60, reply=True)

    except Forbidden as e:
        logger.error(f"Bot cannot forward/send message to BILL_FORWARD_TARGET_ID ({BILL_FORWARD_TARGET_ID}). Check permissions/block status. Error: {e}")
        # Có thể gửi lại lỗi cho ADMIN_USER_ID nếu BILL_FORWARD_TARGET_ID không phải admin
        if ADMIN_USER_ID != BILL_FORWARD_TARGET_ID:
            try:
                 await context.bot.send_message(ADMIN_USER_ID, f"⚠️ Lỗi khi chuyển tiếp bill từ user {user.id} (group {chat.id}) đến target {BILL_FORWARD_TARGET_ID}. Lý do: Bot bị chặn hoặc thiếu quyền.\nẢnh gốc có thể xem tại link: {message.link if hasattr(message,'link') else 'Không có link'}")
            except Exception as e_admin: logger.error(f"Failed to send bill forwarding error notification to ADMIN {ADMIN_USER_ID}: {e_admin}")
    except TelegramError as e_fwd:
         logger.error(f"Telegram error forwarding/sending bill message {message.message_id} to {BILL_FORWARD_TARGET_ID}: {e_fwd}")
         if ADMIN_USER_ID != BILL_FORWARD_TARGET_ID:
              try: await context.bot.send_message(ADMIN_USER_ID, f"⚠️ Lỗi Telegram khi chuyển tiếp bill từ user {user.id} (group {chat.id}) đến target {BILL_FORWARD_TARGET_ID}. Lỗi: {e_fwd}")
              except Exception as e_admin: logger.error(f"Failed to send bill forwarding error notification to ADMIN {ADMIN_USER_ID}: {e_admin}")
    except Exception as e:
        logger.error(f"Unexpected error forwarding/sending bill to {BILL_FORWARD_TARGET_ID}: {e}", exc_info=True)
        if ADMIN_USER_ID != BILL_FORWARD_TARGET_ID:
             try: await context.bot.send_message(ADMIN_USER_ID, f"⚠️ Lỗi không xác định khi chuyển tiếp bill từ user {user.id} (group {chat.id}) đến target {BILL_FORWARD_TARGET_ID}. Chi tiết log.")
             except Exception as e_admin: logger.error(f"Failed to send bill forwarding error notification to ADMIN {ADMIN_USER_ID}: {e_admin}")


# --- Lệnh /addtt (Admin) ---
async def addtt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cấp VIP cho người dùng (chỉ Admin)."""
    if not update or not update.message: return
    admin_user = update.effective_user
    chat = update.effective_chat
    if not admin_user or not chat: return

    # Check Admin
    if admin_user.id != ADMIN_USER_ID:
        logger.warning(f"Unauthorized /addtt attempt by {admin_user.id} ({admin_user.username}) in chat {chat.id}.")
        return

    # Parse Arguments
    args = context.args
    err_txt = None
    target_user_id = None
    days_key_input = None # Key của gói (VD: 15, 30)
    limit = None
    duration_days = None # Số ngày thực tế của gói

    valid_day_keys = list(VIP_PRICES.keys()) # VD: [15, 30]
    valid_days_str = ', '.join(map(str, valid_day_keys)) # "15, 30"

    if len(args) != 2:
        err_txt = (f"⚠️ Sai cú pháp.\n"
                   f"<b>Dùng:</b> <code>/addtt &lt;user_id&gt; &lt;gói_ngày&gt;</code>\n"
                   f"<b>Các gói hợp lệ:</b> {valid_days_str}\n"
                   f"<b>Ví dụ:</b> <code>/addtt 123456789 {valid_day_keys[0] if valid_day_keys else '15'}</code>")
    else:
        try: target_user_id = int(args[0])
        except ValueError: err_txt = f"⚠️ User ID '<code>{html.escape(args[0])}</code>' không hợp lệ."

        if not err_txt:
            try:
                days_key_input = int(args[1])
                if days_key_input not in VIP_PRICES:
                    err_txt = f"⚠️ Gói ngày không hợp lệ. Chỉ chấp nhận: <b>{valid_days_str}</b>."
                else:
                    vip_info = VIP_PRICES[days_key_input]
                    limit = vip_info["limit"]
                    duration_days = vip_info["duration_days"] # Lấy số ngày thực tế
            except ValueError:
                err_txt = f"⚠️ Gói ngày '<code>{html.escape(args[1])}</code>' không phải là số hợp lệ."

    if err_txt:
        try: await update.message.reply_html(err_txt)
        except Exception as e_reply: logger.error(f"Failed to send error reply to admin {admin_user.id}: {e_reply}")
        return

    # Cập nhật dữ liệu VIP
    target_user_id_str = str(target_user_id)
    current_time = time.time()
    current_vip_data = vip_users.get(target_user_id_str)
    start_time = current_time
    operation_type = "Nâng cấp lên" # Mặc định là nâng cấp mới

    if current_vip_data:
         try:
             current_expiry = float(current_vip_data.get("expiry", 0))
             if current_expiry > current_time:
                 start_time = current_expiry # Gia hạn từ ngày hết hạn cũ
                 operation_type = "Gia hạn thêm"
                 logger.info(f"User {target_user_id_str} already VIP. Extending from {datetime.fromtimestamp(start_time).isoformat()}.")
             else:
                 logger.info(f"User {target_user_id_str} was VIP but expired. Treating as new activation.")
         except (ValueError, TypeError):
              logger.warning(f"Invalid expiry data for user {target_user_id_str}. Treating as new activation.")

    new_expiry_ts = start_time + duration_days * 86400 # Tính hạn mới dựa trên duration_days
    new_expiry_dt = datetime.fromtimestamp(new_expiry_ts)
    new_expiry_str = new_expiry_dt.strftime('%H:%M:%S ngày %d/%m/%Y')

    # Cập nhật hoặc tạo mới thông tin VIP
    vip_users[target_user_id_str] = {"expiry": new_expiry_ts, "limit": limit}
    save_data()
    logger.info(f"Admin {admin_user.id} processed VIP for {target_user_id_str}: {operation_type} {duration_days} days. New expiry: {new_expiry_str}, Limit: {limit}")

    # Gửi thông báo cho Admin
    admin_msg = (f"✅ Đã <b>{operation_type} {duration_days} ngày VIP</b> thành công!\n\n"
                 f"👤 User ID: <code>{target_user_id}</code>\n"
                 f"✨ Gói: {duration_days} ngày\n"
                 f"⏳ Hạn sử dụng mới: <b>{new_expiry_str}</b>\n"
                 f"🚀 Giới hạn treo: <b>{limit} users</b>")
    try: await update.message.reply_html(admin_msg)
    except Exception as e: logger.error(f"Failed to send confirmation message to admin {admin_user.id} in chat {chat.id}: {e}")

    # Thông báo cho người dùng (nếu có thể gửi vào group chính)
    user_mention = f"User ID <code>{target_user_id}</code>" # Default
    try:
        target_user_info = await context.bot.get_chat(target_user_id)
        # Ưu tiên mention_html nếu là User, không thì dùng link hoặc ID
        if target_user_info:
             if hasattr(target_user_info, 'mention_html') and target_user_info.mention_html():
                  user_mention = target_user_info.mention_html()
             elif target_user_info.link:
                  user_mention = f"<a href='{target_user_info.link}'>User {target_user_id}</a>"
             else:
                  user_mention = f"User <code>{target_user_id}</code>" # Fallback cuối cùng

    except Exception as e_get_chat:
        logger.warning(f"Could not get chat info for target user {target_user_id}: {e_get_chat}. Using ID instead.")

    group_msg = (f"🎉 Chúc mừng {user_mention}! 🎉\n\n"
                 f"Bạn đã được Admin <b>{operation_type} {duration_days} ngày VIP</b> thành công!\n\n"
                 f"✨ Gói VIP: <b>{duration_days} ngày</b>\n"
                 f"⏳ Hạn sử dụng đến: <b>{new_expiry_str}</b>\n"
                 f"🚀 Giới hạn treo: <b>{limit} tài khoản</b>\n\n"
                 f"Cảm ơn bạn đã ủng hộ DinoTool! ❤️\n"
                 f"(Dùng <code>/lenh</code> để xem lại trạng thái)")

    # Gửi thông báo vào group chính nếu được cấu hình
    target_chat_id_for_notification = ADMIN_USER_ID # Mặc định gửi riêng cho Admin
    if ALLOWED_GROUP_ID:
        target_chat_id_for_notification = ALLOWED_GROUP_ID # Ưu tiên gửi vào group
        logger.info(f"Sending VIP notification for {target_user_id} to group {ALLOWED_GROUP_ID}")
    else:
         logger.info(f"ALLOWED_GROUP_ID not set. Sending VIP notification for {target_user_id} to admin {ADMIN_USER_ID}")

    try:
        await context.bot.send_message(chat_id=target_chat_id_for_notification, text=group_msg, parse_mode=ParseMode.HTML)
    except Exception as e_send_notify:
        logger.error(f"Failed to send VIP notification for user {target_user_id} to chat {target_chat_id_for_notification}: {e_send_notify}")
        # Thông báo lỗi cho admin nếu gửi vào group thất bại
        if admin_user.id != target_chat_id_for_notification:
             try: await context.bot.send_message(admin_user.id, f"⚠️ Không thể gửi thông báo VIP cho user {target_user_id} vào chat {target_chat_id_for_notification}. Lỗi: {e_send_notify}")
             except Exception: pass


# --- Logic Treo ---

# --- YÊU CẦU 3 & 4: Sửa giao diện và tự xóa khi lỗi ---
async def run_treo_loop(user_id_str: str, target_username: str, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Vòng lặp chạy nền cho lệnh /treo, gửi thông báo trạng thái và tự xóa khi lỗi."""
    user_id = int(user_id_str)
    task_name = f"treo_{user_id_str}_{target_username}_in_{chat_id}"
    logger.info(f"[Treo Task Start] Task '{task_name}' started.")
    invoking_user_mention = f"User ID <code>{user_id_str}</code>" # Mention mặc định
    try: # Lấy mention 1 lần khi bắt đầu task
        user_info = await context.bot.get_chat(user_id)
        if user_info:
             m = user_info.mention_html()
             if m: invoking_user_mention = m # Chỉ gán nếu mention hợp lệ
    except Exception: pass # Bỏ qua nếu không lấy được

    last_sleep_time = time.time() # Ghi lại thời điểm sleep cuối cùng

    try:
        while True:
            current_time = time.time()

            # Check 1: Task còn trong danh sách active không? (quan trọng để tránh task ma)
            current_task_in_dict = active_treo_tasks.get(user_id_str, {}).get(target_username)
            # So sánh task hiện tại với task trong dict bằng id hoặc name
            current_asyncio_task = None
            try: current_asyncio_task = asyncio.current_task()
            except RuntimeError: pass # Nếu loop không chạy thì bỏ qua

            if current_task_in_dict is not current_asyncio_task:
                 logger.warning(f"[Treo Task Stop] Task '{task_name}' seems replaced or removed from active_treo_tasks dict (or mismatch). Stopping.")
                 break

            # Check 2: User còn VIP không?
            if not is_user_vip(user_id):
                logger.warning(f"[Treo Task Stop] User {user_id_str} no longer VIP. Stopping task '{task_name}'.")
                # Dừng task và xóa config persistent
                await stop_treo_task(user_id_str, target_username, context, reason="VIP Expired in loop")
                try: await context.bot.send_message(chat_id, f"ℹ️ {invoking_user_mention}, việc treo cho <code>@{html.escape(target_username)}</code> đã dừng do VIP hết hạn.", parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass
                break

            # Check 3: Đã đủ thời gian sleep chưa? (Để tránh gọi API quá nhanh nếu có lỗi)
            elapsed_since_sleep = current_time - last_sleep_time
            if elapsed_since_sleep < TREO_INTERVAL_SECONDS * 0.9: # Cho phép sai số nhỏ
                wait_more = TREO_INTERVAL_SECONDS - elapsed_since_sleep
                logger.debug(f"[Treo Task Wait] Task '{task_name}' needs to wait {wait_more:.1f}s more before API call.")
                await asyncio.sleep(wait_more)
            last_sleep_time = time.time() # Reset timer trước khi gọi API

            # Thực hiện gọi API Follow
            logger.info(f"[Treo Task Run] Task '{task_name}' executing follow for @{target_username}")
            api_result = await call_follow_api(user_id_str, target_username, context.bot.token)
            success = api_result["success"]
            api_message = api_result["message"] or "Không có thông báo từ API." # Đảm bảo không None
            gain = 0

            if success and api_result.get("data"):
                try:
                    gain_str = str(api_result["data"].get("followers_add", "0"))
                    gain = int(gain_str)
                    if gain > 0:
                        treo_stats[user_id_str][target_username] += gain
                        logger.info(f"[Treo Task Stats] Task '{task_name}' added {gain} followers. Cycle gain: {treo_stats[user_id_str][target_username]}")
                except (ValueError, TypeError, KeyError) as e_gain:
                     logger.warning(f"[Treo Task Stats] Task '{task_name}' error parsing gain: {e_gain}. Data: {api_result.get('data')}")
            elif success:
                 logger.info(f"[Treo Task Success] Task '{task_name}' successful but no data/gain info. API Msg: {api_message}")
            else: # API Follow thất bại
                logger.warning(f"[Treo Task Fail] Task '{task_name}' failed. API Msg: {api_message}")

            # --- YÊU CẦU 3: Gửi thông báo trạng thái với giao diện mới ---
            status_lines = []
            sent_status_message = None # Biến để lưu tin nhắn trạng thái đã gửi

            try:
                if success:
                    # Lấy tên từ mention nếu có, không thì dùng ID
                    user_display_name = invoking_user_mention if "User ID" not in invoking_user_mention else f"User <code>{user_id_str}</code>"

                    status_lines.append(f"✅ {user_display_name}: Treo <code>@{html.escape(target_username)}</code> thành công!")
                    status_lines.append(f"➕ Thêm: <b>{gain}</b>")
                    # Chỉ hiển thị message API nếu nó khác các thông báo thành công mặc định
                    if api_message not in ["Follow thành công.", "Không có thông báo từ API."]:
                         status_lines.append(f"💬 <i>{html.escape(api_message)}</i>")
                    else: # Thêm dòng trống nếu không có message API đặc biệt
                        status_lines.append(f"💬 Không có thông báo từ API.") # Hoặc để trống hoàn toàn

                    status_msg = "\n".join(status_lines)
                    sent_status_message = await context.bot.send_message(
                        chat_id=chat_id,
                        text=status_msg,
                        parse_mode=ParseMode.HTML,
                        disable_notification=True # Gửi yên lặng
                    )
                else: # Thất bại
                    # Lấy tên từ mention nếu có
                    user_display_name = invoking_user_mention if "User ID" not in invoking_user_mention else f"User <code>{user_id_str}</code>"

                    status_lines.append(f"❌ {user_display_name}: Treo <code>@{html.escape(target_username)}</code> thất bại!")
                    status_lines.append(f"➕ Thêm: 0")
                    status_lines.append(f"💬 Lý do: <i>{html.escape(api_message)}</i>") # Luôn hiển thị lý do lỗi

                    status_msg = "\n".join(status_lines)
                    sent_status_message = await context.bot.send_message(
                        chat_id=chat_id,
                        text=status_msg,
                        parse_mode=ParseMode.HTML,
                        disable_notification=True
                    )

                    # --- YÊU CẦU 4: Lên lịch xóa tin nhắn thất bại ---
                    if sent_status_message and context.job_queue:
                        job_name_del = f"del_treo_fail_{chat_id}_{sent_status_message.message_id}"
                        context.job_queue.run_once(
                            delete_message_job,
                            TREO_FAILURE_MSG_DELETE_DELAY,
                            data={'chat_id': chat_id, 'message_id': sent_status_message.message_id},
                            name=job_name_del
                        )
                        logger.info(f"Scheduled job '{job_name_del}' to delete failure message {sent_status_message.message_id} in {TREO_FAILURE_MSG_DELETE_DELAY}s.")

            except Forbidden:
                logger.warning(f"Could not send treo status for '{task_name}' to chat {chat_id}. Bot might be kicked/blocked.")
                # Không nên dừng task ở đây, user có thể không ở trong chat đó nữa
            except TelegramError as e_send:
                logger.error(f"Error sending treo status for '{task_name}' to chat {chat_id}: {e_send}")
            except Exception as e_unexp_send:
                logger.error(f"Unexpected error sending treo status for '{task_name}' to chat {chat_id}: {e_unexp_send}", exc_info=True)


            # Chờ đợi đến lần chạy tiếp theo
            sleep_duration = TREO_INTERVAL_SECONDS
            logger.debug(f"[Treo Task Sleep] Task '{task_name}' sleeping for {sleep_duration:.1f} seconds...")
            await asyncio.sleep(sleep_duration)
            last_sleep_time = time.time() # Cập nhật lại thời điểm sleep

    except asyncio.CancelledError:
        logger.info(f"[Treo Task Cancelled] Task '{task_name}' was cancelled externally.")
    except Exception as e:
        logger.error(f"[Treo Task Error] Unexpected error in task '{task_name}': {e}", exc_info=True)
        try:
            await context.bot.send_message(chat_id, f"💥 {invoking_user_mention}: Lỗi nghiêm trọng khi treo <code>@{html.escape(target_username)}</code>. Tác vụ đã dừng. Lỗi: {html.escape(str(e))}", parse_mode=ParseMode.HTML, disable_notification=True)
        except Exception: pass
        # Dừng task và xóa config khi có lỗi nghiêm trọng
        await stop_treo_task(user_id_str, target_username, context, reason=f"Unexpected Error: {e}")
    finally:
        logger.info(f"[Treo Task End] Task '{task_name}' finished.")
        # Đảm bảo task được xóa khỏi runtime dict khi kết thúc (stop_treo_task cũng làm nhưng chắc chắn hơn)
        if user_id_str in active_treo_tasks and target_username in active_treo_tasks[user_id_str]:
             task_in_dict = active_treo_tasks[user_id_str].get(target_username)
             current_task = None
             try: current_task = asyncio.current_task()
             except RuntimeError: pass

             if task_in_dict is current_task and task_in_dict and task_in_dict.done():
                del active_treo_tasks[user_id_str][target_username]
                if not active_treo_tasks[user_id_str]:
                    del active_treo_tasks[user_id_str]
                logger.info(f"[Treo Task Cleanup] Removed finished task '{task_name}' from active tasks dict in finally block.")


# --- Lệnh /treo (VIP) ---
# --- YÊU CẦU 1: Sửa /treo để lưu persistent config ---
async def treo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bắt đầu treo tự động follow cho một user (chỉ VIP). Lưu config."""
    global persistent_treo_configs, active_treo_tasks # Cần sửa đổi
    if not update or not update.message: return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user: return
    user_id = user.id
    user_id_str = str(user_id)
    original_message_id = update.message.message_id
    invoking_user_mention = user.mention_html()

    # Check VIP
    if not is_user_vip(user_id):
        err_msg = f"⚠️ {invoking_user_mention}, lệnh <code>/treo</code> chỉ dành cho <b>VIP</b>.\nDùng <code>/muatt</code> để nâng cấp."
        await send_temporary_message(update, context, err_msg, duration=20)
        await delete_user_message(update, context, original_message_id)
        return

    # Parse Arguments
    args = context.args
    target_username = None
    err_txt = None
    username_regex = r"^[a-zA-Z0-9_.]{2,24}$"

    if not args:
        err_txt = ("⚠️ Chưa nhập username TikTok cần treo.\n"
                   "<b>Cú pháp:</b> <code>/treo username</code>")
    else:
        uname_raw = args[0].strip()
        uname = uname_raw.lstrip("@")
        if not uname: err_txt = "⚠️ Username không được trống."
        elif not re.match(username_regex, uname):
            err_txt = (f"⚠️ Username <code>{html.escape(uname_raw)}</code> không hợp lệ.\n"
                       f"(Chữ, số, '.', '_', dài 2-24)")
        elif uname.startswith('.') or uname.endswith('.') or uname.startswith('_') or uname.endswith('_'):
             err_txt = f"⚠️ Username <code>{html.escape(uname_raw)}</code> không hợp lệ (không bắt đầu/kết thúc bằng '.' hoặc '_')."
        else: target_username = uname

    if err_txt:
        await send_temporary_message(update, context, err_txt, duration=20)
        await delete_user_message(update, context, original_message_id)
        return

    # Check Giới Hạn và Trạng Thái Treo Hiện Tại (dựa vào persistent config)
    if target_username:
        vip_limit = get_vip_limit(user_id)
        # Kiểm tra cả persistent và runtime để đếm số lượng
        persistent_user_configs = persistent_treo_configs.get(user_id_str, {})
        runtime_user_tasks = active_treo_tasks.get(user_id_str, {})
        # Lấy tập hợp các target đang được quản lý (đã lưu hoặc đang chạy)
        all_managed_targets = set(persistent_user_configs.keys()) | set(runtime_user_tasks.keys())
        current_treo_count = len(all_managed_targets)

        # Kiểm tra xem target này đã được treo chưa (trong persistent hoặc runtime)
        if target_username in all_managed_targets:
            logger.info(f"User {user_id} tried to /treo target @{target_username} which is already managed (persistent or runtime).")
            # Kiểm tra xem task runtime có đang chạy không
            existing_runtime_task = runtime_user_tasks.get(target_username)
            if existing_runtime_task and not existing_runtime_task.done():
                 msg = f"⚠️ Bạn đã đang treo cho <code>@{html.escape(target_username)}</code> rồi. Dùng <code>/dungtreo {target_username}</code> để dừng."
            else: # Có thể chỉ có trong persistent hoặc task runtime đã chết
                 msg = f"⚠️ Tài khoản <code>@{html.escape(target_username)}</code> đã được cấu hình treo. Nếu muốn dừng, dùng <code>/dungtreo {target_username}</code>."
            await send_temporary_message(update, context, msg, duration=20)
            await delete_user_message(update, context, original_message_id)
            return

        # Kiểm tra giới hạn trước khi thêm target mới
        if current_treo_count >= vip_limit:
             logger.warning(f"User {user_id} tried to /treo target @{target_username} but reached limit ({current_treo_count}/{vip_limit}).")
             limit_msg = (f"⚠️ Đã đạt giới hạn treo tối đa! ({current_treo_count}/{vip_limit} tài khoản).\n"
                          f"Dùng <code>/dungtreo &lt;username&gt;</code> để giải phóng slot.")
             await send_temporary_message(update, context, limit_msg, duration=30)
             await delete_user_message(update, context, original_message_id)
             return

        # --- Bắt đầu Task Treo Mới ---
        try:
            app = context.application
            # Tạo task chạy nền
            task = app.create_task(
                run_treo_loop(user_id_str, target_username, context, chat_id),
                name=f"treo_{user_id_str}_{target_username}_in_{chat_id}" # Tên task để debug
            )

            # Lưu task vào runtime dict
            active_treo_tasks.setdefault(user_id_str, {})[target_username] = task
            # --- YÊU CẦU 1: Lưu config vào persistent dict ---
            persistent_treo_configs.setdefault(user_id_str, {})[target_username] = chat_id
            save_data() # Lưu lại dữ liệu persistent

            logger.info(f"Successfully created task '{task.get_name()}' and saved persistent config for user {user_id} -> @{target_username}")

            # Thông báo thành công
            # Cập nhật lại số lượng đang treo sau khi thêm
            new_treo_count = len(persistent_treo_configs.get(user_id_str, {}))
            success_msg = (f"✅ <b>Bắt Đầu Treo Thành Công!</b>\n\n"
                           f"👤 Cho: {invoking_user_mention}\n"
                           f"🎯 Target: <code>@{html.escape(target_username)}</code>\n"
                           f"⏳ Tần suất: Mỗi {TREO_INTERVAL_SECONDS // 60} phút\n"
                           f"📊 Slot đã dùng: {new_treo_count}/{vip_limit}")
            await update.message.reply_html(success_msg)
            await delete_user_message(update, context, original_message_id) # Xóa lệnh /treo gốc

        except Exception as e_start_task:
             logger.error(f"Failed to start treo task or save config for user {user_id} target @{target_username}: {e_start_task}", exc_info=True)
             await send_temporary_message(update, context, f"❌ Lỗi hệ thống khi bắt đầu treo cho <code>@{html.escape(target_username)}</code>. Báo Admin.", duration=20)
             await delete_user_message(update, context, original_message_id)
             # Rollback nếu lỗi: xóa khỏi persistent nếu đã thêm
             if user_id_str in persistent_treo_configs and target_username in persistent_treo_configs[user_id_str]:
                  del persistent_treo_configs[user_id_str][target_username]
                  if not persistent_treo_configs[user_id_str]: del persistent_treo_configs[user_id_str]
                  save_data()
                  logger.info(f"Rolled back persistent config for {user_id_str} -> @{target_username} due to start error.")
             # Rollback runtime task nếu đã tạo
             if 'task' in locals() and task and not task.done(): task.cancel()
             if user_id_str in active_treo_tasks and target_username in active_treo_tasks[user_id_str]:
                 del active_treo_tasks[user_id_str][target_username]
                 if not active_treo_tasks[user_id_str]: del active_treo_tasks[user_id_str]

    else: # target_username là None sau khi parse (lỗi logic?)
        logger.error(f"/treo command for user {user_id}: target_username became None unexpectedly.")
        await send_temporary_message(update, context, "❌ Lỗi không xác định khi xử lý username.", duration=15)
        await delete_user_message(update, context, original_message_id)


# --- Lệnh /dungtreo (VIP) ---
# --- YÊU CẦU 1: Sửa /dungtreo để dùng stop_treo_task ---
async def dungtreo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dừng việc treo tự động follow cho một user (chỉ VIP hoặc user có task)."""
    if not update or not update.message: return
    user = update.effective_user
    if not user: return
    user_id = user.id
    user_id_str = str(user_id)
    original_message_id = update.message.message_id
    invoking_user_mention = user.mention_html()

    # Parse Arguments
    args = context.args
    target_username_clean = None
    err_txt = None

    # Lấy danh sách đang treo từ persistent config
    persistent_user_configs = persistent_treo_configs.get(user_id_str, {})

    if not args:
        if not persistent_user_configs:
             err_txt = ("⚠️ Chưa nhập username cần dừng treo.\n"
                        "<b>Cú pháp:</b> <code>/dungtreo username</code>\n"
                        "<i>(Hiện bạn không có tài khoản nào được cấu hình treo.)</i>")
        else:
             running_targets_str = ', '.join([f"<code>@{html.escape(t)}</code>" for t in persistent_user_configs.keys()])
             err_txt = (f"⚠️ Cần chỉ định username muốn dừng treo.\n"
                        f"<b>Cú pháp:</b> <code>/dungtreo username</code>\n"
                        f"<b>Đang treo:</b> {running_targets_str}")
    else:
        target_username_clean = args[0].strip().lstrip("@")
        if not target_username_clean:
            err_txt = "⚠️ Username không được để trống."
        # Không cần kiểm tra regex ở đây, chỉ cần khớp với key trong dict

    if err_txt:
        await send_temporary_message(update, context, err_txt, duration=30)
        await delete_user_message(update, context, original_message_id)
        return

    # Dừng Task và Xóa Config
    if target_username_clean:
        logger.info(f"User {user_id} requesting to stop treo for @{target_username_clean}")
        # Gọi hàm stop_treo_task (đã xử lý cả runtime và persistent)
        stopped = await stop_treo_task(user_id_str, target_username_clean, context, reason=f"User command /dungtreo by {user_id}")

        await delete_user_message(update, context, original_message_id) # Xóa lệnh /dungtreo
        if stopped:
            # Lấy lại số lượng sau khi xóa
            new_treo_count = len(persistent_treo_configs.get(user_id_str, {}))
            vip_limit = get_vip_limit(user_id) # Lấy limit hiện tại
            is_still_vip = is_user_vip(user_id)
            await update.message.reply_html(f"✅ Đã dừng treo và xóa cấu hình cho <code>@{html.escape(target_username_clean)}</code>.\n(Slot đã dùng: {new_treo_count}/{vip_limit if is_still_vip else 'N/A'})")
        else:
            # Nếu stop_treo_task trả về False, nghĩa là target không tồn tại cả trong runtime và persistent
            await send_temporary_message(update, context, f"⚠️ Không tìm thấy cấu hình treo nào cho <code>@{html.escape(target_username_clean)}</code> để dừng.", duration=20)

# --- Job Thống Kê Follow Tăng ---
async def report_treo_stats(context: ContextTypes.DEFAULT_TYPE):
    """Job chạy định kỳ để thống kê và báo cáo user treo tăng follow."""
    global last_stats_report_time, treo_stats
    current_time = time.time()
    logger.info(f"[Stats Job] Starting statistics report job. Last report: {datetime.fromtimestamp(last_stats_report_time).isoformat() if last_stats_report_time else 'Never'}")

    # Chỉ gửi thống kê vào group chính nếu được cấu hình
    target_chat_id_for_stats = ALLOWED_GROUP_ID
    if not target_chat_id_for_stats:
        logger.info("[Stats Job] ALLOWED_GROUP_ID is not set. Stats report skipped.")
        return

    # Tạo bản sao và reset (dùng copy để tránh race condition nếu có)
    stats_snapshot = {}
    if treo_stats: # Chỉ copy nếu có dữ liệu
        try:
            # Deep copy để đảm bảo không ảnh hưởng dict gốc khi reset
            stats_snapshot = json.loads(json.dumps(treo_stats))
        except Exception as e_copy:
             logger.error(f"[Stats Job] Error creating stats snapshot: {e_copy}. Aborting stats run.")
             return # Không chạy nếu không copy được

    # Reset defaultdict gốc ngay sau khi copy thành công
    treo_stats.clear()
    last_stats_report_time = current_time
    save_data() # Lưu trạng thái đã reset và thời gian báo cáo mới
    logger.info(f"[Stats Job] Cleared current stats and updated last report time. Processing snapshot with {len(stats_snapshot)} users.")

    if not stats_snapshot:
        logger.info("[Stats Job] No stats data found in snapshot. Skipping report content generation.")
        # Không gửi tin nhắn "Không có dữ liệu" để tránh spam group
        return

    # Xử lý dữ liệu snapshot
    top_gainers = [] # List of tuples: (gain, user_id_str, target_username)
    total_gain_all = 0
    for user_id_str, targets in stats_snapshot.items():
        if isinstance(targets, dict): # Đảm bảo targets là dict
            for target_username, gain in targets.items():
                if isinstance(gain, int) and gain > 0: # Đảm bảo gain là số nguyên dương
                    top_gainers.append((gain, str(user_id_str), str(target_username))) # Đảm bảo kiểu string
                    total_gain_all += gain
                elif gain > 0:
                     logger.warning(f"[Stats Job] Invalid gain type ({type(gain)}) for {user_id_str}->{target_username}. Skipping.")

    if not top_gainers:
        logger.info("[Stats Job] No positive gains found after processing snapshot. Skipping report.")
        return

    top_gainers.sort(key=lambda x: x[0], reverse=True) # Sắp xếp giảm dần theo gain

    # Tạo nội dung báo cáo
    report_lines = []
    report_lines.append(f"📊 <b>Thống Kê Tăng Follow (24 Giờ Qua)</b> 📊")
    report_lines.append(f"<i>(Tổng cộng: <b>{total_gain_all:,}</b> follow được tăng bởi các tài khoản đang treo)</i>") # Format số
    report_lines.append("\n🏆 <b>Top Tài Khoản Treo Hiệu Quả Nhất:</b>")

    num_top_to_show = 10 # Hiển thị top 10
    displayed_count = 0
    user_mentions_cache = {} # Cache mention để giảm gọi API get_chat

    for gain, user_id_str, target_username in top_gainers[:num_top_to_show]:
        user_mention = user_mentions_cache.get(user_id_str)
        if not user_mention:
            try:
                user_info = await context.bot.get_chat(int(user_id_str))
                m = user_info.mention_html()
                user_mention = m if m else f"User <code>{user_id_str}</code>" # Lấy mention nếu có
                user_mentions_cache[user_id_str] = user_mention
            except Exception as e_get_chat:
                logger.warning(f"[Stats Job] Failed to get mention for user {user_id_str}: {e_get_chat}")
                user_mention = f"User <code>{user_id_str}</code>"
                user_mentions_cache[user_id_str] = user_mention # Lưu cache cả khi lỗi

        # Format số lượng gain
        report_lines.append(f"  🏅 <b>+{gain:,} follow</b> cho <code>@{html.escape(target_username)}</code> (Treo bởi: {user_mention})")
        displayed_count += 1

    if not displayed_count:
         report_lines.append("  <i>Không có dữ liệu tăng follow đáng kể.</i>")

    report_lines.append(f"\n🕒 <i>Cập nhật mỗi 24 giờ.</i>")

    # Gửi báo cáo vào group
    report_text = "\n".join(report_lines)
    try:
        await context.bot.send_message(
            chat_id=target_chat_id_for_stats,
            text=report_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            disable_notification=True # Gửi yên lặng
        )
        logger.info(f"[Stats Job] Successfully sent statistics report to group {target_chat_id_for_stats}.")
    except Exception as e:
        logger.error(f"[Stats Job] Failed to send statistics report to group {target_chat_id_for_stats}: {e}", exc_info=True)

    logger.info("[Stats Job] Statistics report job finished.")


# --- Hàm helper bất đồng bộ để dừng task khi tắt bot ---
async def shutdown_async_tasks(tasks_to_cancel: list[asyncio.Task]):
    """Helper async function to cancel and wait for tasks during shutdown."""
    if not tasks_to_cancel:
        logger.info("No active treo tasks found to cancel during shutdown.")
        return

    logger.info(f"Attempting to gracefully cancel {len(tasks_to_cancel)} active treo tasks...")
    # Hủy tất cả task trước
    for task in tasks_to_cancel:
        if task and not task.done():
            task.cancel()

    # Chờ tất cả kết thúc (với timeout nhỏ cho mỗi task)
    results = await asyncio.gather(*[asyncio.wait_for(task, timeout=2.0) for task in tasks_to_cancel], return_exceptions=True)
    logger.info("Finished waiting for treo task cancellations during shutdown.")

    cancelled_count = 0
    errors_count = 0
    finished_count = 0

    for i, result in enumerate(results):
        task_name = f"Task_{i}"
        try:
            if tasks_to_cancel[i]: task_name = tasks_to_cancel[i].get_name() or task_name
        except: pass

        if isinstance(result, asyncio.CancelledError):
            cancelled_count += 1
            logger.info(f"Task '{task_name}' confirmed cancelled during shutdown.")
        elif isinstance(result, asyncio.TimeoutError):
             errors_count += 1
             logger.warning(f"Task '{task_name}' timed out during shutdown cancellation.")
        elif isinstance(result, Exception):
            errors_count += 1
            logger.error(f"Error occurred in task '{task_name}' during shutdown processing: {result}", exc_info=False)
        else:
            finished_count += 1
            logger.debug(f"Task '{task_name}' finished normally during shutdown (not cancelled/error).")

    logger.info(f"Shutdown task summary: {cancelled_count} cancelled, {errors_count} errors/timeouts, {finished_count} finished normally.")


# --- Main Function ---
def main() -> None:
    """Khởi động và chạy bot."""
    start_time = time.time()
    print("--- Bot DinoTool Starting ---")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("\n--- Configuration Summary ---")
    print(f"Bot Token: {'Loaded' if BOT_TOKEN else 'Missing!'}")
    if ALLOWED_GROUP_ID: print(f"Primary Group ID (Bills/Stats): {ALLOWED_GROUP_ID}")
    else: print("ALLOWED_GROUP_ID: Not Set (Bills/Stats Disabled)")
    print(f"Bill Forward Target ID: {BILL_FORWARD_TARGET_ID}")
    print(f"Admin User ID: {ADMIN_USER_ID}")
    print(f"Link Shortener Key: {'Loaded' if LINK_SHORTENER_API_KEY else 'Missing!'}")
    print(f"Tim API Key: {'Loaded' if API_KEY else 'Missing!'}")
    print(f"Follow API URL: {FOLLOW_API_URL_BASE}")
    print(f"Data File: {DATA_FILE}")
    print(f"Key Expiry: {KEY_EXPIRY_SECONDS / 3600:.1f}h | Activation: {ACTIVATION_DURATION_SECONDS / 3600:.1f}h")
    print(f"Cooldowns: Tim/Fl={TIM_FL_COOLDOWN_SECONDS / 60:.1f}m | GetKey={GETKEY_COOLDOWN_SECONDS / 60:.1f}m")
    print(f"Treo: Interval={TREO_INTERVAL_SECONDS / 60:.1f}m | Fail Delete Delay={TREO_FAILURE_MSG_DELETE_DELAY}s")
    print(f"Stats Interval: {TREO_STATS_INTERVAL_SECONDS / 3600:.1f}h")
    print(f"VIP Prices: {VIP_PRICES}")
    print(f"Payment: {BANK_NAME} - {BANK_ACCOUNT} - {ACCOUNT_NAME}")
    print("-" * 30)

    print("Loading persistent data...")
    load_data()
    print(f"Load complete. Keys: {len(valid_keys)}, Activated: {len(activated_users)}, VIPs: {len(vip_users)}")
    print(f"Cooldowns: Tim={len(user_tim_cooldown)}, Fl={len(user_fl_cooldown)}, GetKey={len(user_getkey_cooldown)}")
    print(f"Persistent Treo Configs Loaded: {sum(len(targets) for targets in persistent_treo_configs.values())} targets for {len(persistent_treo_configs)} users")
    print(f"Initial Treo Stats Users: {len(treo_stats)}, Last Stats Report: {datetime.fromtimestamp(last_stats_report_time).isoformat() if last_stats_report_time else 'Never'}")

    # Cấu hình Application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .job_queue(JobQueue())
        .pool_timeout(120) # Thời gian chờ thread trong pool
        .connect_timeout(60) # Timeout kết nối đến Telegram
        .read_timeout(90)    # Timeout đọc phản hồi từ Telegram
        .write_timeout(90)   # Timeout gửi yêu cầu đến Telegram
        .get_updates_pool_timeout(120) # Timeout cho getUpdates
        .http_version("1.1") # Thử dùng HTTP/1.1 nếu có vấn đề với 2.0
        .build()
    )

    # --- Schedule Jobs ---
    jq = application.job_queue
    if jq:
        jq.run_repeating(cleanup_expired_data, interval=CLEANUP_INTERVAL_SECONDS, first=60, name="cleanup_expired_data_job")
        logger.info(f"Scheduled cleanup job every {CLEANUP_INTERVAL_SECONDS / 60:.0f} minutes.")

        # Job thống kê follow (chạy mỗi 24 giờ) - Chỉ chạy nếu có group ID
        if ALLOWED_GROUP_ID:
            jq.run_repeating(report_treo_stats, interval=TREO_STATS_INTERVAL_SECONDS, first=300, name="report_treo_stats_job")
            logger.info(f"Scheduled statistics report job every {TREO_STATS_INTERVAL_SECONDS / 3600:.1f} hours.")
        else:
             logger.info("Statistics report job skipped (ALLOWED_GROUP_ID not set).")
    else:
         logger.error("JobQueue is not available. Scheduled jobs will not run.")

    # --- Register Handlers ---
    # Lệnh hoạt động mọi nơi
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("lenh", lenh_command))
    application.add_handler(CommandHandler("getkey", getkey_command))
    application.add_handler(CommandHandler("nhapkey", nhapkey_command))
    application.add_handler(CommandHandler("tim", tim_command))
    application.add_handler(CommandHandler("fl", fl_command))
    application.add_handler(CommandHandler("muatt", muatt_command))
    application.add_handler(CommandHandler("treo", treo_command))
    application.add_handler(CommandHandler("dungtreo", dungtreo_command))

    # Lệnh Admin (chỉ admin thực thi, kiểm tra trong hàm)
    application.add_handler(CommandHandler("addtt", addtt_command))

    # Callback Query Handler cho nút gửi bill
    application.add_handler(CallbackQueryHandler(prompt_send_bill_callback, pattern="^prompt_send_bill$"))

    # Handler cho ảnh/bill -> Chỉ hoạt động nếu ALLOWED_GROUP_ID được set và tin nhắn đến từ group đó
    if ALLOWED_GROUP_ID:
        # Chỉ bắt ảnh hoặc document là ảnh, trong group chỉ định, và không phải lệnh
        photo_bill_filter = (filters.PHOTO | filters.Document.IMAGE) & filters.Chat(chat_id=ALLOWED_GROUP_ID) & (~filters.COMMAND) & filters.UpdateType.MESSAGE
        application.add_handler(MessageHandler(photo_bill_filter, handle_photo_bill))
        logger.info(f"Registered photo/bill handler for group {ALLOWED_GROUP_ID} only.")
    else:
         logger.warning("Photo/bill handler is disabled because ALLOWED_GROUP_ID is not set.")


    # --- YÊU CẦU 1: Khởi động lại các task treo đã lưu ---
    print("\nRestarting persistent treo tasks...")
    restored_count = 0
    users_to_cleanup = [] # Lưu user không còn VIP để xóa config
    if persistent_treo_configs:
        for user_id_str, targets in list(persistent_treo_configs.items()): # Dùng list để có thể sửa dict khi duyệt
            try:
                user_id_int = int(user_id_str)
                if not is_user_vip(user_id_int):
                    logger.warning(f"User {user_id_str} from persistent config is no longer VIP. Will remove their treo configs.")
                    users_to_cleanup.append(user_id_str)
                    continue # Chuyển sang user tiếp theo

                vip_limit = get_vip_limit(user_id_int)
                current_user_restored_count = 0
                for target_username, chat_id_int in list(targets.items()): # Dùng list
                    if current_user_restored_count >= vip_limit:
                         logger.warning(f"User {user_id_str} reached VIP limit ({vip_limit}) during restore. Skipping further targets like @{target_username}.")
                         # Xóa target vượt quá giới hạn khỏi persistent config
                         if user_id_str in persistent_treo_configs and target_username in persistent_treo_configs[user_id_str]:
                              del persistent_treo_configs[user_id_str][target_username]
                              if not persistent_treo_configs[user_id_str]: del persistent_treo_configs[user_id_str]
                              save_data() # Lưu ngay sau khi xóa
                         continue

                    # Kiểm tra xem task đã chạy chưa (phòng trường hợp lỗi lặp)
                    if user_id_str in active_treo_tasks and target_username in active_treo_tasks[user_id_str]:
                        logger.info(f"Task for {user_id_str} -> @{target_username} already seems active. Skipping restore.")
                        continue

                    logger.info(f"Restarting treo task for user {user_id_str} -> @{target_username} in chat {chat_id_int}")
                    try:
                        task = application.create_task(
                            run_treo_loop(user_id_str, target_username, application.context_types.DEFAULT_TYPE(application=application, chat_data=None, user_data=None) , chat_id_int),
                            name=f"treo_{user_id_str}_{target_username}_in_{chat_id_int}_restored"
                        )
                        active_treo_tasks.setdefault(user_id_str, {})[target_username] = task
                        restored_count += 1
                        current_user_restored_count += 1
                    except Exception as e_restore:
                        logger.error(f"Failed to restore task for {user_id_str} -> @{target_username}: {e_restore}", exc_info=True)

            except ValueError:
                logger.error(f"Invalid user_id '{user_id_str}' found in persistent_treo_configs. Skipping.")
                users_to_cleanup.append(user_id_str) # Đánh dấu để xóa config lỗi
            except Exception as e_outer_restore:
                 logger.error(f"Unexpected error processing persistent treo config for user {user_id_str}: {e_outer_restore}", exc_info=True)

    # Dọn dẹp config của user không còn VIP hoặc có ID lỗi
    if users_to_cleanup:
        logger.info(f"Cleaning up persistent treo configs for {len(users_to_cleanup)} non-VIP or invalid users...")
        cleaned_count = 0
        for user_id_str_clean in users_to_cleanup:
            if user_id_str_clean in persistent_treo_configs:
                del persistent_treo_configs[user_id_str_clean]
                cleaned_count += 1
        if cleaned_count > 0:
             save_data()
             logger.info(f"Removed persistent configs for {cleaned_count} users.")

    print(f"Successfully restored {restored_count} treo tasks.")
    print("-" * 30)

    print("\nBot initialization complete. Starting polling...")
    logger.info("Bot initialization complete. Starting polling...")
    run_duration = time.time() - start_time
    print(f"(Initialization took {run_duration:.2f} seconds)")

    try:
        # Chạy bot
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping bot gracefully...")
        logger.info("KeyboardInterrupt detected. Stopping bot...")
    except Exception as e:
        print(f"\nCRITICAL ERROR: Bot stopped due to an unhandled exception: {e}")
        logger.critical(f"CRITICAL ERROR: Bot stopped due to unhandled exception: {e}", exc_info=True)
    finally:
        print("\nInitiating shutdown sequence...")
        logger.info("Initiating shutdown sequence...")

        # Dừng các task treo đang chạy (lấy từ active_treo_tasks)
        tasks_to_stop_on_shutdown = []
        if active_treo_tasks:
            logger.info("Collecting active treo tasks from runtime dict for shutdown...")
            for user_id_str, targets in list(active_treo_tasks.items()):
                for target_username, task in list(targets.items()):
                    if task and not task.done():
                        tasks_to_stop_on_shutdown.append(task)
                        try: task_name = task.get_name()
                        except AttributeError: task_name = f"Task_{user_id_str}_{target_username}"
                        logger.debug(f"Added task '{task_name}' to shutdown list.")

        if tasks_to_stop_on_shutdown:
            print(f"Found {len(tasks_to_stop_on_shutdown)} active runtime treo tasks. Attempting cancellation...")
            try:
                 asyncio.run(shutdown_async_tasks(tasks_to_stop_on_shutdown))
            except RuntimeError as e_runtime:
                 logger.error(f"RuntimeError during async task shutdown (maybe loop already stopped?): {e_runtime}")
                 # Fallback: Thử cancel trực tiếp nếu loop có vấn đề
                 for task in tasks_to_stop_on_shutdown:
                      if task and not task.done(): task.cancel()
            except Exception as e_shutdown:
                 logger.error(f"Error during async task shutdown: {e_shutdown}", exc_info=True)
        else:
            print("No active runtime treo tasks found at shutdown.")

        print("Attempting final data save...")
        logger.info("Attempting final data save...")
        save_data()
        print("Final data save attempt complete.")

        print("Bot has stopped.")
        logger.info("Bot has stopped.")
        print(f"Shutdown timestamp: {datetime.now().isoformat()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Ghi lỗi nghiêm trọng ra file riêng nếu main không chạy được
        print(f"\nFATAL ERROR: Could not execute main function: {e}")
        logger.critical(f"FATAL ERROR preventing main execution: {e}", exc_info=True)
        try:
            with open("fatal_error.log", "a", encoding='utf-8') as f:
                f.write(f"\n{datetime.now().isoformat()} - FATAL ERROR: {e}\n")
                import traceback
                traceback.print_exc(file=f)
        except Exception as e_log:
            print(f"Additionally, failed to write fatal error to log file: {e_log}")
