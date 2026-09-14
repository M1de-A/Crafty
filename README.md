# Crafty 2.7

Crafty is a Django marketplace MVP for the Russian market. This release focuses on the order lifecycle, payments, shop-name uniqueness, fractional reviews, and separation of the Django administrator from normal site profiles.

## Windows launch

1. Extract the archive.
2. Double-click `START_WINDOWS.bat`.
3. Open http://127.0.0.1:8000/

The launcher creates `.venv` when needed, installs dependencies, applies migrations, seeds categories/admin, runs a health check, and starts Django. It does **not** activate PowerShell scripts, so the PowerShell execution-policy problem is avoided.

## Payment setup: YooKassa

The payment flow is prepared for YooKassa. Create a `.env` file from `.env.example` and add:

```env
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
```

After payment credentials are configured, the cart creates an order and the order page offers a YooKassa payment button. Crafty stores the YooKassa payment ID/status and has both a return URL and webhook endpoint. YooKassa recommends creating a payment server-side and redirecting the customer to the returned `confirmation_url`; the integration follows that redirect flow.

Webhook URL for a deployed site:

`https://YOUR-DOMAIN/orders/payment/webhook/`

For local development, use a public HTTPS tunnel when testing webhook delivery.

## Order statuses

The order card shows only the current status by default. Hovering it opens an animated status history. Completed stages receive a green rectangular highlight. Cancellation and return have their own visual states and show the stored reason.

Lifecycle:

`Ожидает оплаты → Оплачен → Сборка → Отправлен → Доставлен → Завершён`

Additional states: `Отменён`, `Возврат`, `Спор`.

- Buyer can cancel only during `Сборка` and must provide a reason.
- Seller can cancel only during `Сборка` and must provide a reason.
- Buyer can request `Возврат` after delivery/completion and must provide a reason.
- Cancelling an order restores the reserved stock.

## Reviews

- Rating is selectable in 0.5 increments from 0.5 to 5.0.
- The picker uses an interactive five-star UI.
- After publication, the rating is locked.
- The buyer can later edit only the text and add information to the existing review.

## Shops

Shop names are now unique case-insensitively. Existing duplicate names are automatically renamed during migration before the unique database constraint is applied.

## Administrator separation

Django superusers no longer receive a Crafty `Profile`. Existing superuser profiles are removed by migration. A superuser logging into the site is redirected to `/admin/` and the normal Crafty profile controls are hidden from the site header.

## Database

Run after updating an existing installation:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_crafty
.venv\Scripts\python.exe manage.py crafty_check
```

SQLite remains the default. PostgreSQL support remains available through the existing environment variables.

## Crafty 2.7 changes

- Fixed seller order-status saving.
- Reworked status UI into a hover timeline.
- Added cancellation reasons and cancellation permissions.
- Added `Возврат` status and buyer return request.
- Added YooKassa payment flow, payment return and webhook.
- Made shop names globally unique, case-insensitive.
- Added 0.5-step review ratings.
- Locked published review ratings while allowing text additions.
- Removed the normal Crafty profile from Django superusers.
