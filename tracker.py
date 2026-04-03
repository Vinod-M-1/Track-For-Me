# import time
# from scraper import get_price
# from models import (
#     get_all_products,
#     update_price,
#     insert_price_history,
#     mark_alert_sent
# )
# from email_service import send_email


# def run_tracker():
#     while True:
#         print("\n🔁 Checking prices...")

#         products = get_all_products()

#         for product in products:

#             # 🔥 SKIP if already alerted
#             if product['alert_sent']:
#                 print(f"⏭️ Skipping {product['product_name']} (already alerted)")
#                 continue

#             try:
#                 print("\n-----------------------------")
#                 print("Product:", product['product_name'])

#                 price_str = get_price(product['product_url'])
#                 print("RAW price:", price_str)

#                 # ✅ Safe conversion
#                 try:
#                     price = float(price_str.replace(",", "").strip())
#                 except Exception as e:
#                     print("❌ Price conversion failed:", e)
#                     continue

#                 print("Parsed price:", price)
#                 print("Target price:", product['target_price'])

#                 # 🔹 Update DB
#                 update_price(product['id'], price)

#                 # 🔹 Store history
#                 insert_price_history(product['id'], price)

#                 # 🔹 Check condition (single clean block)
#                 if price <= product['target_price']:
#                     print("✅ Price condition met")
#                     print("🚨 TRIGGERING EMAIL...")

#                     send_email(
#                         product['email'],
#                         product['product_name'],
#                         price
#                     )

#                     mark_alert_sent(product['id'])
#                     print("✅ Email sent & alert marked")

#             except Exception as e:
#                 print("❌ Error processing product:", e)

#         time.sleep(30)   # later change to random 40–59 mins

import time
import re  # 🔹 Added for better price cleaning
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
                print("RAW price from scraper:", price_str)

                # ✅ ROBUST CONVERSION: Remove ₹, Rs, commas, and whitespace
                try:
                    # Extracts only digits and decimal points (e.g., "₹18,999.00" -> "18999.00")
                    clean_price_str = re.sub(r'[^\d.]', '', price_str)
                    
                    if not clean_price_str:
                        raise ValueError("No numeric digits found in price string")
                        
                    price = float(clean_price_str)
                except Exception as e:
                    print(f"❌ Conversion failed for {product['product_name']}: {e}")
                    # If scraping fails, we don't update the price, just move to next product
                    continue 

                print("Parsed price:", price)
                print("Target price:", product['target_price'])

                # 🔹 Update DB with the new numeric price
                update_price(product['id'], price)

                # 🔹 Store history
                insert_price_history(product['id'], price)

                # 🔹 Check condition
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
                print(f"❌ Critical Error processing {product['product_name']}: {e}")

        # Change this to 1800 (30 mins) once you're done testing to avoid IP bans!
        print("\n😴 Sleeping for 60 seconds...")
        time.sleep(60)