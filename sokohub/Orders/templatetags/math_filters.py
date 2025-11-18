from django import template

# This line creates an instance of template.Library, which is used to register
# your custom template tags and filters.
register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument (arg).
    Usage: {{ item.quantity|multiply:item.product_id.price }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0