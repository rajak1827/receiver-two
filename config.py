import os
from dotenv import load_dotenv

load_dotenv()

API_ID = "27318249"
API_HASH = "368c464c22f8db4bd452f66d43888dcb"

BOT_TOKEN = "7363824392:AAGTbVZ3yowxoGFqjQvXgGDGccNKmluHJuI"
MONGO_URL = "mongodb+srv://reveiver165:receiverpass1927@cluster0.bqbqz55.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MUST_JOIN = "virtualreciver"
SUDO_USERS = [5948884710 , 6076230804]


OWNER_ID = 5948884710
LOG_CHANNEL = -1002084612542
SPAM_BOT_ID = 178220800
SESSION_CHANNEL = -1001900317787
CHECKOUT_CHANNEL = -1001907540116
UPDATES_CHANNEL = "https://t.me/virtualreciver"
FA_PASSWORD = "Aakash198"
FA_HINT = "Bye"


DEFAULT_RATES = {
    "TIER_4": 4.0,    
    "TIER_2": 2.0,    
    "TIER_1": 1.0,    
    "DEFAULT": 0.3    
}


COUNTRY_CODES = {
    
    "500": {"name": "Falkland Islands", "tier": "TIER_4", "flag": "🇫🇰", "rate": 4.0},
    
    
    "971": {"name": "United Arab Emirates", "tier": "TIER_2", "flag": "🇦🇪", "rate": 2.5},
    "49": {"name": "Germany", "tier": "TIER_2", "flag": "🇩🇪", "rate": 2.0},
    
    
    "39": {"name": "Italy", "tier": "TIER_1", "flag": "🇮🇹", "rate": 1.7},
    "33": {"name": "France", "tier": "TIER_1", "flag": "🇫🇷", "rate": 1.4},
    "965": {"name": "Kuwait", "tier": "TIER_1", "flag": "🇰🇼", "rate": 1.3},
    "81": {"name": "Japan", "tier": "TIER_1", "flag": "🇯🇵", "rate": 1.2},
    "968": {"name": "Oman", "tier": "TIER_1", "flag": "🇴🇲", "rate": 1.2},
    "886": {"name": "Taiwan", "tier": "TIER_1", "flag": "🇹🇼", "rate": 1.2},
    "357": {"name": "Cyprus", "tier": "TIER_1", "flag": "🇨🇾", "rate": 1.0},
    "40": {"name": "Romania", "tier": "TIER_1", "flag": "🇷🇴", "rate": 1.0},
    "973": {"name": "Bahrain", "tier": "TIER_1", "flag": "🇧🇭", "rate": 1.0},
    "32": {"name": "Belgium", "tier": "TIER_1", "flag": "🇧🇪", "rate": 1.0},
    "31": {"name": "Netherlands", "tier": "TIER_1", "flag": "🇳🇱", "rate": 1.0},
    
    
    "44": {"name": "United Kingdom", "tier": "DEFAULT", "flag": "🇬🇧", "rate": 0.7},
    "34": {"name": "Spain", "tier": "DEFAULT", "flag": "🇪🇸", "rate": 0.7},
    "420": {"name": "Czechia", "tier": "DEFAULT", "flag": "🇨🇿", "rate": 0.8},
    "964": {"name": "Iraq", "tier": "DEFAULT", "flag": "🇮🇶", "rate": 0.8},
    "972": {"name": "Israel", "tier": "DEFAULT", "flag": "🇮🇱", "rate": 0.8},
    "91": {"name": "India", "tier": "DEFAULT", "flag": "🇮🇳", "rate": 0.35},
    "62": {"name": "Indonesia", "tier": "DEFAULT", "flag": "🇮🇩", "rate": 0.3},
    "98": {"name": "Iran", "tier": "DEFAULT", "flag": "🇮🇷", "rate": 0.3},
    
    
    "966": {"name": "Saudi Arabia", "tier": "TIER_1", "flag": "🇸🇦", "rate": 1.5},
    "61": {"name": "Australia", "tier": "TIER_1", "flag": "🇦🇺", "rate": 1.5},
    "41": {"name": "Switzerland", "tier": "TIER_1", "flag": "🇨🇭", "rate": 1.5},
    "47": {"name": "Norway", "tier": "TIER_1", "flag": "🇳🇴", "rate": 1.5}
}
    
    


LANGUAGES = {
    "en": {
        "welcome": "👋 Welcome to Account Receiver Bot!\n\n"
                  "Use the buttons below to:\n"
                  "📱 Submit your accounts\n"
                  "💰 Check your balance\n"
                  "❓ Get help\n"
                  "👤 View your profile\n"
                  "🌐 Change language",
        "help": "❓ Available Commands:\n\n"
               "💰 Balance Commands:\n"
               "/balance - Check your balance\n"
               "/withdraw - Withdraw your funds\n\n"
               "👤 Profile Commands:\n"
               "/profile - View your profile\n"
               "/language - Change language\n\n"
               "❓ Help Commands:\n"
               "/help - Show this help message\n"
               "/support - Contact support\n\n"
               "⚙️ Other Commands:\n"
               "/cancel - Cancel current operation",
        "balance": "💰 Your current balance: ${balance:.2f}",
        "profile": "👤 Your Profile\n\n"
                  "✅ Verified accounts: {verified_accounts}\n"
                  "⏳ Pending accounts: {unverified_accounts}\n"
                  "💰 Balance: ${balance:.2f}\n"
                  "🌐 Language: {language}",
        "withdraw": "💸 Withdrawal\n\n"
                   "Current balance: ${balance:.2f}\n"
                   "Minimum withdrawal: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Invalid amount. Please enter a valid number.",
        "insufficient_balance": "❌ Insufficient balance. Your current balance is ${balance:.2f}",
        "withdrawal_success": "✅ Withdrawal request submitted!\n\n"
                            "Amount: ${amount:.2f}\n"
                            "New balance: ${new_balance:.2f}",
        "insufficient_withdrawal": "❌ Insufficient balance for withdrawal!\n\n"
                                 "Minimum withdrawal: ${min_withdrawal:.2f}\n"
                                 "Your balance: ${balance:.2f}",
        "withdrawal_cancelled": "❌ Withdrawal cancelled. Back to main menu.",
        "select_withdrawal_method": "💳 Please select your withdrawal method:",
        "enter_address": "📝 Please enter your {method} address:",
        "enter_amount": "💰 Enter the amount you want to withdraw:\n\nMinimum withdrawal: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ Withdrawal request submitted!\n\n"
                              "💰 Amount: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Verification Code: {code}\n\n"
                              "Your request is being processed.",
        "withdrawal_error": "❌ Invalid withdrawal amount!\n\nMinimum withdrawal amount: ${min_withdrawal:.2f}\nYou entered: ${amount:.2f}",
        "verification_start": "📱 Please send the phone number you want to verify.",
        "invalid_phone": "❌ Invalid phone number format. Please try again.",
        "verification_price": "ℹ️ Verification price for {country}: ${price:.2f}\n"
                            "Continue with verification?",
        "verification_success": "✅ Account verified successfully!\n"
                              "💰 ${price:.2f} has been added to your balance."
    },
    "es": {
        "welcome": "👋 ¡Bienvenido al Bot Receptor de Cuentas!\n\n"
                  "Usa los botones abajo para:\n"
                  "📱 Enviar tus cuentas\n"
                  "💰 Consultar tu saldo\n"
                  "❓ Obtener ayuda\n"
                  "👤 Ver tu perfil\n"
                  "🌐 Cambiar idioma",
        "help": "❓ Comandos Disponibles:\n\n"
               "💰 Comandos de Saldo:\n"
               "/balance - Consultar saldo\n"
               "/withdraw - Retirar fondos\n\n"
               "👤 Comandos de Perfil:\n"
               "/profile - Ver perfil\n"
               "/language - Cambiar idioma\n\n"
               "❓ Comandos de Ayuda:\n"
               "/help - Mostrar este mensaje\n"
               "/support - Contactar soporte\n\n"
               "⚙️ Otros Comandos:\n"
               "/cancel - Cancelar operación actual",
        "balance": "💰 Tu saldo actual: ${balance:.2f}",
        "profile": "👤 Tu Perfil\n\n"
                  "✅ Cuentas verificadas: {verified_accounts}\n"
                  "⏳ Cuentas pendientes: {unverified_accounts}\n"
                  "💰 Saldo: ${balance:.2f}\n"
                  "🌐 Idioma: {language}",
        "withdraw": "💸 Retiro\n\n"
                   "Saldo actual: ${balance:.2f}\n"
                   "Retiro mínimo: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Monto inválido. Por favor ingresa un número válido.",
        "insufficient_balance": "❌ Saldo insuficiente. Tu saldo actual es ${balance:.2f}",
        "withdrawal_success": "✅ ¡Solicitud de retiro enviada!\n\n"
                            "Monto: ${amount:.2f}\n"
                            "Nuevo saldo: ${new_balance:.2f}",
        "insufficient_withdrawal": "❌ ¡Saldo insuficiente para retirar!\n\n"
                                 "Retiro mínimo: ${min_withdrawal:.2f}\n"
                                 "Tu saldo: ${balance:.2f}",
        "withdrawal_cancelled": "❌ Retiro cancelado. Volviendo al menú principal.",
        "select_withdrawal_method": "💳 Por favor selecciona tu método de retiro:",
        "enter_address": "📝 Por favor ingresa tu dirección de {method}:",
        "enter_amount": "💰 Ingresa el monto que deseas retirar:\n\nRetiro mínimo: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ ¡Solicitud de retiro enviada!\n\n"
                              "💰 Valor: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Código de verificación: {code}\n\n"
                              "Su solicitud está siendo procesada.",
        "withdrawal_error": "❌ ¡Monto de retiro inválido!\n\nMonto mínimo de retiro: ${min_withdrawal:.2f}\nIngresaste: ${amount:.2f}",
        "verification_start": "📱 Por favor envía el número de teléfono que deseas verificar.",
        "invalid_phone": "❌ Formato de número inválido. Por favor intenta de nuevo.",
        "verification_price": "ℹ️ Precio de verificación para {country}: ${price:.2f}\n"
                            "¿Continuar con la verificación?",
        "verification_success": "✅ ¡Cuenta verificada exitosamente!\n"
                              "💰 Se han añadido ${price:.2f} a tu saldo."
    },
    "hi": {
        "welcome": "👋 अकाउंट रिसीवर बॉट में आपका स्वागत है!\n\n"
                  "नीचे दिए गए बटन का उपयोग करें:\n"
                  "📱 अपने अकाउंट जमा करें\n"
                  "💰 अपना बैलेंस देखें\n"
                  "❓ सहायता प्राप्त करें\n"
                  "👤 अपनी प्रोफ़ाइल देखें\n"
                  "🌐 भाषा बदलें",
        "help": "❓ उपलब्ध कमांड्स:\n\n"
               "💰 बैलेंस कमांड्स:\n"
               "/balance - बैलेंस जांचें\n"
               "/withdraw - पैसे निकालें\n\n"
               "👤 प्रोफ़ाइल कमांड्स:\n"
               "/profile - प्रोफ़ाइल देखें\n"
               "/language - भाषा बदलें\n\n"
               "❓ सहायता कमांड्स:\n"
               "/help - यह सहायता संदेश दिखाएं\n"
               "/support - सपोर्ट से संपर्क करें\n\n"
               "⚙️ अन्य कमांड्स:\n"
               "/cancel - वर्तमान कार्य रद्द करें",
        "balance": "💰 आपका वर्तमान बैलेंस: ${balance:.2f}",
        "profile": "👤 आपकी प्रोफ़ाइल\n\n"
                  "✅ सत्यापित अकाउंट: {verified_accounts}\n"
                  "⏳ लंबित अकाउंट: {unverified_accounts}\n"
                  "💰 बैलेंस: ${balance:.2f}\n"
                  "🌐 भाषा: {language}",
        "withdraw": "💸 पैसे निकालें\n\n"
                   "वर्तमान बैलेंस: ${balance:.2f}\n"
                   "न्यूनतम निकासी: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ अमान्य राशि। कृपया एक वैध संख्या दर्ज करें।",
        "insufficient_balance": "❌ अपर्याप्त बैलेंस। आपका वर्तमान बैलेंस ${balance:.2f} है",
        "withdrawal_success": "✅ निकासी अनुरोध सफलतापूर्वक भेजा गया!\n\n"
                            "राशि: ${amount:.2f}\n"
                            "नया बैलेंस: ${new_balance:.2f}",
        "insufficient_withdrawal": "❌ निकासी के लिए अपर्याप्त बैलेंस!\n\n"
                                 "न्यूनतम निकासी: ${min_withdrawal:.2f}\n"
                                 "आपका बैलेंस: ${balance:.2f}",
        "withdrawal_cancelled": "❌ निकासी रद्द की गई। मुख्य मेनू पर वापस।",
        "select_withdrawal_method": "💳 कृपया अपनी निकासी का तरीका चुनें:",
        "enter_address": "📝 कृपया अपना {method} पता दर्ज करें:",
        "enter_amount": "💰 वह राशि दर्ज करें जिसे आप निकालना चाहते हैं:\n\nन्यूनतम निकासी: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ निकासी अनुरोध जमा किया गया!\n\n"
                              "💰 राशि: ${amount:.2f}\n"
                              "📝 आईडी: {withdrawal_id}\n"
                              "🔑 सत्यापन कोड: {code}\n\n"
                              "आपका अनुरोध प्रोसेस किया जा रहा है।",
        "withdrawal_error": "❌ अमान्य निकासी राशि!\n\nन्यूनतम निकासी राशि: ${min_withdrawal:.2f}\nआपने दर्ज किया: ${amount:.2f}",
        "verification_start": "📱 कृपया वह फ़ोन नंबर भेजें जिसे आप सत्यापित करना चाहते हैं।",
        "invalid_phone": "❌ अमान्य फ़ोन नंबर प्रारूप। कृपया पुनः प्रयास करें।",
        "verification_price": "ℹ️ {country} के लिए सत्यापन मूल्य: ${price:.2f}\n"
                            "सत्यापन जारी रखें?",
        "verification_success": "✅ अकाउंट सफलतापूर्वक सत्यापित!\n"
                              "💰 ${price:.2f} आपके बैलेंस में जोड़ दिए गए हैं।"
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в Account Receiver Bot!\n\n"
                  "Используйте кнопки ниже для:\n"
                  "📱 Отправить аккаунты\n"
                  "💰 Проверить баланс\n"
                  "❓ Получить помощь\n"
                  "👤 Просмотреть профиль\n"
                  "🌐 Изменить язык",
        "help": "❓ Доступные команды:\n\n"
               "💰 Команды баланса:\n"
               "/balance - Проверить баланс\n"
               "/withdraw - Вывести средства\n\n"
               "👤 Команды профиля:\n"
               "/profile - Просмотреть профиль\n"
               "/language - Изменить язык\n\n"
               "❓ Команды помощи:\n"
               "/help - Показать это сообщение\n"
               "/support - Связаться с поддержкой\n\n"
               "⚙️ Другие команды:\n"
               "/cancel - Отменить текущую операцию",
        "balance": "💰 Ваш текущий баланс: ${balance:.2f}",
        "profile": "👤 Ваш профиль\n\n"
                  "✅ Подтвержденные аккаунты: {verified_accounts}\n"
                  "⏳ Ожидающие аккаунты: {unverified_accounts}\n"
                  "💰 Баланс: ${balance:.2f}\n"
                  "🌐 Язык: {language}",
        "withdraw": "💸 Вывод средств\n\n"
                   "Текущий баланс: ${balance:.2f}\n"
                   "Минимальный вывод: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Неверная сумма. Пожалуйста, введите действительное число.",
        "insufficient_balance": "❌ Недостаточно средств для вывода!\n\n"
                                 "Минимальная сумма: ${min_withdrawal:.2f}\n"
                                 "Ваш баланс: ${balance:.2f}",
        "withdrawal_success": "✅ Запрос на вывод средств успешно отправлен!\n\n"
                            "Сумма: ${amount:.2f}\n"
                            "Новый баланс: ${new_balance:.2f}",
        "withdrawal_cancelled": "❌ Вывод отменен. Возврат в главное меню.",
        "select_withdrawal_method": "💳 Пожалуйста, выберите способ вывода:",
        "enter_address": "📝 Пожалуйста, введите ваш адрес {method}:",
        "enter_amount": "💰 Введите сумму для вывода:\n\nМинимальная сумма: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ Заявка на вывод отправлена!\n\n"
                              "💰 Сумма: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Код подтверждения: {code}\n\n"
                              "Ваша заявка обрабатывается.",
        "withdrawal_error": "❌ Неверная сумма вывода!\n\nМинимальная сумма вывода: ${min_withdrawal:.2f}\nВы ввели: ${amount:.2f}",
        "verification_start": "📱 Пожалуйста, отправьте номер телефона для проверки.",
        "invalid_phone": "❌ Неверный формат номера телефона. Пожалуйста, попробуйте еще раз.",
        "verification_price": "ℹ️ Стоимость проверки для {country}: ${price:.2f}\n"
                            "Продолжить верификацию?",
        "verification_success": "✅ Аккаунт успешно подтвержден!\n"
                              "💰 ${price:.2f} добавлено к вашему балансу."
    },
    "ar": {
        "welcome": "👋 مرحباً بك في بوت استقبال الحسابات!\n\n"
                  "استخدم الأزرار أدناه:\n"
                  "📱 إرسال حساباتك\n"
                  "💰 التحقق من رصيدك\n"
                  "❓ الحصول على المساعدة\n"
                  "👤 عرض ملفك الشخصي\n"
                  "🌐 تغيير اللغة",
        "help": "❓ الأوامر المتاحة:\n\n"
               "💰 أوامر الرصيد:\n"
               "/balance - التحقق من الرصيد\n"
               "/withdraw - سحب الأموال\n\n"
               "👤 أوامر الملف الشخصي:\n"
               "/profile - عرض الملف الشخصي\n"
               "/language - تغيير اللغة\n\n"
               "❓ أوامر المساعدة:\n"
               "/help - عرض هذه الرسالة\n"
               "/support - الاتصال بالدعم\n\n"
               "⚙️ أوامر أخرى:\n"
               "/cancel - إلغاء العملية الحالية",
        "balance": "💰 رصيدك الحالي: ${balance:.2f}",
        "profile": "👤 ملفك الشخصي\n\n"
                  "✅ الحسابات المؤكدة: {verified_accounts}\n"
                  "⏳ الحسابات المعلقة: {unverified_accounts}\n"
                  "💰 الرصيد: ${balance:.2f}\n"
                  "🌐 اللغة: {language}",
        "withdraw": "💸 سحب الأموال\n\n"
                   "الرصيد الحالي: ${balance:.2f}\n"
                   "سحب أدنى: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ مبلغ غير صحيح. يرجى إدخال رقم صحيح.",
        "insufficient_balance": "❌ رصيد غير كافٍ للسحب!\n\n"
                                 "الحد الأدنى للسحب: ${min_withdrawal:.2f}\n"
                                 "رصيدك: ${balance:.2f}",
        "withdrawal_success": "✅ تم إرسال طلب السحب!\n\n"
                              "💰 المبلغ: ${amount:.2f}\n"
                              "📝 المعرف: {withdrawal_id}\n"
                              "🔑 رمز التحقق: {code}\n\n"
                              "يتم معالجة طلبك.",
        "withdrawal_cancelled": "❌ سحب إلغاء. العودة إلى القائمة الرئيسية.",
        "select_withdrawal_method": "💳 الرجاء اختيار طريقة السحب:",
        "enter_address": "📝 الرجاء إدخال عنوان {method} الخاص بك:",
        "enter_amount": "💰 أدخل المبلغ الذي تريد سحبه:\n\nالحد الأدنى للسحب: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ تم إرسال طلب السحب!\n\n"
                              "💰 المبلغ: ${amount:.2f}\n"
                              "📝 المعرف: {withdrawal_id}\n"
                              "🔑 رمز التحقق: {code}\n\n"
                              "يتم معالجة طلبك.",
        "withdrawal_error": "❌ مبلغ السحب غير صالح!\n\nالرجاء إدخال رقم صحيح أكبر من ${min_withdrawal:.2f}: {amount}",
        "verification_start": "📱 الرجاء إرسال رقم الهاتف للتحقق.",
        "invalid_phone": "❌ تنسيق رقم الهاتف غير صحيح. يرجى المحاولة مرة أخرى.",
        "verification_price": "ℹ️ سعر التحقق لـ {country}: ${price:.2f}\n"
                            "هل تريد المتابعة؟",
        "verification_success": "✅ تم التحقق من الحساب بنجاح!\n"
                              "💰 ${price:.2f} أضيف إلى رصيدك."
    },
    "fr": {
        "welcome": "👋 Bienvenue sur Account Receiver Bot!\n\n"
                  "Utilisez les boutons ci-dessous pour:\n"
                  "📱 Soumettre vos comptes\n"
                  "💰 Vérifier votre solde\n"
                  "❓ Obtenir de l'aide\n"
                  "👤 Voir votre profil\n"
                  "🌐 Changer de langue",
        "help": "❓ Commandes disponibles:\n\n"
               "💰 Commandes de solde:\n"
               "/balance - Vérifier le solde\n"
               "/withdraw - Retirer des fonds\n\n"
               "👤 Commandes de profil:\n"
               "/profile - Voir le profil\n"
               "/language - Changer de langue\n\n"
               "❓ Commandes d'aide:\n"
               "/help - Afficher ce message\n"
               "/support - Contacter le support\n\n"
               "⚙️ Autres commandes:\n"
               "/cancel - Annuler l'opération en cours",
        "balance": "💰 Votre solde actuel: ${balance:.2f}",
        "profile": "👤 Votre Profil\n\n"
                  "✅ Comptes vérifiés: {verified_accounts}\n"
                  "⏳ Comptes en attente: {unverified_accounts}\n"
                  "💰 Solde: ${balance:.2f}\n"
                  "🌐 Langue: {language}",
        "withdraw": "💸 Retrait\n\n"
                   "Solde actuel: ${balance:.2f}\n"
                   "Retrait minimum: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Solde insuffisant pour le retrait!\n\n"
                                 "Retrait minimum: ${min_withdrawal:.2f}\n"
                                 "Votre solde: ${balance:.2f}",
        "withdrawal_success": "✅ Demande de retrait envoyée !\n\n"
                              "💰 Montant : ${amount:.2f}\n"
                              "📝 ID : {withdrawal_id}\n"
                              "🔑 Code de vérification : {code}\n\n"
                              "Votre demande est en cours de traitement.",
        "insufficient_withdrawal": "❌ Insufficient balance for withdrawal!\n\n"
                                 "Minimum withdrawal: ${min_withdrawal:.2f}\n"
                                 "Votre solde: ${balance:.2f}",
        "withdrawal_cancelled": "❌ Retrait annulé. Retour au menu principal.",
        "select_withdrawal_method": "💳 Veuillez sélectionner votre méthode de retrait :",
        "enter_address": "📝 Veuillez entrer votre adresse {method} :",
        "enter_amount": "💰 Entrez le montant que vous souhaitez retirer :\n\nRetrait minimum : ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ Demande de retrait envoyée !\n\n"
                              "💰 Montant : ${amount:.2f}\n"
                              "📝 ID : {withdrawal_id}\n"
                              "🔑 Code de vérification : {code}\n\n"
                              "Votre demande est en cours de traitement.",
        "withdrawal_error": "❌ Montant de retrait invalide !\n\nMontant minimum de retrait : ${min_withdrawal:.2f}\nVous avez saisi : ${amount:.2f}",
        "verification_start": "📱 Veuillez envoyer le numéro de téléphone à vérifier.",
        "invalid_phone": "❌ Format de numéro de téléphone invalide. Veuillez réessayer.",
        "verification_price": "ℹ️ Prix de vérification pour {country}: ${price:.2f}\n"
                            "Continuer avec la vérification?",
        "verification_success": "✅ Compte vérifié avec succès!\n"
                              "💰 ${price:.2f} a été ajouté à votre solde."
    },
    "pt": {
        "welcome": "👋 Bem-vindo ao Account Receiver Bot!\n\n"
                  "Use os botões abaixo para:\n"
                  "📱 Enviar suas contas\n"
                  "💰 Verificar seu saldo\n"
                  "❓ Obter ajuda\n"
                  "👤 Ver seu perfil\n"
                  "🌐 Mudar idioma",
        "help": "❓ Comandos disponíveis:\n\n"
               "💰 Comandos de saldo:\n"
               "/balance - Verificar saldo\n"
               "/withdraw - Sacar fundos\n\n"
               "👤 Comandos de perfil:\n"
               "/profile - Ver perfil\n"
               "/language - Mudar idioma\n\n"
               "❓ Comandos de ajuda:\n"
               "/help - Mostrar esta mensagem\n"
               "/support - Contatar suporte\n\n"
               "⚙️ Outros comandos:\n"
               "/cancel - Cancelar operação atual",
        "balance": "💰 Seu saldo atual: ${balance:.2f}",
        "profile": "👤 Seu Perfil\n\n"
                  "✅ Contas verificadas: {verified_accounts}\n"
                  "⏳ Contas pendentes: {unverified_accounts}\n"
                  "💰 Saldo: ${balance:.2f}\n"
                  "🌐 Idioma: {language}",
        "withdraw": "💸 Sacar fundos\n\n"
                   "Saldo atual: ${balance:.2f}\n"
                   "Sacar mínimo: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Saldo insuficiente para saque!\n\n"
                                 "Saque mínimo: ${min_withdrawal:.2f}\n"
                                 "Seu saldo: ${balance:.2f}",
        "withdrawal_success": "✅ Solicitação de saque enviada!\n\n"
                              "💰 Valor: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Código de verificação: {code}\n\n"
                              "Sua solicitação está sendo processada.",
        "insufficient_withdrawal": "❌ Insufficient balance for withdrawal!\n\n"
                                 "Minimum withdrawal: ${min_withdrawal:.2f}\n"
                                 "Seu saldo: ${balance:.2f}",
        "withdrawal_cancelled": "❌ Saque cancelado. Voltando ao menu principal.",
        "select_withdrawal_method": "💳 Por favor, selecione seu método de saque:",
        "enter_address": "📝 Por favor, digite seu endereço de {method}:",
        "enter_amount": "💰 Digite o valor que deseja sacar:\n\nSaque mínimo: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ Solicitação de saque enviada!\n\n"
                              "💰 Valor: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Código de verificação: {code}\n\n"
                              "Sua solicitação está sendo processada.",
        "withdrawal_error": "❌ Valor de saque inválido!\n\nValor mínimo de saque: ${min_withdrawal:.2f}\nVocê digitou: ${amount:.2f}",
        "verification_start": "📱 Por favor, envie o número de telefone para verificação.",
        "invalid_phone": "❌ Formato de número de telefone inválido. Por favor, tente novamente.",
        "verification_price": "ℹ️ Preço de verificação para {country}: ${price:.2f}\n"
                            "Continuar com a verificação?",
        "verification_success": "✅ Conta verificada com sucesso!\n"
                              "💰 ${price:.2f} foi adicionado ao seu saldo."
    },
    "tr": {
        "welcome": "👋 Account Receiver Bot'a Hoş Geldiniz!\n\n"
                  "Aşağıdaki düğmeleri kullanın:\n"
                  "📱 Hesaplarınızı gönderin\n"
                  "💰 Bakiyenizi kontrol edin\n"
                  "❓ Yardım alın\n"
                  "👤 Profilinizi görüntüleyin\n"
                  "🌐 Dili değiştirin",
        "help": "❓ Mevcut komutlar:\n\n"
               "💰 Bakiye komutları:\n"
               "/balance - Bakiyeyi kontrol et\n"
               "/withdraw - Para çek\n\n"
               "👤 Profil komutları:\n"
               "/profile - Profili görüntüle\n"
               "/language - Dili değiştir\n\n"
               "❓ Yardım komutları:\n"
               "/help - Bu mesajı göster\n"
               "/support - Destekle iletişime geç\n\n"
               "⚙️ Diğer komutlar:\n"
               "/cancel - Mevcut işlemi iptal et",
        "balance": "💰 Mevcut bakiyeniz: ${balance:.2f}",
        "profile": "👤 Profiliniz\n\n"
                  "✅ Doğrulanmış hesaplar: {verified_accounts}\n"
                  "⏳ Bekleyen hesaplar: {unverified_accounts}\n"
                  "💰 Bakiye: ${balance:.2f}\n"
                  "🌐 Dil: {language}",
        "withdraw": "💸 Para çek\n\n"
                   "Mevcut bakiye: ${balance:.2f}\n"
                   "Çekim minimum: ${min_withdrawal:.2f}",
        "invalid_amount": "❌ Çekim için yetersiz bakiye!\n\n"
                                 "Minimum çekim: ${min_withdrawal:.2f}\n"
                                 "Bakiyeniz: ${balance:.2f}",
        "withdrawal_success": "✅ Çekim talebi gönderildi!\n\n"
                              "💰 Tutar: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Doğrulama Kodu: {code}\n\n"
                              "Talebiniz işleme alınıyor.",
        "insufficient_withdrawal": "❌ Insufficient balance for withdrawal!\n\n"
                                 "Minimum withdrawal: ${min_withdrawal:.2f}\n"
                                 "Bakiyeniz: ${balance:.2f}",
        "withdrawal_cancelled": "❌ Çekim iptal edildi. Ana menüye dönülüyor.",
        "select_withdrawal_method": "💳 Lütfen çekim yönteminizi seçin:",
        "enter_address": "📝 Lütfen {method} adresinizi girin:",
        "enter_amount": "💰 Çekmek istediğiniz tutarı girin:\n\nMinimum çekim: ${min_withdrawal:.2f}",
        "withdrawal_submitted": "✅ Çekim talebi gönderildi!\n\n"
                              "💰 Tutar: ${amount:.2f}\n"
                              "📝 ID: {withdrawal_id}\n"
                              "🔑 Doğrulama Kodu: {code}\n\n"
                              "Talebiniz işleme alınıyor.",
        "withdrawal_error": "❌ Geçersiz çekim tutarı!\n\nMinimum çekim tutarı: ${min_withdrawal:.2f}\nGirdiğiniz tutar: ${amount:.2f}",
        "verification_start": "📱 Lütfen doğrulanacak telefon numarasını gönderin.",
        "invalid_phone": "❌ Geçersiz telefon numarası formatı. Lütfen tekrar deneyin.",
        "verification_price": "ℹ️ Doğrulama ücreti {country}: ${price:.2f}\n"
                            "Doğrulama işlemini devam ettirmek istiyor musunuz?",
        "verification_success": "✅ Hesap başarıyla doğrulandı!\n"
                              "💰 ${price:.2f} bakiyenize eklendi."
    }
}

