def calculate_feedback_and_set_image(product_list: list[dict], sum_key: str, count_key: str) -> list[dict]:
    for product in product_list:
        product['feedback'] = round(product[sum_key] / product[count_key], 2) if product[count_key] != 0 else 0

    return product_list