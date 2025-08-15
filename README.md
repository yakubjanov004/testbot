# Alfa Connect Bot

Alfa Connect - telekommunikatsiya kompaniyasi uchun Telegram bot.

## 🚀 Xususiyatlari

### Rollar va funksiyalar:
- **Admin** - Tizim boshqaruvi
- **Manager** - Buyurtmalar va xodimlar boshqaruvi  
- **Controller** - Sifat nazorati va monitoring
- **Call Center Supervisor** - Call center boshqaruvi
- **Call Center** - Mijozlar bilan ishlash
- **Warehouse** - Ombor boshqaruvi
- **Technician** - Texnik xizmatlar
- **Client** - Mijozlar uchun

### Asosiy imkoniyatlar:
- 📊 Export (CSV, Excel, Word, PDF)
- 📥 Inbox tizimi
- 📈 Statistika va hisobotlar
- 🔄 Workflow boshqaruvi
- 👥 Xodimlar boshqaruvi
- 🌐 Ko'p tillilik (O'zbek, Rus)

## 📋 O'rnatish

### 1. Repository ni clone qilish:
```bash
git clone https://github.com/yakubjanov004/mybot.git
cd mybot
```

### 2. Virtual environment yaratish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Dependencies o'rnatish:
```bash
pip install -r requirements.txt
```

### 4. Environment sozlash:
```bash
cp .env.example .env
# .env faylini tahrirlang va BOT_TOKEN ni kiriting
```

### 5. Botni ishga tushirish:
```bash
python main.py
```

### 6. Migratsiyalarni qo‘llash (ixtiyoriy, Postgres sozlangan bo‘lsa):
```bash
python scripts/migrate.py
```

Agar `.env` faylini tez sozlash kerak bo‘lsa, `.env.example` ni nusxa oling:
```bash
cp .env.example .env
```

## 🔧 Konfiguratsiya

`.env` faylida quyidagi sozlamalar mavjud:
- `BOT_TOKEN` - Telegram bot token (@BotFather dan)
- `BOT_ID` - Ixtiyoriy. Agar kiritilmasa, `BOT_TOKEN` dan avtomatik olinadi
- `ADMIN_IDS` - Global adminlar roʻyxati, vergul bilan ajratilgan (masalan: `123,456`)
- `ZAYAVKA_GROUP_ID` - Ixtiyoriy. Arizalar uchun guruh ID si
- `LOG_LEVEL` - Logging darajasi (`INFO`, `DEBUG`, `ERROR`)

- Postgres uchun bitta umumiy URL yoki bo'linma/regionlarga ajratilgan URL lar:
  - `DATABASE_URL` - Umumiy standart baza URL (masalan: `postgresql://user:pass@host:5432/dbname`)
  - `DB_URL_TOSHKENT` yoki `DATABASE_URL_TOSHKENT` - Toshkent bazasi
  - `DB_URL_SAMARQAND` yoki `DATABASE_URL_SAMARQAND` - Samarqand bazasi
  - `CLIENTS_DB_URL` yoki `CLIENTS_DATABASE_URL` - Mijozlar bazasi

- Agar yuqoridagi URL lar berilmagan bo'lsa, quyidagilar orqali `DATABASE_URL` avtomatik yig'iladi:
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

- Region bo‘yicha admin tayinlash hozir DB orqali (region users jadvalidagi `role='admin'`) aniqlanadi.
  `.env` dagi `ADMIN_IDS_*` fallback sifatida ishlatilishi mumkin.

### .env namunasi

```
BOT_TOKEN=7591107647:AAEF1v90SSoi1gJBxhvrzGIzCvUvw9-t0Kg
ADMIN_IDS=1978574076
BOT_ID=7591107647
ZAYAVKA_GROUP_ID="-4867209768"

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=ulugbek202

DB_URL_TOSHKENT=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_toshkent
DB_URL_SAMARQAND=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_samarqand
CLIENTS_DB_URL=postgresql://alfaconnect:ulugbek202@localhost:5432/alfaconnect_clients

# Ixtiyoriy fallback ro'yxatlar
ADMIN_IDS_GLOBAL=125
ADMIN_IDS_TOSHKENT=123
ADMIN_IDS_SAMARQAND=1234
```

## 📁 Fayl strukturasi
