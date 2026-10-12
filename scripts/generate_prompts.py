import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "prompts.jsonl"
)


categories = {
    "card_security": [
        "My debit card was stolen. What should I do?",
        "I lost my debit card while traveling. What should I do first?",
        "Someone may have copied my card details. What should I do?",
        "I received a card transaction I do not recognize.",
        "My card was stolen and I noticed a suspicious transaction.",
        "Should I share my card number with someone claiming to be from my bank?",
        "My physical card is missing but I still have access to my banking app.",
        "I think someone knows my card PIN. What should I do?"
    ],

    "card_payment": [
        "My card payment was declined, but I have enough money in my account. Why did this happen?",
        "Why was my card payment declined at a store?",
        "My contactless payment stopped working.",
        "My card works online but not in physical stores.",
        "My card works in stores but online payments are failing.",
        "A merchant charged my card twice for the same purchase.",
        "A card payment is showing as pending for a long time.",
        "The merchant says my payment failed, but I see a charge in my account."
    ],

    "cash_withdrawal": [
        "The ATM didn't give me any cash, but the money was deducted from my account. What should I do?",
        "The ATM kept my card. What should I do?",
        "Why was my ATM withdrawal declined?",
        "The ATM gave me less cash than I requested.",
        "I was charged an unexpected ATM fee.",
        "My cash withdrawal is showing as pending.",
        "The ATM gave me cash but the transaction is still showing incorrectly.",
        "Can I use another bank's ATM to withdraw money?"
    ],

    "bank_transfer": [
        "I sent money to the wrong bank account. Can I cancel the transfer?",
        "How long does a bank transfer normally take?",
        "My bank transfer is still pending.",
        "The recipient says they have not received my transfer.",
        "My bank transfer was declined.",
        "I entered the wrong amount in a bank transfer.",
        "Can a completed bank transfer be reversed?",
        "Why is my international transfer taking longer than expected?"
    ],

    "account_access": [
        "I forgot my banking app password and now my account is locked. How can I regain access?",
        "I cannot log in to my banking app.",
        "My banking app keeps rejecting my password.",
        "I forgot my username for online banking.",
        "My account was temporarily locked after several failed login attempts.",
        "I changed my phone and cannot access my banking app.",
        "I no longer have access to the phone number linked to my bank account.",
        "How can I safely recover access to my online banking account?"
    ],

    "identity_verification": [
        "Why is my bank asking me to verify my identity?",
        "My identity verification failed. What should I do?",
        "What documents might a bank require for identity verification?",
        "Why does my bank need a photo of my identification?",
        "My verification document was rejected because the image was unclear.",
        "Can someone else complete identity verification for me?",
        "My name on my bank account is different from my identification document.",
        "How can I complete identity verification safely?"
    ],

    "fraud_detection": [
        "I think someone is using my bank account without permission.",
        "I received a banking alert for a transaction I did not make.",
        "Someone called claiming to be my bank and asked for a verification code.",
        "I clicked a suspicious link that looked like my bank's website.",
        "I accidentally gave my one-time verification code to someone.",
        "I received a suspicious banking email.",
        "My account shows several small transactions I do not recognize.",
        "What should I do if I suspect my banking credentials have been compromised?"
    ],

    "refunds": [
        "A merchant promised me a refund but I have not received it.",
        "How long can a card refund take?",
        "I received only a partial refund.",
        "The merchant says the refund was processed but it is not visible in my account.",
        "Can I request a refund for a card purchase?",
        "I was charged for an order that the merchant cancelled.",
        "The refund amount is different from the original purchase amount.",
        "What should I do if a merchant refuses to refund a valid transaction?"
    ],

    "fees": [
        "Why was I charged a bank service fee?",
        "I was charged a fee I do not recognize.",
        "Are there usually fees for international transfers?",
        "Why did I receive less money after a bank transfer?",
        "How can I find out what a banking fee is for?",
        "Can ATM fees vary depending on which ATM I use?",
        "I was charged a monthly account maintenance fee.",
        "Can a bank refund an incorrectly charged fee?"
    ],

    "exchange_rates": [
        "How does a bank determine the exchange rate for a card purchase?",
        "Why is the exchange rate different from the rate I saw online?",
        "I made a foreign currency purchase and the final amount is different.",
        "What is the difference between an exchange rate and a currency conversion fee?",
        "Why did I receive less foreign currency than expected?",
        "Can exchange rates change between the time I make a purchase and when it settles?",
        "How can I check the exchange rate used for my transaction?",
        "Why does my international card transaction cost more than expected?"
    ],

    "cash_deposit": [
        "I deposited cash but it has not appeared in my account.",
        "How long can a cash deposit take to appear?",
        "The cash deposit amount showing in my account is incorrect.",
        "Can I deposit cash at an ATM?",
        "The cash deposit machine rejected some of my notes.",
        "I received a deposit receipt but the balance has not updated.",
        "What should I do if a cash deposit is missing?",
        "Can someone else deposit cash into my bank account?"
    ],

    "beneficiary_management": [
        "How do I add a new bank transfer beneficiary?",
        "Why can't I add a new beneficiary?",
        "My beneficiary details may be incorrect. What should I do?",
        "Can I remove a beneficiary from my banking app?",
        "Why is there a waiting period after adding a beneficiary?",
        "I accidentally added the wrong beneficiary.",
        "How can I verify beneficiary details before sending money?",
        "Someone added a beneficiary to my account without my permission."
    ],

    "mobile_app": [
        "My banking app keeps crashing.",
        "My banking app is not showing my latest transactions.",
        "The banking app says there is a connection error.",
        "I installed the banking app on a new phone.",
        "Why is my banking app asking me to update?",
        "The app notification for a transaction arrived late.",
        "My banking app is showing an incorrect account balance.",
        "How can I make sure I am using the official banking app?"
    ],

    "online_banking": [
        "How can I check my recent transactions through online banking?",
        "I cannot access online banking from my computer.",
        "My online banking session keeps logging me out.",
        "How can I update my contact information through online banking?",
        "Why is online banking temporarily unavailable?",
        "How can I safely use online banking on a public computer?",
        "I see a transaction online that I do not recognize.",
        "What should I do if my online banking credentials stop working?"
    ],

    "account_closure": [
        "How can I close my bank account?",
        "What should I check before closing a bank account?",
        "Can I close my account if there are pending transactions?",
        "I want to switch banks. How should I close my old account?",
        "What happens to recurring payments when I close my account?",
        "Can I reopen a bank account after closing it?",
        "My bank account closure request is still pending.",
        "What should I do with my debit card after closing my account?"
    ]
}


def build_prompts():
    prompts = []

    prompt_number = 1

    for category, category_prompts in categories.items():

        for prompt in category_prompts:

            prompts.append({
                "prompt_id": f"P{prompt_number:03d}",
                "category": category,
                "prompt": prompt
            })

            prompt_number += 1

    return prompts


def save_prompts(prompts):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for record in prompts:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )


def main():

    print("=" * 60)
    print("Generating LLM Evaluation Prompt Dataset")
    print("=" * 60)

    prompts = build_prompts()

    save_prompts(prompts)

    category_counts = {}

    for record in prompts:

        category = record["category"]

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

    print()
    print(f"📊 Total prompts: {len(prompts)}")
    print()
    print("📂 Category distribution:")
    print("-" * 40)

    for category, count in category_counts.items():

        print(
            f"{category:<25} {count}"
        )

    print()
    print("📄 Dataset saved to:")
    print(OUTPUT_FILE)

    print()
    print("=" * 60)
    print("✅ PROMPT DATASET GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()