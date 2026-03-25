import time
from scraper import get_price
from models import (
    get_all_products,
    update_price,
    insert_price_history,
    mark_alert_sent
)
from email_service import send_email


def run_tracker():
    while True:
        print("\n🔁 Checking prices...")

        products = get_all_products()

        for product in products:

            # 🔥 SKIP if already alerted
            if product['alert_sent']:
                print(f"⏭️ Skipping {product['product_name']} (already alerted)")
                continue

            try:
                print("\n-----------------------------")
                print("Product:", product['product_name'])

                price_str = get_price(product['product_url'])
                print("RAW price:", price_str)

                # ✅ Safe conversion
                try:
                    price = float(price_str.replace(",", "").strip())
                except Exception as e:
                    print("❌ Price conversion failed:", e)
                    continue

                print("Parsed price:", price)
                print("Target price:", product['target_price'])

                # 🔹 Update DB
                update_price(product['id'], price)

                # 🔹 Store history
                insert_price_history(product['id'], price)

                # 🔹 Check condition (single clean block)
                if price <= product['target_price']:
                    print("✅ Price condition met")
                    print("🚨 TRIGGERING EMAIL...")

                    send_email(
                        product['email'],
                        product['product_name'],
                        price
                    )

                    mark_alert_sent(product['id'])
                    print("✅ Email sent & alert marked")

            except Exception as e:
                print("❌ Error processing product:", e)

        time.sleep(30)   # later change to random 40–59 mins