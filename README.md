# Alfa Connect Bot

Telegram bot for managing service requests and staff workflows in multiple regions.

## 🚀 Hozirgi holat

Bot asosiy struktura bilan tayyor, lekin hali to'liq ishlamayapti. Asosiy muammolar:

- ✅ **Asosiy struktura** - Barcha handler va keyboard modullar yaratilgan
- ❌ **Database ulanishi** - PostgreSQL server ishlamayapti
- ⚠️ **Import xatoliklari** - Ba'zi modullar bir-birini topa olmayapti
- ⚠️ **To'liq emas** - Ko'p funksiyalar hali yaratilmagan

## 📋 Keyingi qadamlar

### 1. Database serverini ishga tushirish
```bash
# PostgreSQL o'rnatish (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Database yaratish
sudo -u postgres createdb alfaconnect_toshkent
sudo -u postgres createdb alfaconnect_samarqand
sudo -u postgres createdb alfaconnect_clients

# Foydalanuvchi yaratish
sudo -u postgres createuser alfaconnect
sudo -u postgres psql -c "ALTER USER alfaconnect WITH PASSWORD 'ulugbek202';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE alfaconnect_toshkent TO alfaconnect;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE alfaconnect_samarqand TO alfaconnect;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE alfaconnect_clients TO alfaconnect;"
```

### 2. Bot ishga tushirish
```bash
# Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate

# Modellarni o'rnatish
pip install -r requirements.txt

# Bot ishga tushirish
python main.py
```

### 3. GitHub ga o'zgarishlarni yuklash
```bash
git add .
git commit -m "Fix import errors and add missing modules"
git push origin main
```

## 🏗️ Arxitektura

### Database struktura
- **`alfaconnect_toshkent`** - Toshkent region ma'lumotlari
- **`alfaconnect_samarqand`** - Samarqand region ma'lumotlari  
- **`alfaconnect_clients`** - Mijozlar va ularning arizalari

### Handler modullar
- **`handlers/admin/`** - Administrator funksiyalari
- **`handlers/manager/`** - Manager funksiyalari
- **`handlers/technician/`** - Texnik xizmat
- **`handlers/controller/`** - Nazoratchi
- **`handlers/warehouse/`** - Ombor
- **`handlers/call_center/`** - Qo'ng'iroq markazi
- **`handlers/client/`** - Mijoz interfeysi

### Keyboard modullar
- **`keyboards/admin_buttons.py`** - Admin klaviatura
- **`keyboards/manager_buttons.py`** - Manager klaviatura
- **`keyboards/technician_buttons.py`** - Texnik klaviatura
- **`keyboards/controllers_buttons.py`** - Controller klaviatura
- **`keyboards/warehouse_buttons.py`** - Ombor klaviatura

## ⚙️ Sozlash

### .env fayl
```bash
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123,456,789
BOT_ID=your_bot_id
ZAYAVKA_GROUP_ID="-1001234567890"

DB_HOST=localhost
DB_PORT=5432
DB_USER=alfaconnect
DB_PASSWORD=ulugbek202

DB_URL_TOSHKENT=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_toshkent
DB_URL_SAMARQAND=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_samarqand
CLIENTS_DB_URL=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_clients

ADMIN_IDS_TOSHKENT=123,456
ADMIN_IDS_SAMARQAND=789,012

LOG_LEVEL=INFO
```

## 🔧 O'rnatish

### Talablar
- Python 3.8+
- PostgreSQL 12+
- Git

### O'rnatish qadamlar
```bash
# Repository ni klonlash
git clone https://github.com/yakubjanov004/mybot.git
cd mybot

# Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate

# Modellarni o'rnatish
pip install -r requirements.txt

# .env fayl yaratish
cp .env.example .env
# .env faylni o'zgartiring

# Database sozlash (yuqorida ko'rsatilgan)
# Bot ishga tushirish
python main.py
```

## 📊 Test qilish

### 1. Database ulanishini tekshirish
```bash
psql -h localhost -U alfaconnect -d alfaconnect_toshkent
# Parol: ulugbek202
```

### 2. Bot ishlashini tekshirish
```bash
python main.py
# Xatoliklar log fayllarda saqlanadi
```

### 3. Telegram da test qilish
- Botga `/start` buyrug'ini yuboring
- Turli rollar bilan test qiling

## 🐛 Xatoliklarni hal qilish

### Umumiy muammolar
1. **Import xatoliklari** - Modul yo'q, uni yarating
2. **Database ulanishi** - PostgreSQL server ishlamayapti
3. **Keyboard funksiyalari** - Funksiya yo'q, uni qo'shing

### Log fayllar
- `testbot_errors.log` - Xatoliklar
- `testbot_activity.log` - Faollik

## 📝 Yordam

Agar muammolar bo'lsa:
1. Log fayllarni tekshiring
2. Database ulanishini tekshiring
3. GitHub Issues da muammoni yozing

## 🤝 Hissa qo'shish

1. Fork qiling
2. Feature branch yarating
3. O'zgarishlarni commit qiling
4. Pull request yuboring

## 📄 Litsenziya

Bu loyiha ochiq manba hisoblanadi.