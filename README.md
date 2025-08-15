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
git clone https://github.com/yourusername/alfaconnect-bot.git
cd alfaconnect-bot
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

## 🔧 Konfiguratsiya

`.env` faylida quyidagi sozlamalar mavjud:
- `BOT_TOKEN` - Telegram bot token (@BotFather dan)
- `BOT_ID` - Ixtiyoriy. Agar kiritilmasa, `BOT_TOKEN` dan avtomatik olinadi
- `ADMIN_IDS` - Adminlar roʻyxati, vergul bilan ajratilgan (masalan: `123,456`)
- `ZAYAVKA_GROUP_ID` - Ixtiyoriy. Arizalar uchun guruh ID si
- `LOG_LEVEL` - Logging darajasi (`INFO`, `DEBUG`, `ERROR`)

- Postgres uchun bitta umumiy URL yoki bo'linma/regionlarga ajratilgan URL lar:
  - `DATABASE_URL` - Umumiy standart baza URL (masalan: `postgresql://user:pass@host:5432/dbname`)
  - `DB_URL_TOSHKENT` yoki `DATABASE_URL_TOSHKENT` - Toshkent bazasi
  - `DB_URL_SAMARQAND` yoki `DATABASE_URL_SAMARQAND` - Samarqand bazasi
  - `CLIENTS_DB_URL` yoki `CLIENTS_DATABASE_URL` - Mijozlar bazasi

- Agar yuqoridagi URL lar berilmagan bo'lsa, quyidagilar orqali `DATABASE_URL` avtomatik yig'iladi:
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

- Ixtiyoriy rollar uchun IDs (kiritilsa, rol menyulari shu ID egalari bilan bog'lanadi):
  - `MANAGER_ID`, `CLIENT_ID`, `JUNIOR_MANAGER_ID`, `CONTROLLER_ID`, `TECHNICIAN_ID`, `WAREHOUSE_ID`, `CALL_CENTER_SUPERVISOR_ID`, `CALL_CENTER_ID`

## 📁 Fayl strukturasi

```
alfaconnect-bot/
├── handlers/           # Bot handlerlari
│   ├── admin/         # Admin funksiyalari
│   ├── manager/       # Manager funksiyalari
│   ├── controller/    # Controller funksiyalari
│   └── ...
├── keyboards/         # Klaviaturalar
├── states/           # FSM states
├── utils/            # Yordamchi funksiyalar
├── middlewares/      # Middleware
├── filters/          # Filterlar
├── main.py          # Asosiy fayl
└── requirements.txt # Dependencies
```

## 🛠️ Texnologiyalar

- **Python 3.8+**
- **aiogram 3.x** - Telegram Bot framework
- **openpyxl** - Excel fayllar bilan ishlash
- **python-docx** - Word fayllar bilan ishlash
- **reportlab** - PDF generatsiya
- **Faker** - Test ma'lumotlar generatsiyasi

## 📊 Export funksiyalari

Har bir rol uchun maxsus export imkoniyatlari:

### Manager:
- Buyurtmalar
- Statistika
- Xodimlar
- Hisobotlar

### Controller:
- Buyurtmalar (sifat ko'rsatkichlari bilan)
- Sifat nazorati
- Texniklar
- Statistika

### Call Center Supervisor:
- Buyurtmalar
- Xodimlar
- Fikr-mulohazalar
- Workflow

### Admin:
- Foydalanuvchilar
- Buyurtmalar
- Tizim sozlamalari
- Loglar

### Warehouse:
- Inventarizatsiya
- Berilgan materiallar
- Buyurtmalar
- Statistika

## ⚠️ Muhim eslatmalar

1. **Database**: Hozircha database integratsiyasi yo'q, barcha ma'lumotlar fake
2. **Security**: Production uchun qo'shimcha xavfsizlik choralari kerak
3. **Performance**: Katta hajmdagi export uchun optimization kerak

## 🐛 Xatoliklar va takliflar

Xatolik topsangiz yoki taklif bo'lsa, GitHub Issues orqali xabar bering.

## 📄 Litsenziya

MIT License

## 👥 Hissa qo'shish

Pull requestlar qabul qilinadi. Katta o'zgarishlar uchun avval issue oching.

## 📞 Aloqa

Support: @your_support_bot
Email: support@alfaconnect.uz