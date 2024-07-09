from fastapi import Depends
from typing import List

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository,
    AdditionalProductsRepository,
    RecommendedProductsRepository,
    get_product_repository,
    get_additional_products_repository,
    get_recommended_products_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)

    async def add_additional_product(self, primary_id: int, additional_id: int) -> AdditionalProducts:
        additional_product = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.create(instance_data=additional_product)

    async def update_additional_product(self, primary_id: int, additional_id: int) -> AdditionalProducts:
        update_data = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.update(pk=primary_id, update_data=update_data)

    async def delete_additional_product(self, primary_id: int, additional_id: int):
        await self.repository.delete(pk=primary_id, additional_id=additional_id)

    async def get_list_of_additional_products(self, primary_id: int) -> List[AdditionalProducts]:
        return await self.repository.filter(primary_id=primary_id)


class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)

    async def add_recommended_product(self, primary_id: int, recommended_id: int) -> RecommendedProducts:
        recommended_product = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.create(instance_data=recommended_product)

    async def update_recommended_product(self, primary_id: int, recommended_id: int) -> RecommendedProducts:
        update_data = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.update(pk=primary_id, update_data=update_data)

    async def delete_recommended_product(self, primary_id: int, recommended_id: int):
        await self.repository.delete(pk=primary_id, recommended_id=recommended_id)

    async def get_list_of_recommended_products(self, primary_id: int) -> List[RecommendedProducts]:
        return await self.repository.filter(primary_id=primary_id)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


def get_additional_products_service(
        repo: AdditionalProductsRepository = Depends(get_additional_products_repository)) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)


def get_recommended_products_service(repo: RecommendedProductsRepository = Depends(get_recommended_products_repository)) -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)
