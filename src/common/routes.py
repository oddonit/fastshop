class BaseCrudPrefixes:
    root: str = '/'
    detail: str = '/{pk}'
    additional_product: str = '/{product_id}/additional'
    additional_product_with_id: str = '/{product_id}/additional/{additional_id}'
    recommended_products: str = '/{product_id}/recommended'
    recommended_products_with_id: str = '/{product_id}/recommended/{recommended_id}'
