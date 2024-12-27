def check_packaging(pack_size, quantity):
    # Округляем вверх до ближайшего кратного
    if quantity % pack_size == 0:
        return quantity  # уже кратно
    else:


        return ((quantity // pack_size) + 1) * pack_size  # округление вверх

# Пример:
pack_size = 10
quantity = -80

sellable_quantity = check_packaging(pack_size, quantity)
print(f"Мы можем продать: {sellable_quantity} единиц")

