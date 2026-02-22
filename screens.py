import datetime

from hammett.core.handlers import register_button_handler
from hammett.core.hider import ONLY_FOR_ADMIN, Hider
from hammett.core.mixins import StartMixin, Screen
from hammett.core import Button
from hammett.core.constants import SourceTypes
from hammett.core.permission import ignore_permissions
from hammett.conf import settings

from datetime import datetime

from permissions import PaywallPermission

MAIN_MENU_SCREEN_DESCRIPTION = (
    "u bought a book" # change it
)

FAKE_PAYMENT_SCREEN_DESCRIPTION = (
    'which one?' # change it
)

PAYMENT_SCREEN_DESCRIPTION = (
    'u can buy it' # change it
)


class FakePaymentScreen(Screen):

    async def get_description(self, update, context):
        book_size = await self.get_payload(update, context)

        context.user_data['current_book'] = book_size

        books = {
            '20x20': 'Do you want to buy book 20x20? Price: 44.99$',
            '25x25': 'Do you want to buy book 25x25? Price: 64.99$',
            '30x30': 'Do you want to buy book 30x30? Price: 94.99$'
        }

        return books.get(book_size)


    async def add_default_keyboard(self, _update, _context):
        return [
            [
                Button('No',
                       PaymentScreen,
                       source_type=SourceTypes.MOVE_SOURCE_TYPE
                ),
                Button(
                    'Yes',
                    self.handle_payment,
                    source_type=SourceTypes.HANDLER_SOURCE_TYPE,
                ),
            ],
        ]

    @ignore_permissions([PaywallPermission])
    @register_button_handler
    async def handle_payment(self, update, context):
        user = update.effective_user
        settings.PAID_USERS.append(user.id)

        book_size = context.user_data.get('current_book')

        if 'orders' not in context.user_data:
            context.user_data['orders'] = []

        context.user_data['orders'].append({
            'book': book_size,
            'date': str(datetime.now()),
            'price':{
                '20x20': '44.99$',
                '25x25': '64.99$',
                '30x30': '94.99$'
            }.get(book_size, '?')
        })

        context.user_data.pop('current_book', None)

        return await MainMenuScreen().move(update, context)

    @ignore_permissions([PaywallPermission])
    async def move(self, update, context, **kwargs):
        return await super().move(update, context, **kwargs)

class OrdersScreen(Screen):
    async def get_description(self,update,context):
        orders = context.user_data.get('orders', [])

        if not orders:
            return "u havent bought anything yet" # change it

        orders_text = "ur orders:\n\n" # change it
        for i, order in enumerate(orders, 1):
            orders_text += f"{i}. Book {order['book']} - {order['price']}\n"
            orders_text += f"{order['date']}\n\n"

        return orders_text

    async def add_default_keyboard(self, _update, _context):
        return [
            [
                Button('Back to Menu', MainMenuScreen,
                       source_type=SourceTypes.MOVE_SOURCE_TYPE),
            ],
        ]
class AdminPanelScreen(Screen):
    description = 'u admin' # change it

class MainMenuScreen(StartMixin):
    description = MAIN_MENU_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        return [
            [
                Button(
                    'buy another one',
                    PaymentScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ],
            [
                Button(
                    'Orders',
                    OrdersScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                ),
            ]
        ]


class PaymentScreen(Screen):
    description = PAYMENT_SCREEN_DESCRIPTION

    async def add_default_keyboard(self, _update, _context):
        return [
            [
                Button('Book 20x20', FakePaymentScreen,
                       source_type=SourceTypes.MOVE_SOURCE_TYPE, payload='20x20'),
            ],
            [
                Button('Book 25x25', FakePaymentScreen,
                       source_type=SourceTypes.MOVE_SOURCE_TYPE, payload='25x25'),
            ],
            [
                Button('Book 30x30', FakePaymentScreen,
                       source_type=SourceTypes.MOVE_SOURCE_TYPE, payload='30x30'),
            ],

            [
                Button( # just to check the work of the "hiders"
                    'Admin',
                    AdminPanelScreen,
                    source_type=SourceTypes.MOVE_SOURCE_TYPE,
                    hiders=Hider(ONLY_FOR_ADMIN)
                ),
            ]
        ]

    @ignore_permissions([PaywallPermission])
    async def move(self, update, context, **kwargs):
        return await super().move(update, context, **kwargs)

    @ignore_permissions([PaywallPermission])
    async def jump(self, update, context, **kwargs):
        return await  super().jump(update, context, **kwargs)
