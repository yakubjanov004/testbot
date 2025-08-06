# Controller Reply Utilities Guide

Bu qo'llanma controller uchun yangi reply utility'larini qanday ishlatishni ko'rsatadi.

## Asosiy Maqsad

Controller handler'larda barcha reply va inline response'larni to'g'ri boshqarish uchun universal utility funksiyalar yaratildi.

## Asosiy Funksiyalar

### 1. `send_or_edit_message()`
Universal xabar yuborish yoki tahrirlash funksiyasi.

```python
from utils.reply_utils import send_or_edit_message

# Oddiy xabar
await send_or_edit_message(
    message, 
    "Xabar matni", 
    state,
    parse_mode='HTML'
)

# Callback query bilan
await send_or_edit_message(
    callback,
    "Xabar matni",
    state,
    reply_markup=keyboard
)
```

### 2. `answer_callback_query()`
Callback query'ga xavfsiz javob berish.

```python
from utils.reply_utils import answer_callback_query

await answer_callback_query(callback, "Javob matni")
await answer_callback_query(callback, "Xatolik!", show_alert=True)
```

### 3. `reply_with_error()`
Xatolik xabarini yuborish.

```python
from utils.reply_utils import reply_with_error

# Message uchun
await reply_with_error(message, state, "Xatolik yuz berdi")

# Callback query uchun
await reply_with_error(callback, state, "Xatolik yuz berdi")
```

### 4. `reply_with_success()`
Muvaffaqiyat xabarini yuborish.

```python
from utils.reply_utils import reply_with_success

await reply_with_success(message, state, "Muvaffaqiyatli bajarildi!")
```

### 5. `reply_with_info()`
Ma'lumot xabarini yuborish.

```python
from utils.reply_utils import reply_with_info

await reply_with_info(message, state, "ℹ️ Ma'lumot xabari")
```

### 6. `handle_inline_response()`
Inline response uchun.

```python
from utils.reply_utils import handle_inline_response

await handle_inline_response(
    callback,
    state,
    "Response matni",
    show_alert=True
)
```

### 7. `clear_message_state()`
Message state'ni tozalash.

```python
from utils.reply_utils import clear_message_state

await clear_message_state(state)
```

### 8. `send_confirmation_message()`
Tasdiqlash xabarini yuborish.

```python
from utils.reply_utils import send_confirmation_message

await send_confirmation_message(
    message,
    state,
    "❓ Bu amalni bajarishni xohlaysizmi?",
    "confirm_action",
    "cancel_action"
)
```

### 9. `send_list_message()`
Ro'yxat xabarini yuborish.

```python
from utils.reply_utils import send_list_message

items = ["Element 1", "Element 2", "Element 3"]

def format_item(item, index):
    return f"{index}. {item}\n"

await send_list_message(
    message,
    state,
    "📋 Ro'yxat",
    items,
    item_formatter=format_item
)
```

### 10. `send_paginated_message()`
Sahifali xabar yuborish.

```python
from utils.reply_utils import send_paginated_message

await send_paginated_message(
    message,
    state,
    "📄 Sahifali ro'yxat",
    items,
    page=1,
    items_per_page=10,
    navigation_callback_prefix="page"
)
```

### 11. `reply_with_loading()`
Yuklash xabarini yuborish.

```python
from utils.reply_utils import reply_with_loading

await reply_with_loading(message, state, "⏳ Yuklanmoqda...")
```

## Amaliy Misollar

### 1. Oddiy Handler

```python
@router.message(F.text == "Test")
async def test_handler(message: Message, state: FSMContext):
    try:
        await send_or_edit_message(
            message,
            "✅ Test muvaffaqiyatli!",
            state,
            parse_mode='HTML'
        )
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

### 2. Callback Query Handler

```python
@router.callback_query(F.data == "test_button")
async def test_callback_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await answer_callback_query(callback, "Tugma bosildi!")
        
        await send_or_edit_message(
            callback,
            "✅ Callback muvaffaqiyatli!",
            state,
            parse_mode='HTML'
        )
    except Exception as e:
        await reply_with_error(callback, state, f"Xatolik: {e}")
```

### 3. Kompleks Workflow

```python
@router.message(F.text == "Complex Workflow")
async def complex_workflow(message: Message, state: FSMContext):
    try:
        # 1. Yuklash ko'rsatish
        await reply_with_loading(message, state, "⏳ Jarayon boshlanmoqda...")
        
        # 2. Ish bajarish
        import asyncio
        await asyncio.sleep(2)
        
        # 3. Natijani ko'rsatish
        await send_or_edit_message(
            message,
            "✅ Jarayon tugadi!",
            state,
            parse_mode='HTML'
        )
        
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

### 4. Ro'yxat Ko'rsatish

```python
@router.message(F.text == "Show List")
async def show_list(message: Message, state: FSMContext):
    try:
        items = [
            {"name": "Item 1", "status": "active"},
            {"name": "Item 2", "status": "inactive"},
            {"name": "Item 3", "status": "active"}
        ]
        
        def format_item(item, index):
            status_emoji = "🟢" if item["status"] == "active" else "🔴"
            return f"{index}. {status_emoji} {item['name']}\n"
        
        await send_list_message(
            message,
            state,
            "📋 Elementlar ro'yxati",
            items,
            item_formatter=format_item
        )
        
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

### 5. Tasdiqlash Dialog

```python
@router.message(F.text == "Confirm Action")
async def confirm_action(message: Message, state: FSMContext):
    try:
        await send_confirmation_message(
            message,
            state,
            "❓ Bu amalni bajarishni xohlaysizmi?",
            "confirm_delete",
            "cancel_delete"
        )
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")

@router.callback_query(F.data == "confirm_delete")
async def handle_confirm(callback: CallbackQuery, state: FSMContext):
    try:
        # Amalni bajarish
        await reply_with_success(callback, state, "Amal bajarildi!")
    except Exception as e:
        await reply_with_error(callback, state, f"Xatolik: {e}")

@router.callback_query(F.data == "cancel_delete")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    try:
        await reply_with_info(callback, state, "Amal bekor qilindi.")
    except Exception as e:
        await reply_with_error(callback, state, f"Xatolik: {e}")
```

## Xatoliklar bilan Ishlash

### 1. Try-Catch Bloki

```python
@router.message(F.text == "Safe Handler")
async def safe_handler(message: Message, state: FSMContext):
    try:
        # Asosiy logika
        result = await some_operation()
        
        if result:
            await reply_with_success(message, state, "Muvaffaqiyatli!")
        else:
            await reply_with_error(message, state, "Natija topilmadi!")
            
    except Exception as e:
        print(f"Error in safe_handler: {e}")
        await reply_with_error(message, state, "Xatolik yuz berdi!")
```

### 2. Validation

```python
@router.message(F.text == "Validate Input")
async def validate_handler(message: Message, state: FSMContext):
    try:
        # Input tekshirish
        if not message.text or len(message.text) < 3:
            return await reply_with_error(message, state, "Noto'g'ri input!")
        
        # Asosiy logika
        await reply_with_success(message, state, "Input to'g'ri!")
        
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

## State Management

### 1. State Tozalash

```python
@router.message(F.text == "Clear State")
async def clear_state_handler(message: Message, state: FSMContext):
    try:
        await clear_message_state(state)
        await reply_with_success(message, state, "State tozalandi!")
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

### 2. State Saqlash

```python
@router.message(F.text == "Save State")
async def save_state_handler(message: Message, state: FSMContext):
    try:
        # State'ga ma'lumot saqlash
        await state.update_data(
            current_step="completed",
            user_input=message.text
        )
        
        await reply_with_success(message, state, "Ma'lumot saqlandi!")
        
    except Exception as e:
        await reply_with_error(message, state, f"Xatolik: {e}")
```

## Import Qilish

```python
from utils.reply_utils import (
    send_or_edit_message,
    answer_callback_query,
    reply_with_error,
    reply_with_success,
    reply_with_info,
    handle_inline_response,
    clear_message_state,
    send_confirmation_message,
    send_list_message,
    send_paginated_message,
    reply_with_loading
)
```

## Afzalliklar

1. **Universal**: Barcha reply turlari uchun bir xil API
2. **Xavfsiz**: Xatoliklar bilan to'g'ri ishlash
3. **Qulay**: Oddiy va tushunarli funksiyalar
4. **Moslashuvchan**: Turli xil vaziyatlar uchun
5. **Konsistent**: Barcha handler'larda bir xil stil

## Eslatmalar

- Har doim `try-catch` blokidan foydalaning
- Xatolik xabarlarini foydalanuvchi uchun tushunarli qiling
- State'ni to'g'ri boshqaring
- Callback query'larni har doim javoblang
- Loading xabarlarini uzun jarayonlar uchun ishlating