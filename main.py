from hammett.core import Bot
from hammett.core.constants import DEFAULT_STATE


from screens import MainMenuScreen, PaymentScreen, FakePaymentScreen, OrdersScreen, AdminPanelScreen


def main():
    name = 'ShopBot'
    app = Bot(
        name,
        entry_point=MainMenuScreen,
        states={
            DEFAULT_STATE: {FakePaymentScreen, MainMenuScreen, PaymentScreen, OrdersScreen, AdminPanelScreen},
        },
    )
    app.run()


if __name__ == '__main__':
    main()