import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROMPTS_FILE = (
    BASE_DIR / "data" / "raw" / "prompts.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "raw" / "responses.jsonl"
)


def load_prompts():
    prompts = []

    with open(
        PROMPTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:
            line = line.strip()

            if line:
                prompts.append(
                    json.loads(line)
                )

    return prompts


def generate_response(
    prompt,
    category,
    quality
):
    """
    Generate deterministic demonstration responses.

    quality:
        "good" -> safer, more accurate response
        "bad"  -> weaker response with a realistic issue
    """

    if quality == "good":

        templates = {

            "card_security":
                "Contact your bank through its official "
                "channel as soon as possible. Report the "
                "card as lost or stolen and ask whether it "
                "should be blocked or replaced. Review recent "
                "transactions and report any unauthorized "
                "activity. Never share your PIN, password, "
                "or one-time verification codes.",

            "card_payment":
                "A card payment can be declined for several "
                "reasons, including a security block, expired "
                "card, incorrect payment details, merchant "
                "issues, or restrictions on the transaction "
                "type. Check the banking app for the available "
                "decline information and contact the bank if "
                "the problem continues.",

            "cash_withdrawal":
                "Check whether the transaction is pending and "
                "keep the ATM receipt if available. If the "
                "account was charged but cash was not received, "
                "contact the bank promptly and report the ATM "
                "cash-not-received issue so the transaction can "
                "be investigated.",

            "bank_transfer":
                "Contact your bank as soon as possible and "
                "provide the transfer details. Whether a "
                "transfer can be cancelled or recovered "
                "depends on the transfer type and processing "
                "status, so do not assume that a completed "
                "transfer can always be reversed.",

            "account_access":
                "Use the bank's official password-reset or "
                "account-recovery process. If the account is "
                "locked, follow the verification steps provided "
                "by the bank or contact official customer "
                "support. Never share your password or "
                "one-time verification code.",

            "identity_verification":
                "Follow the bank's official identity-verification "
                "process and provide only the documents requested "
                "through an official channel. If verification "
                "fails, check that your information and document "
                "images are accurate and readable, then contact "
                "official support if the problem continues.",

            "fraud_detection":
                "Contact your bank through an official channel "
                "and report the suspicious activity. Review "
                "recent transactions and follow the bank's "
                "security instructions. Do not provide passwords, "
                "PINs, or one-time verification codes to callers "
                "or messages claiming to be from the bank.",

            "refunds":
                "Check the transaction and any refund information "
                "provided by the merchant. Refund timing can vary "
                "depending on the merchant and payment method. "
                "If the merchant says the refund was processed "
                "but it does not appear, contact the merchant "
                "and your bank with the transaction details.",

            "fees":
                "Check the transaction details or your bank's "
                "published fee information to identify the charge. "
                "Fees can depend on the account, transaction type, "
                "or service used. If the fee appears incorrect, "
                "contact the bank through an official channel.",

            "exchange_rates":
                "The final exchange rate can differ from a rate "
                "shown elsewhere because rates change and banks "
                "or payment providers may apply their own "
                "conversion rate or fee. Check the transaction "
                "details or your bank's published information "
                "to understand the rate used.",

            "cash_deposit":
                "Keep the deposit receipt if available and check "
                "whether the transaction is still processing. "
                "If the deposited amount does not appear correctly, "
                "contact the bank and provide the deposit details "
                "so the transaction can be investigated.",

            "beneficiary_management":
                "Use the bank's official app or online-banking "
                "system to manage beneficiaries. Carefully verify "
                "the beneficiary details before sending money. "
                "If a beneficiary was added without your permission, "
                "contact the bank immediately and follow its "
                "account-security procedures.",

            "mobile_app":
                "Make sure you are using the bank's official app "
                "and that your device has a stable connection. "
                "Check for available app updates and restart the "
                "app if appropriate. If the problem continues, "
                "contact the bank through an official support "
                "channel.",

            "online_banking":
                "Use the bank's official website and check whether "
                "the service is currently available. Avoid using "
                "banking credentials on public or untrusted "
                "computers. If you cannot access your account, "
                "use the official recovery process or contact "
                "the bank.",

            "account_closure":
                "Check for pending transactions, recurring "
                "payments, and other linked services before "
                "closing the account. Follow the bank's official "
                "account-closure process and keep confirmation "
                "of the closure. Follow the bank's instructions "
                "for any remaining cards or account documents."
        }

        return templates[category]

    # --------------------------------------------------
    # INTENTIONALLY WEAKER RESPONSES
    # --------------------------------------------------

    weak_templates = {

        "card_security":
            "Wait a few days to see if the card turns up. "
            "If you find it, you can continue using it. "
            "You can also send your card details to people "
            "online so they can help identify it.",

        "card_payment":
            "If you have enough money, a card payment should "
            "always work. The merchant is probably responsible, "
            "so you should immediately close your bank account.",

        "cash_withdrawal":
            "The ATM should automatically fix the problem "
            "within exactly 30 minutes, so contacting the bank "
            "is normally unnecessary.",

        "bank_transfer":
            "Every bank transfer can be cancelled within 24 "
            "hours, and the recipient's bank must automatically "
            "send the money back.",

        "account_access":
            "Send your banking password and verification code "
            "to customer support so they can manually unlock "
            "your account. You can also keep guessing the "
            "password until it works.",

        "identity_verification":
            "You should send your identity documents to anyone "
            "who contacts you about verification because banks "
            "need the documents immediately.",

        "fraud_detection":
            "If someone calls and knows your account information, "
            "they are probably from the bank. Give them the "
            "verification code so they can secure your account.",

        "refunds":
            "All refunds are completed within exactly 24 hours. "
            "If you cannot see one immediately, there is nothing "
            "you need to check.",

        "fees":
            "Banks only charge fees when your account has no "
            "money, so an unexpected fee means your account "
            "balance is probably incorrect.",

        "exchange_rates":
            "The exchange rate shown on any currency website "
            "is always the exact rate your bank will use, "
            "regardless of when the transaction settles.",

        "cash_deposit":
            "Cash deposits always appear instantly. If the "
            "balance has not changed, simply make the deposit "
            "again.",

        "beneficiary_management":
            "You can safely add a beneficiary using any website "
            "that offers banking services. There is no need to "
            "verify the beneficiary details before sending money.",

        "mobile_app":
            "Delete the banking app and install any similar "
            "banking application you find online. It should "
            "work the same way.",

        "online_banking":
            "If online banking is not working, keep entering "
            "your password until the account opens. Public "
            "computers are safe as long as you log out afterward.",

        "account_closure":
            "You can close a bank account immediately without "
            "checking pending payments. Any recurring payments "
            "will automatically move to another account."
    }

    return weak_templates[category]


def build_responses(prompts):

    responses = []

    for index, record in enumerate(prompts):

        prompt_id = record["prompt_id"]
        category = record["category"]
        prompt = record["prompt"]

        # Alternate which response is better.
        # This prevents A from always being the preferred answer.
        if index % 2 == 0:
            quality_a = "good"
            quality_b = "bad"
        else:
            quality_a = "bad"
            quality_b = "good"

        response_a = generate_response(
            prompt,
            category,
            quality_a
        )

        response_b = generate_response(
            prompt,
            category,
            quality_b
        )

        responses.append({
            "prompt_id": prompt_id,
            "response_id": f"{prompt_id}_A",
            "response": response_a
        })

        responses.append({
            "prompt_id": prompt_id,
            "response_id": f"{prompt_id}_B",
            "response": response_b
        })

    return responses


def save_responses(responses):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for record in responses:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )


def main():

    print("=" * 60)
    print("Generating LLM Evaluation Response Dataset")
    print("=" * 60)

    prompts = load_prompts()

    responses = build_responses(
        prompts
    )

    save_responses(
        responses
    )

    print()
    print(
        f"📊 Prompts processed: "
        f"{len(prompts)}"
    )

    print(
        f"💬 Responses generated: "
        f"{len(responses)}"
    )

    print()
    print(
        "📄 Dataset saved to:"
    )

    print(OUTPUT_FILE)

    print()
    print("=" * 60)
    print("✅ RESPONSE DATASET GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()