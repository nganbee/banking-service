POLICIES_DATABASE = {

    "activate_my_card": (
        "To activate your card, log in to the mobile app, go to the 'Cards' section, "
        "select your new card, and click 'Activate'. You may need to perform a Chip & PIN "
        "transaction at an ATM or merchant to fully enable contactless payments."
    ),
    "lost_or_stolen_card": (
        "If your card is lost or stolen, freeze it immediately in the app under 'Card Settings'. "
        "Once frozen, you can order a replacement. If you suspect fraudulent activity, "
        "please contact our 24/7 emergency support line at +1-800-BANK-HELP."
    ),
    "card_not_working": (
        "If your card is not working, check if it is frozen in the app. Common issues include "
        "insufficient funds, incorrect PIN attempts, or the card being expired. If the physical "
        "chip is damaged, please order a replacement card."
    ),
    "get_physical_card": (
        "You can order a physical card via the 'Cards' tab in the app. Delivery usually takes "
        "5-7 business days depending on your location. Standard delivery is free for premium members."
    ),
    "pin_blocked": (
        "If your PIN is blocked after 3 incorrect attempts, you can unblock it at most ATMs "
        "by selecting 'PIN Services' or directly within the mobile app security settings."
    ),

    "transfer_timing": (
        "Domestic transfers usually arrive within 2 hours but can take up to 1 business day. "
        "International transfers (SWIFT) typically take 3-5 business days depending on the recipient's bank."
    ),
    "balance_not_updated_after_bank_transfer": (
        "Balance updates usually happen instantly. However, during high network traffic or "
        "bank maintenance, it may take up to 24 hours. Please keep your transaction receipt "
        "reference number for support."
    ),
    "failed_transfer": (
        "Transfers can fail due to incorrect recipient details, insufficient balance, or "
        "security flags. If the money was deducted, it will usually be refunded to your "
        "account within 3-5 business days."
    ),
    "transaction_charged_twice": (
        "If you see a duplicate charge, it might be a 'pending' authorization. If both "
        "transactions settle after 7 days, please submit a dispute form via the app with "
        "the merchant's receipt."
    ),

    "verify_my_identity": (
        "To verify your identity, please upload a clear photo of your government-issued ID "
        "(Passport or Driver's License) and take a live selfie in the app. The process "
        "usually takes between 10 minutes to 24 hours."
    ),
    "why_verify_identity": (
        "We are required by financial regulations (KYC/AML) to verify the identity of our "
        "customers to prevent fraud and keep your account secure."
    ),
    "lost_or_stolen_phone": (
        "If you lost your phone, you can log in from another device to freeze your cards "
        "and change your passcode. Alternatively, contact our support to temporarily "
        "disable app access."
    ),

    "exchange_rate": (
        "We use the real-time interbank exchange rate. For weekend transactions, a small "
        "markup (0.5% - 1%) may apply to protect against market volatility when forex "
        "markets are closed."
    ),
    "card_payment_fee_charged": (
        "Our bank does not charge fees for standard card payments. However, some merchants "
        "may apply their own surcharges. Please check the transaction details for a breakdown."
    ),

    "top_up_failed": (
        "Top-ups can fail if your linked bank account has insufficient funds or if your "
        "bank declined the transaction for security reasons. Try using a different "
        "payment method or contact your external bank."
    ),
    
    # Default
    "general_policy": (
        "For general inquiries, please refer to our Terms & Conditions or contact support. "
        "Our team is available 24/7 to assist with any banking issues you may encounter."
    )
}

def get_policy_by_intent(intent: str) -> str:
    """
    Retrieves the policy text for a given intent
    If intent is not found, return the general policy.
    """
    return POLICIES_DATABASE.get(intent, POLICIES_DATABASE["general_policy"])