def calculate_total(price, quantity):
    """Calcula el total de una venta."""
    return price * quantity

def update_stock(product, quantity):
    """Actualiza el stock de un producto."""
    if product.stock >= quantity:
        product.stock -= quantity
    else:
        raise ValueError("Insufficient stock")