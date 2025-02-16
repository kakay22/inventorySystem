from .models import Log, Product

def record_log(action, details, user, product=None):
    """
    Records a system activity log.

    Parameters:
    - action (str): A short description of the action (e.g., "Add Product", "Update Stock").
    - details (str): Detailed information about the action performed.
    - user (ProductUser): The user performing the action.
    - product (Product, optional): The related product, if applicable.

    Returns:
    - Log: The created Log instance.
    """
    log = Log.objects.create(
        action=action,
        details=details,
        user=user,
        product=product
    )
    return log
