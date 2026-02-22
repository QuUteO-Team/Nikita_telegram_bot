from hammett.conf import settings
from hammett.core.permission import Permission



class PaywallPermission(Permission):

    async def has_permission(self, update, _context):
        user = update.effective_user
        return user.id in settings.PAID_USERS

    async def handle_permission_denied(self, update, context):
        from screens import PaymentScreen

        return await PaymentScreen().jump(update, context)