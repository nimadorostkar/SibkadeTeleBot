from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CallbackQueryHandler, CommandHandler,\
    ConversationHandler, ContextTypes, MessageHandler, filters, CallbackContext
import json
from datetime import datetime, timedelta, date
import requests
import json

TOKEN = "7445678382:AAG3-dxleieDz_dBJh4YCeMHQeuj389gM6U"



def read_json_from_api_link(api_link):
    try:
        proxies = {'http': 'http://23.88.54.241:8000', 'https': 'https://23.88.54.241:8000'}
        response = requests.get(api_link,proxies=proxies)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")



def add_months(current_date, months_to_add):
    new_date = datetime(
        current_date.year + (current_date.month + months_to_add - 1) // 12,
        (current_date.month + months_to_add - 1) % 12 + 1,
        current_date.day
    )
    return new_date


with open('products.json', 'r') as file:
    data = json.load(file)

CATS=[]
for object_name, items in data.items():
    print(f"Object: {object_name}")
    CATS.append(object_name)
    for item in items:
        print(f"Item: {item}")



#with open('links.json', 'r') as links:
    #link = json.load(links)

link = read_json_from_api_link("http://23.88.54.241:8000/links")


# Define states
CATEGORY, PRODUCT, SUBSCRIPTION = range(3)

# Example data for categories, products, and subscription periods
CATEGORIES = CATS
PRODUCTS = data
SUBSCRIPTIONS = ['2 month', '4 month', '6 month']



async def actions(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    selected_product = context.user_data['product']
    subscription = context.user_data['subscription']
    await query.edit_message_text(text=f'You selected a {selected_product} with {subscription} subscription.')

    if selected_product == "AppleMusic":
        await query.message.reply_text("Please enter your AppleID:")
    elif selected_product == "Spotify":
        await query.message.reply_text("Please enter your Email and Password:")
    elif selected_product == "AppleOne":
        await query.message.reply_text("Please enter your AppleID:")
    else:
        await query.message.reply_text("Please enter your accounts information:")




async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "support":
        await query.message.reply_text("You can contact with @parsakzn for SibkadePartnersBot support.")
        #await context.bot.send_message(chat_id='5554989830', text="SibkadePartners Bot Support...")



async def handle_message(update: Update, context: CallbackContext) -> None:
    first_line = update.message.text.splitlines()[0].lower()
    if first_line.lower() == 'hey sibkade':
        answer = update.message.text.splitlines()[1].lower()
        orders = answer.split(",")
        selected_product, subscription, email_field = orders
        user = update.message.from_user.username
        order_code = datetime.now().strftime("%Y%m%d%H%M%S")

        if subscription == "2":
            subs = "2 month"
        elif subscription == "4":
            subs = "4 month"
        elif subscription == "6":
            subs = "6 month"

        if selected_product == "AppleMusic" or selected_product == "applemusic":
            links_response = requests.get(
                f"http://23.88.54.241:8000/link-search?duration={subs}&is_active=true&type=AppleMusic")
            links_data = links_response.json()
            if links_data:
                link_item = links_data[-1]
                expiration = add_months(datetime.now(), int(subs[0]))
                requests.get(f"http://23.88.54.241:8000/link-add-usage/{link_item['id']}")
                post_data = {
                    'order_code': order_code,
                    'link': link_item['id'],
                    'user': user,
                    'chat_id': update.message.chat_id,
                    'message_id': update.message.message_id,
                    'expiration': expiration.date(),
                    'input': update.message.text
                }
                requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text(
                    f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🪪AppleID: {email_field} \n🛍️ You selected a AppleMusic with {subs} subscription.\n\n🎫Code: {link_item['code']}  \n🔗 Link: \n {link_item['link']} \n\n📅Expiration: {expiration.date()}   \n\n 🙏 Thank you for using our bot",
                    reply_markup=markupp)
            else:
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text("Not active link found for AppleMusic.", reply_markup=markupp)



        elif selected_product == "Spotify" or selected_product == "spotify":
            post_data = {
                'order_code': order_code,
                'user': user,
                'chat_id': update.message.chat_id,
                'message_id': update.message.message_id,
                'input': update.message.text
            }
            requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
            await update.message.reply_text(
                f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🛍️ You selected a Spotify with {subs} subscription.\n\nIt will be sent to you after the desired service is ready.   \n\n 🙏 Thank you for using our bot")


        elif selected_product == "AppleOne" or selected_product == "appleone":
            links_response = requests.get(
                f"http://23.88.54.241:8000/link-search?duration={subs}&is_active=true&type=AppleOne")
            links_data = links_response.json()
            if links_data:
                link_item = links_data[-1]
                expiration = add_months(datetime.now(), int(subs[0]))
                requests.get(f"http://23.88.54.241:8000/link-add-usage/{link_item['id']}")
                post_data = {
                    'order_code': order_code,
                    'link': link_item['id'],
                    'user': user,
                    'chat_id': update.message.chat_id,
                    'message_id': update.message.message_id,
                    'expiration': expiration.date(),
                    'input': update.message.text
                }
                requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text(
                    f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🪪AppleID: {email_field} \n🛍️ You selected a AppleOne with {subs} subscription.\n\n🎫Code: {link_item['code']}  \n🔗 Link: \n {link_item['link']} \n\n📅Expiration: {expiration.date()}   \n\n 🙏 Thank you for using our bot",
                    reply_markup=markupp)
            else:
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text("Not active link found for AppleMusic.", reply_markup=markupp)


    else:
        answer = update.message.text
        selected_product = context.user_data['product']
        subscription = context.user_data['subscription']
        order_code = datetime.now().strftime("%Y%m%d%H%M%S")
        email_field = answer
        user = update.message.chat.username

        #print(answer)
        # print(update.message.chat)
        # print(context.user_data)

        if context.user_data['product'] == "AppleMusic":

            links_response = requests.get(f"http://23.88.54.241:8000/link-search?duration={subscription}&is_active=true&type={selected_product}")
            links_data = links_response.json()
            if links_data:
                link_item = links_data[-1]
                expiration = add_months(datetime.now(), int(subscription[0]))
                requests.get(f"http://23.88.54.241:8000/link-add-usage/{link_item['id']}")
                post_data = {
                    'order_code': order_code,
                    'link': link_item['id'],
                    'user': user,
                    'chat_id': update.message.chat_id,
                    'message_id': update.message.message_id,
                    'expiration': expiration.date(),
                    'input': answer
                }
                requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text(f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🪪AppleID: {email_field} \n🛍️ You selected a {selected_product} with {subscription} subscription.\n\n🎫Code: {link_item['code']}  \n🔗 Link: \n {link_item['link']} \n\n📅Expiration: {expiration.date()}   \n\n 🙏 Thank you for using our bot",reply_markup=markupp)
            else:
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text("Not active link found for AppleMusic.", reply_markup=markupp)


        elif context.user_data['product'] == "Spotify":
            post_data = {
                'order_code': order_code,
                'user': user,
                'chat_id': update.message.chat_id,
                'message_id': update.message.message_id,
                'input': answer
            }
            requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
            await update.message.reply_text(
                f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🛍️ You selected a {selected_product} with {subscription} subscription.\n\nIt will be sent to you after the desired service is ready.   \n\n 🙏 Thank you for using our bot")


        elif context.user_data['product'] == "AppleOne":
            links_response = requests.get(f"http://23.88.54.241:8000/link-search?duration={subscription}&is_active=true&type={selected_product}")
            links_data = links_response.json()
            if links_data:
                link_item = links_data[-1]
                expiration = add_months(datetime.now(), int(subscription[0]))
                requests.get(f"http://23.88.54.241:8000/link-add-usage/{link_item['id']}")
                post_data = {
                    'order_code': order_code,
                    'link': link_item['id'],
                    'user': user,
                    'chat_id': update.message.chat_id,
                    'message_id': update.message.message_id,
                    'expiration': expiration.date(),
                    'input': answer
                }
                requests.post('http://23.88.54.241:8000/add-order/', data=post_data)
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text(
                    f"🗂️ Order Code: {order_code} \n\n👤 User: {user} \n🪪AppleID: {email_field} \n🛍️ You selected a {selected_product} with {subscription} subscription.\n\n🎫Code: {link_item['code']}  \n🔗 Link: \n {link_item['link']} \n\n📅Expiration: {expiration.date()}   \n\n 🙏 Thank you for using our bot",
                    reply_markup=markupp)
            else:
                bttn = InlineKeyboardButton("Contact support", callback_data='support')
                markupp = InlineKeyboardMarkup([[bttn]])
                await update.message.reply_text("Not active link found for AppleOne.", reply_markup=markupp)







async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(category, callback_data=category)] for category in CATEGORIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a category:', reply_markup=reply_markup)
    return CATEGORY

# Category selection handler
async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    category = query.data
    context.user_data['category'] = category
    keyboard = [[InlineKeyboardButton(product, callback_data=product)] for product in PRODUCTS[category]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f'You selected {category}. Now, choose a product:', reply_markup=reply_markup)
    return PRODUCT

# Product selection handler
async def choose_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    product = query.data
    context.user_data['product'] = product
    keyboard = [[InlineKeyboardButton(subscription, callback_data=subscription)] for subscription in SUBSCRIPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f'You selected {product}. Now, choose a subscription period:', reply_markup=reply_markup)
    return SUBSCRIPTION

# Subscription selection handler
async def choose_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    subscription = query.data
    context.user_data['subscription'] = subscription
    await actions(update, context)
    return ConversationHandler.END



def main() -> None:
    application = Application.builder().token(TOKEN).build()
    # Define conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CATEGORY: [CallbackQueryHandler(choose_category)],
            PRODUCT: [CallbackQueryHandler(choose_product)],
            SUBSCRIPTION: [CallbackQueryHandler(choose_subscription)]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
