# from python_moduls.api_yandex_disk import *
# import asyncio

def calculate_feedback_and_set_image(product_list: list[dict], sum_key: str, count_key: str) -> list[dict]:
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    
    # results = loop.run_until_complete(asyncio.gather(*[get_images_product(product['idproduct']) for product in product_list]))
    for product in product_list:
        product['feedback'] = round(product[sum_key] / product[count_key], 2)
        # product['url_path'] = results[product['idproduct'] - 1][0]['sizes'][0]['url'] if len(results[0]) > 0 else ''
        # product['url_path'] = 

    return product_list