### Ishlar ro'yxati (boshlang'ichdan)

Quyida botga kiritilgan o'zgarishlar va ularning sabablari bosqichma-bosqich keltirilgan.

### Maqsad
- 2 ta region (Toshkent, Samarqand) bilan ishlash.
- Xodimlar (staff) ma'lumotlari region DB'larda saqlanadi: `alfaconnect_toshkent` (va kelajakda `alfaconnect_samarqand`).
- Mijozlar (clientlar) `alfaconnect_clients` DB'da saqlanadi.
- /start bosilganda client users jadvalida upsert (create/update), ro'l (role) va staff bo'lsa region(lar)ni aniqlash.

### O'zgartirilgan fayllar va nima qilindi
- `handlers/start_handler.py`
  - /start bosilganda foydalanuvchini `alfaconnect_clients.public.users` ga create/update qiladigan logika qo'shildi.
  - `utils.user_repository.upsert_user_in_clients` o'rniga `database.clients.queries.ensure_global_user` va `get_by_telegram_id` ishlatiladi. Bu `alfaconnect_clients.users` sxemasi bilan mos.
  - Staff rollari (admin, manager, technician, controller, warehouse, call_center, call_center_supervisor, junior_manager) uchun region aniqlash va kerak bo'lsa tanlash klaviaturasi ko'rsatish; client uchun region tanlanmaydi.

- `database/clients/db.py`
  - Mijozlar bazasiga ulanish endi ikkala muhit o'zgaruvchisini ham qabul qiladi: `CLIENTS_DB_URL` yoki `CLIENTS_DATABASE_URL`.

- `database/clients/queries.py`
  - `ensure_global_user` SELECT → UPDATE/INSERT ketma-ketligida ishlaydi (unik indeks talab qilmaydi), `users` jadvaliga mos upsert.
  - `get_by_telegram_id` va boshqa soddalashtirilgan yordamchilar saqlab qolingan.

- `loader.py`
  - `get_user_role` yangilandi: admin aniqlash shartlari:
    - Toshkent DB (`alfaconnect_toshkent.users`) da `role='admin'` bo'lsa — admin.
    - `.env` dagi `ADMIN_IDS_TOSHKENT`/`ADMIN_IDS_SAMARQAND` yoki global `ADMIN_IDS` ichida bo'lsa — admin (fallback).
    - Aks holda DB'dan rol so'raladi; topilmasa `client`.

- `utils/region_context.py`
  - `detect_user_regions` yangilandi: barcha rollar uchun region DB'lardan rol tekshiriladi.
  - Admin uchun: DB'da admin bo'lgan regionlar va `.env`dagi region-admin ro'yxatlari (ADMIN_IDS_<REGION>) union (birlashtiriladi).
  - Client uchun region tanlanmaydi (oqimda ham shunday qo'llaniladi).

- `README.md`
  - `.env` namunasiga siz bergan qiymatlar qo'shildi.
  - Admin aniqlash tartibi (Toshkent DB birlamchi, `.env` fallback) va DB topologiyasi bo'yicha izohlar qo'shildi.

### Konfiguratsiya (.env namuna)
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

ADMIN_IDS_GLOBAL=125
ADMIN_IDS_TOSHKENT=123
ADMIN_IDS_SAMARQAND=1234

LOG_LEVEL=INFO
```

### Ishlash mantig'i (qisqa)
- /start:
  - Client foydalanuvchi `alfaconnect_clients.users` ga create/update qilinadi.
  - Rol aniqlash tartibi: Toshkent DB `role='admin'` → `.env` ADMIN_IDS_* → clients/default DB → `client`.
  - Staff bo'lsa: region(lar) DB'lardan rol bo'yicha olinadi; admin bo'lsa, `.env` region-admin ro'yxati bilan birga birlashtiriladi.
  - Bitta region bo'lsa avtomatik tanlanadi; bir nechta bo'lsa klaviatura bilan tanlanadi. Client uchun region tanlanmaydi.

### Arxitektura va zayavkalar bo'yicha tavsiya
- Clientda "region" yo'q; bir client bir nechta regionda zayavka berishi mumkin.
- Tavsiya etilgan yondashuv (Hybrid):
  - Ochiq zayavkalar: operatsion manba sifatida region DB'lardan yuritiladi.
  - Zayavka yopilganda: soddalashtirilgan nusxasi `alfaconnect_clients` ga ko'chiriladi (client tarixini ko'rsatish uchun).
  - Client UI:
    - Faol zayavkalar — region DB'lardan on-demand.
    - Tarix — `alfaconnect_clients` dan tezkor va yagona joydan.
- Clients DB'dagi `service_requests` uchun tavsiya etilgan maydonlar:
  - `region_code`, `region_request_id`, `client_telegram_id`, `title`, `description`, `address`, `status`, `created_at`, `closed_at`, `total_cost`, `updated_at`.

### Qo'shimcha izohlar
- Indentatsiyalar to'g'rilandi (kerakli joylarda tab → space), kod kompilyatsiya tekshiruvidan o'tkazildi.
- Hech qanday yangi dependency qo'shilmagan (mavjud `requirements.txt` yetarli).

### Hozirgi holat va muammolar (2025-08-15)

#### Yaratilgan modullar:
- `handlers/manager/statistics.py` - Manager statistika funksiyalari
- `handlers/manager/technician_assignment.py` - Texnik tayinlash
- `handlers/manager/word_documents.py` - Hujjat yaratish
- `handlers/manager/notifications.py` - Bildirishnomalar
- `handlers/manager/reports.py` - Hisobotlar
- `handlers/junior_manager/application_creation.py` - Ariza yaratish
- `handlers/junior_manager/application_viewing.py` - Ariza ko'rish
- `handlers/junior_manager/details_input.py` - Ma'lumot kiritish
- `handlers/junior_manager/staff_application_creation.py` - Xodim arizasi
- `handlers/junior_manager/workflow_management.py` - Workflow boshqaruvi
- `handlers/warehouse/workflow_integration.py` - Workflow integratsiyasi

#### Qo'shilgan klaviatura funksiyalari:
- `keyboards/manager_buttons.py` - Barcha manager klaviatura funksiyalari
- `keyboards/technician_buttons.py` - Texnik klaviatura funksiyalari
- `keyboards/controllers_buttons.py` - Controller klaviatura funksiyalari
- `keyboards/call_center_supervisor_buttons.py` - Call center supervisor klaviatura funksiyalari

#### Hali hal qilinmagan muammolar:
1. **Database ulanishi** - PostgreSQL server ishlamayapti
2. **Ko'p modullar** - Hali yaratilmagan yoki to'liq emas
3. **Import xatoliklari** - Ba'zi modullar bir-birini topa olmayapti

#### Keyingi qadamlar:
1. **Database serverini ishga tushirish** - PostgreSQL o'rnatish va sozlash
2. **Eksport qilish** - GitHub repository ga o'zgarishlarni yuklash
3. **Test qilish** - Bot ishlashini tekshirish
4. **Dokumentatsiya** - README va CHANGES fayllarini yangilash