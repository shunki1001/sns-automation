from libs_bq import get_product_data
from libs_openai import generate_post_text
from libs_x import post_to_x


def main():
    try:
        product = get_product_data()
        post_text = generate_post_text(product)
        result = post_to_x(post_text)
        return 200
    except Exception as e:
        return 500
